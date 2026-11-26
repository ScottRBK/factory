"""Observe the cleanup work bound and fair retries at real Git/provider boundaries."""
import json
import shutil
import sys
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture

# Portability: the Nix build sandbox has no /usr/bin/env, so stubs must name the
# interpreter that is actually running the tests.
SHEBANG = f'#!{sys.executable}\n'


def completed_attempts(log):
    if not log.exists():
        return []
    return [json.loads(line) for line in log.read_text().splitlines(keepends=True)
            if line.endswith('\n')]


class CleanupSchedulingTests(CompletedCleanupFixture):
    def test_failed_set_allows_healthy_sibling_in_the_same_batch(self):
        # Arrange: two sets fit in one batch; the first remote always rejects deletion.
        self.configure(sources=('team/app', 'team/library'))
        second = self.workspace / 'repository-1'
        self.add_remote(second, 'team/library')
        message, record = self.recorded(epic=True)
        record['worktrees'] = []
        for root, source in ((self.workspace, 'team/app'), (second, 'team/library')):
            target = root / '.factory/worktrees/epic-feature'
            target.parent.mkdir(parents=True, exist_ok=True)
            self.git(root, 'worktree', 'add', '-b', 'factory/epic-feature', str(target), 'HEAD')
            mapping = {'repository': source, 'local_dir': str(root),
                       'branch': 'factory/epic-feature', 'path': str(target)}
            self.finish_mapping(mapping)
            record['worktrees'].append(mapping)
        self.save(message, record)
        denied, healthy = record['worktrees']
        remote = Path(json.loads(self.env['CLEANUP_REMOTES'])['team/app.git'])
        hook = remote / 'hooks/update'
        hook.write_text('#!/bin/sh\ncase "$3" in 000000*) exit 1;; esac\n')
        hook.chmod(0o755)
        native = shutil.which('git')
        log = self.workspace / 'attempts.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text(SHEBANG + 'import json, os, sys\n'
                           'from pathlib import Path\n'
                           'if "push" in sys.argv and any(a.startswith(":refs/heads/") '
                           'for a in sys.argv):\n'
                           f'    state = json.loads(Path({str(self.state_path)!r}).read_text())\n'
                           f'    with open({str(log)!r}, "a") as stream:\n'
                           '        stream.write(json.dumps([state.get("counts", {}).get('
                           '"team/app", 0), sys.argv[1:]]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(completed_attempts(log)) >= 3 and
                        not self.branch_exists(healthy, remote=True), timeout=15)
        self.stop(process)
        attempts = completed_attempts(log)
        # Assert: both sets share a batch; the failed set retries in the next cycle.
        polls = [poll for poll, _ in attempts]
        self.assertEqual(polls[:3], [0, 0, 1], attempts)
        self.assertGreaterEqual(len(attempts), 3, attempts)
        roots = [args[args.index('-C') + 1] for _, args in attempts]
        self.assertEqual(roots[:3], [denied['local_dir'], healthy['local_dir'],
                                     denied['local_dir']])
        self.assertEqual(len(attempts), len({(p, r) for (p, _), r in zip(attempts, roots)}))
        self.assertTrue(all(polls.count(poll) <= 3 for poll in set(polls)), attempts)
        self.assert_disposed(healthy)
        self.assertTrue(self.branch_exists(denied, remote=True))

    def test_failed_plan_allows_later_plan_in_the_same_batch(self):
        # Arrange: two completed ordinary plans share a repository, not their feature refs.
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        setup = self.start('--existing')
        self.wait_until(setup, lambda: len(self._messages()) == 2)
        self.stop(setup)
        mappings = []
        for message in self._messages():
            task = self.planning_call('get_task', task_id=message['ownership_task_id'])
            record = json.loads(task['description'])
            mapping = record['worktrees'][0]
            self.finish_mapping(mapping)
            self.save(message, record)
            mappings.append(mapping)
        denied, healthy = mappings
        remote = Path(json.loads(self.env['CLEANUP_REMOTES'])['team/app.git'])
        hook = remote / 'hooks/update'
        hook.write_text(f'#!/bin/sh\n[ "$1" != "refs/heads/{denied["branch"]}" ]\n')
        hook.chmod(0o755)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        native = shutil.which('git')
        log = self.workspace / 'push-attempts.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text(SHEBANG + 'import json, os, sys\n'
                           'from pathlib import Path\n'
                           'if "push" in sys.argv and any(a.startswith(":refs/heads/") '
                           'for a in sys.argv):\n'
                           f'    state = json.loads(Path({str(self.state_path)!r}).read_text())\n'
                           f'    with open({str(log)!r}, "a") as stream:\n'
                           '        stream.write(json.dumps([state.get("counts", {}).get('
                           '"team/app", 0), sys.argv[-1]]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(completed_attempts(log)) >= 3 and
                        not self.branch_exists(healthy, remote=True), timeout=15)
        self.stop(process)
        attempts = completed_attempts(log)
        # Assert: both plans share a batch; the failed plan retries in the next cycle.
        self.assertEqual([ref for _, ref in attempts[:3]],
                         [':refs/heads/' + m['branch'] for m in (denied, healthy, denied)])
        polls = [poll for poll, _ in attempts]
        self.assertEqual(polls[:3], [0, 0, 1], attempts)
        self.assertEqual(len(attempts), len({tuple(item) for item in attempts}), attempts)
        self.assertTrue(all(polls.count(poll) <= 3 for poll in set(polls)), attempts)
        self.assert_disposed(healthy)
        self.assertTrue(self.branch_exists(denied, remote=True))
