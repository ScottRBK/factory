import json
from dataclasses import asdict
from pathlib import Path

from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.ports.planning import Planning
from forgetful_factory.application.ports.worktrees import Worktrees
from forgetful_factory.domain.models import FactoryError, Issue, WorkSource


class ScaffoldIssue:
    def __init__(self, planning: Planning, worktrees: Worktrees, workspace: Path,
                 config: FactoryConfiguration):
        self.planning = planning
        self.worktrees = worktrees
        self.workspace = workspace
        self.config = config

    def check(self) -> None:
        self.planning.check()

    def prepare(self, issue: Issue) -> dict:
        plan = self._issue_plan(issue)
        context = self._context(plan)
        tasks = self._ownership(plan['id'], issue.id)
        if len(tasks) > 1:
            raise FactoryError(f'Ambiguous ownership for plan {plan["id"]}; reconcile duplicates.')
        if not tasks and context.get('ownership_create_started'):
            raise FactoryError('Ownership creation uncertain; inspect all plan tasks and confirm '
                               'the earlier request stopped before explicitly reconciling '
                               'ownership_create_started in the plan context. No retry was made.')
        mappings = []
        if tasks:
            mappings = json.loads(tasks[0]['description'])['worktrees']
        elif not issue.epic:
            repository = next(r for r in self.config.repository
                              if r.work_source.reference.casefold() == issue.source.reference)
            name = issue.source.reference.replace('/', '-') + f'-{issue.number}'
            mappings = [{'repository': issue.source.reference, 'local_dir': repository.local_dir,
                         'branch': f'factory/{name}',
                         'path': str(self.workspace / '.factory/worktrees' / name)}]
        self._ensure_worktrees(mappings, recorded=bool(tasks))
        if not tasks:
            context['ownership_create_started'] = True
            self.planning.update_plan(plan['id'], context=json.dumps(context))
            try:
                self.planning.create_task(
                    plan_id=plan['id'], title='Feature ownership',
                    description=json.dumps({'kind': 'factory-ownership',
                                            'workspace': str(self.workspace),
                                            'external_ref': issue.id, 'worktrees': mappings}))
            except FactoryError:
                pass
            tasks = self._ownership(plan['id'], issue.id)
            if len(tasks) != 1:
                raise FactoryError('Ownership creation uncertain; reconcile all plan tasks. '
                                   'The create-intent is saved; no automatic retry is permitted.')
        task = tasks[0]
        return {'plan_id': plan['id'], 'ownership_task_id': task['id'], 'worktrees': mappings,
                'epic': issue.epic, 'repositories': [asdict(r) for r in self.config.repository]}

    def _issue_plan(self, issue: Issue) -> dict:
        plans = self.planning.plans(issue.id)
        if len(plans) > 1:
            raise FactoryError(f'Ambiguous plans for {issue.id}; reconcile duplicates.')
        if not plans:
            try:
                self.planning.create_plan(
                    title=issue.title, project_id=self.config.forgetful.project_id,
                    external_ref=issue.id, source_url=issue.url,
                    context=json.dumps({'workspace': str(self.workspace), 'issue': asdict(issue)}))
            except FactoryError:
                # A failed response does not tell us whether the unique create committed.
                pass
            plans = self.planning.plans(issue.id)
        if len(plans) != 1:
            raise FactoryError(f'Plan creation uncertain for {issue.id}; '
                               'reconcile before retrying.')
        plan = self.planning.get_plan(plans[0]['id'])
        if plan['project_id'] != self.config.forgetful.project_id:
            raise FactoryError(f'{issue.id} already belongs to another project; reconcile it.')
        return plan

    def unfinished(self) -> list[Issue]:
        issues = []
        sources = {r.work_source.reference.casefold() for r in self.config.repository}
        for summary in self.planning.plans():
            if not self._is_unfinished_factory_plan(summary, sources):
                continue
            plan = self.planning.get_plan(summary['id'])
            context = self._context(plan)
            try:
                snapshot = dict(context['issue'])
                source = WorkSource(**snapshot.pop('source'))
                if context['workspace'] != str(self.workspace) or source.reference not in sources:
                    continue
                issue = Issue(source, **snapshot)
                if issue.id != plan['external_ref']:
                    raise ValueError('Issue changed')
                issues.append(issue)
            except (KeyError, TypeError, ValueError) as error:
                if (plan.get('external_ref') or '').startswith('github:'):
                    raise FactoryError('Cannot restore factory plan; '
                                       'reconcile its context.') from error
        return issues

    def _is_unfinished_factory_plan(self, summary: dict, sources: set[str]) -> bool:
        if (summary['project_id'] != self.config.forgetful.project_id
                or summary['status'] not in ('draft', 'active')):
            return False
        reference = summary.get('external_ref') or ''
        return any(reference.startswith(f'github:{source}#') for source in sources)

    def _context(self, plan: dict) -> dict:
        try:
            context = json.loads(plan.get('context') or '{}')
            if not isinstance(context, dict) or 'workspace' not in context:
                raise ValueError('Missing association')
        except (TypeError, ValueError) as error:
            raise FactoryError('Factory plan has invalid context; reconcile its workspace '
                               'association without creating another plan.') from error
        if context['workspace'] != str(self.workspace):
            raise FactoryError('Plan belongs to another workspace. One workspace per plan is '
                               'supported; its lease cannot coordinate other factories. '
                               'Stop the other factory and explicitly reconcile the association.')
        return context

    def _ownership(self, plan_id: int, external_ref: str) -> list[dict]:
        owners = []
        for task in self.planning.tasks(plan_id):
            try:
                record = json.loads(task.get('description') or '{}')
            except (TypeError, ValueError):
                record = {}
            marked = isinstance(record, dict) and record.get('kind') == 'factory-ownership'
            if not marked and task.get('title') != 'Feature ownership':
                continue
            if (not marked or record.get('workspace') != str(self.workspace)
                    or record.get('external_ref') != external_ref
                    or not isinstance(record.get('worktrees'), list)
                    or task.get('plan_id') != plan_id):
                raise FactoryError('Ownership record is invalid or belongs to another workspace; '
                                   'reconcile the full task description before continuing.')
            owners.append(task)
        return owners

    def _ensure_worktrees(self, mappings: list[dict], *, recorded: bool) -> None:
        seen = set()
        for mapping in mappings:
            try:
                if not isinstance(mapping, dict) or any(
                        not isinstance(mapping.get(key), str) or not mapping[key]
                        for key in ('repository', 'local_dir', 'branch', 'path')):
                    raise ValueError('Incomplete mapping')
                if not Path(mapping['path']).is_absolute() or mapping['path'] in seen:
                    raise ValueError('Invalid or duplicate path')
                seen.add(mapping['path'])
                repository = next(r for r in self.config.repository
                                  if r.local_dir == mapping['local_dir'] and
                                  r.work_source.reference.casefold() == mapping['repository'])
            except (ValueError, StopIteration) as error:
                raise FactoryError('Invalid ownership worktree mapping; reconcile it with the '
                                   'configured repositories; work is preserved.') from error
            self.worktrees.ensure(repository.local_dir, mapping['branch'], mapping['path'],
                                  recorded=recorded, remote=repository.remote)
