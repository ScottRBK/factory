"""Cleanup validation and inspection at approved public boundaries."""
import copy
import subprocess
import tempfile
import unittest
from pathlib import Path

from forgetful_factory.adapters.filesystem.git_worktrees import GitWorktrees
from forgetful_factory.application.cleanup_marker import (
    CleanupMarkerError,
    validate_cleanup_marker,
)
from forgetful_factory.application.ports.worktrees import WorktreeProblem


class PersistedCleanupMarkerTests(unittest.TestCase):
    commit = 'a' * 40

    def marker(self, **changes):
        marker = {
            'state': 'removed',
            'pull_request_url': 'https://github.com/team/app/pull/3',
            'merge_commit': self.commit,
        }
        marker.update(changes)
        return marker

    def mapping(self, marker):
        return {'repository': 'team/app', 'cleanup': marker}

    def test_returns_semantic_state_for_absent_pending_and_removed_markers(self):
        # Arrange
        absent = {'repository': 'team/app'}
        pending = self.mapping(self.marker(state='pending'))
        removed = self.mapping(self.marker(merge_commit='b' * 64))
        mixed_case_repository = self.mapping(
            self.marker(pull_request_url='https://github.com/Team/App/pull/3'))
        original_mixed_case = copy.deepcopy(mixed_case_repository)

        # Act / Assert
        self.assertIsNone(validate_cleanup_marker(absent))
        self.assertEqual(validate_cleanup_marker(pending), 'pending')
        self.assertEqual(validate_cleanup_marker(removed), 'removed')
        self.assertEqual(validate_cleanup_marker(mixed_case_repository), 'removed')
        self.assertEqual(mixed_case_repository, original_mixed_case)

    def test_rejects_every_malformed_marker_and_noncanonical_url_without_mutation(self):
        malformed = [
            None,
            [],
            'removed',
            {},
            self.marker(state='complete'),
            self.marker(state=['removed']),
            self.marker(merge_commit=123),
            self.marker(merge_commit='abcd'),
            self.marker(merge_commit='x' * 40),
            self.marker(pull_request_url=3),
        ]
        for url in (
            'https://github.com/other/repo/pull/3',
            'https://github.com/Team/Other/pull/3',
            'HTTPS://github.com/Team/App/pull/3',
            'https://GitHub.com/Team/App/pull/3',
            'https://github.com/Team/App/Pull/3',
            'https://github.com/Team/App/pull/3#fragment',
            'https://github.com/team/app/pull/0',
            'https://github.com/team/app/pull/03',
            'https://github.com/team/app/pull/3?unexpected=yes',
            'https://github.com/team/app/pull/3/',
        ):
            malformed.append(self.marker(pull_request_url=url))

        for marker in malformed:
            with self.subTest(marker=marker):
                # Arrange
                mapping = self.mapping(marker)
                before = copy.deepcopy(mapping)

                # Act / Assert
                with self.assertRaises(CleanupMarkerError):
                    validate_cleanup_marker(mapping)
                self.assertEqual(mapping, before)


