import json
from collections.abc import Callable
from dataclasses import dataclass
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
from forgetful_factory.domain.models import FactoryError, Issue, WorkSource
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


class WatchFactory:
    def __init__(self, tracking: WorkTrackingService, terminal: ForemanTerminal,
                 scaffold: ScaffoldIssue):
        self.tracking = tracking
        self.terminal = terminal
        self.scaffold = scaffold

    def run(self, config: FactoryConfiguration, workspace: Path, interval: float,
            choose_existing: Callable[[], bool], report: Callable[[str], None],
            report_error: Callable[[str], None]) -> None:
        report('Checking Forgetful planning access; waiting for native sign-in/refresh if '
               'needed. Browser OAuth may open; Ctrl-C cancels and preserves saved work.')
        existing = choose_existing()
        report(self.terminal.startup_hint())
        self._watch(config, workspace, interval, existing, report, report_error)

    def _watch(self, config: FactoryConfiguration, workspace: Path, interval: float,
               existing: bool, report: Callable[[str], None],
               report_error: Callable[[str], None]) -> None:
        sources = tuple(dict.fromkeys(
            WorkSource(repository.work_source.provider, repository.work_source.reference.casefold())
            for repository in config.repository
        ))
        seen: dict[str, str] = {}
        baseline: dict[str, str] = {}
        baselined: set[WorkSource] = set()
        blocked: dict[str, BlockedWork] = {}
        pending_lookup: dict[str, Issue] = {}
        known: dict[str, BlockedWork] = {}
        recovered: set[str] = set()
        alerts = WatcherAlerts(self.terminal, report_error)
        checked = False
        inventoried = False
        manual_pause = False
        pending_repositories = {r.local_dir: r for r in config.repository}
        try:
            self.terminal.start()
            report('Foreman session ready; model access unverified. '
                   'Resource loading unverified. Submission is not agent receipt.')
            while True:
                for path, repository in tuple(pending_repositories.items()):
                    subject = f'repository:{path}'
                    try:
                        self.scaffold.check_repository(repository)
                    except RepositoryProblem as error:
                        alerts.send(subject, error, scope='repository', code=error.code,
                                    retry='read_only', provider=repository.work_source.provider,
                                    source=repository.work_source.reference, paths=error.paths)
                    else:
                        del pending_repositories[path]
                        alerts.clear(subject)
                if not checked:
                    try:
                        self.scaffold.check()
                    except FactoryError as error:
                        alerts.send('planning_access', error, scope='factory',
                                    code='planning_access_failed', retry='read_only')
                        self.terminal.wait(interval)
                        continue
                    alerts.clear('planning_access')
                    checked = True
                    report('Forgetful planning access checked; submission is not agent receipt.')
                if not inventoried:
                    try:
                        summaries = self.scaffold.unfinished()
                    except FactoryError as error:
                        alerts.send('inventory', error, scope='factory',
                                    code='inventory_read_failed', retry='read_only')
                        self.terminal.wait(interval)
                        continue
                    alerts.clear('inventory')
                    candidates: dict[str, list[int]] = {}
                    for summary in summaries:
                        reference = summary['external_ref']
                        candidates.setdefault(reference, []).append(summary['id'])
                    for reference, plan_ids in candidates.items():
                        # No candidate becomes the primary identity of an ambiguous inventory.
                        work = BlockedWork(reference, plan_ids[0] if len(plan_ids) == 1 else None)
                        blocked[reference] = work
                        if len(plan_ids) > 1:
                            self._alert_plan(alerts, work, ScaffoldProblem(
                                'plan_ambiguous',
                                f'Ambiguous plans for {reference}; reconcile duplicates.',
                                plan_ids=tuple(sorted(plan_ids))))
                        recovered.add(reference)
                    inventoried = True
                attempted = set(blocked)
                shared_read_failed = False
                for subject, work in tuple(blocked.items()):
                    if manual_pause:
                        break
                    if work.plan_id is None:
                        continue
                    try:
                        result = self.scaffold.recover(
                            work.plan_id, work.reference, issue=work.issue, task_ids=work.task_ids)
                    except UncertainScaffold as error:
                        manual_pause = True
                        alerts.send('manual', error, scope='factory', code=error.code,
                                    retry='manual_reconciliation', issue_id=work.reference,
                                    plan_id=work.plan_id)
                        break
                    except RepositoryProblem as error:
                        if not work.task_ids:
                            work.task_ids = error.task_ids
                        # The repository alert already covers all blocked work using this path.
                        # Keep each pinned plan pending without duplicating that same problem.
                        if not any(path in pending_repositories for path in error.paths):
                            self._alert_plan(alerts, work, error)
                        continue
                    except ScaffoldReadProblem as error:
                        if not work.task_ids:
                            work.task_ids = error.task_ids
                        shared_read_failed = True
                        alerts.send('recovery_read', error, scope='factory',
                                    code=error.code, retry='read_only',
                                    issue_id=work.reference, plan_id=work.plan_id,
                                    ownership_task_ids=work.task_ids,
                                    ownership_task_id=(work.task_ids[0] if work.task_ids
                                                       and len(work.task_ids) == 1 else None))
                        break
                    except ScaffoldProblem as error:
                        if not work.task_ids:
                            work.task_ids = error.task_ids
                        self._alert_plan(alerts, work, error)
                        continue
                    except FactoryError as error:
                        # Recovery calls only read operations, so retrying cannot replay writes.
                        shared_read_failed = True
                        alerts.send('recovery_read', error, scope='factory',
                                    code='recovery_read_failed', retry='read_only',
                                    issue_id=work.reference, plan_id=work.plan_id)
                        break
                    del blocked[subject]
                    alerts.clear(subject)
                    if result is not None:
                        issue, scaffold = result
                        self._submit(issue, scaffold, seen, report, recovered=work.recovered)
                        work.task_ids = (scaffold['ownership_task_id'],)
                    elif work.issue is not None:
                        seen[subject] = work.issue.revision
                    known[subject] = work
                if shared_read_failed:
                    self.terminal.wait(interval)
                    continue
                for source in sources:
                    issues = self._read_issues(source, config.watcher_label, alerts)
                    if issues is None:
                        continue
                    if manual_pause or shared_read_failed:
                        continue
                    first_baseline = not existing and source not in baselined
                    if first_baseline:
                        # Cover the complete first-success batch before intake can pause it.
                        # Recovered and blocked work retains its own pending identity/revision.
                        for issue in issues:
                            if (issue.id not in recovered and issue.id not in blocked
                                    and issue.id not in pending_lookup):
                                baseline[issue.id] = issue.revision
                        baselined.add(source)
                        report(f'Baseline {source.reference}: {len(issues)} matching issues.')
                    repository = next(r for r in config.repository
                                      if r.work_source.provider == source.provider
                                      and r.work_source.reference.casefold() == source.reference)
                    if repository.local_dir in pending_repositories:
                        continue
                    eligible = {issue.id for issue in issues}
                    current = {issue.id: issue for issue in issues}
                    for issue in pending_lookup.values():
                        if issue.source == source:
                            current.setdefault(issue.id, issue)
                    issues = tuple(current.values())
                    for issue in issues:
                        if issue.id in blocked:
                            blocked[issue.id].issue = issue
                            continue
                        if issue.id in attempted or seen.get(issue.id) == issue.revision:
                            continue
                        if baseline.get(issue.id) == issue.revision:
                            continue
                        attempted.add(issue.id)
                        try:
                            work = known.get(issue.id)
                            if work is None:
                                # A failed pre-write lookup has no creation authority. First
                                # establish whether a saved identity now needs read-only recovery.
                                plan_id = self.scaffold.lookup(issue)
                                pending_lookup.pop(issue.id, None)
                                if plan_id is not None:
                                    work = BlockedWork(issue.id, plan_id, issue, recovered=False)
                                elif issue.id not in eligible:
                                    # A successful current poll removed creation authority.
                                    # Saved work may still be discovered by the read-only lookup.
                                    alerts.clear(f'intake:{issue.id}')
                                    continue
                            if work is not None:
                                result = self.scaffold.recover(
                                    work.plan_id, issue.id, issue=issue, task_ids=work.task_ids)
                                scaffold = result[1] if result is not None else None
                            else:
                                scaffold = self.scaffold.prepare(issue)
                        except UncertainScaffold as error:
                            manual_pause = True
                            alerts.send('manual', error, scope='factory', code=error.code,
                                        retry='manual_reconciliation', issue_id=issue.id,
                                        plan_id=error.plan_id)
                            break
                        except RepositoryProblem as error:
                            if error.plan_id is not None:
                                work = BlockedWork(issue.id, error.plan_id, issue, error.task_ids,
                                                   recovered=False)
                                blocked[issue.id] = work
                                self._alert_plan(alerts, work, error)
                            else:
                                pending_repositories[repository.local_dir] = repository
                                alerts.send(f'repository:{repository.local_dir}', error,
                                            scope='repository', code=error.code, retry='read_only',
                                            provider=source.provider, source=source.reference,
                                            paths=error.paths)
                            continue
                        except IntakeProblem as error:
                            # No identity or write exists to retain. Only a currently eligible
                            # issue may try fresh preflight again on the next successful poll.
                            alerts.send(f'intake:{issue.id}', error, scope='issue', code=error.code,
                                        retry='next_poll', issue_id=issue.id, paths=error.paths)
                            continue
                        except ScaffoldReadProblem as error:
                            if error.plan_id is None:
                                pending_lookup[issue.id] = issue
                            else:
                                blocked[issue.id] = BlockedWork(issue.id, error.plan_id, issue,
                                                               error.task_ids, recovered=False)
                            shared_read_failed = True
                            alerts.send('recovery_read', error, scope='factory', code=error.code,
                                        retry='read_only', issue_id=issue.id, plan_id=error.plan_id,
                                        ownership_task_ids=error.task_ids,
                                        ownership_task_id=(error.task_ids[0] if error.task_ids
                                                           and len(error.task_ids) == 1 else None))
                            break
                        except ScaffoldProblem as error:
                            work = BlockedWork(issue.id, error.plan_id, issue, error.task_ids,
                                               recovered=False)
                            blocked[issue.id] = work
                            self._alert_plan(alerts, work, error)
                            continue
                        except FactoryError as error:
                            # The operation may include writes. Never replay an unknown outcome.
                            manual_pause = True
                            alerts.send('manual', error, scope='factory',
                                        code='scaffold_operation_uncertain',
                                        retry='manual_reconciliation', issue_id=issue.id)
                            break
                        self._submit(issue, scaffold, seen, report)
                        alerts.clear(f'intake:{issue.id}')
                        if scaffold is not None:
                            known[issue.id] = BlockedWork(
                                issue.id, scaffold['plan_id'], issue,
                                (scaffold['ownership_task_id'],), recovered=False)
                        elif work is not None:
                            known[issue.id] = work
                if not shared_read_failed and not pending_lookup:
                    alerts.clear('recovery_read')
                self.terminal.wait(interval)
        finally:
            try:
                self.terminal.close()
            except FactoryError as error:
                report_error(str(error))

    @staticmethod
    def _alert_plan(alerts: WatcherAlerts, work: BlockedWork, error: ScaffoldProblem) -> None:
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
        identities = dict(issue_id=work.reference,
                          plan_id=None if error.plan_ids else work.plan_id,
                          plan_ids=error.plan_ids, paths=paths, cause=cause)
        candidates = error.candidate_task_ids
        if candidates is not None or work.task_ids is not None:
            identities['ownership_task_ids'] = (candidates if candidates is not None
                                                else work.task_ids)
        if work.task_ids and len(work.task_ids) == 1:
            identities['ownership_task_id'] = work.task_ids[0]
        alerts.send(work.reference, error, scope='plan', code=error.code,
                    retry=('user_approved_repair' if error.code == 'setup_incomplete' else
                           'read_only' if work.plan_id is not None else 'manual_reconciliation'),
                    **identities)

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
