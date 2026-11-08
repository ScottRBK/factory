"""Public watch retains unfinished verification without interpreting the Markdown agreement."""
import json

from test_planning_watch import PlanningWatchFixture


class AgreementRecoveryTests(PlanningWatchFixture):
    def test_closed_issue_restart_retains_required_verification_and_handoff_evidence(self):
        # Arrange: intake uses real temporary Git, external provider/Forgetful and native CLI.
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        original, = self._messages()
        verification = self.planning_call(
            'create_task', plan_id=original['plan_id'], title='Verify staging deployment',
            description='Required: actual merged revision. Missing deployment evidence; keep open.')
        # External service fixture represents an owner that has returned a merge handoff.
        state_path = self.workspace / '.factory/fixture-plans.json'
        state = json.loads(state_path.read_text())
        plan, = state['plans']
        plan['status'] = 'active'
        owner = next(t for t in state['tasks'] if t['id'] == original['ownership_task_id'])
        owner.update(state='doing', assigned_agent='returned-native-owner')
        details = json.loads(owner['description'])
        details['handoff'] = 'Merged PR https://github.com/team/app/pull/9; awaiting deployment.'
        details['shared_requirements'] = 'Deployment required; deployed E2E not required.'
        owner['description'] = json.dumps(details)
        next(t for t in state['tasks'] if t['id'] == verification['id'])['state'] = 'waiting'
        state_path.write_text(json.dumps(state))
        agreement = self.workspace / '.factory/definition_of_done.md'
        agreement.write_text('# Delivery\n\nMerge and deploy; deployed E2E is not required.\n')
        saved = agreement.read_bytes()
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        # Act: closure/new-only must not hide unfinished work, or create replacement resources.
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: bool(self._messages() or self.alerts()))
        baseline = self.polls()
        self.wait_until(restarted, lambda: self.polls() >= baseline + 2)
        code, _, errors = self.stop(restarted)
        # Assert: notification submission is not proof that a model followed the DoD.
        self.assertEqual(code, 130, errors)
        recovered, = self._messages()
        self.assertTrue(recovered['recovered'])
        for key in ('plan_id', 'ownership_task_id', 'worktrees'):
            self.assertEqual(recovered[key], original[key])
        actual_owner = self.planning_call('get_task', task_id=owner['id'])
        self.assertEqual(actual_owner, owner)
        actual_check = self.planning_call('get_task', task_id=verification['id'])
        self.assertEqual(actual_check['state'], 'waiting')
        actual_plan = self.planning_call('get_plan', plan_id=plan['id'])
        self.assertEqual(actual_plan['status'], 'active')
        self.assertEqual(agreement.read_bytes(), saved)
        final = json.loads(state_path.read_text())
        self.assertEqual(sum(tool == 'create_plan' for tool, _ in final['calls']), 1)
        self.assertEqual(sum(tool == 'create_task' for tool, _ in final['calls']), 2)
        self.assertFalse(self.alerts())
