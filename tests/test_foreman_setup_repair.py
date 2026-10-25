"""Approved native repair observed through the watch CLI; no model compliance claim."""
import json
import subprocess

from test_planning_watch import PlanningWatchFixture


class ForemanSetupRepairTests(PlanningWatchFixture):
    def setUp(self):
        super().setUp()
        self.control = self.workspace / 'planning-control.json'
        self.control.write_text('{}')
        self.env['PROFILE_PLANNING_CONTROL'] = str(self.control)

    def fault(self, **control):
        replacement = self.control.with_suffix('.next')
        replacement.write_text(json.dumps(control))
        replacement.replace(self.control)

    def polls(self):
        return json.loads(self.state_path.read_text()).get('counts', {}).get('team/app', 0)

    def native_owner(self, plan_id, *, number=1, mappings=None):
        # The test acts as the user-approved native repair, never as watcher authorization.
        plan = self.planning_call('get_plan', plan_id=plan_id)
        if mappings is None:
            path = self.workspace / f'.factory/worktrees/team-app-{number}'
            branch = f'factory/team-app-{number}'
            subprocess.run(['git', '-C', str(self.workspace), 'worktree', 'add', '-b',
                            branch, str(path), 'HEAD'], check=True, capture_output=True)
            mappings = [dict(repository='team/app', local_dir=str(self.workspace),
                             branch=branch, path=str(path))]
        return self.planning_call('create_task', plan_id=plan_id, title='Feature ownership',
                                  description=json.dumps(dict(
                                      kind='factory-ownership', workspace=str(self.workspace),
                                      external_ref=plan['external_ref'], worktrees=mappings)))

    def native_plan(self, number=1):
        issue = dict(source=dict(provider='github', reference='team/app'), number=number,
                     title='Interrupted setup', url=f'https://github.com/team/app/issues/{number}',
                     body='Requirements', revision='unchanged', epic=False)
        return self.planning_call('create_plan', title=issue['title'], project_id=12,
                                  external_ref=f'github:team/app#{number}', source_url=issue['url'],
                                  context=json.dumps(dict(workspace=str(self.workspace),
                                                          issue=issue)))

    def assert_approved_repair_guidance(self, alert):
        self.assertEqual(alert['code'], 'setup_incomplete')
        self.assertEqual(alert['scope'], 'plan')
        self.assertEqual(alert['retry'], 'user_approved_repair')
        for text in ('user', 'approval', 'get_plan', 'query_tasks', 'get_task', 'create_task',
                     'prior', 'Git', 'PR', 'factory-ownership', 'workspace', 'external_ref',
                     'worktrees', 'repository', 'local_dir', 'branch', 'path',
                     'no ownership task was previously established',
                     'Never replace a previously established ownership task'):
            self.assertIn(text, alert['recovery'])

    def test_path_conflict_needs_approved_native_completion_even_after_path_is_clear(self):
        # Arrange: setup was already saved; recovery must preserve this user directory.
        saved_plan = self.native_plan()
        target = self.workspace / '.factory/worktrees/team-app-1'
        target.mkdir(parents=True)
        (target / 'user.txt').write_text('TOP_SECRET preserve user data')
        skill = self.workspace / '.factory/agents/foreman/skills/foreman/SKILL.md'
        skill.write_text('---\nname: foreman\ndescription: Old user guidance.\n---\n'
                         'Keep my edits.\n')
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()) and bool(self._messages()))
        self.assert_approved_repair_guidance(self.alerts()[0])
        plan_id = self.alerts()[0]['plan_id']
        self.assertEqual(plan_id, saved_plan['id'])
        plan = self.planning_call('get_plan', plan_id=plan_id)
        # Act: clearing the conflict and closing the issue do not authorize watcher creation.
        saved = target.with_name('saved-user-work')
        target.rename(saved)
        self.script({'team/app': [[[]]]})
        self.wait_until(process, lambda: self.polls() >= 4)
        self.assertEqual(len(self.alerts()), 1, 'The same incomplete setup is one alert episode')
        self.assertFalse(target.exists())
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        self.assertEqual(len(self._messages()), 1)
        # Act: the user approves native completion of this exact existing plan.
        owner = self.native_owner(plan_id)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        # Assert: read-only observation uses the original plan and first established owner ID.
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[-1]['plan_id'], plan_id)
        self.assertEqual(self._messages()[-1]['ownership_task_id'], owner['id'])
        self.assertEqual(self.planning_call('get_plan', plan_id=plan_id), plan)
        self.assertEqual((saved / 'user.txt').read_text(), 'TOP_SECRET preserve user data')
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        self.assertIn('Keep my edits.', skill.read_text())
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 2)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 2)

    def test_first_approved_owner_is_pinned_before_mapping_validation_and_survives_restart(self):
        # Arrange: a persisted incomplete plan has never established an ownership identity.
        self.native_plan()
        target = self.workspace / '.factory/worktrees/team-app-1'
        target.mkdir(parents=True)
        self.script({'team/app': [[[self.issue(1)]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: bool(self.alerts()))
        plan_id = self.alerts()[0]['plan_id']
        self.stop(first)
        target.rmdir()
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assert_approved_repair_guidance(self.alerts()[0])
        self.wait_until(process, lambda: self.polls() >= 3)
        self.assertFalse(target.exists())
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        # Act: user-approved native repair establishes an ID before its mapping is corrected.
        bad_mapping = dict(repository='team/app', local_dir=str(self.workspace),
                           branch='factory/team-app-1', path='relative-invalid-path')
        owner = self.native_owner(plan_id, mappings=[bad_mapping])
        self.wait_until(process, lambda: any(a['code'] == 'mapping_invalid' for a in self.alerts()))
        self.assertEqual(self.alerts()[-1].get('ownership_task_id'), owner['id'])
        replacement = self.native_owner(plan_id, mappings=[])
        self.fault(responses={'query_tasks': {'tasks': [replacement], 'total_count': 1}})
        self.wait_until(process, lambda: self.alerts()[-1]['code'] == 'ownership_identity_changed')
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.alerts()[-1].get('ownership_task_id'), owner['id'])
        # Act: repair only the original owner's mapping; never adopt the replacement.
        subprocess.run(['git', '-C', str(self.workspace), 'worktree', 'add', '-b',
                        bad_mapping['branch'], str(target), 'HEAD'],
                       check=True, capture_output=True)
        record = json.loads(owner['description'])
        record['worktrees'][0]['path'] = str(target)
        owner = self.planning_call('update_task', task_id=owner['id'],
                                   description=json.dumps(record))
        self.fault(responses={'query_tasks': {'tasks': [owner], 'total_count': 1}})
        self.wait_until(process, lambda: len(self._messages()) == 1)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])

    def test_first_lookup_read_retries_without_identity_and_keeps_new_only_pending_revisions(self):
        # Arrange: both sources establish empty first-success baselines.
        self.configure(sources=('team/app', 'team/healthy'))
        self.script({'team/app': [[[]]], 'team/healthy': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: json.loads(self.state_path.read_text())
                        .get('counts', {}).get('team/healthy', 0) >= 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1, updated_at='pending')]]],
                     'team/healthy': [[[self.issue(3, updated_at='healthy')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertNotIn('plan_id', self.alerts()[0])
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.planning_call('list_plans')['plans'], [])
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(len(self.alerts()), 1, 'Unchanged read failure is one alert episode')
        # Act: service repair permits fresh intake; it must not consume the pending revision.
        self.script({'team/app': [[[self.issue(1, updated_at='new-revision'),
                                    self.issue(2, updated_at='new2')]]],
                     'team/healthy': [[[self.issue(3, updated_at='healthy')]]]})
        self.fault()
        self.wait_until(process, lambda: {m['id'] for m in self._messages()} == {
            'github:team/app#1', 'github:team/app#2', 'github:team/healthy#3'}
            and any(m['id'] == 'github:team/app#1' and m['revision'] == 'new-revision'
                    for m in self._messages()))
        code, _, errors = self.stop(process)
        # Assert: no manual latch, fabricated ID, forgotten work or duplicate create.
        self.assertEqual(code, 130, errors)
        revisions = [(m['id'], m['revision']) for m in self._messages()]
        self.assertEqual(len(revisions), len(set(revisions)))
        self.assertIn(('github:team/app#1', 'new-revision'), revisions)
        self.assertIn(('github:team/app#2', 'new2'), revisions)
        self.assertIn(('github:team/healthy#3', 'healthy'), revisions)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 3)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 3)

    def assert_saved_plan_read_repair(self, **fault):
        # Arrange: the plan commits before a detail or ownership read fails.
        self.fault(**fault)
        self.script({'team/app': [[[self.issue(1, updated_at='unchanged'), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        plan_id = self.alerts()[0]['plan_id']
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(len(state['plans']), 1)
        self.assertEqual(state['tasks'], [])
        before = state['plans'][0]
        # Act: service repair alone permits read-only recovery, never completion of setup.
        self.fault()
        self.wait_until(process, lambda: any(a['code'] == 'setup_incomplete' for a in self.alerts())
                        and len(self._messages()) == 1)
        self.assert_approved_repair_guidance(self.alerts()[-1])
        self.assertEqual(self._messages()[0]['id'], 'github:team/app#2')
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        self.assertEqual(self.planning_call('get_plan', plan_id=plan_id), before)
        # Act: approved native completion remains observable after the issue closes.
        self.script({'team/app': [[[]]]})
        owner = self.native_owner(plan_id)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[-1]['plan_id'], plan_id)
        self.assertEqual(self._messages()[-1]['ownership_task_id'], owner['id'])
        self.assertEqual(self._messages()[-1]['revision'], 'unchanged')
        self.assertEqual(self.planning_call('get_plan', plan_id=plan_id), before)
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_saved_plan_malformed_detail_requires_approved_native_completion(self):
        self.assert_saved_plan_read_repair(responses={'get_plan': {'id': 999, 'project_id': 12}})

    def test_saved_plan_detail_transport_failure_is_read_only_and_repairable(self):
        self.assert_saved_plan_read_repair(fail='get_plan')

    def test_saved_plan_ownership_query_failure_is_read_only_and_repairable(self):
        self.assert_saved_plan_read_repair(fail='query_tasks')

    def test_existing_incomplete_plan_in_intake_is_never_automatically_completed(self):
        # Arrange: startup inventory finishes before a saved plan appears in issue intake.
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 1)
        plan = self.native_plan()
        self.script({'team/app': [[[self.issue(1, updated_at='unchanged')]]]})
        # Act
        self.wait_until(process, lambda: bool(self.alerts()) or bool(self._messages()))
        # Assert: an existing plan never re-enters first-time creation, even without a marker.
        self.assertEqual(self._messages(), [])
        self.assert_approved_repair_guidance(self.alerts()[0])
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan['id'])['tasks'], [])
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        self.native_owner(plan['id'])
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)

    def test_failed_lookup_can_pin_a_later_saved_plan_without_entering_creation(self):
        # Arrange: a pre-write lookup has no identity while service access is unavailable.
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1, updated_at='unchanged')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertNotIn('plan_id', self.alerts()[0])
        plan = self.native_plan()
        # Act: a saved identity is discovered after access recovers and the issue closes.
        self.script({'team/app': [[[]]]})
        self.fault()
        self.wait_until(process, lambda: any(a['code'] == 'setup_incomplete'
                                            for a in self.alerts()))
        self.assertEqual(self.alerts()[-1]['plan_id'], plan['id'])
        self.assertEqual(self._messages(), [])
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        self.native_owner(plan['id'])
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)

    def git_fault(self, command, *, after=False, after_plan=False):
        control = self.workspace / 'git-control.json'
        control.write_text(json.dumps(dict(command=command, after=after, after_plan=after_plan)))
        wrapper = self.bin / 'git'
        wrapper.write_text(
            '#!/usr/bin/python3\nimport json, os, subprocess, sys\nfrom pathlib import Path\n'
            f'control = json.loads(Path({str(control)!r}).read_text())\n'
            f'state_path = Path({str(self.workspace / ".factory/fixture-plans.json")!r})\n'
            'plans = json.loads(state_path.read_text())["plans"] if state_path.exists() else []\n'
            'args = sys.argv[1:]\npattern = control.get("command", [])\n'
            'if (pattern and args[2:2 + len(pattern)] == pattern\n'
            '        and (not control.get("after_plan") or plans)):\n'
            '    if control.get("after"):\n'
            '        subprocess.run(["/usr/bin/git", *args], check=True)\n'
            '    sys.exit("TOP_SECRET controlled Git operation failure")\n'
            'os.execv("/usr/bin/git", ["git", *args])\n')
        wrapper.chmod(0o755)
        return control

    def repair_git(self, control):
        replacement = control.with_suffix('.next')
        replacement.write_text('{}')
        replacement.replace(control)

    def test_pre_add_git_read_failure_needs_read_retry_then_approved_setup_completion(self):
        # Arrange: preflight passes, then the Git read fails after actual plan creation commits.
        control = self.git_fault(['remote', 'get-url', 'origin'], after_plan=True)
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        plan_id = self.alerts()[0]['plan_id']
        self.assertEqual(len(self.planning_call('list_plans')['plans']), 1)
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        # Act: repairing the read must not resume creation-capable prepare on the saved plan.
        self.repair_git(control)
        self.wait_until(process, lambda: any(a['code'] == 'setup_incomplete' for a in self.alerts())
                        and len(self._messages()) == 1)
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        owner = self.native_owner(plan_id)
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[-1]['ownership_task_id'], owner['id'])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_recorded_git_read_failure_pins_established_owner_before_a_replacement_appears(self):
        # Arrange: an established ownership candidate is read before native Git becomes unavailable.
        plan = self.native_plan()
        owner = self.native_owner(plan['id'])
        control = self.git_fault(['rev-parse', '--path-format=absolute', '--git-common-dir'])
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self.alerts()[0].get('ownership_task_id'), owner['id'])
        # Act: read repair cannot select a different task for that same plan.
        replacement = self.native_owner(plan['id'], mappings=[])
        self.fault(responses={'query_tasks': {'tasks': [replacement], 'total_count': 1}})
        self.repair_git(control)
        self.wait_until(process, lambda: any(a['code'] == 'ownership_identity_changed'
                                            for a in self.alerts()))
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.alerts()[-1]['ownership_task_id'], owner['id'])
        self.fault(responses={'query_tasks': {'tasks': [owner], 'total_count': 1}})
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])

    def test_post_task_write_read_failure_latches_until_deliberate_reconciled_restart(self):
        # Arrange: native task creation commits, then its readback becomes unavailable.
        command = self.bin / 'forgetful'
        original = command.read_text()
        point = "        if tool == 'list_plans':"
        self.assertEqual(original.count(point), 1)
        command.write_text(original.replace(point,
            "        if tool == 'query_tasks' and any(c[0] == 'create_task' "
            "for c in state['calls']):\n"
            "            save_planning_state()\n"
            "            sys.exit('TOP_SECRET post-task readback failure')\n" + point))
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertEqual(self.alerts()[0]['code'], 'ownership_create_uncertain')
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(len(state['tasks']), 1)
        plan, owner = state['plans'][0], state['tasks'][0]
        self.assertTrue(json.loads(plan['context'])['ownership_create_started'])
        # Act: service repair alone must not clear uncertainty or repeat a write.
        command.write_text(original)
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 4)
        self.assertEqual(self._messages(), [])
        self.assertEqual(len(self.alerts()), 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        # Act: after explicit native inspection/reconciliation, deliberately restart read-only.
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(restarted)[0], 130)
        self.assertEqual(self._messages()[0]['plan_id'], plan['id'])
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        self.assertEqual(self.planning_call('get_plan', plan_id=plan['id']), plan)
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)

    def test_uncertain_missing_first_owner_needs_approved_native_repair_and_restart(self):
        # Arrange: the create-intent commits, but task creation has an unknown failed outcome.
        self.fault(fail='create_task')
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        alert = self.alerts()[0]
        self.assertEqual(alert['retry'], 'manual_reconciliation')
        for text in ('user approval', 'query_tasks', 'get_task', 'create_task',
                     'factory-ownership', 'no ownership task was previously established',
                     'Never replace a previously established ownership task'):
            self.assertIn(text, alert['recovery'])
        plan_id = alert['plan_id']
        plan = self.planning_call('get_plan', plan_id=plan_id)
        self.assertTrue(json.loads(plan['context'])['ownership_create_started'])
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        # Act: inspect native state and complete the first owner only after simulated user approval.
        self.fault()
        mapping = dict(repository='team/app', local_dir=str(self.workspace),
                       branch='factory/team-app-1',
                       path=str(self.workspace / '.factory/worktrees/team-app-1'))
        owner = self.native_owner(plan_id, mappings=[mapping])
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 4)
        self.assertEqual(self._messages(), [], 'Uncertain writes cannot self-clear after repair')
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(restarted)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        self.assertEqual(self.planning_call('get_plan', plan_id=plan_id), plan)
        self.assertEqual(self.planning_call('get_task', task_id=owner['id']), owner)

    def assert_owner_detail_read_repair(self, malformed):
        # Arrange: a real existing owner is not changed by transport or invalid detail replies.
        plan = self.native_plan()
        owner = self.native_owner(plan['id'])
        if malformed:
            self.fault(responses={'get_task': dict(owner, id='TOP_SECRET invalid full identity')})
        else:
            self.fault(fail='get_task')
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'read_only')
        self.assertEqual(self.alerts()[0]['plan_id'], plan['id'])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))
        # Act/Assert: access correction restores the original owner without state mutation.
        self.fault()
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        self.assertEqual(self.planning_call('get_task', task_id=owner['id']), owner)

    def test_owner_detail_transport_failure_retries_read_only(self):
        self.assert_owner_detail_read_repair(malformed=False)

    def test_owner_detail_malformed_reply_retries_read_only(self):
        self.assert_owner_detail_read_repair(malformed=True)

    def test_unknown_plan_create_readback_never_retries_create_and_restart_stays_read_only(self):
        # Arrange: native plan creation commits but the first confirming lookup cannot be read.
        command = self.bin / 'forgetful'
        original = command.read_text()
        point = "        if tool == 'list_plans':"
        self.assertEqual(original.count(point), 1)
        command.write_text(original.replace(point,
            "        if tool == 'list_plans' and any(c[0] == 'create_plan' "
            "for c in state['calls']):\n"
            "            save_planning_state()\n"
            "            sys.exit('TOP_SECRET unknown plan readback')\n" + point))
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        self.assertNotIn('plan_id', self.alerts()[0])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        plan, = state['plans']
        # Act: repairing a read after an unknown write cannot authorize another create.
        command.write_text(original)
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 4)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: bool(self.alerts()))
        self.assert_approved_repair_guidance(self.alerts()[0])
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan['id'])['tasks'], [])
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        owner = self.native_owner(plan['id'])
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(restarted)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)

    def test_unknown_git_add_outcome_needs_native_inspection_approved_completion_and_restart(self):
        # Arrange: real Git creates the tree, but its external command reports failure afterwards.
        control = self.git_fault(['worktree', 'add'], after=True)
        self.script({'team/app': [[[self.issue(1)]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        plan_id = self.alerts()[0]['plan_id']
        target = self.workspace / '.factory/worktrees/team-app-1'
        self.assertTrue((target / '.git').exists(), 'Fault must follow the actual Git write')
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan_id)['tasks'], [])
        # Act: inspect the committed tree and approve native completion; watcher stays latched.
        self.repair_git(control)
        owner = self.native_owner(plan_id, mappings=[dict(repository='team/app',
            local_dir=str(self.workspace), branch='factory/team-app-1', path=str(target))])
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 4)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(restarted)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        self.assertNotIn('TOP_SECRET', json.dumps(self.alerts()))

    def test_submitted_identities_survive_updated_issue_lookup_failure_and_reject_replacement(self):
        # Arrange: an acknowledged notification already established both immutable identities.
        plan = self.native_plan()
        owner = self.native_owner(plan['id'])
        self.script({'team/app': [[[self.issue(1, updated_at='unchanged')]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.fault(fail='list_plans', fail_arguments={'external_ref': 'github:team/app#1'})
        self.script({'team/app': [[[self.issue(1, updated_at='changed')]]]})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0].get('plan_id'), plan['id'])
        self.assertEqual(self.alerts()[0].get('ownership_task_id'), owner['id'])
        # Act: read repair returns a replacement plan, not the previously submitted identity.
        replacement = self.native_plan()
        self.native_owner(replacement['id'], mappings=[])
        self.fault(responses={'list_plans': {'plans': [replacement], 'total_count': 1}})
        self.wait_until(process, lambda: any(a['code'] == 'plan_identity_changed'
                                            for a in self.alerts()))
        self.assertEqual(len(self._messages()), 1)
        self.assertEqual(self.alerts()[-1]['plan_id'], plan['id'])
        # Act/Assert: only the original plan/task can deliver the unchanged pending revision.
        self.fault(responses={'list_plans': {'plans': [plan], 'total_count': 1}})
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.assertEqual(self.stop(process)[0], 130)
        self.assertEqual(self._messages()[-1]['plan_id'], plan['id'])
        self.assertEqual(self._messages()[-1]['ownership_task_id'], owner['id'])
        self.assertEqual(self._messages()[-1]['revision'], 'changed')

    def test_cleared_intent_never_authorizes_completion_in_watch_or_after_restart(self):
        # Arrange: a saved create-intent with no known owner requires manual reconciliation.
        plan = self.native_plan()
        context = json.loads(plan['context'])
        context['ownership_create_started'] = True
        self.planning_call('update_plan', plan_id=plan['id'], context=json.dumps(context))
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(self.alerts()[0]['retry'], 'manual_reconciliation')
        # Act: hostile external marker clearing is a negative input, never the supported repair.
        context.pop('ownership_create_started')
        self.planning_call('update_plan', plan_id=plan['id'], context=json.dumps(context))
        observed = self.polls()
        self.wait_until(process, lambda: self.polls() >= observed + 3)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.stop(process)[0], 130)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: bool(self.alerts()))
        self.assert_approved_repair_guidance(self.alerts()[0])
        self.wait_until(restarted, lambda: self.polls() >= 3)
        self.assertFalse((self.workspace / '.factory/worktrees/team-app-1').exists())
        self.assertEqual(self.planning_call('query_tasks', plan_id=plan['id'])['tasks'], [])
        # Act/Assert: only approved native completion establishes the first owner.
        owner = self.native_owner(plan['id'])
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.assertEqual(self.stop(restarted)[0], 130)
        self.assertEqual(self._messages()[0]['ownership_task_id'], owner['id'])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'update_plan' for c in state['calls']), 2)

