"""Completed-plan disposal through public watch, native CLI fixtures and real Git remotes."""
import json
import subprocess
from pathlib import Path

from test_planning_watch import PlanningWatchFixture

SSH = '''#!/usr/bin/env python3
import json
import os
import shlex
import sys
command, repository = shlex.split(sys.argv[-1])
remotes = json.loads(os.environ['CLEANUP_REMOTES'])
if command not in ('git-upload-pack', 'git-receive-pack') or repository not in remotes:
    sys.exit('Unknown disposable transport target')
os.execvp('git', ['git', command.removeprefix('git-'), remotes[repository]])
'''


class CompletedCleanupFixture(PlanningWatchFixture):
    def setUp(self):
        super().setUp()
        transport = self.bin / 'disposable-ssh'
        transport.write_text(SSH)
        transport.chmod(0o755)
        self.env.update(GIT_SSH_COMMAND=str(transport), GIT_SSH_VARIANT='ssh',
                        CLEANUP_REMOTES='{}')
        self.add_remote(self.workspace, 'team/app')

    def git(self, repository, *arguments):
        return subprocess.check_output(['git', '-C', str(repository), *arguments],
                                       env=self.env, text=True, stderr=subprocess.PIPE).strip()

    def add_remote(self, repository, source):
        remote = self.workspace / ('bare-' + source.replace('/', '-'))
        subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
        branch = self.git(repository, 'branch', '--show-current')
        self.git(remote, 'symbolic-ref', 'HEAD', f'refs/heads/{branch}')
        remotes = json.loads(self.env['CLEANUP_REMOTES'])
        remotes[source + '.git'] = str(remote)
        self.env['CLEANUP_REMOTES'] = json.dumps(remotes)
        self.git(repository, 'push', 'origin', branch)
        return remote

    def recorded(self, *, epic=False):
        # Arrange ordinary work through the public watcher before completing it externally.
        labels = ('factory', 'epic') if epic else ('factory',)
        self.script({'team/app': [[[self.issue(labels=labels)]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: bool(self._messages() or self.alerts()))
        self.stop(first)
        self.assertEqual(len(self._messages()), 1, self.alerts())
        message = self._messages()[0]
        task = self.planning_call('get_task', task_id=message['ownership_task_id'])
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        return message, json.loads(task['description'])

    def save(self, message, record, *, status='completed'):
        self.planning_call('update_task', task_id=message['ownership_task_id'],
                           description=json.dumps(record))
        self.planning_call('update_plan', plan_id=message['plan_id'], status=status)

    def finish_mapping(self, mapping):
        mapping['target_branch'] = self.git(mapping['local_dir'], 'branch', '--show-current')
        self.git(mapping['local_dir'], 'push', 'origin', mapping['branch'])

    def branch_exists(self, mapping, *, remote=False):
        if remote:
            return bool(self.git(mapping['local_dir'], 'ls-remote', '--heads', 'origin',
                                 f'refs/heads/{mapping["branch"]}'))
        return f'refs/heads/{mapping["branch"]}' in self.git(
            mapping['local_dir'], 'for-each-ref', '--format=%(refname)', 'refs/heads').splitlines()

    def assert_disposed(self, mapping):
        self.assertFalse(Path(mapping['path']).exists())
        self.assertNotIn(mapping['path'], self.git(mapping['local_dir'], 'worktree', 'list',
                                                  '--porcelain'))
        self.assertFalse(self.branch_exists(mapping))
        self.assertFalse(self.branch_exists(mapping, remote=True))


class CompletedCleanupTests(CompletedCleanupFixture):
    def test_completed_during_downtime_is_disposed_without_intake_or_policy_reads(self):
        # Arrange: no DoD file, closed issue, new-only intake, unmerged local/remote commits.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        target = Path(mapping['path'])
        self.git(target, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-qm', 'Extra unmerged commit is disposable')
        (target / 'dirty.txt').write_text('Disposable untracked work')
        (target / '.gitignore').write_text('ignored.txt\n')
        (target / 'ignored.txt').write_text('Disposable ignored work')
        self.finish_mapping(mapping)
        self.save(message, record)
        (self.workspace / '.factory/definition_of_done.md').unlink()
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        code, _, errors = self.stop(process)
        # Assert: Git facts, not a cleanup marker or instruction phrase, establish disposal.
        self.assertEqual(code, 130, errors)
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.alerts(), [])
        self.assertEqual(self.planning_call('get_plan', plan_id=message['plan_id'])['status'],
                         'completed')
        self.assertEqual(json.loads(self.planning_call(
            'get_task', task_id=message['ownership_task_id'])['description']), record)
        self.assertEqual(self.planning_call('list_plans')['total_count'], 1)
        self.assertTrue((self.workspace / '.git').is_dir())

    def test_new_intake_records_exact_merge_target_for_later_disposal(self):
        # Arrange / Act
        _, record = self.recorded()
        # Assert: saved ownership, not watcher prose, supplies the protected target.
        mapping, = record['worktrees']
        self.assertEqual(mapping.get('target_branch'),
                         self.git(self.workspace, 'branch', '--show-current'))

    def test_registered_worktree_outside_factory_directory_is_never_disposed(self):
        # Arrange: a valid linked worktree is not enough to authorize an arbitrary path.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        original = mapping['path']
        mapping['path'] = str(self.workspace / 'valuable-user-worktree')
        self.git(self.workspace, 'worktree', 'move', original, mapping['path'])
        self.finish_mapping(mapping)
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).is_dir(), 'Removed non-Factory user worktree')
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))

    def test_completion_with_contradictory_issue_snapshot_cannot_authorize_disposal(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        context = json.loads(plan['context'])
        context['issue']['number'] = 44
        self.planning_call('update_plan', plan_id=message['plan_id'], context=json.dumps(context))
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['code'] == 'plan_recovery_invalid' for a in self.alerts()))

    def test_only_completed_status_authorizes_disposal_while_watching(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        for status in ('draft', 'active', 'archived'):
            with self.subTest(status=status):
                self.save(message, record, status=status)
                self.script({'team/app': [[[]]]})
                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: self.polls() >= 2)
                self.stop(process)
                # Assert
                self.assertTrue(Path(mapping['path']).exists())
                self.assertTrue(self.branch_exists(mapping))
                self.assertTrue(self.branch_exists(mapping, remote=True))
                self.terminal_log.unlink()
        self.save(message, record, status='active')
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.planning_call('update_plan', plan_id=message['plan_id'], status='completed')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.stop(process)
        self.assert_disposed(mapping)

    def test_missing_target_and_missing_or_competing_ownership_block_only_that_plan(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        original_task = self.planning_call('get_task', task_id=message['ownership_task_id'])
        for mode in ('missing-target', 'missing-owner', 'invalid-owner', 'competing-owner'):
            with self.subTest(mode=mode):
                broken = json.loads(json.dumps(record))
                title = original_task['title']
                duplicate = None
                if mode == 'missing-target':
                    broken['worktrees'][0].pop('target_branch')
                elif mode == 'missing-owner':
                    broken['kind'] = 'retired-ownership'
                    title = 'Retired ownership'
                elif mode == 'invalid-owner':
                    broken['workspace'] = '/tmp/another-factory'
                else:
                    duplicate = self.planning_call('create_task', plan_id=message['plan_id'],
                                                   title='Feature ownership',
                                                   description=json.dumps(record))
                self.planning_call('update_task', task_id=message['ownership_task_id'],
                                   title=title, description=json.dumps(broken))
                self.script({'team/app': [[[]]]})
                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: self.polls() >= 2)
                self.stop(process)
                # Assert
                self.assertTrue(Path(mapping['path']).exists())
                self.assertTrue(self.branch_exists(mapping, remote=True))
                self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))
                if duplicate:
                    self.planning_call('update_task', task_id=duplicate['id'], title='Retired',
                                       description='{}')
                self.terminal_log.unlink()

    def test_project_workspace_and_source_mismatches_never_authorize_cleanup(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        changes = ({'project_id': 99}, {'external_ref': 'github:foreign/repository#1'},
                   {'context': json.dumps({'workspace': '/tmp/foreign-factory'})},
                   {'context': '{malformed'}, {'external_ref': 'github:team/app#01'})
        for change in changes:
            with self.subTest(change=change):
                self.planning_call('update_plan', plan_id=message['plan_id'], **change)
                self.script({'team/app': [[[]]]})
                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: self.polls() >= 2)
                self.stop(process)
                # Assert
                self.assertTrue(Path(mapping['path']).exists())
                self.assertTrue(self.branch_exists(mapping, remote=True))
                self.planning_call('update_plan', plan_id=message['plan_id'], **{
                    key: plan[key] for key in change})
                self.terminal_log.unlink()

    def test_native_git_identity_lock_default_and_merge_target_protections(self):
        # Arrange: each attempt must preserve path, branch, ignored content and remote ref.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        target = Path(mapping['path'])
        work = target / 'valuable.txt'
        work.write_text('Preserve while identity is unsafe')
        self.save(message, record)
        gitfile = (target / '.git').read_text()
        original_origin = self.git(self.workspace, 'remote', 'get-url', 'origin')
        for mode in ('locked', 'branch', 'gitdir', 'foreign-common', 'root', 'origin',
                     'target', 'default', 'main-checkout', 'ref', 'symlink', 'symlink-parent'):
            with self.subTest(mode=mode):
                changed = json.loads(json.dumps(record))
                if mode == 'locked':
                    self.git(self.workspace, 'worktree', 'lock', mapping['path'])
                elif mode == 'branch':
                    self.git(target, 'switch', '-c', 'unrelated-branch')
                elif mode == 'gitdir':
                    (target / '.git').write_text(f'gitdir: {self.workspace / ".git"}\n')
                elif mode == 'foreign-common':
                    foreign = self.workspace / 'foreign-git-root'
                    subprocess.run(['git', 'init', '-q', str(foreign)], check=True)
                    (target / '.git').write_text(f'gitdir: {foreign / ".git"}\n')
                elif mode == 'symlink-parent':
                    saved_parent = target.parent.with_name('saved-worktree-parent')
                    target.parent.rename(saved_parent)
                    target.parent.symlink_to(saved_parent, target_is_directory=True)
                elif mode == 'root':
                    self.git(self.workspace, 'config', 'extensions.worktreeConfig', 'true')
                    self.git(target, 'config', '--worktree', 'core.worktree', str(self.workspace))
                elif mode == 'origin':
                    self.git(self.workspace, 'remote', 'set-url', 'origin',
                             'git@github.com:unrelated/repo.git')
                elif mode == 'target':
                    changed['worktrees'][0]['target_branch'] = mapping['branch']
                elif mode == 'default':
                    remote = json.loads(self.env['CLEANUP_REMOTES'])['team/app.git']
                    self.git(remote, 'symbolic-ref', 'HEAD', f'refs/heads/{mapping["branch"]}')
                elif mode == 'main-checkout':
                    changed['worktrees'][0]['path'] = str(self.workspace)
                elif mode == 'ref':
                    changed['worktrees'][0]['branch'] = 'feature:refs/heads/master'
                else:
                    alias = target.parent / 'symlink-alias'
                    alias.symlink_to(target, target_is_directory=True)
                    changed['worktrees'][0]['path'] = str(alias)
                self.save(message, changed)
                self.script({'team/app': [[[]]]})
                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: self.polls() >= 2)
                self.stop(process)
                # Assert
                self.assertTrue(target.is_dir(), mode)
                self.assertEqual(work.read_text(), 'Preserve while identity is unsafe')
                self.assertTrue(self.branch_exists(mapping))
                self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()), mode)
                if mode == 'locked':
                    self.git(self.workspace, 'worktree', 'unlock', mapping['path'])
                elif mode == 'branch':
                    self.git(target, 'switch', mapping['branch'])
                elif mode in ('gitdir', 'foreign-common'):
                    (target / '.git').write_text(gitfile)
                elif mode == 'symlink-parent':
                    target.parent.unlink()
                    saved_parent.rename(target.parent)
                elif mode == 'root':
                    self.git(target, 'config', '--worktree', '--unset', 'core.worktree')
                elif mode == 'origin':
                    self.git(self.workspace, 'remote', 'set-url', 'origin', original_origin)
                elif mode == 'default':
                    self.git(remote, 'symbolic-ref', 'HEAD',
                             f'refs/heads/{mapping["target_branch"]}')
                elif mode == 'symlink':
                    alias.unlink()
                self.assertTrue(self.branch_exists(mapping, remote=True))
                self.terminal_log.unlink()

    def test_overlapping_plan_mappings_protect_both_plans_without_blocking_safe_cleanup(self):
        # Arrange: another plan claims a nested worktree inside the first tree.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        other = self.planning_call('create_plan', project_id=12, status='active',
                                   external_ref='github:team/app#2',
                                   context=self.planning_call('get_plan', plan_id=1)['context'])
        nested = dict(mapping, branch='factory/second', path=str(Path(mapping['path']) / 'nested'))
        self.git(self.workspace, 'worktree', 'add', '-b', nested['branch'], nested['path'], 'HEAD')
        other_record = dict(record, external_ref='github:team/app#2', worktrees=[nested])
        self.planning_call('create_task', plan_id=other['id'], title='Feature ownership',
                           description=json.dumps(other_record))
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists(), 'Deleted parent of another plan worktree')
        self.assertTrue(Path(nested['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['code'] == 'cleanup_ownership_conflict' for a in self.alerts()))

    def test_status_reopened_during_inventory_read_is_rechecked_before_disposal(self):
        # Arrange: the native service changes status between the plan and ownership replies.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        executable = self.bin / 'forgetful'
        source = executable.read_text()
        needle = "        if control.get('incomplete') == tool:"
        self.assertEqual(source.count(needle), 1)
        source = source.replace(needle, """        if tool == 'get_task':
            for plan in state['plans']:
                if plan['id'] == result['plan_id']:
                    plan['status'] = 'active'
            save_planning_state()
""" + needle)
        executable.write_text(source)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))

    def test_separate_push_destination_cannot_delete_an_unrelated_remote_branch(self):
        # Arrange: origin fetch identity matches, but Git would push to another repository.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        remote = self.workspace / 'unrelated-bare'
        subprocess.run(['git', 'init', '--bare', '-q', str(remote)], check=True)
        self.git(self.workspace, 'push', str(remote), mapping['branch'])
        remotes = json.loads(self.env['CLEANUP_REMOTES'])
        remotes['team/unrelated.git'] = str(remote)
        self.env['CLEANUP_REMOTES'] = json.dumps(remotes)
        self.git(self.workspace, 'config', 'remote.origin.pushurl',
                 'git@github.com:team/unrelated.git')
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertIn(f'refs/heads/{mapping["branch"]}',
                      self.git(remote, 'for-each-ref', '--format=%(refname)'))
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))

    def test_another_plans_recorded_merge_target_is_not_a_disposable_feature_ref(self):
        # Arrange: the completed feature branch is now a recorded target of another plan.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        other = self.planning_call('create_plan', project_id=12, status='active',
                                   external_ref='github:team/app#2',
                                   context=self.planning_call('get_plan', plan_id=1)['context'])
        target = self.workspace / '.factory/worktrees/other-plan'
        self.git(self.workspace, 'worktree', 'add', '-b', 'factory/other-plan', str(target), 'HEAD')
        other_mapping = dict(mapping, branch='factory/other-plan', path=str(target),
                             target_branch=mapping['branch'])
        self.planning_call('create_task', plan_id=other['id'], title='Feature ownership',
                           description=json.dumps(dict(record, external_ref='github:team/app#2',
                                                       worktrees=[other_mapping])))
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(target.exists())

    def test_malformed_path_reports_a_problem_without_stopping_watcher_or_other_intake(self):
        # Arrange: service text can contain an embedded NUL; it must never become a Git target.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        original_path = mapping['path']
        self.finish_mapping(mapping)
        mapping['path'] += '\x00suffix'
        self.save(message, record)
        self.script({'team/app': [[[self.issue(3)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()) and bool(self._messages()))
        self.wait_until(process, lambda: self.polls() >= 2)
        code, _, errors = self.stop(process)
        # Assert
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)
        self.assertTrue(Path(original_path).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertEqual([m['number'] for m in self._messages()], [3])

    def test_unreadable_new_merge_target_is_retryable_intake_not_an_uncertain_write(self):
        # Arrange: a detached main checkout has no unambiguous starting merge target.
        branch = self.git(self.workspace, 'branch', '--show-current')
        self.git(self.workspace, 'switch', '--detach', 'HEAD')
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        # Assert: no write occurred; normal intake can resume after the repository is repaired.
        self.assertEqual(self.alerts()[0]['scope'], 'issue')
        self.assertEqual(self.alerts()[0]['retry'], 'next_poll')
        self.assertEqual(self.planning_call('list_plans')['total_count'], 0)
        self.git(self.workspace, 'switch', branch)
        self.wait_until(process, lambda: bool(self._messages()))
        self.stop(process)
        self.assertEqual(self.planning_call('list_plans')['total_count'], 1)

    def test_canonical_duplicate_mapping_cannot_authorize_a_second_unrelated_branch(self):
        # Arrange: two text paths name the same tree but claim different branches.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        unrelated = dict(mapping, branch='factory/valuable-user-branch')
        self.git(self.workspace, 'branch', unrelated['branch'], 'HEAD')
        self.git(self.workspace, 'push', 'origin', unrelated['branch'])
        record['worktrees'].append(dict(unrelated, path=mapping['path'] + '/'))
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert: contradiction is rejected before any mapping's destructive stage.
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(self.branch_exists(unrelated))
        self.assertTrue(self.branch_exists(unrelated, remote=True))

    def test_secondary_repository_scaffold_is_ignored_without_replacing_local_ignore_rules(self):
        # Arrange: the shared workspace's .factory ignore rules cannot cover the second root.
        self.configure(sources=('team/app', 'team/library'))
        second = self.workspace / 'repository-1'
        self.add_remote(second, 'team/library')
        self.script({'team/app': [[[]]], 'team/library': [[[self.issue(1)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self._messages()))
        self.stop(process)
        # Assert: the linked tree cannot accidentally become a gitlink in the main checkout.
        mapping = self._messages()[0]['worktrees'][0]
        self.assertEqual(mapping['local_dir'], str(second))
        self.assertTrue(Path(mapping['path']).is_relative_to(second / '.factory/worktrees'))
        ignored = subprocess.run(['git', '-C', str(second), 'check-ignore', mapping['path']],
                                 env=self.env, capture_output=True, text=True)
        self.assertEqual(ignored.returncode, 0, ignored.stderr)
        self.assertNotIn('.factory', self.git(second, 'status', '--porcelain'))
        ignore = second / '.factory/worktrees/.gitignore'
        ignore.write_text('*\n# Preserve my edited local ignore rules.\n')
        before = ignore.read_bytes()
        self.script({'team/app': [[[]]], 'team/library': [[[self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) >= 3)
        self.stop(process)
        self.assertEqual(ignore.read_bytes(), before)
