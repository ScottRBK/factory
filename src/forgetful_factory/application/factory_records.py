"""Shared saved-record and repository identity checks; no lifecycle writes."""
import json
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.ports.local_repositories import LocalRepositories
from forgetful_factory.application.ports.planning import Planning
from forgetful_factory.application.watcher_problems import RepositoryProblem, ScaffoldProblem
from forgetful_factory.domain.models import RepositoryReference
from forgetful_factory.forge.model import RepositoryRef
from forgetful_factory.forge.ports import Forge
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.model import Ticket, TicketSource


class FactoryRecords:
    def __init__(self, planning: Planning, workspace: Path, config: FactoryConfiguration,
                 repositories: LocalRepositories, forge: Forge):
        self.planning = planning
        self.workspace = workspace
        self.config = config
        self.repositories = repositories
        self.forge = forge

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
        self.check_source(repository)

    def check_source(self, repository: RepositoryReference) -> RepositoryRef:
        """Return the forge repository of the remote, checking it against the ticket source."""
        try:
            hosted = self.forge.repository(repository.remote)
        except FactoryError as error:
            raise RepositoryProblem('repository_source_mismatch', str(error),
                                    paths=(repository.local_dir,)) from error
        source = repository.work_source
        # The remote names the ticket source only when one service is both forge and ticketing.
        if hosted.forge == source.provider and hosted.reference != source.reference.casefold():
            raise RepositoryProblem('repository_source_mismatch',
                                    f'Origin/source mapping differs for {repository.local_dir}.',
                                    paths=(repository.local_dir,))
        return hosted

    def snapshot(self, context: dict, external_ref: str) -> Ticket:
        try:
            snapshot = dict(context['issue'])
            source = TicketSource(**snapshot.pop('source'))
            issue = Ticket(source, **snapshot)
            if (not isinstance(source.provider, str) or not isinstance(source.reference, str)
                    or not isinstance(issue.key, str) or not issue.key
                    or any(not isinstance(field, str) for field in (
                        issue.title, issue.url, issue.body, issue.revision))
                    or type(issue.epic) is not bool or issue.id != external_ref):
                raise ValueError('Invalid saved issue or changed association')
            return issue
        except (KeyError, TypeError, ValueError) as error:
            raise ScaffoldProblem('plan_recovery_invalid',
                                  'Cannot restore factory plan; reconcile its context.') from error

    @staticmethod
    def active(plan: dict) -> bool:
        status = plan.get('status')
        if (not isinstance(status, str)
                or status not in ('draft', 'active', 'completed', 'archived')):
            raise ScaffoldProblem('plan_status_invalid',
                                  'Saved plan status is invalid; reconcile it before continuing.')
        return status in ('draft', 'active')

    def context(self, plan: dict) -> dict:
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

    def ownership(self, plan_id: int, external_ref: str) -> list[dict]:
        return self.ownership_records(plan_id, external_ref, self.planning.tasks(plan_id))

    def ownership_records(self, plan_id: int, external_ref: str,
                          tasks: list[dict]) -> list[dict]:
        candidates = []
        for task in tasks:
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

    def mapping_repository(self, mapping: dict, seen: set[str]) -> RepositoryReference:
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
