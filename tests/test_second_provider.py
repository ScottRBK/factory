"""A non-GitHub ticketing provider runs through intake, recovery and cleanup on a GitHub forge.

Import rules cannot see hard-coded GitHub strings, patterns or numeric-key assumptions in the
core. This runs the public watch CLI with the `tracker` fake (keys such as ENG-7) composed in.
"""
import json
from pathlib import Path

from contracts.ticketing import FakeTicketing
from test_completed_cleanup import CompletedCleanupFixture

from forgetful_factory.ticketing.model import TicketSource

TESTS = Path(__file__).parent
ENTRYPOINT = (
    'import os, sys; from pathlib import Path; sys.path.insert(0, os.environ["FACTORY_TESTS"]); '
    'from contracts.ticketing import FakeTicketing; '
    'import forgetful_factory.cli.bootstrap as bootstrap; '
    'bootstrap.TICKETING["tracker"] = '
    'lambda timeout: FakeTicketing(Path(os.environ["TRACKER_STATE"])); '
    'from forgetful_factory.cli.main import main; raise SystemExit(main())'
)


class SecondProviderTests(CompletedCleanupFixture):
    entrypoint = ('-c', ENTRYPOINT)
    source = TicketSource('tracker', 'platform')

    def setUp(self):
        super().setUp()
        self.env.update(FACTORY_TESTS=str(TESTS),
                        TRACKER_STATE=str(self.workspace / 'tracker.json'))
        self.tracker = FakeTicketing(self.workspace / 'tracker.json')

    def configure(self, labels=('factory',), sources=(), provider=''):
        # Tickets come from the tracker; code lives on GitHub at team/app.
        (self.workspace / '.factory').mkdir(exist_ok=True)
        (self.workspace / '.factory/factory.toml').write_text(
            'watcher_label = ["factory"]\n'
            'foreman_agent_file = "agents/foreman/agent.json"\n'
            'execution_enabled = false\n\n'
            '[[repository]]\n'
            f'local_dir = {json.dumps(str(self.workspace))}\n'
            'remote = "git@github.com:team/app.git"\n'
            'provider = "tracker"\nsource = "platform"\n\n'
            '[forgetful]\ninstance = "server"\nproject_id = 12\n'
            'server = "https://memory.example/custom-endpoint"\n')

    def ownership(self, message):
        task = self.planning_call('get_task', task_id=message['ownership_task_id'])
        return json.loads(task['description'])

    def test_tracker_ticket_is_planned_recovered_and_cleaned_up(self):
        # Arrange
        self.tracker.publish(self.source, [{'key': 'ENG-7', 'title': 'Add a habitat',
                                            'body': 'Requirements', 'labels': ['factory'],
                                            'state': 'open'}])
        # Act 1: intake through the public watcher.
        first = self.start('--existing')
        self.wait_until(first, lambda: bool(self._messages() or self.alerts()))
        code, _, errors = self.stop(first)
        # Assert 1: ids, keys and names come from the ticket, not GitHub patterns.
        self.assertEqual(self.alerts(), [], errors)
        message, = self._messages()
        self.assertEqual((message['id'], message['key']), ('tracker:platform#ENG-7', 'ENG-7'))
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        self.assertEqual(plan['external_ref'], 'tracker:platform#ENG-7')
        record = self.ownership(message)
        mapping, = record['worktrees']
        self.assertEqual(mapping['branch'], 'factory/platform-ENG-7')
        self.assertEqual(self.git(mapping['path'], 'branch', '--show-current'),
                         'factory/platform-ENG-7')
        # Act 2: the owner records a GitHub PR marker; a restart recovers the unfinished plan.
        mapping['cleanup'] = {'state': 'pending',
                              'pull_request_url': 'https://github.com/team/app/pull/7',
                              'merge_commit': 'a' * 40}
        self.planning_call('update_task', task_id=message['ownership_task_id'],
                           description=json.dumps(record))
        self.terminal_log.unlink()
        restarted = self.start('--existing')
        self.wait_until(restarted, lambda: bool(self._messages() or self.alerts()))
        code, _, errors = self.stop(restarted)
        # Assert 2: the marker is checked against the remote's repository, not the ticket source.
        self.assertEqual(self.alerts(), [], errors)
        recovered, = self._messages()
        self.assertTrue(recovered['recovered'])
        # Act 3: complete the plan; cleanup must treat the tracker reference as in scope.
        self.terminal_log.unlink()
        self.tracker.publish(self.source, [])
        self.finish_mapping(mapping)
        self.save(message, record)
        cleanup = self.start('--new-only')
        self.wait_until(cleanup, lambda: not self.branch_exists(mapping, remote=True), timeout=15)
        code, _, errors = self.stop(cleanup)
        # Assert 3
        self.assertEqual(code, 130, errors)
        self.assert_disposed(mapping)
        self.assertEqual(self.alerts(), [])
