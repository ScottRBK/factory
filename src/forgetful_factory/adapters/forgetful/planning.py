from pathlib import Path

from forgetful_factory.adapters.forgetful.connection import AgentForgetfulConnection
from forgetful_factory.application.configuration import ForgetfulConnection
from forgetful_factory.application.ports.planning import PlanningReadError
from forgetful_factory.domain.models import FactoryError


def _positive_id(value: object) -> bool:
    return type(value) is int and value > 0


class ForgetfulPlanning:
    def __init__(self, workspace: Path, connection: ForgetfulConnection, *,
                 execution_enabled: bool, term_grace: float = 3):
        self.cli = AgentForgetfulConnection(workspace, term_grace)
        self.connection = connection
        self.execution_enabled = execution_enabled

    def check(self) -> None:
        self.cli.check(self.connection, execution_enabled=self.execution_enabled)

    def _call(self, tool: str, **fields) -> dict:
        return self.cli.call(self.connection, tool, **fields)

    def _read(self, tool: str, **fields) -> dict:
        try:
            return self._call(tool, **fields)
        except FactoryError as error:
            raise PlanningReadError(str(error)) from error

    def plans(self, external_ref: str | None = None) -> list[dict]:
        result = self._read('list_plans', **(
            {'external_ref': external_ref} if external_ref is not None else {}))
        return self._rows(result, 'plans')

    @staticmethod
    def _rows(result: dict, key: str) -> list[dict]:
        rows = result.get(key)
        count = result.get('total_count')
        if (not isinstance(rows, list) or type(count) is not int or count < 0
                or count != len(rows)
                or any(not isinstance(row, dict) or not _positive_id(row.get('id')) for row in rows)
                or len({row['id'] for row in rows}) != len(rows)):
            raise PlanningReadError(f'Forgetful returned incomplete or invalid {key}; '
                                    'reconcile the native inventory before continuing.')
        return rows

    def get_plan(self, plan_id: int) -> dict:
        plan = self._read('get_plan', plan_id=plan_id)
        if (not _positive_id(plan.get('id')) or plan['id'] != plan_id
                or not _positive_id(plan.get('project_id'))):
            raise PlanningReadError('Forgetful returned invalid plan identity or project '
                                    'association; reconcile the native read reply '
                                    'before continuing.')
        return plan

    def create_plan(self, **fields) -> dict:
        return self._call('create_plan', **fields)

    def update_plan(self, plan_id: int, **fields) -> dict:
        return self._call('update_plan', plan_id=plan_id, **fields)

    def tasks(self, plan_id: int) -> list[dict]:
        rows = self._rows(self._read('query_tasks', plan_id=plan_id), 'tasks')
        return [self._task(row['id'], plan_id) for row in rows]

    def _task(self, task_id: int, plan_id: int) -> dict:
        task = self._read('get_task', task_id=task_id)
        if (not _positive_id(task.get('id')) or task['id'] != task_id
                or not _positive_id(task.get('plan_id')) or task['plan_id'] != plan_id):
            raise PlanningReadError('Forgetful returned invalid task identity or association; '
                                    'reconcile the native read reply before continuing.')
        return task

    def create_task(self, **fields) -> dict:
        return self._call('create_task', **fields)

    def update_task(self, task_id: int, **fields) -> dict:
        return self._call('update_task', task_id=task_id, **fields)
