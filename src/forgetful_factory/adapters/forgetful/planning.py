from pathlib import Path

from forgetful_factory.adapters.forgetful.connection import AgentForgetfulConnection
from forgetful_factory.application.configuration import ForgetfulConnection
from forgetful_factory.domain.models import FactoryError


class ForgetfulPlanning:
    def __init__(self, workspace: Path, connection: ForgetfulConnection):
        self.cli = AgentForgetfulConnection(workspace)
        self.connection = connection

    def check(self) -> None:
        self.cli.check(self.connection)

    def _call(self, tool: str, **fields) -> dict:
        return self.cli.call(self.connection, tool, **fields)

    def plans(self, external_ref: str | None = None) -> list[dict]:
        result = self._call('list_plans', **(
            {'external_ref': external_ref} if external_ref is not None else {}))
        return self._rows(result, 'plans')

    @staticmethod
    def _rows(result: dict, key: str) -> list[dict]:
        rows = result.get(key)
        if (not isinstance(rows, list) or result.get('total_count') != len(rows)
                or any(not isinstance(row, dict) or type(row.get('id')) is not int
                       for row in rows)):
            raise FactoryError(f'Forgetful returned incomplete {key}; stop and reconcile.')
        return rows

    def get_plan(self, plan_id: int) -> dict:
        return self._call('get_plan', plan_id=plan_id)

    def create_plan(self, **fields) -> dict:
        return self._call('create_plan', **fields)

    def update_plan(self, plan_id: int, **fields) -> dict:
        return self._call('update_plan', plan_id=plan_id, **fields)

    def tasks(self, plan_id: int) -> list[dict]:
        rows = self._rows(self._call('query_tasks', plan_id=plan_id), 'tasks')
        return [self._call('get_task', task_id=row['id']) for row in rows]

    def create_task(self, **fields) -> dict:
        return self._call('create_task', **fields)

    def update_task(self, task_id: int, **fields) -> dict:
        return self._call('update_task', task_id=task_id, **fields)
