"""Recorded cleanup replay through public watch, native call doubles and real temporary Git."""
import json
import subprocess
from pathlib import Path

from test_planning_watch import PlanningWatchFixture


class CleanupRecoveryTests(PlanningWatchFixture):
    def git(self, repository, *args):
        return subprocess.check_output(['git', '-C', str(repository), *args], text=True).strip()

    def recorded_issue(self, *, epic=False):
        labels = ('factory', 'epic') if epic else ('factory',)
        self.script({'team/app': [[[self.issue(labels=labels)]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        message = self._messages()[0]
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        task = self.planning_call('get_task', task_id=message['ownership_task_id'])
        return message, json.loads(task['description'])

    def cleanup(self, state='removed', repository=None):
        return {'state': state, 'pull_request_url': 'https://github.com/team/app/pull/3',
                'merge_commit': self.git(repository or self.workspace, 'rev-parse', 'HEAD')}

    def save_record(self, record):
        self.planning_call('update_task', task_id=1, description=json.dumps(record))

    def test_removed_mapping_restores_same_unfinished_plan_without_recreation_or_mutation(self):
        self.assert_removed_mapping_restores('https://github.com/team/app/pull/3')

    def assert_removed_mapping_restores(self, url):
        original, record = self.recorded_issue()
        mapping = record['worktrees'][0]
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        mapping['cleanup'] = self.cleanup()
        mapping['cleanup']['pull_request_url'] = url
        record['owner_notes'] = 'Preserve deployment and E2E follow-up.'
        self.save_record(record)
        before = self.planning_call('get_task', task_id=1)['description']
        registry = self.git(self.workspace, 'worktree', 'list', '--porcelain')
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.stop(restarted)
        restored = self._messages()[0]
        self.assertEqual(restored['plan_id'], original['plan_id'])
        self.assertEqual(restored['ownership_task_id'], original['ownership_task_id'])
        self.assertEqual(restored['worktrees'], record['worktrees'])
        self.assertTrue(restored['recovered'])
        self.assertFalse(Path(mapping['path']).exists())
        self.assertEqual(self.git(self.workspace, 'worktree', 'list', '--porcelain'), registry)
        self.assertEqual(self.planning_call('get_task', task_id=1)['description'], before)
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)
        self.assertEqual(self.planning_call('list_plans')['total_count'], 1)

    def assert_recovery_pauses(self, record, message):
        self.save_record(record)
        before = self.planning_call('get_task', task_id=1)['description']
        self.terminal_log.unlink(missing_ok=True)
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted, synchronize_poll=True)
        self.assertEqual(self._messages(), [], 'Conflicting work reached the Foreman')
        self.assertIn(message, stderr)
        self.assertIn('reconcile', stderr)
        self.assertNotIn('Traceback', stderr)
        self.assertEqual(self.planning_call('get_task', task_id=1)['description'], before)
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)

    def test_absent_pending_and_invalid_cleanup_never_recreate_the_tree(self):
        _, record = self.recorded_issue()
        mapping = record['worktrees'][0]
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        self.assert_recovery_pauses(record, 'worktree missing')
        mapping['cleanup'] = self.cleanup('pending')
        self.assert_recovery_pauses(record, 'cleanup is pending')
        mapping['cleanup'] = None
        self.assert_recovery_pauses(record, 'cleanup')
        self.assertFalse(Path(mapping['path']).exists())

    def test_pending_existing_tree_replays_intent_without_removal_or_record_mutation(self):
        _, record = self.recorded_issue()
        mapping = record['worktrees'][0]
        mapping['cleanup'] = self.cleanup('pending')
        self.save_record(record)
        before = self.planning_call('get_task', task_id=1)['description']
        registry = self.git(self.workspace, 'worktree', 'list', '--porcelain')
        restarted = self.start('--existing')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.stop(restarted)
        self.assertEqual(self._messages()[0]['worktrees'], record['worktrees'])
        self.assertTrue(Path(mapping['path']).is_dir())
        self.assertEqual(self.git(self.workspace, 'worktree', 'list', '--porcelain'), registry)
        self.assertEqual(self.planning_call('get_task', task_id=1)['description'], before)

    def test_removed_marker_routes_occupied_path_and_changed_origin_without_mutation(self):
        _, record = self.recorded_issue()
        mapping = record['worktrees'][0]
        mapping['cleanup'] = self.cleanup()
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        target = Path(mapping['path'])
        target.mkdir()
        work = target / 'work.txt'
        work.write_bytes(b'Preserve this work.\n')
        registry = self.git(self.workspace, 'worktree', 'list', '--porcelain')
        self.assert_recovery_pauses(record, 'cleanup conflicts')
        self.assertEqual(work.read_bytes(), b'Preserve this work.\n')
        self.assertEqual(self.git(self.workspace, 'worktree', 'list', '--porcelain'), registry)
        work.unlink()
        target.rmdir()
        self.git(self.workspace, 'remote', 'set-url', 'origin', 'git@github.com:other/repo.git')
        self.assert_recovery_pauses(record, 'origin changed')
        self.assertEqual(self.git(self.workspace, 'remote', 'get-url', 'origin'),
                         'git@github.com:other/repo.git')
        self.assertFalse(target.exists())

    def test_epic_replays_removed_and_live_repository_mappings_without_weakening_live_checks(self):
        self.configure(sources=('team/app', 'team/library'))
        _, record = self.recorded_issue(epic=True)
        self.script({'team/app': [[[]]], 'team/library': [[[]]]})
        second = self.workspace / 'repository-1'
        record['worktrees'] = []
        for repository, source, branch in ((self.workspace, 'team/app', 'factory/app'),
                                           (second, 'team/library', 'factory/library')):
            target = self.workspace / '.factory/worktrees' / source.replace('/', '-')
            target.parent.mkdir(exist_ok=True)
            self.git(repository, 'worktree', 'add', '-b', branch, str(target), 'HEAD')
            record['worktrees'].append({'repository': source, 'local_dir': str(repository),
                                        'branch': branch, 'path': str(target)})
        removed, active = record['worktrees']
        removed['cleanup'] = self.cleanup()
        self.git(self.workspace, 'worktree', 'remove', removed['path'])
        self.save_record(record)
        restarted = self.start('--existing')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.stop(restarted)
        self.assertEqual(self._messages()[0]['worktrees'], record['worktrees'])
        self.assertFalse(Path(removed['path']).exists())
        self.assertEqual(self.git(active['path'], 'branch', '--show-current'), active['branch'])
        self.git(second, 'worktree', 'remove', active['path'])
        self.assert_recovery_pauses(record, 'worktree missing')
        self.assertFalse(Path(active['path']).exists())
