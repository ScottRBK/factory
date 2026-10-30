import json
import subprocess
import time
from pathlib import Path

from test_watch import WatchFixture


class PlanningWatchFixture(WatchFixture):
    def planning_call(self, tool, **arguments):
        role = self.workspace / '.factory'
        result = subprocess.run(
            [str(self.bin / 'forgetful'), 'call', tool, '--args', json.dumps(arguments),
             '--json', '--server', 'https://memory.example/custom-endpoint'],
            cwd=role, env=self.env, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def _messages(self):
        return [json.loads(e['text'].split('External issue data: ', 1)[1])
                for e in self.events() if e['kind'] == 'send'
                and e['text'].startswith('Factory issue notification.')]

    def alerts(self):
        return [json.loads(e['text'].split('External problem data: ', 1)[1])
                for e in self.events() if e['kind'] == 'send'
                and e['text'].startswith('Factory watcher alert.')]

    def polls(self, source='team/app'):
        state = json.loads(self.state_path.read_text())
        return state.get('counts', {}).get(source, 0)

    def assert_paused(self, process, *, synchronize_poll=False):
        self.wait_until(process, lambda: bool(self.alerts()))
        if synchronize_poll:
            observed = self.polls()
            # Counts mark request entry. Two later entries prove one later cycle completed.
            self.wait_until(process, lambda: self.polls() >= observed + 2)
        else:
            time.sleep(0.2)
        self.assertIsNone(process.poll(), 'Safety failure terminated supervising watcher')
        self.assertEqual(self._messages(), [], 'Blocked work reached Foreman as ordinary work')
        self.assertEqual(len(self.alerts()), 1,
                         f'Unchanged failure sent repeated alerts: {self.alerts()}')
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        return errors


class PlanningWatchTests(PlanningWatchFixture):
    def test_long_issue_uses_placeholder_and_recovers_closed_work_with_stable_ids(self):
        # Arrange: escaped Unicode titles must also fit after the ownership-intent update.
        title = '🦕' * 240 + ' "habitat"\\\n'
        body = 'Full requirements: 🦕 "habitat"\\\n' * 200
        self.script({'team/app': [[[self.issue(title=title, body=body,
                                              updated_at='revision-long')]]]})
        # Act: public CLI intake, then restart with the issue absent from the open poll.
        first = self.start('--existing')
        self.wait_until(first, lambda: bool(self._messages() or self.alerts()))
        self.stop(first)
        # Assert: the external service enforces the real context limit, not a fixture bypass.
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(len(self._messages()), 1, state.get('rejections', self.alerts()))
        original = self._messages()[0]
        self.assertEqual(original['body'], body)
        plan = self.planning_call('get_plan', plan_id=original['plan_id'])
        context = json.loads(plan['context'])
        placeholder = (f'This is a placeholder description for github issue #1: {title}. '
                       'The feature owner will update it after reviewing the issue/plan.')
        self.assertEqual(context['issue']['body'], placeholder)
        self.assertEqual(context['workspace'], str(self.workspace))
        self.assertTrue(context['ownership_create_started'])
        self.assertEqual(context['issue']['source'],
                         {'provider': 'github', 'reference': 'team/app'})
        self.assertEqual(context['issue']['revision'], 'revision-long')
        self.assertEqual(plan['external_ref'], 'github:team/app#1')
        self.assertEqual(plan['source_url'], 'https://github.com/team/app/issues/1')
        writes = [args['context'] for tool, args in state['calls']
                  if tool in ('create_plan', 'update_plan') and 'context' in args]
        self.assertEqual(len(writes), 2)
        self.assertTrue(all(len(value) <= 2000 for value in writes))
        self.assertNotIn('rejections', state)
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: bool(self._messages() or self.alerts()))
        self.stop(restarted)
        recovered, = self._messages()
        self.assertTrue(recovered['recovered'])
        self.assertEqual(recovered['body'], placeholder)
        for key in ('plan_id', 'ownership_task_id', 'worktrees', 'revision', 'title'):
            self.assertEqual(recovered[key], original[key])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(tool == 'create_plan' for tool, _ in state['calls']), 1)
        self.assertEqual(sum(tool == 'create_task' for tool, _ in state['calls']), 1)

    def test_repointed_worktree_pauses_delivery_and_preserves_existing_work(self):
        self.assert_worktree_identity_checked('branch')

    def test_worktree_gitdir_is_checked_even_when_actual_branch_matches(self):
        self.assert_worktree_identity_checked('gitdir')

    def test_worktree_root_is_checked_even_when_branch_and_gitdir_match(self):
        self.assert_worktree_identity_checked('root')

    def assert_worktree_identity_checked(self, mismatch):
        # Arrange: registration is intact, but the target uses another HEAD/index or root.
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        mapping = self._messages()[0]['worktrees'][0]
        target = Path(mapping['path'])
        gitfile = target / '.git'
        if mismatch == 'root':
            subprocess.run(['git', '-C', str(self.workspace), 'config',
                            'extensions.worktreeConfig', 'true'], check=True)
            subprocess.run(['git', '-C', str(target), 'config', '--worktree',
                            'core.worktree', str(self.workspace)], check=True)
            actual_root = subprocess.check_output(
                ['git', '-C', str(target), 'rev-parse', '--show-toplevel'], text=True).strip()
            self.assertEqual(actual_root, str(self.workspace))
        else:
            gitfile.write_text(f'gitdir: {self.workspace / ".git"}\n')
            if mismatch == 'gitdir':
                subprocess.run(['git', '-C', str(self.workspace), 'symbolic-ref',
                                'HEAD', f'refs/heads/{mapping["branch"]}'], check=True)
        redirected = gitfile.read_text()
        work = target / 'unfinished.txt'
        work.write_text('Keep my work.\n')
        main_index = (self.workspace / '.git/index').read_bytes()
        registry = subprocess.check_output(
            ['git', '-C', str(self.workspace), 'worktree', 'list', '--porcelain'], text=True)
        self.assertIn(f'branch refs/heads/{mapping["branch"]}', registry)
        actual_branch = subprocess.check_output(
            ['git', '-C', str(target), 'branch', '--show-current'], text=True).strip()
        if mismatch == 'branch':
            self.assertNotEqual(actual_branch, mapping['branch'])
        else:
            self.assertEqual(actual_branch, mapping['branch'])
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted)
        # Assert
        self.assertEqual(self._messages(), [], 'Mismatched worktree reached the Foreman')
        self.assertIn('worktree mismatch', stderr)
        self.assertIn('reconcile', stderr)
        self.assertEqual(gitfile.read_text(), redirected)
        self.assertEqual(work.read_text(), 'Keep my work.\n')
        self.assertEqual((self.workspace / '.git/index').read_bytes(), main_index)
        self.assertEqual(subprocess.check_output(
            ['git', '-C', str(self.workspace), 'worktree', 'list', '--porcelain'], text=True),
            registry)

    def test_new_only_restart_delivers_changes_to_already_owned_issue(self):
        # Arrange
        self.script({'team/app': [[[self.issue(body='Original', updated_at='revision-1')]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        self.terminal_log.unlink()
        self.script({'team/app': [[[self.issue(body='Answer while offline',
                                              updated_at='revision-2')]]]})
        # Act
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 2)
        self.stop(restarted)
        # Assert
        self.assertEqual(self._messages()[-1]['body'], 'Answer while offline')
        self.assertEqual(self._messages()[-1]['ownership_task_id'], 1)

    def test_changed_repository_origin_pauses_reuse_of_recorded_worktree(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        subprocess.run(['git', '-C', str(self.workspace), 'remote', 'set-url', 'origin',
                        'git@github.com:other/repository.git'], check=True)
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted)
        # Assert
        self.assertIn('origin changed', stderr)
        self.assertEqual(self._messages(), [])

    def test_invalid_recorded_mapping_reports_reconciliation_without_traceback(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        task = self.planning_call('get_task', task_id=1)
        record = json.loads(task['description'])
        record['worktrees'] = [{}]
        self.planning_call('update_task', task_id=1, description=json.dumps(record))
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted)
        # Assert
        self.assertNotIn('Traceback', stderr)
        self.assertIn('mapping', stderr)
        self.assertEqual(self._messages(), [])

    def test_changed_child_selector_needs_no_factory_reconciliation_before_root_launch(self):
        # Arrange
        child = self.workspace / '.factory/agents/feature-owner/agent.json'
        document = json.loads(child.read_text())
        document['agent']['effort'] = 'low'
        child.write_text(json.dumps(document))
        before = child.read_bytes()
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)
        # Assert: the extension owns reading child settings at future dispatch/reload.
        self.assertEqual(code, 130, errors)
        self.assertEqual(child.read_bytes(), before)
        launch, = [e for e in self.events() if e['kind'] == 'launch']
        self.assertEqual(launch['roster'],
                         str(self.workspace / '.factory/agents/foreman/agent.json'))

    def test_foreman_launches_from_native_role_directory_with_selected_child_roster(self):
        # Arrange
        role = self.workspace / '.factory/agents/foreman'
        (role / 'APPEND_SYSTEM.md').write_text('Preserve my additional guidance.')
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        self.stop(process)
        # Assert
        launch = next(e for e in self.events() if e['kind'] == 'launch')
        self.assertEqual(launch['cwd'], str(role))
        self.assertEqual(launch['roster'], str(role / 'agent.json'))
        self.assertIsNone(launch['prompt'])
        self.assertEqual(launch['project'], '12')
        self.assertEqual(launch['forgetful_dir'], str(self.workspace / '.factory'))
        self.assertEqual(launch['forgetful_config'], str(self.workspace / '.factory/cli-config'))
        self.assertEqual((role / 'APPEND_SYSTEM.md').read_text(),
                         'Preserve my additional guidance.')

    def test_epic_defers_repository_worktrees_to_owner(self):
        # Arrange
        self.script({'team/app': [[[self.issue(labels=('factory', 'EPIC'))]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.stop(process)
        # Assert
        self.assertEqual(self._messages()[0]['worktrees'], [])
        self.assertIs(self._messages()[0]['epic'], True)
        self.assertEqual(self._messages()[0]['repositories'][0]['local_dir'], str(self.workspace))
        task = self.planning_call('get_task', task_id=1)
        self.assertEqual(json.loads(task['description'])['worktrees'], [])
        self.assertFalse((self.workspace / '.factory/worktrees').exists())

    def test_lost_task_response_reuses_committed_task(self):
        # Arrange
        self.env['PLANNING_LOST_RESPONSE'] = 'create_task'
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.stop(process)
        # Assert
        self.assertEqual(self._messages()[0]['ownership_task_id'], 1)
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)

    def test_missing_recorded_worktree_pauses_without_recreating_it(self):
        # Arrange
        from pathlib import Path
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        path = Path(self._messages()[0]['worktrees'][0]['path'])
        path.rename(path.with_name('saved-user-work'))
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted)
        # Assert
        self.assertIn('worktree mismatch', stderr)
        self.assertFalse(path.exists())
        self.assertTrue(path.with_name('saved-user-work').exists())
        self.assertEqual(self._messages(), [])

    def test_native_login_without_project_access_alerts_after_launch_without_scaffolding(self):
        # Arrange
        self.env['PROFILE_PROJECT_ACCESS'] = 'denied'
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        stderr = self.assert_paused(process)
        # Assert
        self.assertIn('planning check failed', stderr)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'send', 'close'])

    def test_full_ownership_record_is_reused_after_title_edit(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        self.planning_call('update_task', task_id=1, title='Own the clarified feature')
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.stop(restarted)
        # Assert
        self.assertEqual(self._messages()[0]['ownership_task_id'], 1)
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['total_count'], 1)

    def test_plan_associated_with_another_workspace_is_refused(self):
        # Arrange
        self.planning_call('create_plan', title='Other factory', project_id=12,
                           external_ref='github:team/app#1', status='draft',
                           context=json.dumps({'workspace': '/another/factory'}))
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        stderr = self.assert_paused(process)
        # Assert
        self.assertIn('another workspace', stderr)
        self.assertEqual(self._messages(), [])
        self.assertEqual(self.planning_call('query_tasks', plan_id=1)['tasks'], [])

    def test_uncertain_task_creation_is_not_retried_after_restart(self):
        # Arrange
        self.env['PLANNING_UNCERTAIN_CREATE'] = 'create_task'
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.assert_paused(first)
        del self.env['PLANNING_UNCERTAIN_CREATE']
        self.terminal_log.unlink()
        # Act
        restarted = self.start('--existing')
        stderr = self.assert_paused(restarted)
        # Assert
        self.assertIn('Ownership creation uncertain', stderr)
        self.assertEqual(self._messages(), [])
        state = json.loads((self.workspace / '.factory/fixture-plans.json').read_text())
        self.assertEqual(sum(call[0] == 'create_task' for call in state['calls']), 1)

    def test_lost_plan_creation_response_is_reconciled_by_unique_reference(self):
        # Arrange
        self.env['PLANNING_LOST_RESPONSE'] = 'create_plan'
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        self.stop(process)
        # Assert
        self.assertEqual(self._messages()[0]['plan_id'], 1)
        self.assertEqual(self._messages()[0]['ownership_task_id'], 1)

    def test_restart_restores_legacy_full_snapshot_even_without_open_issue(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        first = self.start('--existing')
        self.wait_until(first, lambda: len(self._messages()) == 1)
        self.stop(first)
        original = self._messages()[0]
        # Older Factory versions saved the full body in the same recovery JSON shape.
        plan = self.planning_call('get_plan', plan_id=original['plan_id'])
        context = json.loads(plan['context'])
        context['issue']['body'] = 'Legacy full issue requirements'
        self.planning_call('update_plan', plan_id=original['plan_id'],
                           context=json.dumps(context))
        self.terminal_log.unlink()
        self.script({'team/app': [[[]]]})
        # Act
        restarted = self.start('--new-only')
        self.wait_until(restarted, lambda: len(self._messages()) == 1)
        self.stop(restarted)
        # Assert
        self.assertEqual(self._messages()[0]['plan_id'], original['plan_id'])
        self.assertEqual(self._messages()[0]['worktrees'], original['worktrees'])
        self.assertTrue(self._messages()[0]['recovered'])
        self.assertEqual(self._messages()[0]['ownership_task_id'], original['ownership_task_id'])
        self.assertEqual(self._messages()[0]['body'], 'Legacy full issue requirements')

    def test_changed_issue_reuses_plan_task_and_worktree(self):
        # Arrange
        first = self.issue(body='First', updated_at='revision-1')
        changed = self.issue(body='Clarification', updated_at='revision-2')
        self.script({'team/app': [[[first]], [[changed]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 2)
        self.stop(process)
        # Assert
        first, second = self._messages()
        self.assertEqual(second['body'], 'Clarification')
        for key in ('plan_id', 'ownership_task_id', 'worktrees'):
            self.assertEqual(first[key], second[key])

    def test_issue_is_scaffolded_before_terminal_submission(self):
        # Arrange
        self.script({'team/app': [[[self.issue(body='Build the feature',
                                              updated_at='2026-10-17T10:00:00Z')]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
        _, _, stderr = self.stop(process)
        # Assert
        message = next(e['text'] for e in self.events() if e['kind'] == 'send')
        payload = json.loads(message.split('External issue data: ', 1)[1])
        self.assertEqual(payload['plan_id'], 1, stderr)
        self.assertEqual(payload['ownership_task_id'], 1)
        self.assertEqual(payload['body'], 'Build the feature')
        plan = self.planning_call('get_plan', plan_id=payload['plan_id'])
        context = json.loads(plan['context'])
        self.assertEqual(context['issue']['body'],
                         'This is a placeholder description for github issue #1: '
                         'Implement feature. The feature owner will update it after '
                         'reviewing the issue/plan.')
        self.assertTrue(context['ownership_create_started'])
        self.assertLessEqual(len(plan['context']), 2000)
        mapping = payload['worktrees'][0]
        self.assertEqual(mapping['repository'], 'team/app')
        branch = subprocess.check_output(
            ['git', '-C', mapping['path'], 'branch', '--show-current'], text=True).strip()
        self.assertEqual(branch, mapping['branch'])
        ignored = subprocess.run(['git', '-C', str(self.workspace),
                                  'check-ignore', mapping['path']],
                                 capture_output=True)
        self.assertEqual(ignored.returncode, 0, 'Factory worktrees must not enter the origin index')
        self.assertEqual(payload['revision'], '2026-10-17T10:00:00Z')
