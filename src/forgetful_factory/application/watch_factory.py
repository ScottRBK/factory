import json
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.ports.foreman_terminal import ForemanTerminal
from forgetful_factory.application.scaffold_issue import ScaffoldIssue
from forgetful_factory.application.watcher_problems import (
    IntakeProblem,
    RepositoryProblem,
    ScaffoldProblem,
    ScaffoldReadProblem,
    UncertainScaffold,
    WatcherAlerts,
)
from forgetful_factory.domain.models import (
    FactoryError,
    Issue,
    RepositoryReference,
    WorkSource,
)
from forgetful_factory.domain.services.work_tracking import WorkTrackingService


@dataclass
class BlockedWork:
    reference: str
    plan_id: int | None
    issue: Issue | None = None
    task_ids: tuple[int, ...] | None = None
    recovered: bool = True
    setup_paths: tuple[str, ...] = ()
    setup_cause: str | None = None


@dataclass
class _WatchState:
    seen: dict[str, str]
    baseline: dict[str, str]
    baselined: set[WorkSource]
    blocked: dict[str, BlockedWork]
    pending_lookup: dict[str, Issue]
    known: dict[str, BlockedWork]
    recovered: set[str]
    pending_repositories: dict[str, RepositoryReference]
    checked: bool = False
    inventoried: bool = False
    manual_pause: bool = False


class _WorkAction(Enum):
    COMPLETE = auto()
    RETRY = auto()
    PAUSE_READS = auto()
    PAUSE_MANUAL = auto()


