"""Durable terminal cleanup authority through public watch and real disposable Git."""
import json
import shutil
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture, plan_records

from forgetful_factory.factory.adapters.cleanup_receipts import FileCleanupReceipts
from forgetful_factory.factory.ports import CleanupPlan, CleanupSet
from forgetful_factory.shared.errors import FactoryError


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

    def log_git(self, name):
        """Log each Git command watch runs, then run the real Git."""
        native = shutil.which('git')
        log = self.workspace / name
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                           f'with open({str(log)!r}, "a") as stream:\n'
                           '    stream.write(json.dumps(sys.argv[1:]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        return log


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
        log = self.log_git('restart-git-commands.jsonl')
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: self.polls() >= 3)
        _, text, _ = self.stop(restarted)
        # Assert: only ordinary startup root/origin reads occur, never another cleanup index.
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertFalse(any('--git-common-dir' in args or 'worktree' in args or
                             'ls-remote' in args or 'push' in args for args in calls), calls)
        (self.bin / 'git').unlink()
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
        self.assertEqual(self._messages()[0]['key'], '3')
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
        self.assertEqual(json.loads(receipt.read_text())['version'], 2)

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


class CleanupPlanRecordTests(CleanupReceiptFixture):
    def test_first_cycle_after_upgrade_records_cleaned_plans_without_deleting_again(self):
        # Arrange: an older Factory disposed the set and saved a version 1 receipt.
        message, _, mapping = prepare_completed_set(self)
        first = self.start('--new-only')
        self.wait_until(first, lambda: bool(plan_records(self.workspace)), timeout=15)
        self.stop(first)
        receipt = self.workspace / '.factory/cleanup-finished.json'
        finished = json.loads(receipt.read_text())['finished']
        receipt.write_text(json.dumps({'version': 1, 'finished': finished}))
        commit = self.human_refs(mapping)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        log = self.log_git('upgrade-git-commands.jsonl')
        # Act
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: bool(plan_records(self.workspace)))
        self.stop(restarted)
        # Assert: receipts alone close the plan. No cleanup Git command runs again.
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertFalse(any('--git-common-dir' in args or 'worktree' in args or
                             'ls-remote' in args or 'push' in args for args in calls), calls)
        (self.bin / 'git').unlink()
        self.assertEqual(self.git(mapping['local_dir'], 'rev-parse', mapping['branch']), commit)
        self.assertEqual(json.loads(receipt.read_text()), {
            'version': 2, 'finished': finished, 'plans': [{
                'workspace': str(self.workspace), 'backend': finished[0]['backend'],
                'plan_id': message['plan_id'], 'external_ref': finished[0]['external_ref']}]})

    def test_plan_is_recorded_only_after_every_set_is_confirmed(self):
        # Arrange: the remote refuses branch deletion, so disposal fails.
        _, _, mapping = prepare_completed_set(self)
        remote = Path(json.loads(self.env['CLEANUP_REMOTES'])['team/app.git'])
        hook = remote / 'hooks/update'
        hook.write_text('#!/bin/sh\ncase "$3" in 000000*) exit 1;; esac\n')
        hook.chmod(0o755)
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2 and any(
            a['scope'] == 'cleanup' for a in self.alerts()))
        # Assert: a failed set keeps the plan open for the next poll.
        self.assertEqual(plan_records(self.workspace), [])
        # Act
        hook.unlink()
        self.wait_until(process, lambda: bool(plan_records(self.workspace)))
        self.stop(process)
        # Assert
        self.assert_disposed(mapping)

    def test_plan_without_worktrees_is_recorded_and_out_of_scope_plans_are_not(self):
        # Arrange: a completed plan with no mappings, and a completed plan for a source that
        # no configured repository owns.
        message, record = self.recorded()
        record['worktrees'] = []
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        other = self.planning_call('create_plan', title='Other source',
                                   project_id=plan['project_id'], status='completed',
                                   external_ref='github:other/app#5')
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(plan_records(self.workspace)))
        self.wait_until(process, lambda: self.polls() >= 3)
        self.stop(process)
        # Assert
        self.assertEqual([row['plan_id'] for row in plan_records(self.workspace)],
                         [message['plan_id']])
        self.assertNotEqual(other['id'], message['plan_id'])
        self.assertTrue(Path(message['worktrees'][0]['path']).is_dir())


