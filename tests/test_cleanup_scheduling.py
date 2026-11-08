"""Observe the cleanup work bound and fair retries at real Git/provider boundaries."""
import json
import shutil
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture


class CleanupSchedulingTests(CompletedCleanupFixture):
    def test_one_set_per_cycle_and_failed_first_set_cannot_starve_its_sibling(self):
        # Arrange: one plan has two sets; the first remote always rejects deletion.
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
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                           'from pathlib import Path\n'
                           'if "--symref" in sys.argv:\n'
                           f'    state = json.loads(Path({str(self.state_path)!r}).read_text())\n'
                           f'    with open({str(log)!r}, "a") as stream:\n'
                           '        stream.write(json.dumps([state.get("counts", {}).get('
                           '"team/app", 0), sys.argv[1:]]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 4 and
                        not self.branch_exists(healthy, remote=True))
        self.stop(process)
        attempts = [json.loads(line) for line in log.read_text().splitlines()]
        # Assert: native work from two sets must not occur between the same provider polls.
        polls = [poll for poll, _ in attempts]
        self.assertEqual(len(polls), len(set(polls)), attempts)
        self.assertGreaterEqual(len(attempts), 3, attempts)
        roots = [args[args.index('-C') + 1] for _, args in attempts]
        self.assertEqual(roots[:3], [denied['local_dir'], healthy['local_dir'],
                                     denied['local_dir']])
        self.assert_disposed(healthy)
        self.assertTrue(self.branch_exists(denied, remote=True))

    def test_failed_plan_cannot_starve_a_later_completed_plan(self):
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
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
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
        self.wait_until(process, lambda: self.polls() >= 4)
        self.stop(process)
        attempts = [json.loads(line) for line in log.read_text().splitlines()]
        # Assert: a failed plan spends its turn, not the entire cycle or later plans' turns.
        self.assertEqual([ref for _, ref in attempts[:3]],
                         [':refs/heads/' + m['branch'] for m in (denied, healthy, denied)])
        polls = [poll for poll, _ in attempts]
        self.assertEqual(len(polls), len(set(polls)), attempts)
        self.assert_disposed(healthy)
        self.assertTrue(self.branch_exists(denied, remote=True))
