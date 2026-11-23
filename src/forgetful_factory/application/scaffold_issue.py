import json
import re
from dataclasses import asdict
from pathlib import Path

from forgetful_factory.application.cleanup_marker import (
    CleanupMarkerError,
    validate_cleanup_marker,
)
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.factory_records import FactoryRecords
from forgetful_factory.application.ports.local_repositories import LocalRepositories
from forgetful_factory.application.ports.worktrees import (
    WorktreeProblem,
    WorktreeReadError,
    Worktrees,
)
from forgetful_factory.application.watcher_problems import (
    IntakeProblem,
    ScaffoldProblem,
    ScaffoldReadProblem,
    UncertainScaffold,
)
from forgetful_factory.domain.models import RepositoryReference
from forgetful_factory.forge.ports import Forge
from forgetful_factory.planning.ports import PlanningReadError, PlanStore
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.model import Ticket, TicketSource


def worktree_name(ticket: Ticket) -> str:
    """Name of the branch suffix and folder. Characters Git or paths refuse become '-'."""
    key = re.sub(r'[^A-Za-z0-9._-]', '-', ticket.key)
    return ticket.source.reference.replace('/', '-') + f'-{key}'


class ScaffoldIssue:
    def __init__(self, planning: PlanStore, worktrees: Worktrees, workspace: Path,
                 config: FactoryConfiguration, repositories: LocalRepositories,
                 forge: Forge):
        self.planning = planning
        self.worktrees = worktrees
        self.workspace = workspace
        self.config = config
        self.records = FactoryRecords(planning, workspace, config, repositories, forge)

    def check(self) -> None:
        self.planning.check()

    def check_repository(self, repository: RepositoryReference) -> None:
        self.records.check_repository(repository)

    def prepare(self, issue: Ticket) -> dict | None:
        plan_id = self.lookup(issue)
        if plan_id is not None:
            result = self.recover(plan_id, issue.id, issue=issue)
            return result[1] if result is not None else None
        mappings = self.preflight(issue)
        plan = self._create_plan(issue)
        try:
            return self._prepare_plan(issue, plan, mappings)
        except ScaffoldProblem as error:
            error.plan_id = plan['id']
            raise
        except PlanningReadError as error:
            raise ScaffoldReadProblem('recovery_read_failed', str(error),
                                      plan_id=plan['id']) from error
        except FactoryError as error:
            raise UncertainScaffold('scaffold_operation_uncertain', str(error),
                                    plan_id=plan['id']) from error

    def _repository(self, source: TicketSource) -> RepositoryReference:
        return next(r for r in self.config.repository
                    if r.work_source.provider == source.provider
                    and r.work_source.reference.casefold() == source.reference.casefold())

    def _initial_mappings(self, issue: Ticket) -> list[dict]:
        if issue.epic:
            return []
        repository = self._repository(issue.source)
        name = worktree_name(issue)
        return [{'repository': issue.source.reference, 'local_dir': repository.local_dir,
                 'branch': f'factory/{name}',
                 'path': str(Path(repository.local_dir) / '.factory/worktrees' / name),
                 'target_branch': self.worktrees.target_branch(repository.local_dir)}]

    def preflight(self, issue: Ticket) -> list[dict]:
        self.records.check_repository(self._repository(issue.source))
        try:
            mappings = self._initial_mappings(issue)
        except WorktreeReadError as error:
            raise IntakeProblem('worktree_read_failed', str(error),
                                paths=(self._repository(issue.source).local_dir,)) from error
        for mapping in mappings:
            try:
                self.worktrees.inspect(mapping['local_dir'], mapping['branch'], mapping['path'],
                                       remote=self._repository(issue.source).remote)
            except WorktreeProblem as error:
                raise IntakeProblem(error.code, str(error), paths=error.paths) from error
            except WorktreeReadError as error:
                raise IntakeProblem('worktree_read_failed', str(error),
                                    paths=(mapping['path'],)) from error

        return mappings

    def _prepare_plan(self, issue: Ticket, plan: dict,
                      initial_mappings: list[dict]) -> dict | None:
        context = self.records.context(plan)
        if not self.records.active(plan):
            return None
        tasks, mappings = self._setup_ownership(plan['id'], issue, context, initial_mappings)
        self._ensure_setup_worktrees(mappings, tasks)
        if not tasks:
            tasks = self._create_ownership(plan['id'], issue.id, context, mappings)
        task = tasks[0]
        return {'plan_id': plan['id'], 'ownership_task_id': task['id'], 'worktrees': mappings,
                'epic': issue.epic, 'repositories': [asdict(r) for r in self.config.repository]}

    def _setup_ownership(self, plan_id: int, issue: Ticket,
                         context: dict, initial_mappings: list[dict]
                         ) -> tuple[list[dict], list[dict]]:
        tasks = self.records.ownership(plan_id, issue.id)
        if len(tasks) > 1:
            raise ScaffoldProblem(
                'ownership_ambiguous',
                f'Ambiguous ownership for plan {plan_id}; reconcile duplicates.',
                candidate_task_ids=tuple(sorted(task['id'] for task in tasks)))
        if not tasks and context.get('ownership_create_started'):
            raise UncertainScaffold(
                'ownership_create_uncertain',
                'Ownership creation uncertain; inspect all plan tasks and confirm '
                'the earlier request stopped before explicitly reconciling '
                'ownership_create_started in the plan context. No retry was made.')
        mappings = (json.loads(tasks[0]['description'])['worktrees'] if tasks
                    else initial_mappings)
        return tasks, mappings

    def _ensure_setup_worktrees(self, mappings: list[dict], tasks: list[dict]) -> None:
        task_ids = tuple(task['id'] for task in tasks)
        try:
            self._ensure_worktrees(mappings, recorded=bool(tasks))
        except WorktreeReadError as error:
            raise ScaffoldReadProblem('recovery_read_failed', str(error),
                                      task_ids=task_ids) from error
        except ScaffoldProblem as error:
            error.task_ids = task_ids
            if not tasks:
                error.cause = error.code
                error.code = 'setup_incomplete'
            raise

    def _create_ownership(self, plan_id: int, external_ref: str, context: dict,
                          mappings: list[dict]) -> list[dict]:
        context['ownership_create_started'] = True
        self.planning.update_plan(plan_id, context=json.dumps(context, ensure_ascii=False))
        try:
            self.planning.create_task(
                plan_id=plan_id, title='Feature ownership',
                description=json.dumps({'kind': 'factory-ownership',
                                        'workspace': str(self.workspace),
                                        'external_ref': external_ref, 'worktrees': mappings}))
        except FactoryError:
            pass
        try:
            tasks = self.records.ownership(plan_id, external_ref)
        except FactoryError as error:
            raise UncertainScaffold('ownership_create_uncertain', str(error)) from error
        if len(tasks) != 1:
            raise UncertainScaffold(
                'ownership_create_uncertain',
                'Ownership creation uncertain; reconcile all plan tasks. '
                'The create-intent is saved; no automatic retry is permitted.')
        return tasks

    def lookup(self, issue: Ticket) -> int | None:
        """Read-only identity lookup; no create has been attempted on this path."""
        try:
            plans = self.planning.plans(issue.id)
        except PlanningReadError as error:
            raise ScaffoldReadProblem('recovery_read_failed', str(error)) from error
        if len(plans) > 1:
            raise ScaffoldProblem('plan_ambiguous',
                                  f'Ambiguous plans for {issue.id}; reconcile duplicates.',
                                  plan_ids=tuple(sorted(plan['id'] for plan in plans)))
        return plans[0]['id'] if plans else None

    def _create_plan(self, issue: Ticket) -> dict:
        snapshot = asdict(issue)
        snapshot['body'] = (
            f'This is a placeholder description for {issue.source.provider} '
            f'issue #{issue.key}: {issue.title}. '
            'The feature owner will update it after reviewing the issue/plan.')
        try:
            self.planning.create_plan(
                title=issue.title,
                external_ref=issue.id, source_url=issue.url,
                context=json.dumps({'workspace': str(self.workspace), 'issue': snapshot},
                                   ensure_ascii=False))
        except FactoryError:
            # A failed response does not tell us whether the unique create committed.
            pass
        try:
            plans = self.planning.plans(issue.id)
        except FactoryError as error:
            # There is no pinned identity yet. A failed read cannot authorize create replay.
            raise UncertainScaffold('plan_create_uncertain', str(error)) from error
        if len(plans) != 1:
            raise UncertainScaffold('plan_create_uncertain',
                                    f'Plan creation uncertain for {issue.id}; '
                                    'reconcile before retrying.')
        plan_id = plans[0]['id']
        try:
            plan = self.planning.get_plan(plan_id)
        except PlanningReadError as error:
            raise ScaffoldReadProblem('recovery_read_failed', str(error),
                                      plan_id=plan_id) from error
        if plan.get('id') != plan_id or plan.get('external_ref') != issue.id:
            raise ScaffoldProblem('plan_identity_changed',
                                  'Saved plan identity changed; reconcile it.', plan_id=plan_id)
        if not self.planning.owns(plan):
            raise ScaffoldProblem('plan_project_mismatch',
                                  f'{issue.id} already belongs to another project; reconcile it.',
                                  plan_id=plan['id'])
        return plan

    def unfinished(self) -> list[dict]:
        prefixes = {r.work_source.id_prefix for r in self.config.repository}
        return [p for p in self.planning.plans()
                if self._is_unfinished_factory_plan(p, prefixes)]

    def recover(self, plan_id: int, external_ref: str, *, issue: Ticket | None = None,
                task_ids: tuple[int, ...] | None = None) -> tuple[Ticket, dict] | None:
        """Read known identities only. Missing records never fall back to scaffolding."""
        try:
            plan = self._recovery_plan(plan_id, external_ref)
            context = self.records.context(plan)
            if not self.records.active(plan):
                return None
            snapshot = self.records.snapshot(context, external_ref)
            self.records.check_repository(self._repository(snapshot.source))
            owners = self.records.ownership(plan_id, external_ref)
            current_ids = tuple(sorted(task['id'] for task in owners))
            self._validate_recovery_candidates(owners, current_ids, task_ids)
            task_ids = current_ids
            owner = self._sole_recovery_owner(owners, context)
            mappings = json.loads(owner['description'])['worktrees']
            self._ensure_worktrees(mappings, recorded=True)
            recovered_issue = issue or snapshot
            return recovered_issue, {
                'plan_id': plan_id, 'ownership_task_id': owner['id'],
                'worktrees': mappings, 'epic': recovered_issue.epic,
                'repositories': [asdict(r) for r in self.config.repository]}
        except ScaffoldProblem as error:
            error.plan_id = plan_id
            if error.task_ids is None:
                error.task_ids = task_ids
            raise
        except FactoryError as error:
            # Every recovery operation is read-only, including mapping/Git revalidation.
            raise ScaffoldReadProblem('recovery_read_failed', str(error), plan_id=plan_id,
                                      task_ids=task_ids) from error

    def _recovery_plan(self, plan_id: int, external_ref: str) -> dict:
        matches = self.planning.plans(external_ref)
        if len(matches) > 1:
            raise ScaffoldProblem('plan_ambiguous',
                                  'Multiple plans match this issue; reconcile duplicates.',
                                  plan_ids=tuple(sorted(plan['id'] for plan in matches)))
        if len(matches) != 1 or matches[0]['id'] != plan_id:
            raise ScaffoldProblem('plan_identity_changed',
                                  'Saved plan is missing or replaced; reconcile it.')
        plan = self.planning.get_plan(plan_id)
        if plan.get('id') != plan_id or plan.get('external_ref') != external_ref:
            raise ScaffoldProblem('plan_identity_changed',
                                  'Saved plan identity changed; reconcile it.')
        if not self.planning.owns(plan):
            raise ScaffoldProblem('plan_project_mismatch',
                                  'Saved plan belongs to another project; reconcile it.')
        return plan

    @staticmethod
    def _validate_recovery_candidates(owners: list[dict], current_ids: tuple[int, ...],
                                      known_ids: tuple[int, ...] | None) -> None:
        if known_ids and current_ids != known_ids:
            raise ScaffoldProblem('ownership_identity_changed',
                                  'Saved ownership is missing or replaced; reconcile it.',
                                  candidate_task_ids=current_ids)
        if len(owners) > 1:
            raise ScaffoldProblem('ownership_ambiguous',
                                  'Multiple valid ownership candidates need reconciliation.',
                                  candidate_task_ids=current_ids)

    @staticmethod
    def _sole_recovery_owner(owners: list[dict], context: dict) -> dict:
        if owners:
            return owners[0]
        if context.get('ownership_create_started'):
            raise UncertainScaffold(
                'ownership_create_uncertain',
                'Ownership creation uncertain; inspect all plan tasks and confirm the '
                'earlier request stopped before explicitly reconciling '
                'ownership_create_started in the plan context. No retry was made.')
        raise ScaffoldProblem('setup_incomplete',
                              'Saved ownership is missing or ambiguous; reconcile it.')

    def _is_unfinished_factory_plan(self, summary: dict, prefixes: set[str]) -> bool:
        project_id = summary.get('project_id')
        status = summary.get('status')
        if (type(project_id) is int and not self.planning.owns(summary)
                or status in ('completed', 'archived')):
            return False
        # A known reference with invalid association/status still needs per-plan recovery checks.
        reference = summary.get('external_ref') or ''
        if not isinstance(reference, str):
            raise FactoryError('Factory plan inventory has invalid references; reconcile it.')
        return any(reference.startswith(prefix) for prefix in prefixes)

    def _ensure_worktrees(self, mappings: list[dict], *, recorded: bool) -> None:
        seen = set()
        for mapping in mappings:
            repository = self.records.mapping_repository(mapping, seen)
            self._ensure_validated_mapping(repository, mapping, recorded=recorded)

    def _ensure_validated_mapping(self, repository: RepositoryReference, mapping: dict, *,
                                  recorded: bool) -> None:
        try:
            self._ensure_mapping(repository, mapping, recorded=recorded)
        except ScaffoldProblem as error:
            error.paths = (mapping['path'],)
            raise
        except WorktreeProblem as error:
            raise ScaffoldProblem(error.code, str(error),
                                  paths=error.paths or (mapping['path'],)) from error

    def _ensure_mapping(self, repository, mapping: dict, *, recorded: bool) -> None:
        hosted = self.records.check_source(repository)
        try:
            state = validate_cleanup_marker(mapping, self.records.forge, hosted)
        except CleanupMarkerError as error:
            raise ScaffoldProblem('cleanup_invalid', str(error)) from error
        if state == 'removed':
            self.worktrees.verify_removed(repository.local_dir, mapping['branch'], mapping['path'],
                                          remote=repository.remote)
            return
        try:
            self.worktrees.ensure(repository.local_dir, mapping['branch'], mapping['path'],
                                  recorded=recorded, remote=repository.remote)
        except WorktreeProblem as error:
            if state == 'pending':
                raise ScaffoldProblem(
                    'cleanup_pending', 'Worktree cleanup is pending; reconcile the interrupted '
                    'removal before changing its record. ' + str(error)) from error
            raise
