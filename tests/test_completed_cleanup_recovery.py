"""Partial disposal and historical-marker recovery at the public watch/native Git boundary."""
import json
import shutil
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture

from forgetful_factory.deadlines import DeadlinePolicy


class CompletedCleanupRecoveryTests(CompletedCleanupFixture):
    def test_multi_repository_remote_denial_continues_other_mapping_and_recovers_on_restart(self):
        # Arrange: one plan owns two repository worktrees; only the first remote denies deletion.
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
        first, healthy = record['worktrees']
        remote = Path(json.loads(self.env['CLEANUP_REMOTES'])['team/app.git'])
        hook = remote / 'hooks/update'
        hook.write_text('#!/bin/sh\ncase "$3" in 000000*) exit 1;; esac\n')
        hook.chmod(0o755)
        self.script({'team/app': ['Fixture GitHub unavailable'], 'team/library': [[[]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()) and
                        not self.branch_exists(healthy, remote=True))
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert: the first resource is partially removed, never rolled back or reopened.
        self.assertFalse(Path(first['path']).exists())
        self.assertFalse(self.branch_exists(first))
        self.assertTrue(self.branch_exists(first, remote=True))
        self.assert_disposed(healthy)
        self.assertEqual(self._messages(), [])
        self.assertTrue(any(a['code'] == 'cleanup_operation_uncertain' for a in self.alerts()))
        self.assertEqual(self.planning_call('get_plan', plan_id=message['plan_id'])['status'],
                         'completed')
        self.assertEqual(json.loads(self.planning_call('get_task', task_id=1)['description']),
                         record)
        # Act: repair only the disposable remote, then restart with only the healthy set confirmed.
        hook.unlink()
        self.terminal_log.unlink()
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: not self.branch_exists(first, remote=True))
        self.stop(restarted)
        self.assert_disposed(first)
        self.assert_disposed(healthy)
        self.assertEqual(self._messages(), [])

    def _check_legacy_marker(self, state):
        # Arrange: legacy removal is not terminal proof; both native feature refs still exist.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        mapping['cleanup'] = {'state': state,
                              'pull_request_url': 'https://github.com/team/app/pull/3',
                              'merge_commit': self.git(self.workspace, 'rev-parse', 'HEAD')}
        self.save(message, record)
        output = self.workspace / 'legacy-cleanup-output'
        # Act: wait for durable completion, not merely disappearance during deletion.
        with output.open('w') as stream:
            process = self.start('--new-only', stdout=stream)
            self.wait_until(process, lambda: 'Cleanup confirmed' in output.read_text())
            self.stop(process)
        # Assert: marker/evidence is unchanged; absence was established by native checks.
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])
        self.assertEqual(json.loads(self.planning_call('get_task', task_id=1)['description']),
                         record)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: self.polls() >= 2)
        self.stop(restarted)
        self.assert_disposed(mapping)

    def test_old_removed_marker_never_replaces_actual_resource_checks(self):
        self._check_legacy_marker('removed')

    def test_old_pending_marker_never_replaces_actual_resource_checks(self):
        self._check_legacy_marker('pending')

    def test_branch_checked_out_elsewhere_blocks_ref_deletion_without_removing_that_tree(self):
        # Arrange: the recorded tree is already gone, but its branch has a different checkout.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        borrowed = self.workspace / 'borrowed-user-checkout'
        self.git(self.workspace, 'worktree', 'add', str(borrowed), mapping['branch'])
        (borrowed / 'keep.txt').write_text('Keep this checkout')
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertFalse(Path(mapping['path']).exists())
        self.assertEqual((borrowed / 'keep.txt').read_text(), 'Keep this checkout')
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['code'] == 'cleanup_operation_uncertain' for a in self.alerts()))
        # Restart reconciliation can finish after the user removes the other checkout.
        self.git(self.workspace, 'worktree', 'remove', '--force', str(borrowed))
        process = self.start('--new-only')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.stop(process)
        self.assert_disposed(mapping)

    def test_intake_manual_pause_and_github_failure_do_not_hide_later_completion(self):
        # Arrange: plan 1 is excluded from unfinished recovery; new plan 2 has uncertain setup.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record, status='archived')
        self.env['PLANNING_UNCERTAIN_CREATE'] = 'create_task'
        self.script({'team/app': [[[self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: any(a['retry'] == 'manual_reconciliation'
                                            for a in self.alerts()))
        second = self.planning_call('get_plan', plan_id=2)
        self.script({'team/app': ['Fixture GitHub intake unavailable']})
        # Act
        self.planning_call('update_plan', plan_id=message['plan_id'], status='completed')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.planning_call('get_plan', plan_id=2), second)
        self.assertTrue((self.workspace / '.factory/worktrees/team-app-2').exists())
        self.assertEqual(self.planning_call('list_plans')['total_count'], 2)
        self.assertEqual(self.planning_call('query_tasks', plan_id=2)['total_count'], 0)

    def test_lost_or_timed_out_worktree_response_is_reconciled_without_repeating_removal(self):
        # Arrange: a native Git launcher loses only the response, after real Git removed the tree.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        native_git = shutil.which('git')
        log = self.workspace / 'git-write-log.jsonl'
        git = self.bin / 'git'
        git.write_text('#!/usr/bin/env python3\nimport json, subprocess, sys, time\n'
                       f'result = subprocess.run([{native_git!r}, *sys.argv[1:]])\n'
                       'if "remove" in sys.argv and "worktree" in sys.argv:\n'
                       f'    with open({str(log)!r}, "a") as log:\n'
                       '        log.write(json.dumps(sys.argv[1:]) + "\\n")\n'
                       '    time.sleep(2)\n'
                       'sys.exit(result.returncode)\n')
        git.chmod(0o755)
        # Act: timeout is real, using the existing immutable public deadline seam.
        process = self.start('--new-only', deadlines=DeadlinePolicy(external_command=0.5))
        self.wait_until(process, lambda: bool(self.alerts()) and
                        not self.branch_exists(mapping, remote=True), timeout=10)
        self.wait_until(process, lambda: self.polls() >= 2)
        _, output, errors = self.stop(process)
        # Assert: no journal/marker was needed, and removal was not replayed after uncertainty.
        self.assertIn('timed out', errors)
        self.assertIn('Cleanup confirmed', output)
        self.assert_disposed(mapping)
        self.assertEqual(len(log.read_text().splitlines()), 1)
        self.assertEqual(json.loads(self.planning_call(
            'get_task', task_id=1)['description']), record)

    def test_incomplete_inventory_prevents_deletion_until_native_reply_is_complete(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        control = self.workspace / 'native-control.json'
        control.write_text(json.dumps({'incomplete': 'list_plans'}))
        self.env['PROFILE_PLANNING_CONTROL'] = str(control)
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        # Act
        control.write_text('{}')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])
        self.assertEqual({a['code'] for a in self.alerts()},
                         {'inventory_read_failed', 'cleanup_inventory_read_failed'})

    def test_absent_local_ref_does_not_hide_a_branch_still_registered_elsewhere(self):
        # Arrange: a manual ref deletion leaves another checkout's symbolic HEAD in place.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        borrowed = self.workspace / 'other-unborn-checkout'
        self.git(self.workspace, 'worktree', 'add', str(borrowed), mapping['branch'])
        self.git(self.workspace, 'update-ref', '-d', f'refs/heads/{mapping["branch"]}')
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(borrowed.exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))

    def test_local_branch_absence_is_confirmed_before_remote_deletion(self):
        # Arrange: a concurrent writer recreates the local branch after native Git deletion.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        native_git = shutil.which('git')
        git = self.bin / 'git'
        git.write_text('#!/usr/bin/env python3\nimport subprocess, sys\n'
                       f'result = subprocess.run([{native_git!r}, *sys.argv[1:]])\n'
                       'if "branch" in sys.argv and "-D" in sys.argv:\n'
                       f'    subprocess.run([{native_git!r}, "-C", {str(self.workspace)!r},\n'
                       f'                    "branch", {mapping["branch"]!r},\n'
                       '                    "HEAD"], check=True)\n'
                       'sys.exit(result.returncode)\n')
        git.chmod(0o755)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        _, output, _ = self.stop(process)
        # Assert
        self.assertFalse(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertNotIn('Cleanup confirmed', output)

    def test_missing_owner_isolated_from_another_completed_plan_and_new_issue_intake(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        context = json.loads(plan['context'])
        context['issue']['number'] = 2
        broken = self.planning_call('create_plan', project_id=12, status='completed',
                                    external_ref='github:team/app#2', context=json.dumps(context))
        self.script({'team/app': [[[self.issue(3)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True)
                        and bool(self._messages()) and bool(self.alerts()))
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual([m['number'] for m in self._messages()], [3])
        self.assertEqual(self.planning_call('get_plan', plan_id=broken['id'])['status'],
                         'completed')
        self.assertEqual(self.planning_call('query_tasks', plan_id=broken['id'])['tasks'], [])
        self.assertTrue(any(a['plan_id'] == broken['id'] and a['code'] == 'ownership_missing'
                            for a in self.alerts()))

    def test_advertised_completed_summary_cannot_override_an_active_full_plan(self):
        # Arrange: inventory summary is stale, and actual full native plan remains active.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record, status='active')
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        control = self.workspace / 'native-control.json'
        control.write_text(json.dumps({'responses': {'list_plans': {
            'plans': [dict(plan, status='completed')], 'total_count': 1}}}))
        self.env['PROFILE_PLANNING_CONTROL'] = str(control)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertEqual(self.planning_call('get_plan', plan_id=message['plan_id'])['status'],
                         'active')

    def test_exact_path_and_branch_claim_collisions_block_completed_resource_only(self):
        # Arrange: even a foreign/archived owner cannot be ignored if it claims this resource.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        other = self.planning_call('create_plan', project_id=99, status='archived',
                                   external_ref='github:team/foreign#4', context='{}')
        task = self.planning_call('create_task', plan_id=other['id'], title='Feature ownership',
                                  description='{}')
        for collision in ('path', 'branch'):
            with self.subTest(collision=collision):
                other_mapping = dict(mapping)
                if collision == 'path':
                    other_mapping['branch'] = 'factory/unrelated'
                else:
                    other_mapping['path'] = str(self.workspace / '.factory/worktrees/elsewhere')
                self.planning_call('update_task', task_id=task['id'], description=json.dumps(
                    dict(record, workspace='/tmp/foreign-factory', worktrees=[other_mapping])))
                self.script({'team/app': [[[]]]})
                # Act
                process = self.start('--new-only')
                self.wait_until(process, lambda: self.polls() >= 2)
                self.stop(process)
                # Assert
                self.assertTrue(Path(mapping['path']).exists())
                self.assertTrue(self.branch_exists(mapping, remote=True))
                self.assertTrue(any(a['code'] == 'cleanup_ownership_conflict'
                                    for a in self.alerts()))
                self.terminal_log.unlink()

    def test_inaccessible_remote_preserves_resources_and_retries_after_access_repair(self):
        # Arrange: no credentials/network are used; move the actual disposable bare repository.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        remote = Path(json.loads(self.env['CLEANUP_REMOTES'])['team/app.git'])
        unavailable = remote.with_name('temporarily-unavailable-bare')
        remote.rename(unavailable)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))
        unavailable.rename(remote)
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.wait_until(process, lambda: self.polls() >= 3)
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])

    def test_occupied_absent_mapping_and_prunable_registration_need_reconciliation(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        target = Path(mapping['path'])
        saved = target.with_name('saved-actual-worktree')
        target.rename(saved)
        # Act: registration still points at the now-missing path; do not prune it.
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(saved.exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertIn(mapping['path'], self.git(self.workspace, 'worktree', 'list', '--porcelain'))
        # An occupied path without registration is also not an already-absent success.
        saved.rename(target)
        self.git(self.workspace, 'worktree', 'remove', mapping['path'])
        target.mkdir()
        (target / 'user.txt').write_text('Preserve this unrelated directory')
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        self.assertEqual((target / 'user.txt').read_text(), 'Preserve this unrelated directory')
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))

    def test_invalid_full_task_withholds_all_disposal_until_claims_are_readable(self):
        # Arrange: unreadable full tasks cannot establish whether resources are independent.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        context = json.loads(plan['context'])
        context['issue']['number'] = 2
        broken = self.planning_call('create_plan', project_id=12, status='completed',
                                    external_ref='github:team/app#2', context=json.dumps(context))
        task = self.planning_call('create_task', plan_id=broken['id'], title='Feature ownership',
                                  description=json.dumps(dict(record, worktrees=[],
                                                              external_ref='github:team/app#2')))
        control = self.workspace / 'native-control.json'
        control.write_text(json.dumps({'response_cases': [{'tool': 'get_task',
            'arguments': {'task_id': task['id']}, 'result': dict(task, id=999)}]}))
        self.env['PROFILE_PLANNING_CONTROL'] = str(control)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a.get('plan_id') == broken['id'] for a in self.alerts()))
        self.assertEqual(self._messages(), [])

    def test_active_summary_cannot_hide_a_completed_full_plan(self):
        # Arrange: completion discovery must not use a stale summary as the status authority.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        control = self.workspace / 'native-control.json'
        control.write_text(json.dumps({'responses': {'list_plans': {
            'plans': [dict(plan, status='active')], 'total_count': 1}}}))
        self.env['PROFILE_PLANNING_CONTROL'] = str(control)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)
        self.assertEqual(self._messages(), [])

    def test_duplicate_reference_with_unreadable_details_cannot_authorize_a_primary_plan(self):
        # Arrange: complete inventory reports a competing identity, whose full reply is invalid.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        duplicate = self.planning_call('create_plan', **{key: plan[key] for key in (
            'project_id', 'status', 'external_ref', 'context')})
        control = self.workspace / 'native-control.json'
        control.write_text(json.dumps({'response_cases': [{'tool': 'get_plan',
            'arguments': {'plan_id': duplicate['id']}, 'result': dict(duplicate, id=999)}]}))
        self.env['PROFILE_PLANNING_CONTROL'] = str(control)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert: no choice between the two plan identities was established.
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertTrue(any(a['code'] == 'cleanup_read_failed'
                            and a.get('plan_id') == duplicate['id'] for a in self.alerts()))

    def test_lost_remote_delete_acknowledgement_rechecks_absence_without_pushing_twice(self):
        # Arrange: actual receive-pack deletes the ref, then the local launcher loses its reply.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        native_git = shutil.which('git')
        log = self.workspace / 'remote-delete-log.jsonl'
        git = self.bin / 'git'
        git.write_text('#!/usr/bin/env python3\nimport json, subprocess, sys\n'
                       f'result = subprocess.run([{native_git!r}, *sys.argv[1:]])\n'
                       f'if "push" in sys.argv and {":refs/heads/" + mapping["branch"]!r}'
                       ' in sys.argv:\n'
                       f'    with open({str(log)!r}, "a") as log:\n'
                       '        log.write(json.dumps(sys.argv[1:]) + "\\n")\n'
                       '    sys.exit("Fixture lost remote deletion acknowledgement")\n'
                       'sys.exit(result.returncode)\n')
        git.chmod(0o755)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()) and self.polls() >= 2)
        _, output, errors = self.stop(process)
        # Assert: actual absence, not the failed acknowledgement or a marker, proves completion.
        self.assert_disposed(mapping)
        self.assertEqual(len(log.read_text().splitlines()), 1)
        self.assertIn('Fixture lost remote deletion acknowledgement', errors)
        self.assertIn('Cleanup confirmed', output)
        self.assertEqual(self._messages(), [])
        self.assertEqual(json.loads(self.planning_call(
            'get_task', task_id=1)['description']), record)

    def append_repository(self, root, source):
        config = self.workspace / '.factory/factory.toml'
        with config.open('a') as stream:
            stream.write('\n[[repository]]\n' + f'local_dir = {json.dumps(str(root))}\n'
                         + f'remote = "git@github.com:{source}.git"\n'
                         + f'provider = "github"\nsource = "{source}"\n')

    def competing_plan(self, record, mapping, *, source='team/app'):
        plan = self.planning_call('get_plan', plan_id=1)
        context = json.loads(plan['context'])
        context['issue']['number'] = 2
        context['issue']['source']['reference'] = source
        other = self.planning_call('create_plan', project_id=12, status='archived',
                                   external_ref=f'github:{source}#2', context=json.dumps(context))
        self.planning_call('create_task', plan_id=other['id'], title='Feature ownership',
                           description=json.dumps(dict(record, external_ref=f'github:{source}#2',
                                                       worktrees=[mapping])))

    def test_independent_clones_cannot_dispose_another_plans_shared_remote_feature_ref(self):
        # Arrange: separate local branch namespaces, but the same GitHub repository/remote ref.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        second = self.workspace / 'independent-clone'
        remote = json.loads(self.env['CLEANUP_REMOTES'])['team/app.git']
        self.git(self.workspace, 'clone', '--quiet', remote, str(second))
        self.git(second, 'remote', 'set-url', 'origin', 'git@github.com:team/app.git')
        self.git(second, 'branch', mapping['branch'], 'HEAD')
        self.append_repository(second, 'team/app')
        self.competing_plan(record, dict(mapping, local_dir=str(second),
                                         path=str(second / '.factory/worktrees/other-plan')))
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertIn(mapping['branch'], self.git(second, 'branch', '--list', mapping['branch']))
        self.assertTrue(any(a['code'] == 'cleanup_ownership_conflict' for a in self.alerts()))

    def test_configured_roots_sharing_common_gitdir_protect_each_others_local_refs(self):
        # Arrange: linked roots can have different origins but still share local branch refs.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        second = self.workspace / 'second-configured-checkout'
        self.git(self.workspace, 'worktree', 'add', '-b', 'second-root', str(second), 'HEAD')
        self.git(self.workspace, 'config', 'extensions.worktreeConfig', 'true')
        self.git(self.workspace, 'config', '--unset-all', 'remote.origin.url')
        self.git(self.workspace, 'config', '--worktree', 'remote.origin.url',
                 'git@github.com:team/app.git')
        self.git(second, 'config', '--worktree', 'remote.origin.url',
                 'git@github.com:team/library.git')
        self.add_remote(second, 'team/library')
        self.append_repository(second, 'team/library')
        self.competing_plan(record, dict(mapping, repository='team/library', local_dir=str(second),
                                         path=str(second / '.factory/worktrees/other-plan'),
                                         target_branch='second-root'), source='team/library')
        self.save(message, record)
        self.script({'team/app': [[[]]], 'team/library': [[[]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))
        self.assertEqual(self.git(second, 'branch', '--show-current'), 'second-root')
        self.assertTrue(any(a['code'] == 'cleanup_ownership_conflict' for a in self.alerts()))
        # A wrong origin blocks disposal there, but cannot erase its readable local-ref claim.
        self.git(second, 'config', '--worktree', 'remote.origin.url',
                 'git@github.com:team/wrong-origin.git')
        self.script({'team/app': [[[]]], 'team/library': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))

    def test_nested_configured_main_checkout_is_not_disposable_worktree_content(self):
        # Arrange: a configured independent checkout is nested within a completed-plan tree.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        nested = Path(mapping['path']) / 'configured-main-checkout'
        remote = json.loads(self.env['CLEANUP_REMOTES'])['team/app.git']
        self.git(self.workspace, 'clone', '--quiet', remote, str(nested))
        self.git(nested, 'remote', 'set-url', 'origin', 'git@github.com:team/app.git')
        self.append_repository(nested, 'team/app')
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assertTrue((nested / '.git').is_dir(), 'Removed another configured main checkout')
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping, remote=True))