class CleanupPlanReferenceTests(CleanupReceiptFixture):
    def test_plans_that_share_a_reference_are_reported_and_never_recorded(self):
        # Arrange: two owned completed plans use one reference. Each has a valid owner and
        # nothing to dispose, so no Git read or claim index finds the duplicate.
        message, record = self.recorded()
        record['worktrees'] = []
        self.save(message, record)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        twin = self.planning_call('create_plan', **{key: plan[key] for key in (
            'title', 'project_id', 'status', 'external_ref', 'context')})
        self.planning_call('create_task', plan_id=twin['id'], title='Feature ownership',
                           description=json.dumps(record))
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 3 and len(
            [a for a in self.alerts() if a['code'] == 'cleanup_ownership_conflict']) == 2)
        self.stop(process)
        # Assert
        self.assertEqual(plan_records(self.workspace), [])
        conflicts = [a for a in self.alerts() if a['code'] == 'cleanup_ownership_conflict']
        self.assertEqual({a['plan_id'] for a in conflicts}, {plan['id'], twin['id']})
        self.assertEqual(conflicts[0]['plan_ids'], sorted((plan['id'], twin['id'])))


class CleanupReceiptFileTests(unittest.TestCase):
    """The receipt file format, read and written at the file boundary."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        (self.workspace / '.factory').mkdir()
        self.path = self.workspace / '.factory/cleanup-finished.json'
        self.receipts = FileCleanupReceipts(self.workspace)
        workspace = str(self.workspace)
        self.resource = CleanupSet(workspace, 'local:fixture', 3, 'github:team/app#3',
                                   'team/app', workspace, 'factory/team-app-3',
                                   workspace + '/.factory/worktrees/team-app-3')
        self.plan = CleanupPlan(workspace, 'local:fixture', 3, 'github:team/app#3')

    def write(self, value):
        self.path.write_text(json.dumps(value))
        self.path.chmod(0o600)

    def test_version_1_loads_without_plan_records_and_is_saved_as_version_2(self):
        # Arrange
        self.write({'version': 1, 'finished': [asdict(self.resource)]})
        # Act
        loaded = self.receipts.load()
        self.receipts.confirm_plans([self.plan])
        # Assert
        self.assertEqual((loaded.sets, loaded.plans), ({self.resource}, set()))
        self.assertEqual(json.loads(self.path.read_text()), {
            'version': 2, 'finished': [asdict(self.resource)], 'plans': [asdict(self.plan)]})

    def test_plan_records_survive_later_set_confirmations(self):
        # Act
        self.receipts.confirm_plans([self.plan])
        self.receipts.confirm(self.resource)
        loaded = self.receipts.load()
        # Assert
        self.assertEqual((loaded.sets, loaded.plans), ({self.resource}, {self.plan}))

    def test_several_plans_are_recorded_in_one_write(self):
        # Arrange
        other = CleanupPlan(self.plan.workspace, self.plan.backend, 4, 'github:team/app#4')
        self.receipts.confirm_plans([self.plan])
        before = self.path.stat().st_ino
        # Act
        self.receipts.confirm_plans([other, CleanupPlan(**asdict(self.plan))])
        # Assert: one replacement holds both; a plan already recorded is not added twice.
        self.assertNotEqual(self.path.stat().st_ino, before)
        self.assertEqual(self.receipts.load().plans, {self.plan, other})

    def test_unknown_versions_fields_and_damaged_plan_records_are_refused(self):
        plan = asdict(self.plan)
        version = {'version': 2, 'finished': []}
        documents = {
            'unknown version': {'version': 3, 'finished': [], 'plans': []},
            'version 1 with plans': {'version': 1, 'finished': [], 'plans': []},
            'version 2 without plans': version,
            'unknown top field': dict(version, plans=[], extra=1),
            'plans not a list': dict(version, plans={}),
            'unknown plan field': dict(version, plans=[dict(plan, repository='team/app')]),
            'missing plan field': dict(version, plans=[
                {key: value for key, value in plan.items() if key != 'external_ref'}]),
            'plan id zero': dict(version, plans=[dict(plan, plan_id=0)]),
            'plan id text': dict(version, plans=[dict(plan, plan_id='3')]),
            'empty reference': dict(version, plans=[dict(plan, external_ref='')]),
            'control character': dict(version, plans=[dict(plan, backend='local:\n')]),
            'relative workspace': dict(version, plans=[dict(plan, workspace='workspace')]),
            'other workspace': dict(version, plans=[dict(plan, workspace='/elsewhere')]),
            'duplicate plans': dict(version, plans=[plan, plan]),
        }
        for name, document in documents.items():
            with self.subTest(name):
                # Arrange
                self.write(document)
                # Act / Assert: refused, and the file stays as it was.
                with self.assertRaises(FactoryError):
                    self.receipts.load()
                with self.assertRaises(FactoryError):
                    self.receipts.confirm_plans([self.plan])
                self.assertEqual(json.loads(self.path.read_text()), document)
