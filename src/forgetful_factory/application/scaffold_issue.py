import json
import re
from dataclasses import asdict
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.ports.local_repositories import LocalRepositories
from forgetful_factory.application.ports.planning import Planning, PlanningReadError
from forgetful_factory.application.ports.work_source_resolver import WorkSourceResolver
from forgetful_factory.application.ports.worktrees import (
    WorktreeProblem,
    WorktreeReadError,
    Worktrees,
)
from forgetful_factory.application.watcher_problems import (
    IntakeProblem,
    RepositoryProblem,
    ScaffoldProblem,
    ScaffoldReadProblem,
    UncertainScaffold,
)
from forgetful_factory.domain.models import FactoryError, Issue, RepositoryReference, WorkSource


def _cleanup_state(mapping: dict) -> str | None:
    if 'cleanup' not in mapping:
        return None
    cleanup = mapping['cleanup']
    if not isinstance(cleanup, dict):
        raise ScaffoldProblem(
            'cleanup_invalid',
            'Invalid worktree cleanup record; reconcile it before continuing.')
    state = cleanup.get('state')
    url = cleanup.get('pull_request_url')
    commit = cleanup.get('merge_commit')
    repository = re.escape(mapping['repository'])
    expected = rf'https://github\.com/(?ai:{repository})/pull/[1-9][0-9]*'
    if (state not in ('pending', 'removed') or not isinstance(url, str)
            or re.fullmatch(expected, url) is None or not isinstance(commit, str)
            or re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', commit) is None):
        raise ScaffoldProblem(
            'cleanup_invalid', 'Invalid worktree cleanup state or merge evidence; reconcile the '
            'matching canonical GitHub PR URL and full merge commit SHA.')
    return state


class ScaffoldIssue:
    def __init__(self, planning: Planning, worktrees: Worktrees, workspace: Path,
                 config: FactoryConfiguration, repositories: LocalRepositories,
                 sources: WorkSourceResolver):
        self.planning = planning
        self.worktrees = worktrees
        self.workspace = workspace
        self.config = config
        self.repositories = repositories
        self.sources = sources

    def check(self) -> None:
        self.planning.check()

    def check_repository(self, repository: RepositoryReference) -> None:
        try:
            remote = self.repositories.origin(Path(repository.local_dir))
        except FactoryError as error:
            raise RepositoryProblem('repository_read_failed', str(error),
                                    paths=(repository.local_dir,)) from error
        if remote != repository.remote:
            raise RepositoryProblem('repository_origin_changed',
                                    f'Repository origin changed for {repository.local_dir}; '
                                    'reconcile Git and saved configuration.',
                                    paths=(repository.local_dir,))
        self._check_source(repository)

    def _check_source(self, repository: RepositoryReference) -> None:
        try:
            source = self.sources.source_from_remote(repository.remote)
        except FactoryError as error:
            raise RepositoryProblem('repository_source_mismatch', str(error),
                                    paths=(repository.local_dir,)) from error
        expected = repository.work_source
        if source != WorkSource(expected.provider, expected.reference.casefold()):
            raise RepositoryProblem('repository_source_mismatch',
                                    f'Origin/source mapping differs for {repository.local_dir}.',
                                    paths=(repository.local_dir,))

    def prepare(self, issue: Issue) -> dict | None:
        plan_id = self.lookup(issue)
        if plan_id is not None:
            result = self.recover(plan_id, issue.id, issue=issue)
            return result[1] if result is not None else None
        self.preflight(issue)
        plan = self._create_plan(issue)
        try:
            return self._prepare_plan(issue, plan)
        except ScaffoldProblem as error:
            error.plan_id = plan['id']
            raise
        except PlanningReadError as error:
            raise ScaffoldReadProblem('recovery_read_failed', str(error),
                                      plan_id=plan['id']) from error
        except FactoryError as error:
            raise UncertainScaffold('scaffold_operation_uncertain', str(error),
                                    plan_id=plan['id']) from error

    def _repository(self, source: WorkSource) -> RepositoryReference:
        return next(r for r in self.config.repository
                    if r.work_source.provider == source.provider
                    and r.work_source.reference.casefold() == source.reference.casefold())

    def _initial_mappings(self, issue: Issue) -> list[dict]:
        if issue.epic:
            return []
        repository = self._repository(issue.source)
        name = issue.source.reference.replace('/', '-') + f'-{issue.number}'
        return [{'repository': issue.source.reference, 'local_dir': repository.local_dir,
                 'branch': f'factory/{name}',
                 'path': str(self.workspace / '.factory/worktrees' / name)}]

    def preflight(self, issue: Issue) -> None:
        self.check_repository(self._repository(issue.source))
        for mapping in self._initial_mappings(issue):
            try:
                self.worktrees.inspect(mapping['local_dir'], mapping['branch'], mapping['path'],
                                       remote=self._repository(issue.source).remote)
            except WorktreeProblem as error:
                raise IntakeProblem(error.code, str(error), paths=error.paths) from error
            except WorktreeReadError as error:
                raise IntakeProblem('worktree_read_failed', str(error),
                                    paths=(mapping['path'],)) from error

    def _prepare_plan(self, issue: Issue, plan: dict) -> dict | None:
        context = self._context(plan)
        if not self._active(plan):
            return None
        tasks, mappings = self._setup_ownership(plan['id'], issue, context)
        self._ensure_setup_worktrees(mappings, tasks)
        if not tasks:
            tasks = self._create_ownership(plan['id'], issue.id, context, mappings)
        task = tasks[0]
        return {'plan_id': plan['id'], 'ownership_task_id': task['id'], 'worktrees': mappings,
                'epic': issue.epic, 'repositories': [asdict(r) for r in self.config.repository]}

    def _setup_ownership(self, plan_id: int, issue: Issue,
                         context: dict) -> tuple[list[dict], list[dict]]:
        tasks = self._ownership(plan_id, issue.id)
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
                    else self._initial_mappings(issue))
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
        self.planning.update_plan(plan_id, context=json.dumps(context))
        try:
            self.planning.create_task(
                plan_id=plan_id, title='Feature ownership',
                description=json.dumps({'kind': 'factory-ownership',
                                        'workspace': str(self.workspace),
                                        'external_ref': external_ref, 'worktrees': mappings}))
        except FactoryError:
            pass
        try:
            tasks = self._ownership(plan_id, external_ref)
        except FactoryError as error:
            raise UncertainScaffold('ownership_create_uncertain', str(error)) from error
        if len(tasks) != 1:
            raise UncertainScaffold(
                'ownership_create_uncertain',
                'Ownership creation uncertain; reconcile all plan tasks. '
                'The create-intent is saved; no automatic retry is permitted.')
        return tasks

    def lookup(self, issue: Issue) -> int | None:
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

    def _create_plan(self, issue: Issue) -> dict:
        try:
            self.planning.create_plan(
                title=issue.title, project_id=self.config.forgetful.project_id,
                external_ref=issue.id, source_url=issue.url,
                context=json.dumps({'workspace': str(self.workspace), 'issue': asdict(issue)}))
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
        if plan.get('project_id') != self.config.forgetful.project_id:
            raise ScaffoldProblem('plan_project_mismatch',
                                  f'{issue.id} already belongs to another project; reconcile it.',
                                  plan_id=plan['id'])
        return plan

    def unfinished(self) -> list[dict]:
        sources = {r.work_source.reference.casefold() for r in self.config.repository}
        return [p for p in self.planning.plans()
                if self._is_unfinished_factory_plan(p, sources)]

    def recover(self, plan_id: int, external_ref: str, *, issue: Issue | None = None,
                task_ids: tuple[int, ...] | None = None) -> tuple[Issue, dict] | None:
        """Read known identities only. Missing records never fall back to scaffolding."""
        try:
            plan = self._recovery_plan(plan_id, external_ref)
            context = self._context(plan)
            if not self._active(plan):
                return None
            snapshot = self._snapshot(context, external_ref)
            self.check_repository(self._repository(snapshot.source))
            owners = self._ownership(plan_id, external_ref)
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
        if plan.get('project_id') != self.config.forgetful.project_id:
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

    def _snapshot(self, context: dict, external_ref: str) -> Issue:
        try:
            snapshot = dict(context['issue'])
            source = WorkSource(**snapshot.pop('source'))
            issue = Issue(source, **snapshot)
            if (not isinstance(source.provider, str) or not isinstance(source.reference, str)
                    or type(issue.number) is not int or issue.number < 1
                    or any(not isinstance(field, str) for field in (
                        issue.title, issue.url, issue.body, issue.revision))
                    or type(issue.epic) is not bool or issue.id != external_ref):
                raise ValueError('Invalid saved issue or changed association')
            return issue
        except (KeyError, TypeError, ValueError) as error:
            raise ScaffoldProblem('plan_recovery_invalid',
                                  'Cannot restore factory plan; reconcile its context.') from error

    def _is_unfinished_factory_plan(self, summary: dict, sources: set[str]) -> bool:
        project_id = summary.get('project_id')
        status = summary.get('status')
        if (type(project_id) is int and project_id != self.config.forgetful.project_id
                or status in ('completed', 'archived')):
            return False
        # A known reference with invalid association/status still needs per-plan recovery checks.
        reference = summary.get('external_ref') or ''
        if not isinstance(reference, str):
            raise FactoryError('Factory plan inventory has invalid references; reconcile it.')
        return any(reference.startswith(f'github:{source}#') for source in sources)

    @staticmethod
    def _active(plan: dict) -> bool:
        status = plan.get('status')
        if (not isinstance(status, str)
                or status not in ('draft', 'active', 'completed', 'archived')):
            raise ScaffoldProblem('plan_status_invalid',
                                  'Saved plan status is invalid; reconcile it before continuing.')
        return status in ('draft', 'active')

    def _context(self, plan: dict) -> dict:
        try:
            context = json.loads(plan.get('context') or '{}')
            if not isinstance(context, dict) or 'workspace' not in context:
                raise ValueError('Missing association')
        except (TypeError, ValueError) as error:
            raise ScaffoldProblem(
                'plan_context_invalid', 'Factory plan has invalid context; reconcile its workspace '
                'association without creating another plan.') from error
        if context['workspace'] != str(self.workspace):
            raise ScaffoldProblem(
                'plan_workspace_mismatch', 'Plan belongs to another workspace. One workspace per '
                'plan is supported; its lease cannot coordinate other factories. '
                'Stop the other factory and explicitly reconcile the association.')
        return context

    def _ownership(self, plan_id: int, external_ref: str) -> list[dict]:
        candidates = []
        for task in self.planning.tasks(plan_id):
            try:
                record = json.loads(task.get('description') or '{}')
            except (TypeError, ValueError):
                record = {}
            marked = isinstance(record, dict) and record.get('kind') == 'factory-ownership'
            if not marked and task.get('title') != 'Feature ownership':
                continue
            candidates.append((task, record, marked))
        owners = []
        task_ids = tuple(task['id'] for task, _, _ in candidates)
        for task, record, marked in candidates:
            if (not marked or record.get('workspace') != str(self.workspace)
                    or record.get('external_ref') != external_ref
                    or not isinstance(record.get('worktrees'), list)
                    or task.get('plan_id') != plan_id):
                raise ScaffoldProblem(
                    'ownership_invalid',
                    'Ownership record is invalid or belongs to another workspace; '
                    'reconcile the full task description before continuing.', task_ids=task_ids)
            owners.append(task)
        return owners

    def _ensure_worktrees(self, mappings: list[dict], *, recorded: bool) -> None:
        seen = set()
        for mapping in mappings:
            repository = self._mapping_repository(mapping, seen)
            self._ensure_validated_mapping(repository, mapping, recorded=recorded)

    def _mapping_repository(self, mapping: dict, seen: set[str]) -> RepositoryReference:
        try:
            if not isinstance(mapping, dict):
                raise ValueError('Mapping is not an object')
            repository_name = mapping.get('repository')
            local_dir = mapping.get('local_dir')
            branch = mapping.get('branch')
            path = mapping.get('path')
            if (not isinstance(repository_name, str) or not repository_name
                    or not isinstance(local_dir, str) or not local_dir
                    or not isinstance(branch, str) or not branch
                    or not isinstance(path, str) or not path):
                raise ValueError('Incomplete mapping')
            if not Path(path).is_absolute() or path in seen:
                raise ValueError('Invalid or duplicate path')
            repository = next(r for r in self.config.repository
                              if r.local_dir == local_dir and
                              r.work_source.reference.casefold() == repository_name)
        except (ValueError, StopIteration) as error:
            raise ScaffoldProblem(
                'mapping_invalid', 'Invalid ownership worktree mapping; reconcile it with the '
                'configured repositories; work is preserved.') from error
        seen.add(path)
        return repository

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
        self._check_source(repository)
        state = _cleanup_state(mapping)
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
