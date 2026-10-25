"""Execution permission checks through watch CLI and the external terminal/backend fixtures."""
import json
import time

from profile_support import events
from test_planning_watch import PlanningWatchFixture


class WorkerWatchPermissionTests(PlanningWatchFixture):
    def permission_fixture(self):
        log = self.workspace / 'permission-reads.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        program = self.bin / 'forgetful'
        content = program.read_text()
        marker = "tools = [{'name': tool, 'parameters': {"
        self.assertEqual(content.count(marker), 1)
        program.write_text(content.replace(
            marker, "tools = [{'name': tool, 'description': 'TOP_SECRET native tool details', "
            "'parameters': {"))
        self.script({'team/app': [[[self.issue(1)]]]})
        return log, program

    def test_execution_watch_alerts_and_waits_for_verification_permission_before_intake(self):
        # Arrange: this test changes the public execution permission, without dispatching workers.
        config = self.workspace / '.factory/factory.toml'
        content = config.read_text()
        self.assertIn('execution_enabled = false', content)
        config.write_text(content.replace('execution_enabled = false', 'execution_enabled = true'))
        receipt = self.workspace / '.factory/setup-complete.json'
        completion = receipt.read_bytes()
        log, program = self.permission_fixture()
        # Act: missing verify_criterion is checked after a valid Foreman is ready.
        process = self.start('--existing', '--interval', '.5')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: sum(e['args'][:2] == ['tools', 'list']
                                           for e in events(log)) >= 3)
        time.sleep(.1)
        self.assertIsNone(process.poll())
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'send'])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.alerts()[0]['code'], 'planning_access_failed')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self._messages(), [])
        self.assertFalse((self.workspace / '.factory/fixture-plans.json').exists())
        self.assertNotIn('counts', json.loads(self.state_path.read_text()))
        calls = [e['args'][:2] for e in events(log) if e['name'] == 'forgetful']
        self.assertGreaterEqual(calls.count(['tools', 'list']), 3)
        self.assertTrue(all(call in (['call', 'get_project'], ['tools', 'list']) for call in calls))
        # Act: correct only the external permission catalog; the same watcher must recover.
        condition = "failure == 'verification' and tool == 'verify_criterion'"
        content = program.read_text()
        self.assertEqual(content.count(condition), 1)
        program.write_text(content.replace(condition, 'False'))
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, output, errors = self.stop(process)
        # Assert: no credential output, setup mutation, duplicate root or premature intake.
        self.assertEqual(code, 130, errors)
        self.assertIn('planning check failed', errors)
        self.assertNotIn('TOP_SECRET', output + errors + json.dumps(self.events()))
        self.assertEqual(receipt.read_bytes(), completion)
        self.assertEqual(sum(e['kind'] == 'launch' for e in self.events()), 1)
        self.assertEqual(sum(e['kind'] == 'close' for e in self.events()), 1)
        self.assertEqual(len(self.alerts()), 1)
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)

    def test_planning_only_watch_accepts_twelve_tools_without_verification_permission(self):
        # Arrange: the same twelve-tool catalog is sufficient when execution is disabled.
        self.permission_fixture()
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, output, errors = self.stop(process)
        # Assert: planning-only intake can scaffold and notify; no agent work is dispatched.
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.alerts(), [])
        self.assertNotIn('TOP_SECRET', output + errors + json.dumps(self.events()))
        self.assertEqual(self._messages()[0]['plan_id'], 1)
        self.assertEqual(sum(e['kind'] == 'launch' for e in self.events()), 1)