class RemovedWorktreeVerificationTests(unittest.TestCase):
    remote = 'git@github.com:team/app.git'

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repository = self.root / 'repository'
        subprocess.run(['git', 'init', '-q', str(self.repository)], check=True)
        self.git('remote', 'add', 'origin', self.remote)
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-qm', 'fixture')
        self.worktrees = GitWorktrees()

    def git(self, *arguments):
        return subprocess.check_output(
            ['git', '-C', str(self.repository), *arguments], text=True).strip()

    def verify_removed(self, branch, target):
        self.worktrees.verify_removed(
            str(self.repository), branch, str(target), remote=self.remote)

    def assert_conflict(self, branch, target, code='removed_worktree_conflict', paths=None):
        with self.assertRaises(WorktreeProblem) as raised:
            self.verify_removed(branch, target)
        self.assertEqual(raised.exception.code, code)
        expected_paths = (str(target),) if paths is None else paths
        self.assertEqual(raised.exception.paths, expected_paths)

    def test_rejects_each_occupied_path_form_without_mutation(self):
        for kind in ('file', 'directory', 'dangling-symlink', 'symlink-loop'):
            with self.subTest(kind=kind):
                # Arrange
                target = self.root / f'{kind}-target'
                if kind == 'file':
                    target.write_bytes(b'Preserve this file.\n')
                elif kind == 'directory':
                    target.mkdir()
                    (target / 'work.txt').write_bytes(b'Preserve this work.\n')
                elif kind == 'dangling-symlink':
                    target.symlink_to(self.root / 'absent-target')
                else:
                    target.symlink_to(target)
                registry = self.git('worktree', 'list', '--porcelain')

                # Act
                self.assert_conflict(f'factory/{kind}', target)

                # Assert
                self.assertEqual(self.git('worktree', 'list', '--porcelain'), registry)
                if kind == 'file':
                    self.assertEqual(target.read_bytes(), b'Preserve this file.\n')
                elif kind == 'directory':
                    self.assertEqual((target / 'work.txt').read_bytes(),
                                     b'Preserve this work.\n')
                elif kind == 'dangling-symlink':
                    self.assertEqual(target.readlink(), self.root / 'absent-target')
                else:
                    self.assertEqual(target.readlink(), target)

    def test_rejects_live_stale_and_relocated_registrations_without_mutation(self):
        # Arrange: start with a live native registration and user work.
        branch = 'factory/registered'
        target = self.root / 'registered'
        retained = self.root / 'retained'
        self.git('worktree', 'add', '-b', branch, str(target), 'HEAD')
        work = target / 'unfinished.txt'
        work.write_bytes(b'Preserve registered work.\n')
        live = self.git('worktree', 'list', '--porcelain')
        live_gitfile = (target / '.git').read_bytes()

        # Act / Assert: live registration.
        self.assert_conflict(branch, target)
        self.assertEqual(self.git('worktree', 'list', '--porcelain'), live)
        self.assertEqual(work.read_bytes(), b'Preserve registered work.\n')
        self.assertEqual((target / '.git').read_bytes(), live_gitfile)

        # Act / Assert: stale registration after an external path move.
        target.rename(retained)
        stale = self.git('worktree', 'list', '--porcelain')
        stale_gitfile = (retained / '.git').read_bytes()
        self.assertIn('prunable', stale)
        self.assert_conflict(branch, target)
        self.assertEqual(self.git('worktree', 'list', '--porcelain'), stale)
        self.assertEqual((retained / '.git').read_bytes(), stale_gitfile)
        self.assertEqual((retained / 'unfinished.txt').read_bytes(),
                         b'Preserve registered work.\n')

        # Act / Assert: native relocation still owns the branch at another path.
        retained.rename(target)
        self.git('worktree', 'move', str(target), str(retained))
        relocated = self.git('worktree', 'list', '--porcelain')
        relocated_gitfile = (retained / '.git').read_bytes()
        self.assert_conflict(branch, target)
        self.assertEqual(self.git('worktree', 'list', '--porcelain'), relocated)
        self.assertFalse(target.exists())
        self.assertEqual((retained / '.git').read_bytes(), relocated_gitfile)
        self.assertEqual((retained / 'unfinished.txt').read_bytes(),
                         b'Preserve registered work.\n')

    def test_rejects_changed_origin_without_mutating_git_or_path(self):
        # Arrange
        target = self.root / 'removed'
        registry = self.git('worktree', 'list', '--porcelain')
        changed = 'git@github.com:other/repo.git'
        self.git('remote', 'set-url', 'origin', changed)

        # Act
        self.assert_conflict(
            'factory/removed', target, code='repository_origin_changed', paths=())

        # Assert
        self.assertEqual(self.git('remote', 'get-url', 'origin'), changed)
        self.assertEqual(self.git('worktree', 'list', '--porcelain'), registry)
        self.assertFalse(target.exists())
