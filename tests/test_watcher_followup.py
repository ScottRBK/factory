"""Follow-up regressions at the public watch CLI and native external boundaries."""
import json
import subprocess
from pathlib import Path

import test_foreman_setup_repair as setup_repair
from test_planning_watch import PlanningWatchFixture


class FollowupFixture(PlanningWatchFixture):
    def setUp(self):
        super().setUp()
        self.control = self.workspace / 'planning-control.json'
        self.control.write_text('{}')
        self.env['PROFILE_PLANNING_CONTROL'] = str(self.control)

    fault = setup_repair.ForemanSetupRepairTests.fault
    polls = setup_repair.ForemanSetupRepairTests.polls
    native_plan = setup_repair.ForemanSetupRepairTests.native_plan
    native_owner = setup_repair.ForemanSetupRepairTests.native_owner
    git_fault = setup_repair.ForemanSetupRepairTests.git_fault
    repair_git = setup_repair.ForemanSetupRepairTests.repair_git

    def _state(self):
        path = self.workspace / '.factory/fixture-plans.json'
        return json.loads(path.read_text()) if path.exists() else dict(plans=[], tasks=[], calls=[])


class PendingEligibilityTests(FollowupFixture):
    def assert_ineligible_pending_is_not_created(self, **excluded):
        # Arrange: new work arrives after an empty new-only baseline, then lookup fails.
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1, updated_at='old')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        # Act: successful polls exclude this issue before the backend read is repaired.
        self.script({'team/app': [[[self.issue(1, updated_at='excluded', **excluded)]]]})
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(len(self.alerts()), 1)
        self.fault()
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 4)
        # Assert: stale data may discover saved work, but cannot authorize fresh scaffolding.
        self.assertIsNone(process.poll())
        self.assertEqual(self._state()['plans'], [])
        self.assertEqual(self._state()['tasks'], [])
        self.assertEqual(self._messages(), [])
        # Act: eligible work may return with a new revision, alongside genuinely new work.
        self.script({'team/app': [[[self.issue(1, updated_at='eligible-again'), self.issue(2)]]]})
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual([(m['id'], m['revision']) for m in self._messages()], [
            ('github:team/app#1', 'eligible-again'), ('github:team/app#2', '')])
        self.assertEqual(sum(c[0] == 'create_plan' for c in self._state()['calls']), 2)

    def test_closed_pending_lookup_drops_without_create_and_reopen_keeps_latest_revision(self):
        self.assert_ineligible_pending_is_not_created(state='closed')

    def test_unlabelled_pending_lookup_drops_without_create_and_relabel_allows_new_work(self):
        self.assert_ineligible_pending_is_not_created(labels=('other',))

    def test_unlabelled_pending_lookup_still_discovers_saved_plan_read_only(self):
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1)]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        plan = self.native_plan()
        self.script({'team/app': [[[self.issue(1, labels=('other',))]]]})
        self.wait_until(process, lambda: self.polls() >= 3)
        self.fault()
        self.wait_until(process, lambda: any(a['code'] == 'setup_incomplete'
                                            for a in self.alerts()))
        self.assertEqual(self.alerts()[-1]['plan_id'], plan['id'])
        self.assertEqual(self._state()['tasks'], [])
        owner = self.native_owner(plan['id'])
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])


