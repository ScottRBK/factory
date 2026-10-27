"""Forgetful planning reads through the real adapter and controlled CLI boundary."""
import json
import tempfile
import unittest
from pathlib import Path

from forgetful_factory.adapters.forgetful.planning import ForgetfulPlanning
from forgetful_factory.application.configuration import ForgetfulConnection
from forgetful_factory.application.ports.planning import PlanningReadError

MISSING = object()
INVALID_IDENTIFIERS = (
    True,
    False,
    0,
    -1,
    1.0,
    'TOP_SECRET invalid identifier',
    None,
)
INVENTORY_IDENTIFIERS = (
    True,
    False,
    0,
    -1,
    1.0,
    'TOP_SECRET row identifier',
    None,
    [],
    {},
)
INVALID_COUNTS = (False, True, -1, 1.0, '1', None)

FORGETFUL = '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

root = Path(sys.argv[0]).resolve().parent.parent
args = sys.argv[1:]
if len(args) != 7 or args[0] != 'call' or args[2] != '--args':
    sys.exit('unexpected Forgetful arguments')
if args[4:] != ['--server', 'https://memory.example/test', '--json']:
    sys.exit('unexpected Forgetful target')
tool = args[1]
arguments = json.loads(args[3])
control = json.loads((root / 'responses.json').read_text())
response = control[tool]
if tool == 'get_task' and response and all(key.isdigit() for key in response):
    response = response[str(arguments['task_id'])]
with (root / 'calls.jsonl').open('a') as stream:
    stream.write(json.dumps({
        'tool': tool,
        'arguments': arguments,
        'cwd': os.getcwd(),
        'has_token': 'FORGETFUL_TOKEN' in os.environ,
    }) + '\\n')
