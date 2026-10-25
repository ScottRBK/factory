"""Watcher alerts at the CLI, real Git and external program boundaries."""
import json
import subprocess
from pathlib import Path

from test_planning_watch import PlanningWatchFixture


class WatcherAlertTests(PlanningWatchFixture):
    def setUp(self):
        super().setUp()
        self.control = self.workspace / 'planning-control.json'
        self.control.write_text('{}')
        self.env['PROFILE_PLANNING_CONTROL'] = str(self.control)

    def fault(self, **control):
        replacement = self.control.with_suffix('.next')
        replacement.write_text(json.dumps(control))
        replacement.replace(self.control)

    def seed(self, numbers=(1, 2)):
        self.script({'team/app': [[[self.issue(n, updated_at='same-revision')
                                    for n in numbers]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == len(numbers))
        self.stop(process)
        messages = self._messages()
        self.terminal_log.unlink()
        return messages

    def polls(self):
        return json.loads(self.state_path.read_text()).get('counts', {}).get('team/app', 0)

    def test_new_only_covers_first_success_batch_before_interrupted_recovered_intake(self):
        # Arrange: #1 is recovered work; #2 already exists at the first successful source read.
        self.seed((1,))
        plan = self.planning_call('get_plan', plan_id=1)
        changed = self.issue(1, updated_at='changed')
        old = self.issue(2, updated_at='old')
        self.script({'team/app': ['HTTP 503 unavailable', [[changed, old]]]})
        process = self.start('--new-only', '--interval', '0.5')
        self.wait_until(process, lambda: any(a['code'] == 'source_read_failed'
                                            for a in self.alerts()))
        self.fault(responses={'get_plan': dict(plan, id=999)})
        self.wait_until(process, lambda: any(a['code'] == 'recovery_read_failed'
                                            for a in self.alerts()))
        self.assertEqual(len(self._messages()), 1)
        # Act: repair without editing either issue; #3 arrives after that first successful read.
        self.fault()
        self.script({'team/app': [[[changed, old, self.issue(3, updated_at='new')]]]})
        self.wait_until(process, lambda: len(self._messages()) >= 3)
        self.wait_until(process, lambda: self.polls() >= 4)
        code, _, errors = self.stop(process)
        # Assert: interrupted intake cannot turn old #2 into new work or swallow new #3.
        self.assertEqual(code, 130, errors)
        self.assertEqual([(m['id'], m['revision']) for m in self._messages()], [
            ('github:team/app#1', 'same-revision'), ('github:team/app#1', 'changed'),
            ('github:team/app#3', 'new')])
        state = self.planning_call('list_plans')
        self.assertEqual([p['external_ref'] for p in state['plans']],
                         ['github:team/app#1', 'github:team/app#3'])
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)

    def duplicate_plan(self, plan_id=1):
        plan = self.planning_call('get_plan', plan_id=plan_id)
        return self.planning_call('create_plan', **{key: plan[key] for key in (
            'title', 'project_id', 'external_ref', 'source_url', 'context')})

    def assert_ambiguous_plan_alert(self, alert, plan_ids):
        self.assertEqual(alert['code'], 'plan_ambiguous')
        self.assertEqual(alert['scope'], 'plan')
        self.assertEqual(alert['issue_id'], 'github:team/app#1')
        self.assertEqual(alert.get('plan_ids'), plan_ids)
        self.assertNotIn('plan_id', alert, 'Ambiguity cannot establish a primary plan')

    def test_duplicate_startup_plans_alert_all_candidates_without_choosing_or_writes(self):
        # Arrange: two active plans share one reference; an unrelated plan is healthy.
        self.seed()
        duplicate = self.duplicate_plan()
        task = self.planning_call('get_task', task_id=1)
        self.script({'team/app': [[[]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()) and len(self._messages()) == 1)
        self.wait_until(process, lambda: self.polls() >= 3)
        code, _, errors = self.stop(process)
        # Assert: both known IDs are reported, neither is selected or replaced.
        self.assertEqual(code, 130, errors)
        self.assertEqual(len(self.alerts()), 1)
        self.assert_ambiguous_plan_alert(self.alerts()[0], [1, duplicate['id']])
        self.assertEqual([m['plan_id'] for m in self._messages()], [2])
        self.assertEqual(self.planning_call('get_task', task_id=1), task)
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 3)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 2)
        self.assertEqual(sum(c[0] == 'update_plan' for c in state['calls']), 2)

    def test_duplicate_initial_intake_plans_report_candidates_without_primary(self):
        # Arrange: completed plans are absent from the startup unfinished inventory.
        self.seed((1,))
        duplicate = self.duplicate_plan()
        for plan_id in (1, duplicate['id']):
            self.planning_call('update_plan', plan_id=plan_id, status='completed')
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        # Act: both plans become active before this issue enters ordinary intake.
        for plan_id in (1, duplicate['id']):
            self.planning_call('update_plan', plan_id=plan_id, status='active')
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        self.wait_until(process, lambda: bool(self.alerts()) and bool(self._messages()))
        self.wait_until(process, lambda: self.polls() >= 3)
        code, _, errors = self.stop(process)
        # Assert: ambiguity remains isolated and does not authorize a choice.
        self.assertEqual(code, 130, errors)
        self.assertEqual(len(self.alerts()), 1)
        self.assert_ambiguous_plan_alert(self.alerts()[0], [1, duplicate['id']])
        self.assertEqual([m['id'] for m in self._messages()], ['github:team/app#2'])
        self.assertEqual(self.planning_call('query_tasks', plan_id=duplicate['id'])['tasks'], [])

    def test_duplicate_recovery_candidates_never_replace_the_pinned_plan(self):
        # Arrange: a known plan is pinned while its original worktree needs repair.
        original, = self.seed((1,))
        target = Path(original['worktrees'][0]['path'])
        saved = target.with_name('saved-original-tree')
        target.rename(saved)
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        # Act: duplicate candidates are reported, then only the replacement is returned.
        duplicate = self.duplicate_plan()
        self.wait_until(process, lambda: len(self.alerts()) >= 2)
        self.assert_ambiguous_plan_alert(self.alerts()[-1], [1, duplicate['id']])
        original_plan = self.planning_call('get_plan', plan_id=original['plan_id'])
        self.fault(responses={'list_plans': {
            'plans': [duplicate, original_plan], 'total_count': 2}})
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(len(self.alerts()), 2, 'Candidate order does not change the problem')
        self.fault(responses={'list_plans': {'plans': [duplicate], 'total_count': 1}})
        self.wait_until(process, lambda: self.alerts()[-1]['code'] == 'plan_identity_changed')
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.alerts()[-1]['plan_id'], original['plan_id'])
        # Act: reconcile the duplicate association and restore the original tree.
        self.planning_call('update_plan', plan_id=duplicate['id'],
                           external_ref='github:team/app#99')
        self.fault()
        saved.rename(target)
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        # Assert: the pinned original identity is still the only recovery authority.
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['ownership_task_id'], original['ownership_task_id'])

    def test_missing_tree_alerts_once_keeps_healthy_plan_and_recovers_closed_new_only(self):
        # Arrange: both plans exist; one saved tree is temporarily absent.
        original, healthy = self.seed()
        target = Path(original['worktrees'][0]['path'])
        saved = target.with_name('saved-user-work')
        (target / 'unfinished.txt').write_text('Preserve my work.')
        target.rename(saved)
        self.planning_call('update_task', task_id=1, state='doing', version=4,
                           assigned_agent='native-busy-owner')
        task_before = self.planning_call('get_task', task_id=1)
        self.script({'team/app': [[[]]]})
        # Act: recovery must work even when the issue is closed and new-only is selected.
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.wait_until(process, lambda: self.polls() >= 3)
        # Assert: the other plan reaches Foreman and the blocked plan is preserved.
        self.assertIsNone(process.poll())
        self.assertEqual(self._messages()[0]['plan_id'], healthy['plan_id'])
        self.assertEqual(len(self.alerts()), 1)
        alert = self.alerts()[0]
        self.assertEqual(alert['scope'], 'plan')
        self.assertEqual(alert['issue_id'], 'github:team/app#1')
        self.assertEqual(alert['plan_id'], original['plan_id'])
        self.assertEqual(alert['ownership_task_id'], original['ownership_task_id'])
        self.assertIn(str(target), alert['paths'])
        self.assertFalse(target.exists())
        self.assertEqual(self.planning_call('get_task', task_id=1), task_before)
        # Act: repair the same tree without changing the GitHub revision.
        saved.rename(target)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.wait_until(process, lambda: self.polls() >= 6)
        code, _, errors = self.stop(process)
        # Assert: exactly one recovery notification, with the original identities.
        self.assertEqual(code, 130, errors)
        restored = self._messages()[-1]
        for field in ('plan_id', 'ownership_task_id', 'worktrees'):
            self.assertEqual(restored[field], original[field])
        self.assertEqual((target / 'unfinished.txt').read_text(), 'Preserve my work.')
        self.assertEqual(len(self._messages()), 2)
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)
        self.assertEqual(self.planning_call('list_plans')['total_count'], 2)
        self.assertEqual(self.planning_call('get_task', task_id=1), task_before)

    def test_source_failure_deduplicates_and_resets_after_success_with_first_success_baseline(self):
        # Arrange: healthy source can deliver while another source remains unavailable.
        self.configure(sources=('team/app', 'team/healthy'))
        self.script({'team/app': ['TOP_SECRET\x1b[31m backend failure'],
                     'team/healthy': [[[]], [[self.issue(3)]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(len(self.alerts()), 1)
        # Act: the failing source's first success must baseline existing issues.
        self.script({'team/app': [[[self.issue(1)]], [[self.issue(1), self.issue(2)]]],
                     'team/healthy': [[[self.issue(3)]]]})
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.script({'team/app': ['TOP_SECRET\x1b[31m backend failure'],
                     'team/healthy': [[[self.issue(3)]]]})
        self.wait_until(process, lambda: len(self.alerts()) == 2)
        code, _, errors = self.stop(process)
        # Assert: repeated failure after success is a fresh alert episode.
        self.assertEqual(code, 130, errors)
        self.assertEqual([m['id'] for m in self._messages()],
                         ['github:team/healthy#3', 'github:team/app#2'])
        self.assertTrue(all(a['scope'] == 'source' and a['retry'] == 'next_poll'
                            and a['source'] == 'team/app' for a in self.alerts()))
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        self.assertIn('TOP_SECRET', errors)
        self.assertIn('polling', self.alerts()[0]['summary'])
        self.assertIn('next poll', self.alerts()[0]['recovery'])
        self.assertIn('user', self.alerts()[0]['recovery'])

    def test_changed_source_diagnostics_remain_local_while_alert_is_suppressed(self):
        # Arrange: two causes belong to the same agent-facing source failure episode.
        unavailable = 'TOP_SECRET HTTP 503 controlled outage'
        denied = 'TOP_SECRET HTTP 401 controlled authentication failure'
        self.script({'team/app': [unavailable]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 3 and len(self.alerts()) == 1)
        # Act: change only the local cause, then recover and recur with the original cause.
        self.script({'team/app': [denied]})
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertIsNone(process.poll())
        self.assertEqual(len(self.alerts()), 1)
        self.script({'team/app': [[[]]]})
        self.wait_until(process, lambda: self.polls() >= 3)
        self.script({'team/app': [unavailable]})
        self.wait_until(process, lambda: self.polls() >= 3 and len(self.alerts()) == 2)
        code, _, errors = self.stop(process)
        # Assert: changed causes reach the operator once, but never enter an agent message.
        self.assertEqual(code, 130, errors)
        self.assertEqual(errors.count(unavailable), 2, errors)
        self.assertEqual(errors.count(denied), 1, errors)
        self.assertEqual(self.alerts()[0], self.alerts()[1])
        self.assertEqual(self._messages(), [])
        messages = [event['text'] for event in self.events() if event['kind'] == 'send']
        for marker in ('TOP_SECRET', 'HTTP 503', 'HTTP 401'):
            self.assertNotIn(marker, json.dumps(messages))

    def assert_shared_read_pause(self, **fault):
        # Arrange: service access or a complete inventory cannot be established.
        self.seed((1,))
        before = self.planning_call('get_task', task_id=1)
        log = self.workspace / 'native-calls.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.fault(**fault)
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        tool = fault.get('fail', fault.get('incomplete'))
        self.wait_until(process, lambda: sum(
            json.loads(line)['args'][:2] == ['call', tool]
            for line in log.read_text().splitlines()) >= 3)
        # Assert: complete inventory is required before using any returned entries.
        self.assertIsNone(process.poll())
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertFalse(any(json.loads(line)['args'][:2] in (
            ['call', 'create_plan'], ['call', 'create_task'], ['call', 'update_plan'])
            for line in log.read_text().splitlines()))
        # Act: service repair needs no watcher restart.
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.planning_call('get_task', task_id=1), before)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_planning_access_pause_can_alert_after_foreman_launch_and_recover(self):
        self.assert_shared_read_pause(fail='get_project')

    def test_inventory_read_failure_pauses_and_read_only_repair_restores_saved_work(self):
        self.assert_shared_read_pause(fail='list_plans')

    def test_partial_inventory_is_not_used_as_a_complete_inventory(self):
        self.assert_shared_read_pause(incomplete='list_plans')

    def test_uncertain_create_alerts_stays_alive_and_never_replays_in_this_watch(self):
        # Arrange: no ownership is returned after a task create with unknown outcome.
        self.env['PLANNING_UNCERTAIN_CREATE'] = 'create_task'
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: self.polls() >= 4)
        code, _, errors = self.stop(process)
        # Assert: no repeating create and no automatic replacement or task state changes.
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.alerts()[0]['code'], 'ownership_create_uncertain')
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertIn('manual', self.alerts()[0]['recovery'].lower())
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)
        self.assertEqual(len(state['plans']), 1)
        self.assertTrue(json.loads(state['plans'][0]['context'])['ownership_create_started'])

    def test_unknown_operational_write_pauses_all_processing_until_manual_reconciliation(self):
        # Arrange: saving create intent can have an uncertain outcome too.
        self.fault(fail='update_plan')
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.assertIsNone(process.poll())
        self.fault()
        # Act: a repaired service does not authorize replay of an uncertain write.
        log = self.workspace / '.factory/fixture-plans.json'
        before = log.read_bytes()
        self.wait_until(process, lambda: self.polls() >= 4)
        code, _, errors = self.stop(process)
        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertEqual(log.read_bytes(), before)
        self.assertEqual(self._messages(), [])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_uncertain_plan_create_is_alerted_without_repeating_create(self):
        self.env['PLANNING_UNCERTAIN_CREATE'] = 'create_plan'
        self.script({'team/app': [[[self.issue()]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: self.polls() >= 4)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.alerts()[0]['code'], 'plan_create_uncertain')
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertNotIn('plan_id', self.alerts()[0], 'Unknown identities must be omitted')
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(state['plans'], [])
        self.assertEqual(state['tasks'], [])

    def test_missing_plan_read_pauses_without_recreation_and_safe_read_repair_recovers(self):
        original, = self.seed((1,))
        self.fault(fail='get_plan')
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: self.alerts()[0]['retry'] == 'read_only')
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['code'], 'recovery_read_failed')
        self.assertIsNone(process.poll())
        self.assertEqual(self._messages(), [])
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.stop(process)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)

    def test_malformed_ownership_pins_original_task_even_if_a_replacement_is_returned(self):
        original, healthy = self.seed()
        task = self.planning_call('get_task', task_id=1)
        self.planning_call('update_task', task_id=1, description='malformed ownership')
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.assertEqual(self._messages()[0]['plan_id'], healthy['plan_id'])
        self.assertEqual(self.alerts()[0]['ownership_task_id'], original['ownership_task_id'])
        # Act: a new valid record is not the saved ownership identity.
        replacement = self.planning_call('create_task', plan_id=1, title='Feature ownership',
                                         description=task['description'])
        self.fault(responses={'query_tasks': {'tasks': [replacement], 'total_count': 1}})
        self.wait_until(process, lambda: any(a['code'] == 'ownership_identity_changed'
                                            for a in self.alerts()))
        self.assertEqual(len(self._messages()), 1)
        self.stop(process)

    def test_completed_blocked_plan_clears_without_dispatch_even_with_open_issue_updates(self):
        original, = self.seed((1,))
        target = Path(original['worktrees'][0]['path'])
        saved = target.with_name('saved-work')
        target.rename(saved)
        self.script({'team/app': [[[self.issue(1, updated_at='same-revision')]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.planning_call('update_plan', plan_id=1, status='completed')
        saved.rename(target)
        self.wait_until(process, lambda: self.polls() >= 4)
        self.script({'team/app': [[[self.issue(1, updated_at='new-revision')]]]})
        self.wait_until(process, lambda: self.polls() >= 3)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.planning_call('get_plan', plan_id=1)['status'], 'completed')

    def test_invalid_recovery_snapshot_is_isolated_and_repairs_without_issue_edit(self):
        original, healthy = self.seed()
        plan = self.planning_call('get_plan', plan_id=1)
        context = json.loads(plan['context'])
        del context['issue']
        self.planning_call('update_plan', plan_id=1, context=json.dumps(context))
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.assertEqual(self.alerts()[0]['code'], 'plan_recovery_invalid')
        self.assertEqual(self._messages()[0]['plan_id'], healthy['plan_id'])
        self.planning_call('update_plan', plan_id=1, context=plan['context'])
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.stop(process)
        self.assertEqual(self._messages()[-1]['plan_id'], original['plan_id'])

    def test_pending_cleanup_does_not_classify_an_unknown_git_read_as_plan_local_safety(self):
        original, = self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        record = json.loads(task['description'])
        record['worktrees'][0]['cleanup'] = {
            'state': 'pending', 'pull_request_url': 'https://github.com/team/app/pull/3',
            'merge_commit': '1' * 40}
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        # Arrange: external Git read fails operationally, without a known safety mismatch.
        git = self.bin / 'git'
        marker = self.workspace / 'recorded-git-read-failed'
        git.write_text('#!/usr/bin/python3\nimport os, sys\n'
                       'from pathlib import Path\n'
                       'if "--git-common-dir" in sys.argv:\n'
                       f'    Path({str(marker)!r}).write_text("recorded common-dir read")\n'
                       '    sys.exit("TOP_SECRET unknown Git failure")\n'
                       'os.execv("/usr/bin/git", ["git", *sys.argv[1:]])\n')
        git.chmod(0o755)
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(marker.read_text(), 'recorded common-dir read')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        git.unlink()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['worktrees'], record['worktrees'])
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertIn('TOP_SECRET', errors)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_cleanup_canonical_repair_changed_problem_and_recurrence(self):
        original, = self.seed((1,))
        mapping = original['worktrees'][0]
        subprocess.run(['git', '-C', str(self.workspace), 'worktree', 'remove', mapping['path']],
                       check=True)
        self.script({'team/app': [[[self.issue(1, updated_at='same-revision')]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        task = self.planning_call('get_task', task_id=1)
        record = json.loads(task['description'])
        cleanup = {'state': 'removed', 'pull_request_url': 'https://GitHub.com/team/app/pull/3',
                   'merge_commit': subprocess.check_output(
                       ['git', '-C', str(self.workspace), 'rev-parse', 'HEAD'], text=True).strip()}
        record['worktrees'][0]['cleanup'] = cleanup
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.wait_until(process, lambda: len(self.alerts()) == 2)
        self.assertEqual(self.alerts()[-1]['code'], 'cleanup_invalid')
        cleanup['pull_request_url'] = 'https://github.com/team/app/pull/3'
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.wait_until(process, lambda: len(self._messages()) == 1)
        # Act: same defect after successful notification is a new episode.
        cleanup['pull_request_url'] = 'https://GitHub.com/team/app/pull/3'
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.script({'team/app': [[[self.issue(1, updated_at='revision-2')]]]})
        self.wait_until(process, lambda: len(self.alerts()) == 3)
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(len(self.alerts()), 3)
        cleanup['pull_request_url'] = 'https://github.com/team/app/pull/3'
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertFalse(Path(mapping['path']).exists())
        self.assertTrue(all(m['ownership_task_id'] == 1 for m in self._messages()))
        self.assertEqual(self._messages()[-1]['worktrees'], record['worktrees'])

    def assert_alert_delivery_is_fatal(self, mode):
        original, = self.seed((1,))
        target = Path(original['worktrees'][0]['path'])
        target.rename(target.with_name('saved-user-work'))
        self.env[mode] = '1'
        process = self.start('--existing')
        stdout, errors = process.communicate(timeout=15)
        self.assertEqual(process.returncode, 1, errors)
        self.assertIn('worktree mismatch', errors)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'send', 'close'])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self._messages(), [])
        self.assertFalse(target.exists())
        return errors

    def test_alert_send_failure_preserves_local_problem_and_original_fatal_delivery(self):
        errors = self.assert_alert_delivery_is_fatal('WATCH_SEND_FAIL')
        self.assertIn('delivery failed', errors)

    def test_alert_send_timeout_preserves_local_problem_without_retry(self):
        errors = self.assert_alert_delivery_is_fatal('WATCH_SEND_HANG')
        self.assertIn('timed out', errors)

    def test_alert_paths_are_json_escaped_and_external_content_is_excluded(self):
        original, = self.seed((1,))
        mapping = original['worktrees'][0]
        target = Path(mapping['path']).with_name('tree\n\x1b[31m"quoted')
        subprocess.run(['git', '-C', str(self.workspace), 'worktree', 'move',
                        mapping['path'], str(target)], check=True)
        task = self.planning_call('get_task', task_id=1)
        record = json.loads(task['description'])
        record['worktrees'][0]['path'] = str(target)
        record['secret'] = 'TOP_SECRET ownership prose'
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        target.rename(target.with_name('saved-work'))
        self.script({'team/app': [[[self.issue(body='TOP_SECRET issue prose')]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.stop(process)
        text = next(e['text'] for e in self.events() if e['kind'] == 'send')
        self.assertNotIn('\x1b', text)
        self.assertNotIn('\n', text)
        self.assertNotIn('TOP_SECRET', text)
        self.assertIn(str(target), self.alerts()[0]['paths'])

    def test_blocked_plan_and_task_disappearance_never_fall_back_to_creation(self):
        original, = self.seed((1,))
        target = Path(original['worktrees'][0]['path'])
        saved = target.with_name('saved-work')
        target.rename(saved)
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        # Act: the service no longer returns the saved plan, then its saved ownership task.
        self.fault(responses={'list_plans': {'plans': [], 'total_count': 0}})
        self.wait_until(process, lambda: len(self.alerts()) == 2)
        saved.rename(target)
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self._messages(), [])
        self.fault(responses={'query_tasks': {'tasks': [], 'total_count': 0}})
        self.wait_until(process, lambda: len(self.alerts()) == 3)
        self.wait_until(process, lambda: self.polls() >= 5)
        self.assertEqual(self._messages(), [])
        # Act: only the original records allow read-only recovery.
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['ownership_task_id'], original['ownership_task_id'])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)

    def test_malformed_snapshot_field_is_a_plan_problem_and_does_not_exit_watcher(self):
        self.seed()
        plan = self.planning_call('get_plan', plan_id=1)
        context = json.loads(plan['context'])
        context['issue']['source']['reference'] = None
        self.planning_call('update_plan', plan_id=1, context=json.dumps(context))
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.assertEqual(self.alerts()[0]['code'], 'plan_recovery_invalid')
        self.assertEqual(self._messages()[0]['plan_id'], 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)

    def test_invalid_saved_plan_status_alerts_instead_of_silently_consuming_revision(self):
        original, healthy = self.seed()
        self.planning_call('update_plan', plan_id=1, status=None)
        self.script({'team/app': [[[self.issue(1, updated_at='same-revision')]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.assertEqual(self.alerts()[0]['code'], 'plan_status_invalid')
        self.assertEqual(self._messages()[0]['plan_id'], healthy['plan_id'])
        self.planning_call('update_plan', plan_id=1, status='active')
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[-1]['plan_id'], original['plan_id'])

    def test_malformed_plan_project_association_does_not_hide_saved_closed_work(self):
        self.seed()
        self.planning_call('update_plan', plan_id=1, project_id=None)
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self._messages(), [])
        self.planning_call('update_plan', plan_id=1, project_id=12)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual({m['plan_id'] for m in self._messages()}, {1, 2})

    def test_valid_project_id_mismatch_is_plan_local_and_other_plans_continue(self):
        self.seed()
        self.planning_call('update_plan', plan_id=1, project_id=13)
        self.script({'team/app': [[[self.issue(1, updated_at='same-revision')]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.assertEqual(self.alerts()[0]['scope'], 'plan')
        self.assertEqual(self.alerts()[0]['code'], 'plan_project_mismatch')
        self.assertEqual(self._messages()[0]['plan_id'], 2)
        self.planning_call('update_plan', plan_id=1, project_id=12)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[-1]['plan_id'], 1)

    def test_duplicate_ownership_alert_is_unchanged_between_intake_and_read_only_recheck(self):
        original, = self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        # Keep this out of startup recovery so the first failure is ordinary intake.
        self.planning_call('update_plan', plan_id=1, status='completed')
        self.planning_call('create_task', plan_id=1, title='Feature ownership',
                           description=task['description'])
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.planning_call('update_plan', plan_id=1, status='active')
        self.script({'team/app': [[[self.issue(1, updated_at='revision-2')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.wait_until(process, lambda: self.polls() >= 4)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.alerts()[0]['code'], 'ownership_ambiguous')
        self.assertEqual(self.alerts()[0]['plan_id'], original['plan_id'])

    def test_intake_invalid_full_plan_pauses_read_only_before_any_mutation(self):
        self.seed((1,))
        plan = self.planning_call('update_plan', plan_id=1, status='completed')
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.planning_call('update_plan', plan_id=1, status='active')
        self.fault(responses={'get_plan': dict(plan, id=999, status='active')})
        self.script({'team/app': [[[self.issue(1, updated_at='revision-2')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['code'], 'recovery_read_failed')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self.alerts()[0]['plan_id'], 1)
        self.assertEqual(self._messages(), [])
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertFalse(any(c[0] in ('create_task', 'update_plan') and c[1]['plan_id'] == 999
                             for c in state['calls']))

    def test_alert_prefix_matches_foreman_guidance_and_identifies_external_problem_data(self):
        original, = self.seed((1,))
        target = Path(original['worktrees'][0]['path'])
        target.rename(target.with_name('saved-work'))
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.stop(process)
        sent = next(e['text'] for e in self.events() if e['kind'] == 'send')
        self.assertTrue(sent.startswith('Factory watcher alert. External problem data: '), sent)

    def assert_invalid_full_record_pauses(self, tool, response):
        # Arrange: only the external reply is corrupted; saved records remain unchanged.
        before = self.planning_call('get_task', task_id=1)
        log = self.workspace / 'record-reads.jsonl'
        log.unlink(missing_ok=True)
        self.env['PROFILE_LOG'] = str(log)
        self.fault(responses={tool: response})
        self.script({'team/app': [[[]]]})
        # Act: no open issue is needed to keep saved work pending.
        process = self.start('--new-only')
        try:
            self.wait_until(process, lambda: bool(self.alerts()))
            self.wait_until(process, lambda: sum(
                json.loads(line)['args'][:2] == ['call', tool]
                for line in log.read_text().splitlines()) >= 3)
            # Assert: malformed identities cannot enter a work notification or alert.
            self.assertIsNone(process.poll())
            self.assertEqual(self._messages(), [])
            self.assertEqual(len(self.alerts()), 1)
            self.assertEqual(self.alerts()[0]['scope'], 'factory')
            self.assertEqual(self.alerts()[0]['retry'], 'read_only')
            self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
            self.fault()
            self.wait_until(process, lambda: len(self._messages()) == 1)
            code, _, errors = self.stop(process)
            self.assertEqual(code, 130, errors)
            self.assertNotIn('Traceback', errors)
            self.assertEqual(self._messages()[0]['ownership_task_id'], 1)
            self.assertIs(type(self._messages()[0]['ownership_task_id']), int)
            self.assertEqual(self.planning_call('get_task', task_id=1), before)
            state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
            self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)
        finally:
            self.fault()
            self.cleanup_process(process)
            self.terminal_log.unlink(missing_ok=True)

    def test_full_task_reply_must_match_the_requested_task_identity(self):
        self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        self.assert_invalid_full_record_pauses('get_task', dict(task, id=2))

    def test_full_task_reply_rejects_missing_or_malformed_id_and_plan_association(self):
        self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        for field in ('id', 'plan_id'):
            for value in (True, False, 0, -1, 1.0, 'TOP_SECRET invalid identifier', None, 2):
                with self.subTest(field=field, value=value):
                    self.assert_invalid_full_record_pauses('get_task', dict(task, **{field: value}))
            with self.subTest(field=field, missing=True):
                response = dict(task)
                del response[field]
                self.assert_invalid_full_record_pauses('get_task', response)

    def test_full_plan_reply_requires_exact_requested_positive_id_and_positive_project_id(self):
        self.seed((1,))
        plan = self.planning_call('get_plan', plan_id=1)
        for field in ('id', 'project_id'):
            values = [True, False, 0, -1, 1.0, 'TOP_SECRET invalid identifier', None]
            if field == 'id':
                values.append(2)
            for value in values:
                with self.subTest(field=field, value=value):
                    self.assert_invalid_full_record_pauses('get_plan', dict(plan, **{field: value}))
            with self.subTest(field=field, missing=True):
                response = dict(plan)
                del response[field]
                self.assert_invalid_full_record_pauses('get_plan', response)

    def test_full_plan_boolean_identity_cannot_prove_recovery(self):
        self.seed((1,))
        plan = self.planning_call('get_plan', plan_id=1)
        self.assert_invalid_full_record_pauses('get_plan', dict(plan, id=True))

    def test_duplicate_task_rows_cannot_hide_a_competing_ownership_record(self):
        # Arrange: count matches, but one duplicated implementation hides the second owner.
        self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        implementation = self.planning_call('create_task', plan_id=1, title='Implementation',
                                            description='Implementation details')
        competing = self.planning_call('create_task', plan_id=1, title='Feature ownership',
                                       description=task['description'])
        self.fault(responses={'query_tasks': {
            'tasks': [task, implementation, implementation], 'total_count': 3}})
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self._messages(), [])
        # Act: a complete valid inventory now reveals genuine competing owners.
        self.fault()
        self.wait_until(process, lambda: any(a['code'] == 'ownership_ambiguous'
                                            for a in self.alerts()))
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.planning_call('get_task', task_id=competing['id']), competing)
        self.assertEqual(self.planning_call('get_task', task_id=1), task)

    def test_false_inventory_count_is_not_a_complete_empty_plan_list(self):
        self.seed((1,))
        self.assert_invalid_full_record_pauses('list_plans', {'plans': [], 'total_count': False})

    def test_duplicate_plan_ids_are_not_a_complete_plan_inventory(self):
        self.seed((1,))
        plan = self.planning_call('get_plan', plan_id=1)
        self.assert_invalid_full_record_pauses('list_plans', {
            'plans': [plan, plan], 'total_count': 2})

    def test_plan_and_task_inventory_counts_and_row_ids_use_exact_integer_types(self):
        self.seed((1,))
        for tool, key in (('list_plans', 'plans'), ('query_tasks', 'tasks')):
            for count in (False, True, -1, 1.0, '1', None):
                with self.subTest(tool=tool, count=count):
                    rows = [] if count is False else [{'id': 1}]
                    self.assert_invalid_full_record_pauses(tool, {key: rows, 'total_count': count})
            for identity in (True, False, 0, -1, 1.0, 'TOP_SECRET row identifier', None, [], {}):
                with self.subTest(tool=tool, identity=identity):
                    self.assert_invalid_full_record_pauses(tool, {
                        key: [{'id': identity}], 'total_count': 1})
            with self.subTest(tool=tool, missing_id=True):
                self.assert_invalid_full_record_pauses(tool, {key: [{}], 'total_count': 1})

    def test_unknown_nonempty_status_keeps_closed_new_only_plan_pending_until_repaired(self):
        original, = self.seed((1,))
        self.planning_call('update_plan', plan_id=1, status='actve')
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self.alerts()[0]['code'], 'plan_status_invalid')
        self.assertEqual(self._messages(), [])
        self.planning_call('update_plan', plan_id=1, status='active')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['ownership_task_id'], original['ownership_task_id'])

    def test_task_cancelled_status_cannot_clear_a_blocked_plan_or_consume_its_revision(self):
        original, = self.seed((1,))
        tree = Path(original['worktrees'][0]['path'])
        saved = tree.with_name('saved-user-work')
        tree.rename(saved)
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.planning_call('update_plan', plan_id=1, status='cancelled')
        self.wait_until(process, lambda: any(a['code'] == 'plan_status_invalid'
                                            for a in self.alerts()))
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self._messages(), [])
        saved.rename(tree)
        self.planning_call('update_plan', plan_id=1, status='active')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['revision'], 'same-revision')

    def test_worktree_parent_user_file_pauses_supervision_without_repeating_creation(self):
        # Arrange: initial preflight passes; a file appears after the last write-time Git read.
        parent = self.workspace / '.factory/worktrees'
        marker = self.workspace / 'late-parent-conflict'
        git = self.bin / 'git'
        git.write_text('#!/usr/bin/python3\nimport json, subprocess, sys\n'
                       'from pathlib import Path\n'
                       f'state = Path({str(self.workspace / ".factory/fixture-plans.json")!r})\n'
                       f'parent = Path({str(parent)!r})\nmarker = Path({str(marker)!r})\n'
                       'args = sys.argv[1:]\n'
                       'result = subprocess.run(["/usr/bin/git", *args], capture_output=True)\n'
                       'if (args[2:3] == ["for-each-ref"] and state.exists()\n'
                       '        and json.loads(state.read_text())["plans"]\n'
                       '        and not marker.exists()):\n'
                       '    parent.write_text("TOP_SECRET existing user file")\n'
                       '    marker.touch()\n'
                       'sys.stdout.buffer.write(result.stdout)\n'
                       'sys.stderr.buffer.write(result.stderr)\nsys.exit(result.returncode)\n')
        git.chmod(0o755)
        registry = subprocess.check_output(
            ['git', '-C', str(self.workspace), 'worktree', 'list', '--porcelain'], text=True)
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertTrue(marker.exists(), 'Fault must be injected after the plan/write-time read')
        self.assertEqual(self._messages(), [])
        self.assertEqual(parent.read_text(), 'TOP_SECRET existing user file')
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        state = self.workspace / '.factory/fixture-plans.json'
        before = state.read_bytes()
        # Act: repairing the path does not authorize replay of the creation path.
        parent.rename(parent.with_name('saved-parent-file'))
        target = self.polls() + 3
        self.wait_until(process, lambda: self.polls() >= target)
        self.assertIsNone(process.poll())
        self.assertEqual(state.read_bytes(), before)
        self.assertEqual(self._messages(), [])
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)
        self.assertEqual(subprocess.check_output(
            ['git', '-C', str(self.workspace), 'worktree', 'list', '--porcelain'], text=True),
            registry)
        calls = json.loads(before)['calls']
        self.assertEqual(sum(c[0] == 'create_plan' for c in calls), 1)
        self.assertFalse(any(c[0] == 'create_task' for c in calls))

    def test_removed_worktree_path_io_failure_pauses_read_only_and_repairs_without_restart(self):
        # Arrange: this valid-shaped path causes a real ENAMETOOLONG filesystem read error.
        original, = self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        record = json.loads(task['description'])
        mapping = record['worktrees'][0]
        mapping['path'] = str(Path(mapping['path']).with_name('TOP_SECRET-' + 'x' * 300))
        mapping['cleanup'] = {'state': 'removed',
                              'pull_request_url': 'https://github.com/team/app/pull/3',
                              'merge_commit': '1' * 40}
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.assertIsNone(process.poll())
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self._messages(), [])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        self.assertEqual(self.planning_call('get_task', task_id=1)['description'],
                         json.dumps(record))
        self.planning_call('update_task', task_id=1, description=task['description'])
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)
        self.assertIn('TOP_SECRET', errors)
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['worktrees'], original['worktrees'])

    def test_complete_missing_plan_lookup_isolates_absence_even_when_detail_read_would_fail(self):
        # Arrange: lookup proves this known plan absent; its detail endpoint also fails.
        original, healthy = self.seed()
        task = self.planning_call('update_task', task_id=1, state='doing',
                                  assigned_agent='busy-native-owner', version=4)
        state_path = self.workspace / '.factory/fixture-plans.json'
        before = json.loads(state_path.read_text())
        self.fault(fail='get_plan', fail_arguments={'plan_id': 1}, response_cases=[{
            'tool': 'list_plans', 'arguments': {'external_ref': 'github:team/app#1'},
            'result': {'plans': [], 'total_count': 0}}])
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1 and len(self._messages()) == 1)
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self.alerts()[0]['scope'], 'plan')
        self.assertEqual(self.alerts()[0]['code'], 'plan_identity_changed')
        self.assertEqual(self._messages()[0]['plan_id'], healthy['plan_id'])
        current = json.loads(state_path.read_text())
        self.assertEqual(sum(c == ['get_plan', {'plan_id': 1}] for c in current['calls']),
                         sum(c == ['get_plan', {'plan_id': 1}] for c in before['calls']))
        self.assertEqual(current['plans'], before['plans'])
        self.assertEqual(current['tasks'], before['tasks'])
        # Act: restoring the original record requires no issue edit or creation.
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 2)
        target = self.polls() + 2
        self.wait_until(process, lambda: self.polls() >= target)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(len(self._messages()), 2)
        self.assertEqual(self._messages()[-1]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[-1]['ownership_task_id'], original['ownership_task_id'])
        self.assertEqual(self.planning_call('get_task', task_id=1), task)
        current = json.loads(state_path.read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in current['calls']), 2)
        self.assertEqual(sum(c[0] == 'create_task' for c in current['calls']), 2)

    def test_archived_plan_is_finished_for_closed_recovery_and_ordinary_intake(self):
        self.seed((1,))
        self.planning_call('update_plan', plan_id=1, status='archived')
        self.script({'team/app': [[[]], [[self.issue(1, updated_at='same-revision')]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertEqual(self.alerts(), [])
        self.assertEqual(self._messages(), [])
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self.planning_call('get_plan', plan_id=1)['status'], 'archived')

    def test_intake_invalid_full_task_rechecks_known_plan_without_repeating_writes(self):
        self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        self.planning_call('update_plan', plan_id=1, status='completed')
        self.script({'team/app': [[[]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.planning_call('update_plan', plan_id=1, status='active')
        self.fault(responses={'get_task': dict(task, id='TOP_SECRET invalid task')})
        self.script({'team/app': [[[self.issue(1, updated_at='revision-2')]]]})
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self._messages(), [])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['ownership_task_id'], 1)
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)
        self.assertEqual(self.planning_call('get_task', task_id=1), task)

    def test_missing_tree_explains_cause_and_user_discussion_without_updated_skill(self):
        # Arrange: an existing workspace retains its old, user-edited Foreman guidance.
        original, = self.seed((1,))
        skill = self.workspace / '.factory/agents/foreman/skills/foreman/SKILL.md'
        skill.write_text('---\nname: foreman\ndescription: Existing guidance.\n---\n'
                         'Preserve my existing setup.\n')
        subprocess.run(['git', '-C', str(self.workspace), 'worktree', 'remove',
                        original['worktrees'][0]['path']], check=True)
        self.script({'team/app': [[[]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self.alerts()) == 1)
        code, _, errors = self.stop(process)
        # Assert: this message must explain itself even without an upgraded skill.
        self.assertEqual(code, 130, errors)
        alert = self.alerts()[0]
        self.assertIn('worktree', alert['summary'].lower())
        self.assertIn('missing', alert['summary'].lower())
        self.assertIn('user', alert['recovery'].lower())
        self.assertIn('Git', alert['recovery'])
        self.assertIn('PR', alert['recovery'])
        self.assertIn('Preserve my existing setup.', skill.read_text())

    def test_intake_shared_read_pause_prevents_writes_in_later_sources(self):
        # Arrange: force ordinary intake, with another source waiting to create new work.
        self.seed((1,))
        task = self.planning_call('get_task', task_id=1)
        self.planning_call('update_plan', plan_id=1, status='completed')
        self.configure(sources=('team/app', 'team/healthy'))
        self.script({'team/app': [[[]]], 'team/healthy': [[[]]]})
        log = self.workspace / 'native-calls.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        process = self.start('--existing')
        self.wait_until(process, lambda: json.loads(self.state_path.read_text())
                        .get('counts', {}).get('team/healthy', 0) >= 1)
        self.planning_call('update_plan', plan_id=1, status='active')
        self.fault(responses={'get_task': dict(task, id='invalid full task')})
        self.script({'team/app': [[[self.issue(1, updated_at='changed')]]],
                     'team/healthy': [[[self.issue(2)]]]})
        # Act: wait through failed read/recheck calls rather than timing the source loop.
        self.wait_until(process, lambda: len(self.alerts()) >= 1)
        self.wait_until(process, lambda: sum(
            json.loads(line)['args'][:2] == ['call', 'get_task']
            for line in log.read_text().splitlines()) >= 3)
        # Assert: a shared pause covers later sources in this same poll, not just the next one.
        self.assertIsNone(process.poll())
        self.assertEqual(self.alerts()[0]['scope'], 'factory')
        self.assertEqual(self.planning_call('list_plans')['total_count'], 1)
        self.assertEqual(self._messages(), [])
        # Act: a corrected read permits both sources to continue with normal notifications.
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual([m['id'] for m in self._messages()],
                         ['github:team/app#1', 'github:team/healthy#2'])