class OwnershipReconciliationTests(FollowupFixture):
    def retire(self, task, survivor_id):
        record = json.loads(task['description'])
        record.update(kind='factory-retired-ownership', retained_ownership_task_id=survivor_id)
        return self.planning_call('update_task', task_id=task['id'],
                                  title='Retired duplicate ownership',
                                  description=json.dumps(record))

    def assert_either_unconfirmed_survivor(self, keep_second):
        # Arrange: neither duplicate has ever been confirmed as the single owner by watch.
        plan = self.native_plan()
        first = self.native_owner(plan['id'])
        record = json.loads(first['description'])
        record.update(notes='Preserve notes and history',
                      links=['https://example.invalid/evidence'])
        first = self.planning_call('update_task', task_id=first['id'],
                                   description=json.dumps(record))
        second = self.planning_call('create_task', plan_id=plan['id'], title=first['title'],
                                    description=first['description'])
        survivor, retired = (second, first) if keep_second else (first, second)
        skill = self.workspace / '.factory/agents/foreman/skills/foreman/SKILL.md'
        skill.write_text('---\nname: foreman\ndescription: Old guidance.\n---\nKeep my edits.\n')
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        alert = self.alerts()[0]
        self.assertEqual(alert['code'], 'ownership_ambiguous')
        self.assertEqual(alert['ownership_task_ids'], [first['id'], second['id']])
        self.assertNotIn('ownership_task_id', alert)
        for text in ('user approval', 'update_task', 'title', 'kind', 'Feature ownership',
                     'factory-ownership', 'transition_task', 'not compare-and-swap'):
            self.assertIn(text, alert['recovery'])
        # Act: changing only the title does not retire its ownership kind.
        self.planning_call('update_task', task_id=retired['id'],
                           title='Retired duplicate ownership')
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.fault(responses={'query_tasks': {'tasks': [second, first], 'total_count': 2}})
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(len(self.alerts()), 1, 'Candidate ordering does not change the episode')
        self.fault()
        # Act: simulated user-approved native metadata repair changes both designations in place.
        repaired = self.retire(retired, survivor['id'])
        self.wait_until(process, lambda: bool(self._messages()) or any(
            a['code'] == 'ownership_identity_changed' for a in self.alerts()))
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual([m['ownership_task_id'] for m in self._messages()], [survivor['id']])
        # Assert: only native metadata changed; no task, claim, worktree or history was discarded.
        self.assertEqual(self.planning_call('get_task', task_id=survivor['id']), survivor)
        self.assertEqual(self.planning_call('get_task', task_id=retired['id']), repaired)
        for field in ('state', 'version', 'assigned_agent'):
            self.assertEqual(repaired[field], retired[field])
        for field in ('workspace', 'external_ref', 'worktrees', 'notes', 'links'):
            self.assertEqual(json.loads(repaired['description'])[field], record[field])
        self.assertIn('Keep my edits.', skill.read_text())
        self.assertEqual(self._state()['plans'], [plan])
        self.assertEqual(len(self._state()['tasks']), 2)

    def test_approved_retirement_accepts_first_candidate_when_no_owner_was_confirmed(self):
        self.assert_either_unconfirmed_survivor(keep_second=False)

    def test_approved_retirement_accepts_second_candidate_when_no_owner_was_confirmed(self):
        self.assert_either_unconfirmed_survivor(keep_second=True)

    def test_retirement_cannot_replace_a_sole_owner_pinned_before_mapping_repair(self):
        plan = self.native_plan()
        first = self.native_owner(plan['id'])
        target = Path(json.loads(first['description'])['worktrees'][0]['path'])
        saved = target.with_name('saved-owner-work')
        target.rename(saved)
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['ownership_task_id'], first['id'])
        second = self.planning_call('create_task', plan_id=plan['id'], title=first['title'],
                                    description=first['description'])
        self.retire(first, second['id'])
        saved.rename(target)
        self.wait_until(process, lambda: any(a['code'] == 'ownership_identity_changed'
                                            for a in self.alerts()))
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.alerts()[-1]['ownership_task_id'], first['id'])
        # Restore the pinned record, and retire the extra designation without deleting work.
        self.retire(second, first['id'])
        self.planning_call('update_task', task_id=first['id'], title=first['title'],
                           description=first['description'])
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], first['id'])