class WatchFactory:
    def __init__(self, tracking: WorkTrackingService, terminal: ForemanTerminal,
                 scaffold: ScaffoldIssue):
        self.tracking = tracking
        self.terminal = terminal
        self.scaffold = scaffold

    def run(self, config: FactoryConfiguration, workspace: Path, interval: float,
            choose_existing: Callable[[], bool], report: Callable[[str], None],
            report_error: Callable[[str], None]) -> None:
        # The CLI owns the workspace lease; watching uses the resolved configuration snapshot.
        del workspace
        report('Checking Forgetful planning access; waiting for native sign-in/refresh if '
               'needed. Browser OAuth may open; Ctrl-C cancels and preserves saved work.')
        existing = choose_existing()
        report(self.terminal.startup_hint())
        self._watch(config, interval, existing, report, report_error)

    def _watch(self, config: FactoryConfiguration, interval: float, existing: bool,
               report: Callable[[str], None], report_error: Callable[[str], None]) -> None:
        sources = tuple(dict.fromkeys(
            WorkSource(repository.work_source.provider,
                       repository.work_source.reference.casefold())
            for repository in config.repository
        ))
        state = _WatchState(
            seen={},
            baseline={},
            baselined=set(),
            blocked={},
            pending_lookup={},
            known={},
            recovered=set(),
            pending_repositories={r.local_dir: r for r in config.repository},
        )
        alerts = WatcherAlerts(self.terminal, report_error)
        try:
            self.terminal.start()
            report('Foreman session ready; model access unverified. '
                   'Resource loading unverified. Submission is not agent receipt.')
            while True:
                self._check_pending_repositories(state, alerts)
                if not self._check_planning_access(state, alerts, report):
                    self.terminal.wait(interval)
                    continue
                if not self._load_inventory(state, alerts):
                    self.terminal.wait(interval)
                    continue
                attempted, shared_read_failed = self._recover_blocked(
                    state, alerts, report)
                if shared_read_failed:
                    self.terminal.wait(interval)
                    continue
                shared_read_failed = self._poll_sources(
                    sources, config, existing, state, attempted, alerts, report)
                if not shared_read_failed and not state.pending_lookup:
                    alerts.clear('recovery_read')
                self.terminal.wait(interval)
        finally:
            try:
                self.terminal.close()
            except FactoryError as error:
                report_error(str(error))

    def _check_pending_repositories(self, state: _WatchState,
                                    alerts: WatcherAlerts) -> None:
        for path, repository in tuple(state.pending_repositories.items()):
            subject = f'repository:{path}'
            try:
                self.scaffold.check_repository(repository)
            except RepositoryProblem as error:
                alerts.send(subject, error, scope='repository', code=error.code,
                            retry='read_only', provider=repository.work_source.provider,
                            source=repository.work_source.reference, paths=error.paths)
                continue
            del state.pending_repositories[path]
            alerts.clear(subject)

    def _check_planning_access(self, state: _WatchState, alerts: WatcherAlerts,
                               report: Callable[[str], None]) -> bool:
        if state.checked:
            return True
        try:
            self.scaffold.check()
        except FactoryError as error:
            alerts.send('planning_access', error, scope='factory',
                        code='planning_access_failed', retry='read_only')
            return False
        alerts.clear('planning_access')
        state.checked = True
        report('Forgetful planning access checked; submission is not agent receipt.')
        return True

    def _load_inventory(self, state: _WatchState, alerts: WatcherAlerts) -> bool:
        if state.inventoried:
            return True
        try:
            summaries = self.scaffold.unfinished()
        except FactoryError as error:
            alerts.send('inventory', error, scope='factory',
                        code='inventory_read_failed', retry='read_only')
            return False
        alerts.clear('inventory')
        candidates: dict[str, list[int]] = {}
        for summary in summaries:
            candidates.setdefault(summary['external_ref'], []).append(summary['id'])
        for reference, plan_ids in candidates.items():
            self._remember_inventory_candidate(reference, plan_ids, state, alerts)
        state.inventoried = True
        return True

    def _remember_inventory_candidate(self, reference: str, plan_ids: list[int],
                                      state: _WatchState, alerts: WatcherAlerts) -> None:
        # No candidate becomes the primary identity of an ambiguous inventory.
        work = BlockedWork(reference, plan_ids[0] if len(plan_ids) == 1 else None)
        state.blocked[reference] = work
        if len(plan_ids) > 1:
            self._alert_plan(alerts, work, ScaffoldProblem(
                'plan_ambiguous',
                f'Ambiguous plans for {reference}; reconcile duplicates.',
                plan_ids=tuple(sorted(plan_ids))))
        state.recovered.add(reference)

    def _recover_blocked(self, state: _WatchState, alerts: WatcherAlerts,
                         report: Callable[[str], None]) -> tuple[set[str], bool]:
        attempted = set(state.blocked)
        for subject, work in tuple(state.blocked.items()):
            if state.manual_pause:
                break
            if work.plan_id is None:
                continue
            action = self._recover_work(subject, work, state, alerts, report)
            if action is _WorkAction.PAUSE_MANUAL:
                state.manual_pause = True
                break
            if action is _WorkAction.PAUSE_READS:
                return attempted, True
        return attempted, False

    def _recover_work(self, subject: str, work: BlockedWork, state: _WatchState,
                      alerts: WatcherAlerts,
                      report: Callable[[str], None]) -> _WorkAction:
        try:
            result = self.scaffold.recover(
                work.plan_id, work.reference, issue=work.issue, task_ids=work.task_ids)
        except UncertainScaffold as error:
            alerts.send('manual', error, scope='factory', code=error.code,
                        retry='manual_reconciliation', issue_id=work.reference,
                        plan_id=work.plan_id)
            return _WorkAction.PAUSE_MANUAL
        except RepositoryProblem as error:
            self._handle_recovery_repository_problem(work, error, state, alerts)
            return _WorkAction.RETRY
        except ScaffoldReadProblem as error:
            self._handle_recovery_read_problem(work, error, alerts)
            return _WorkAction.PAUSE_READS
        except ScaffoldProblem as error:
            self._remember_task_ids(work, error.task_ids)
            self._alert_plan(alerts, work, error)
            return _WorkAction.RETRY
        except FactoryError as error:
            # Recovery calls only read operations, so retrying cannot replay writes.
            alerts.send('recovery_read', error, scope='factory',
                        code='recovery_read_failed', retry='read_only',
                        issue_id=work.reference, plan_id=work.plan_id)
            return _WorkAction.PAUSE_READS
        self._complete_recovery(subject, work, result, state, alerts, report)
        return _WorkAction.COMPLETE

    def _handle_recovery_repository_problem(
            self, work: BlockedWork, error: RepositoryProblem,
            state: _WatchState, alerts: WatcherAlerts) -> None:
        self._remember_task_ids(work, error.task_ids)
        # The repository alert already covers all blocked work using this path.
        # Keep each pinned plan pending without duplicating that same problem.
        if not any(path in state.pending_repositories for path in error.paths):
            self._alert_plan(alerts, work, error)

    def _handle_recovery_read_problem(self, work: BlockedWork,
                                      error: ScaffoldReadProblem,
                                      alerts: WatcherAlerts) -> None:
        self._remember_task_ids(work, error.task_ids)
        ownership_task_id = self._sole_task_id(work.task_ids)
        alerts.send('recovery_read', error, scope='factory', code=error.code,
                    retry='read_only', issue_id=work.reference, plan_id=work.plan_id,
                    ownership_task_ids=work.task_ids,
                    ownership_task_id=ownership_task_id)

    @staticmethod
    def _remember_task_ids(work: BlockedWork,
                           task_ids: tuple[int, ...] | None) -> None:
        if not work.task_ids:
            work.task_ids = task_ids

    def _complete_recovery(self, subject: str, work: BlockedWork,
                           result: tuple[Issue, dict] | None, state: _WatchState,
                           alerts: WatcherAlerts,
                           report: Callable[[str], None]) -> None:
        del state.blocked[subject]
        alerts.clear(subject)
        if result is not None:
            issue, scaffold = result
            self._submit(issue, scaffold, state.seen, report, recovered=work.recovered)
            work.task_ids = (scaffold['ownership_task_id'],)
        elif work.issue is not None:
            state.seen[subject] = work.issue.revision
        state.known[subject] = work

    def _poll_sources(self, sources: tuple[WorkSource, ...],
                      config: FactoryConfiguration, existing: bool,
                      state: _WatchState, attempted: set[str], alerts: WatcherAlerts,
                      report: Callable[[str], None]) -> bool:
        shared_read_failed = False
        for source in sources:
            issues = self._read_issues(source, config.watcher_label, alerts)
            if issues is None:
                continue
            if state.manual_pause or shared_read_failed:
                continue
            if not existing and source not in state.baselined:
                self._baseline_source(source, issues, state, report)
            repository = self._repository_for_source(config, source)
            shared_read_failed = self._process_source(
                source, issues, repository, state, attempted, alerts, report)
        return shared_read_failed

    def _process_source(self, source: WorkSource, issues: tuple[Issue, ...],
                        repository: RepositoryReference, state: _WatchState,
                        attempted: set[str], alerts: WatcherAlerts,
                        report: Callable[[str], None]) -> bool:
        if repository.local_dir in state.pending_repositories:
            return False
        eligible = {issue.id for issue in issues}
        current = {issue.id: issue for issue in issues}
        self._include_pending_lookups(source, current, state.pending_lookup)
        return self._process_issues(
            tuple(current.values()), eligible, repository, state, attempted, alerts, report)

    @staticmethod
    def _baseline_source(source: WorkSource, issues: tuple[Issue, ...],
                         state: _WatchState, report: Callable[[str], None]) -> None:
        # Cover the complete first-success batch before intake can pause it.
        # Recovered and blocked work retains its own pending identity/revision.
        for issue in issues:
            if (issue.id not in state.recovered and issue.id not in state.blocked
                    and issue.id not in state.pending_lookup):
                state.baseline[issue.id] = issue.revision
        state.baselined.add(source)
        report(f'Baseline {source.reference}: {len(issues)} matching issues.')

    @staticmethod
    def _repository_for_source(config: FactoryConfiguration,
                               source: WorkSource) -> RepositoryReference:
        return next(repository for repository in config.repository
                    if repository.work_source.provider == source.provider
                    and repository.work_source.reference.casefold() == source.reference)

    @staticmethod
    def _include_pending_lookups(source: WorkSource, current: dict[str, Issue],
                                 pending_lookup: dict[str, Issue]) -> None:
        for issue in pending_lookup.values():
            if issue.source == source:
                current.setdefault(issue.id, issue)

    def _process_issues(self, issues: tuple[Issue, ...], eligible: set[str],
                        repository: RepositoryReference, state: _WatchState,
                        attempted: set[str], alerts: WatcherAlerts,
                        report: Callable[[str], None]) -> bool:
        for issue in issues:
            if issue.id in state.blocked:
                state.blocked[issue.id].issue = issue
                continue
            if self._skip_issue(issue, state, attempted):
                continue
            attempted.add(issue.id)
            action = self._process_issue(
                issue, eligible, repository, state, alerts, report)
            if action is _WorkAction.PAUSE_MANUAL:
                state.manual_pause = True
                break
            if action is _WorkAction.PAUSE_READS:
                return True
        return False

    @staticmethod
    def _skip_issue(issue: Issue, state: _WatchState, attempted: set[str]) -> bool:
        return (issue.id in attempted or state.seen.get(issue.id) == issue.revision
                or state.baseline.get(issue.id) == issue.revision)

    def _process_issue(self, issue: Issue, eligible: set[str],
                       repository: RepositoryReference, state: _WatchState,
                       alerts: WatcherAlerts,
                       report: Callable[[str], None]) -> _WorkAction:
        work = state.known.get(issue.id)
        try:
            if work is None:
                plan_id = self.scaffold.lookup(issue)
                state.pending_lookup.pop(issue.id, None)
                if plan_id is not None:
                    work = BlockedWork(issue.id, plan_id, issue, recovered=False)
                elif issue.id not in eligible:
                    # A successful current poll removed creation authority. Saved work may
                    # still be discovered by the read-only lookup.
                    alerts.clear(f'intake:{issue.id}')
                    return _WorkAction.RETRY
            if work is not None:
                result = self.scaffold.recover(
                    work.plan_id, issue.id, issue=issue, task_ids=work.task_ids)
                scaffold = result[1] if result is not None else None
            else:
                scaffold = self.scaffold.prepare(issue)
        except UncertainScaffold as error:
            alerts.send('manual', error, scope='factory', code=error.code,
                        retry='manual_reconciliation', issue_id=issue.id,
                        plan_id=error.plan_id)
            return _WorkAction.PAUSE_MANUAL
        except RepositoryProblem as error:
            self._handle_intake_repository_problem(
                issue, repository, error, state, alerts)
            return _WorkAction.RETRY
        except IntakeProblem as error:
            # No identity or write exists to retain. Only a currently eligible issue may try
            # fresh preflight again on the next successful poll.
            alerts.send(f'intake:{issue.id}', error, scope='issue', code=error.code,
                        retry='next_poll', issue_id=issue.id, paths=error.paths)
            return _WorkAction.RETRY
        except ScaffoldReadProblem as error:
            self._handle_intake_read_problem(issue, error, state, alerts)
            return _WorkAction.PAUSE_READS
        except ScaffoldProblem as error:
            self._handle_intake_scaffold_problem(issue, error, state, alerts)
            return _WorkAction.RETRY
        except FactoryError as error:
            # The operation may include writes. Never replay an unknown outcome.
            alerts.send('manual', error, scope='factory',
                        code='scaffold_operation_uncertain',
                        retry='manual_reconciliation', issue_id=issue.id)
            return _WorkAction.PAUSE_MANUAL
        self._complete_intake(issue, scaffold, work, state, alerts, report)
        return _WorkAction.COMPLETE

    def _handle_intake_repository_problem(
            self, issue: Issue, repository: RepositoryReference,
            error: RepositoryProblem, state: _WatchState,
            alerts: WatcherAlerts) -> None:
        if error.plan_id is not None:
            work = BlockedWork(issue.id, error.plan_id, issue, error.task_ids,
                               recovered=False)
            state.blocked[issue.id] = work
            self._alert_plan(alerts, work, error)
            return
        state.pending_repositories[repository.local_dir] = repository
        alerts.send(f'repository:{repository.local_dir}', error,
                    scope='repository', code=error.code, retry='read_only',
                    provider=repository.work_source.provider,
                    source=repository.work_source.reference.casefold(), paths=error.paths)

    @staticmethod
    def _handle_intake_read_problem(issue: Issue, error: ScaffoldReadProblem,
                                    state: _WatchState, alerts: WatcherAlerts) -> None:
        if error.plan_id is None:
            state.pending_lookup[issue.id] = issue
        else:
            state.blocked[issue.id] = BlockedWork(
                issue.id, error.plan_id, issue, error.task_ids, recovered=False)
        ownership_task_id = WatchFactory._sole_task_id(error.task_ids)
        alerts.send('recovery_read', error, scope='factory', code=error.code,
                    retry='read_only', issue_id=issue.id, plan_id=error.plan_id,
                    ownership_task_ids=error.task_ids,
                    ownership_task_id=ownership_task_id)

    def _handle_intake_scaffold_problem(self, issue: Issue, error: ScaffoldProblem,
                                        state: _WatchState,
                                        alerts: WatcherAlerts) -> None:
        work = BlockedWork(issue.id, error.plan_id, issue, error.task_ids, recovered=False)
        state.blocked[issue.id] = work
        self._alert_plan(alerts, work, error)

    def _complete_intake(self, issue: Issue, scaffold: dict | None,
                         work: BlockedWork | None, state: _WatchState,
                         alerts: WatcherAlerts,
                         report: Callable[[str], None]) -> None:
        self._submit(issue, scaffold, state.seen, report)
        alerts.clear(f'intake:{issue.id}')
        if scaffold is not None:
            state.known[issue.id] = BlockedWork(
                issue.id, scaffold['plan_id'], issue,
                (scaffold['ownership_task_id'],), recovered=False)
        elif work is not None:
            state.known[issue.id] = work

    @staticmethod
    def _sole_task_id(task_ids: tuple[int, ...] | None) -> int | None:
        if task_ids and len(task_ids) == 1:
            return task_ids[0]
        return None

    @staticmethod
    def _alert_plan(alerts: WatcherAlerts, work: BlockedWork,
                    error: ScaffoldProblem) -> None:
        paths = error.paths
        cause = error.cause
        if error.code == 'setup_incomplete':
            # Keep the known setup location while read-only checks wait for a first owner.
            # Losing that context is not a changed problem or permission to create there.
            if not work.setup_paths:
                work.setup_paths = paths
            paths = work.setup_paths
            if work.setup_cause is None:
                work.setup_cause = cause
            cause = work.setup_cause
        identities = {
            'issue_id': work.reference,
            'plan_id': None if error.plan_ids else work.plan_id,
            'plan_ids': error.plan_ids,
            'paths': paths,
            'cause': cause,
        }
        candidates = error.candidate_task_ids
        if candidates is not None or work.task_ids is not None:
            identities['ownership_task_ids'] = (
                candidates if candidates is not None else work.task_ids)
        if work.task_ids and len(work.task_ids) == 1:
            identities['ownership_task_id'] = work.task_ids[0]
        if error.code == 'setup_incomplete':
            retry = 'user_approved_repair'
        elif work.plan_id is not None:
            retry = 'read_only'
        else:
            retry = 'manual_reconciliation'
        alerts.send(work.reference, error, scope='plan', code=error.code,
                    retry=retry, **identities)

    def _submit(self, issue: Issue, scaffold: dict | None, seen: dict[str, str],
                report: Callable[[str], None], *, recovered: bool = False) -> None:
        if scaffold is None:
            seen[issue.id] = issue.revision
            return
        message = 'Factory issue notification. External issue data: ' + json.dumps({
            'id': issue.id, 'repository': issue.source.reference,
            'number': issue.number, 'title': issue.title, 'url': issue.url,
            'body': issue.body, 'revision': issue.revision, 'recovered': recovered, **scaffold,
        })
        self.terminal.send(message)
        seen[issue.id] = issue.revision
        report(f'Submitted {issue.id} to Pi (submission only).')

    def _read_issues(self, source: WorkSource, labels: tuple[str, ...],
                     alerts: WatcherAlerts) -> tuple[Issue, ...] | None:
        subject = f'source:{source.provider}:{source.reference}'
        try:
            issues = self.tracking.list_issues(source, labels)
        except FactoryError as error:
            alerts.send(subject, FactoryError(f'{error} Will retry next poll.'), scope='source',
                        code='source_read_failed', retry='next_poll',
                        provider=source.provider, source=source.reference)
            return None
        alerts.clear(subject)
        return issues