print(json.dumps(response))
'''


class PlanningAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        (self.workspace / '.factory').mkdir()
        executable = self.workspace / 'bin/forgetful'
        executable.parent.mkdir()
        executable.write_text(FORGETFUL)
        executable.chmod(0o755)
        connection = ForgetfulConnection(
            instance='server',
            executable=str(executable),
            server='https://memory.example/test',
            project_id=12,
        )
        self.planning = ForgetfulPlanning(
            self.workspace,
            connection,
            execution_enabled=False,
        )

    def responses(self, **responses):
        (self.workspace / 'responses.json').write_text(json.dumps(responses))

    def calls(self):
        path = self.workspace / 'calls.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()]

    @staticmethod
    def changed(record, field, value):
        changed = dict(record)
        if value is MISSING:
            del changed[field]
        else:
            changed[field] = value
        return changed

    @staticmethod
    def inventory_cases(key):
        for count in INVALID_COUNTS:
            rows = [] if count is False else [{'id': 1}]
            yield f'count={count!r}', {key: rows, 'total_count': count}
        for identity in INVENTORY_IDENTIFIERS:
            yield f'id={identity!r}', {key: [{'id': identity}], 'total_count': 1}
        yield 'missing id', {key: [{}], 'total_count': 1}

    def test_tasks_reject_malformed_full_task_identity_and_association(self):
        # Arrange: preserve the former watcher's exact 18 task-detail corruptions.
        task = {'id': 1, 'plan_id': 1, 'title': 'Ownership'}
        cases = [
            (field, value, self.changed(task, field, value))
            for field in ('id', 'plan_id')
            for value in (*INVALID_IDENTIFIERS, 2, MISSING)
        ]
        self.assertEqual(len(cases), 18)

        for field, value, response in cases:
            with self.subTest(field=field, value=value):
                self.responses(
                    query_tasks={'tasks': [{'id': 1}], 'total_count': 1},
                    get_task=response,
                )
                # Act and assert: the public read rejects unsafe full task records.
                with self.assertRaisesRegex(
                        PlanningReadError, 'invalid task identity or association'):
                    self.planning.tasks(1)

        calls = self.calls()
        self.assertEqual(len(calls), 36)
        self.assertEqual({call['tool'] for call in calls}, {'query_tasks', 'get_task'})

    def test_get_plan_rejects_malformed_identity_and_project_association(self):
        # Arrange: preserve the former watcher's exact 17 plan-detail corruptions.
        plan = {'id': 1, 'project_id': 12, 'title': 'Issue plan'}
        cases = []
        for field in ('id', 'project_id'):
            values = [*INVALID_IDENTIFIERS]
            if field == 'id':
                values.append(2)
            values.append(MISSING)
            cases.extend((field, value, self.changed(plan, field, value)) for value in values)
        self.assertEqual(len(cases), 17)

        for field, value, response in cases:
            with self.subTest(field=field, value=value):
                self.responses(get_plan=response)
                # Act and assert: the requested plan needs a trustworthy identity and project.
                with self.assertRaisesRegex(
                        PlanningReadError, 'invalid plan identity or project association'):
                    self.planning.get_plan(1)

        calls = self.calls()
        self.assertEqual(len(calls), 17)
        self.assertTrue(all(call['arguments'] == {'plan_id': 1} for call in calls))

    def test_plans_reject_malformed_count_and_row_identity(self):
        # Arrange: preserve the former watcher's exact 16 plan-inventory corruptions.
        cases = list(self.inventory_cases('plans'))
        self.assertEqual(len(cases), 16)

        for label, response in cases:
            with self.subTest(case=label):
                self.responses(list_plans=response)
                # Act and assert: an incomplete inventory cannot become planning facts.
                with self.assertRaisesRegex(
                        PlanningReadError, 'incomplete or invalid plans'):
                    self.planning.plans()

        calls = self.calls()
        self.assertEqual(len(calls), 16)
        self.assertTrue(all(call['arguments'] == {} for call in calls))

    def test_tasks_reject_malformed_count_and_row_identity(self):
        # Arrange: preserve the former watcher's exact 16 task-inventory corruptions.
        cases = list(self.inventory_cases('tasks'))
        self.assertEqual(len(cases), 16)

        for label, response in cases:
            with self.subTest(case=label):
                self.responses(
                    query_tasks=response,
                    get_task={'id': 1, 'plan_id': 1, 'title': 'Ownership'},
                )
                # Act and assert: malformed summary rows never drive full task reads.
                with self.assertRaisesRegex(
                        PlanningReadError, 'incomplete or invalid tasks'):
                    self.planning.tasks(1)

        calls = self.calls()
        self.assertEqual(len(calls), 16)
        self.assertTrue(all(call['tool'] == 'query_tasks' for call in calls))

    def test_plans_return_valid_empty_inventory(self):
        # Arrange
        self.responses(list_plans={'plans': [], 'total_count': 0})
        # Act
        plans = self.planning.plans()
        # Assert: a valid empty boundary returns instead of always raising.
        self.assertEqual(plans, [])

    def test_plans_return_valid_multiple_rows_and_forwards_reference(self):
        # Arrange
        self.responses(list_plans={
            'plans': [{'id': 1, 'title': 'First'}, {'id': 2, 'title': 'Second'}],
            'total_count': 2,
        })
        # Act
        plans = self.planning.plans('github:team/app#1')
        # Assert
        self.assertEqual([plan['title'] for plan in plans], ['First', 'Second'])
        self.assertEqual(self.calls()[0]['arguments'], {'external_ref': 'github:team/app#1'})
        self.assertEqual(self.calls()[0]['cwd'], str(self.workspace / '.factory'))
        self.assertFalse(self.calls()[0]['has_token'])

    def test_get_plan_returns_valid_positive_boundary(self):
        # Arrange
        plan = {'id': 1, 'project_id': 1, 'title': 'Boundary plan'}
        self.responses(get_plan=plan)
        # Act
        result = self.planning.get_plan(1)
        # Assert
        self.assertEqual(result, plan)
        self.assertEqual(self.calls()[0]['arguments'], {'plan_id': 1})

    def test_tasks_return_valid_empty_inventory(self):
        # Arrange
        self.responses(query_tasks={'tasks': [], 'total_count': 0})
        # Act
        tasks = self.planning.tasks(1)
        # Assert
        self.assertEqual(tasks, [])

    def test_tasks_return_valid_multiple_full_records(self):
        # Arrange
        first = {'id': 1, 'plan_id': 1, 'title': 'Ownership'}
        second = {'id': 2, 'plan_id': 1, 'title': 'Implementation'}
        self.responses(
            query_tasks={'tasks': [{'id': 1}, {'id': 2}], 'total_count': 2},
            get_task={'1': first, '2': second},
        )
        # Act
        tasks = self.planning.tasks(1)
        # Assert: valid task inventories resolve through public full-record behavior.
        self.assertEqual(tasks, [first, second])
        self.assertEqual(
            [(call['tool'], call['arguments']) for call in self.calls()],
            [('query_tasks', {'plan_id': 1}),
             ('get_task', {'task_id': 1}),
             ('get_task', {'task_id': 2})],
        )


if __name__ == '__main__':
    unittest.main()