class RepositoryPreflightTests(FollowupFixture):
    def set_origin(self, remote):
        subprocess.run(['git', '-C', str(self.workspace), 'remote', 'set-url', 'origin', remote],
                       check=True)

    def test_startup_wrong_origin_pauses_only_affected_repository_before_any_plan(self):
        # Arrange: origin differs from the saved remote; a second configured repo is safe.
        self.configure(sources=('team/app', 'team/healthy'))
        self.set_origin('https://TOP_SECRET:credential@github.com/other/repo.git')
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]],
                     'team/healthy': [[[self.issue(3)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'repository_origin_changed')
        self.assertEqual(self.alerts()[0]['scope'], 'repository')
        self.assertNotIn('plan_id', self.alerts()[0])
        self.wait_until(process, lambda: bool(self._messages()))
        self.assertEqual([p['external_ref'] for p in self._state()['plans']],
                         ['github:team/healthy#3'])
        self.assertEqual(len(self.alerts()), 1)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        self.assertNotIn('github.com', json.dumps(self.alerts()))
        # Act: a Git-only correction allows fresh automatic intake, with no issue edits.
        self.set_origin('git@github.com:team/app.git')
        self.wait_until(process, lambda: len(self._messages()) == 3)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual({m['id'] for m in self._messages()}, {
            'github:team/app#1', 'github:team/app#2', 'github:team/healthy#3'})

    def test_origin_changed_after_startup_is_checked_again_before_next_plan(self):
        self.configure(sources=('team/app', 'team/healthy'))
        self.script({'team/app': [[[]]], 'team/healthy': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.set_origin('git@github.com:other/repo.git')
        self.script({'team/app': [[[self.issue(1)]]], 'team/healthy': [[[self.issue(3)]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'repository_origin_changed')
        self.assertNotIn('plan_id', self.alerts()[0])
        self.wait_until(process, lambda: bool(self._messages()))
        self.assertEqual([p['external_ref'] for p in self._state()['plans']],
                         ['github:team/healthy#3'])
        self.set_origin('git@github.com:team/app.git')
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.assertEqual(self.stop(process)[0], 130)

    def test_fresh_path_conflict_creates_nothing_there_and_correction_allows_fresh_intake(self):
        target = self.workspace / '.factory/worktrees/team-app-1'
        target.mkdir(parents=True)
        (target / 'user.txt').write_text('TOP_SECRET preserve data')
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()) and bool(self._messages()))
        self.assertEqual(self.alerts()[0]['code'], 'worktree_path_conflict')
        self.assertNotIn('plan_id', self.alerts()[0])
        self.assertEqual([p['external_ref'] for p in self._state()['plans']],
                         ['github:team/app#2'])
        saved = target.with_name('saved-user-directory')
        target.rename(saved)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual((saved / 'user.txt').read_text(), 'TOP_SECRET preserve data')
        self.assertEqual(len(self._state()['tasks']), 2)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_unused_existing_branch_is_found_before_plan_and_preserved_on_correction(self):
        branch = 'factory/team-app-1'
        subprocess.run(['git', '-C', str(self.workspace), 'branch', branch], check=True)
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'worktree_branch_conflict')
        self.assertEqual(self._state()['plans'], [])
        subprocess.run(['git', '-C', str(self.workspace), 'branch', '-m', branch,
                        'preserved-user-branch'], check=True)
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        subprocess.run(['git', '-C', str(self.workspace), 'show-ref', '--verify',
                        'refs/heads/preserved-user-branch'], check=True, capture_output=True)

    def test_pre_add_read_failure_is_retryable_without_any_saved_plan(self):
        control = self.git_fault(['worktree', 'list'])
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'worktree_read_failed')
        self.assertNotIn('plan_id', self.alerts()[0])
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(self._state()['plans'], [])
        self.assertEqual(len(self.alerts()), 1)
        self.repair_git(control)
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(sum(c[0] == 'create_plan' for c in self._state()['calls']), 1)

    def test_backend_read_episode_clears_even_when_fresh_path_is_still_blocked(self):
        target = self.workspace / '.factory/worktrees/team-app-1'
        target.mkdir(parents=True)
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1)]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.fault()
        self.wait_until(process, lambda: any(a['code'] == 'worktree_path_conflict'
                                            for a in self.alerts()))
        # A healthy backend read ended its episode, even though a different safety fact remains.
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(sum(a['code'] == 'recovery_read_failed' for a in self.alerts()), 2)
        self.assertEqual(self._state()['plans'], [])
        self.fault()
        target.rmdir()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
    def test_startup_empty_source_still_alerts_mapping_that_matches_wrong_saved_origin(self):
        # Arrange: saved and actual URLs agree, but the configured source names another repo.
        wrong = 'git@github.com:other/repo.git'
        self.set_origin(wrong)
        config = self.workspace / '.factory/factory.toml'
        config.write_text(config.read_text().replace('git@github.com:team/app.git', wrong))
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'repository_source_mismatch')
        self.assertIsNone(process.poll())
        self.assertEqual(self._state()['plans'], [])
        self.assertEqual(self._messages(), [])
        # Updating the file cannot change this running watcher's configuration snapshot.
        config.write_text(config.read_text().replace(wrong, 'git@github.com:team/app.git'))
        self.set_origin('git@github.com:team/app.git')
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(self._state()['plans'], [])
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--existing')
        self.wait_until(restarted, lambda: self.polls() >= 3)
        self.assertEqual(self.alerts(), [])
        self.assertEqual(self.stop(restarted)[0], 130)

    def test_epic_requires_valid_source_mapping_but_defers_worktree_choice(self):
        target = self.workspace / '.factory/worktrees/team-app-1'
        target.mkdir(parents=True)
        (target / 'user.txt').write_text('Preserve epic planning choices')
        self.set_origin('git@github.com:other/repo.git')
        self.script({'team/app': [[[self.issue(1, labels=('factory', 'epic'))]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self._state()['plans'], [])
        self.set_origin('git@github.com:team/app.git')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertTrue(self._messages()[0]['epic'])
        self.assertEqual(self._messages()[0]['worktrees'], [])
        self.assertEqual((target / 'user.txt').read_text(), 'Preserve epic planning choices')

    def test_startup_repository_read_outage_has_no_plan_and_retries_safely(self):
        control = self.git_fault(['remote', 'get-url', 'origin'])
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'repository_read_failed')
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(self._state()['plans'], [])
        self.assertEqual(len(self.alerts()), 1)
        self.repair_git(control)
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_bad_repository_path_read_stays_local_and_repair_preserves_git_data(self):
        self.configure(sources=('team/app', 'team/broken'))
        repository = self.workspace / 'repository-1'
        saved = self.workspace / 'saved-repository'
        repository.rename(saved)
        repository.symlink_to(repository.name)
        self.script({'team/app': [[[self.issue(1)]]], 'team/broken': [[[self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['code'], 'repository_read_failed')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual([p['external_ref'] for p in self._state()['plans']],
                         ['github:team/app#1'])
        repository.unlink()  # Remove only this fixture's loop, preserving the real Git directory.
        saved.rename(repository)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)
        self.assertTrue((repository / '.git').is_dir())

    def test_changed_origin_after_plan_commit_remains_saved_repair_with_controlled_cause(self):
        # Actual native plan creation commits, then an external actor changes Git before add.
        command = self.bin / 'forgetful'
        original = command.read_text()
        point = '        save_planning_state()\n        if os.environ.get'
        self.assertEqual(original.count(point), 1)
        command.write_text(original.replace(point,
            "        if tool == 'create_plan':\n"
            "            import subprocess\n"
            f"            subprocess.run(['git', '-C', {str(self.workspace)!r}, 'remote', "
            "'set-url', 'origin', 'git@github.com:other/repo.git'], check=True)\n" + point))
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        first = self.alerts()[0]
        self.assertEqual(first['code'], 'setup_incomplete')
        self.assertEqual(first.get('cause'), 'repository_origin_changed')
        self.assertEqual(len(self._state()['plans']), 1,
                         'Fault must follow the actual plan write')
        plan_id = first['plan_id']
        self.assertEqual(self._state()['tasks'], [])
        command.write_text(original)
        self.set_origin('git@github.com:team/app.git')
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(self._state()['tasks'], [],
                         'Saved setup cannot automatically complete')
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        owner = self.native_owner(plan_id)
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
