"""Durable terminal cleanup authority through public watch and real disposable Git."""
import json
import shutil
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture


def prepare_completed_set(fixture):
    message, record = fixture.recorded()
    mapping = record['worktrees'][0]
    fixture.finish_mapping(mapping)
    fixture.save(message, record)
    return message, record, mapping


class CleanupReceiptFixture(CompletedCleanupFixture):
    def human_refs(self, mapping):
        root = mapping['local_dir']
        tree = self.git(root, 'rev-parse', 'HEAD^{tree}')
        commit = self.git(root, '-c', 'user.name=Human', '-c', 'user.email=h@example.invalid',
                          'commit-tree', tree, '-p', self.git(root, 'rev-parse', 'HEAD'),
                          '-m', 'New human work after durable confirmation')
        self.git(root, 'branch', mapping['branch'], commit)
        self.git(root, 'push', 'origin', f'{commit}:refs/heads/{mapping["branch"]}')
        return commit


class CleanupReceiptTests(CleanupReceiptFixture):
    def test_confirmed_set_survives_restart_and_does_not_own_new_human_refs(self):
        # Arrange / Act: observe final cleanup confirmation before reusing these names.
        _, _, mapping = prepare_completed_set(self)
        output = self.workspace / 'watch-output'
        with output.open('w') as stream:
            first = self.start('--new-only', stdout=stream)
            self.wait_until(first, lambda: 'Cleanup confirmed' in output.read_text())
            self.stop(first)
        self.assert_disposed(mapping)
        commit = self.human_refs(mapping)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        native = shutil.which('git')
        log = self.workspace / 'restart-git-commands.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                           f'with open({str(log)!r}, "a") as stream:\n'
                           '    stream.write(json.dumps(sys.argv[1:]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: self.polls() >= 3)
        _, text, _ = self.stop(restarted)
        # Assert: only ordinary startup root/origin reads occur, never another cleanup index.
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertFalse(any('--git-common-dir' in args or 'worktree' in args or
                             'ls-remote' in args or 'push' in args for args in calls), calls)
        wrapper.unlink()
        # A native completed plan is not permanent disposal authority.
        self.assertEqual(self.git(mapping['local_dir'], 'rev-parse', mapping['branch']), commit)
        self.assertIn(commit, self.git(mapping['local_dir'], 'ls-remote', '--heads', 'origin',
                                       mapping['branch']))
        self.assertNotIn('Cleanup confirmed', text)

    def test_unreadable_or_malformed_receipt_withholds_disposal_but_not_safe_intake(self):
        # Arrange: receipt contents are local authority, never a reason to assume no receipts.
        _, _, mapping = prepare_completed_set(self)
        receipt = self.workspace / '.factory/cleanup-finished.json'
        receipt.write_text('{broken authority')
        receipt.chmod(0o600)
        self.script({'team/app': [[[self.issue(3)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self._messages()))
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertEqual(self._messages()[0]['number'], 3)
        self.assertTrue(any(a['code'] == 'cleanup_receipt_failed' for a in self.alerts()))
        self.assertEqual(receipt.read_text(), '{broken authority')

    def test_symlink_receipt_blocks_disposal_until_operator_repairs_storage(self):
        # Arrange
        _, _, mapping = prepare_completed_set(self)
        target = self.workspace / 'human-receipt.json'
        target.write_text('{"version": 1, "finished": []}')
        receipt = self.workspace / '.factory/cleanup-finished.json'
        receipt.symlink_to(target)
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(any(a['code'] == 'cleanup_receipt_failed' for a in self.alerts()))
        # Act: exact disposable storage repair, not resource recreation.
        receipt.unlink()
        self.wait_until(process, lambda: receipt.exists())
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(target.read_text(), '{"version": 1, "finished": []}')

    def test_failed_receipt_write_reserves_names_and_rechecks_facts_before_confirmation(self):
        # Arrange: storage changes only after cleanup begins, at the external Git boundary.
        _, _, mapping = prepare_completed_set(self)
        native = shutil.which('git')
        receipt = self.workspace / '.factory/cleanup-finished.json'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\nfrom pathlib import Path\n'
                           'if "push" in sys.argv and any(a.startswith(":refs/heads/") '
                           'for a in sys.argv):\n'
                           f'    Path({str(receipt)!r}).mkdir(exist_ok=True)\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        output = self.workspace / 'watch-output'
        with output.open('w') as stream:
            process = self.start('--new-only', stdout=stream)
            self.wait_until(process, lambda: any(a['code'] == 'cleanup_receipt_failed'
                                                for a in self.alerts()))
            # Native removal alone must not report completion.
            self.assertNotIn('Cleanup confirmed', output.read_text())
            self.assert_disposed(mapping)
            # Names are still reserved: unfinished cleanup owns these resources.
            commit = self.human_refs(mapping)
            self.assertTrue(commit)
            wrapper.unlink()
            receipt.rmdir()
            # Act: fresh facts must find and dispose these still-reserved native refs.
            self.wait_until(process, lambda: 'Cleanup confirmed' in output.read_text())
            self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(output.read_text().count('Cleanup confirmed'), 1)
        self.assertEqual(json.loads(receipt.read_text())['version'], 1)

    def test_sibling_failure_cannot_reopen_a_durably_confirmed_set_after_restart(self):
        # Arrange: one completed epic, two independent repository sets, one rejecting remote.
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
        output = self.workspace / 'watch-output'
        with output.open('w') as stream:
            process = self.start('--new-only', stdout=stream)
            self.wait_until(process, lambda: 'Cleanup confirmed' in output.read_text())
            self.stop(process)
        self.assert_disposed(healthy)
        self.assertTrue(self.branch_exists(denied, remote=True))
        commit = self.human_refs(healthy)
        hook.unlink()
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]], 'team/library': [[[]]]})
        # Act
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: self.polls() >= 3)
        self.stop(restarted)
        # Assert: the pending sibling is retried, not the terminal set.
        self.assert_disposed(denied)
        self.assertEqual(self.git(second, 'rev-parse', healthy['branch']), commit)
        self.assertIn(commit, self.git(second, 'ls-remote', '--heads', 'origin', healthy['branch']))

    def test_changed_target_does_not_reopen_a_confirmed_resource_set(self):
        # Arrange
        message, record, mapping = prepare_completed_set(self)
        output = self.workspace / 'watch-output'
        with output.open('w') as stream:
            first = self.start('--new-only', stdout=stream)
            self.wait_until(first, lambda: 'Cleanup confirmed' in output.read_text())
            self.stop(first)
        commit = self.human_refs(mapping)
        mapping['target_branch'] = 'reviewed-different-target'
        self.save(message, record)
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: self.polls() >= 3)
        self.stop(restarted)
        # Assert: a protective constraint is not a new resource-set identity.
        self.assertEqual(self.git(mapping['local_dir'], 'rev-parse', mapping['branch']), commit)
        self.assertIn(commit, self.git(mapping['local_dir'], 'ls-remote', '--heads', 'origin',
                                       mapping['branch']))
