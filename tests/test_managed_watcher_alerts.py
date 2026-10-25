"""Managed alert/recovery through the real SDK and private tmux, without inference."""
import json
import subprocess
import time
from pathlib import Path

from lifecycle_support import LifecycleFixture
from test_init import INIT_SETTINGS


class ManagedWatcherAlertTests(LifecycleFixture):
    def setUp(self):
        super().setUp()
        self.env['PYTHONDONTWRITEBYTECODE'] = '1'

    def inputs(self):
        log = self.workspace / 'pi.jsonl'
        return [event['input'] for line in log.read_text().splitlines()
                if 'input' in (event := json.loads(line))] if log.exists() else []

    def messages(self, prefix):
        return [json.loads(text.split(': ', 1)[1]) for text in self.inputs()
                if text.startswith(prefix)]

    def wait_for(self, predicate):
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        self.fail('Managed watcher did not reach expected state')

    def native_planning(self, repo, tool, **fields):
        result = subprocess.run(
            [str(self.bin / 'forgetful'), 'call', tool, '--args', json.dumps(fields),
             '--json', '--local'], cwd=repo, env=self.env,
            capture_output=True, text=True, check=True)
        return json.loads(result.stdout)

    def test_repository_preflight_alert_and_fresh_repair_keep_the_same_foreman(self):
        repo = self.repo(name='r')
        self.git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-qm', 'fixture')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertEqual(self.foreman(repo).returncode, 0)
        original = self.status(repo)
        self.git(repo, 'remote', 'set-url', 'origin', 'git@github.com:other/repo.git')
        issue_prefix = 'Factory issue notification. External issue data: '
        alert_prefix = 'Factory watcher alert. External problem data: '
        self.state.write_text(json.dumps(dict(issues=[dict(
            number=1, title='Fresh work', labels=[dict(name='factory')], state='open',
            html_url='https://github.com/team/app/issues/1', body='Requirements',
            updated_at='unchanged')])))
        started = self.watch(repo, '--start', '--existing', '--interval', '.05')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.wait_for(lambda: len(self.messages(alert_prefix)) == 1)
        self.assertEqual(self.messages(alert_prefix)[0]['scope'], 'repository')
        self.assertEqual(self.messages(alert_prefix)[0]['code'], 'repository_origin_changed')
        self.assertNotIn('plan_id', self.messages(alert_prefix)[0])
        self.assertEqual(self.messages(issue_prefix), [])
        self.assertEqual(self.native_planning(repo, 'list_plans')['plans'], [])
        paused = self.status(repo)
        self.assertEqual(paused['watcher'], 'running')
        self.assertEqual(paused['target'], original['target'])
        self.assertEqual(paused['owner_pid'], original['owner_pid'])
        # Git-only correction can authorize fresh intake; no saved plan needed native repair.
        self.git(repo, 'remote', 'set-url', 'origin', 'git@github.com:team/app.git')
        self.wait_for(lambda: len(self.messages(issue_prefix)) == 1)
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        after = self.status(repo)
        self.assertEqual(after['target'], original['target'])
        self.assertEqual(after['owner_pid'], original['owner_pid'])
        self.assertEqual(after['foreman'], 'ready')
        self.assertEqual(len(self.native_planning(repo, 'list_plans')['plans']), 1)
        self.assertEqual(len(self.messages(alert_prefix)), 1)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_approved_first_setup_repair_keeps_foreman_and_unrelated_busy_ownership_records(self):
        # Arrange: the same real SDK/private-tmux Foreman has a saved unrelated busy task.
        repo = self.repo(name='r')
        self.git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-qm', 'fixture')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertEqual(self.foreman(repo).returncode, 0)
        original = self.status(repo)
        issue_prefix = 'Factory issue notification. External issue data: '
        alert_prefix = 'Factory watcher alert. External problem data: '
        issue = dict(number=2, title='Healthy saved work', labels=[dict(name='factory')],
                     html_url='https://github.com/team/app/issues/2', state='open',
                     body='Requirements', updated_at='unchanged')
        self.state.write_text(json.dumps(dict(issues=[issue])))
        started = self.watch(repo, '--start', '--existing', '--interval', '.05')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.wait_for(lambda: len(self.messages(issue_prefix)) == 1)
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        first = self.messages(issue_prefix)[0]
        busy = self.native_planning(repo, 'update_task', task_id=first['ownership_task_id'],
                                    state='doing', assigned_agent='busy-native-owner', version=4)
        target = repo / '.factory/worktrees/team-app-1'
        target.mkdir()
        (target / 'user.txt').write_text('Preserve user data')
        issue.update(number=1, title='Interrupted setup',
                     html_url='https://github.com/team/app/issues/1')
        # A real saved incomplete plan distinguishes repair from the new pre-write checks.
        snapshot = dict(source=dict(provider='github', reference='team/app'), number=1,
                        title=issue['title'], url=issue['html_url'], body=issue['body'],
                        revision=issue['updated_at'], epic=False)
        saved_plan = self.native_planning(repo, 'create_plan', title=issue['title'], project_id=12,
            external_ref='github:team/app#1', source_url=issue['html_url'],
            context=json.dumps(dict(workspace=str(repo), issue=snapshot)))
        self.state.write_text(json.dumps(dict(issues=[issue])))
        started = self.watch(repo, '--start', '--existing', '--interval', '.05')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.wait_for(lambda: len(self.messages(alert_prefix)) == 1)
        alert = self.messages(alert_prefix)[0]
        self.assertEqual(alert['code'], 'setup_incomplete')
        self.assertEqual(alert['plan_id'], saved_plan['id'])
        self.assertIn('user approval', alert['recovery'])
        plan = self.native_planning(repo, 'get_plan', plan_id=alert['plan_id'])
        # Act: path correction alone cannot create the tree or the first ownership task.
        saved = target.with_name('saved-user-data')
        target.rename(saved)
        self.wait_for(lambda: sum(c[0] == 'query_tasks' and c[1]['plan_id'] == plan['id']
                                 for c in json.loads((self.workspace / 'plans.json').read_text())
                                 ['calls']) >= 4)
        self.assertFalse(target.exists())
        self.assertEqual(self.native_planning(repo, 'query_tasks', plan_id=plan['id'])['tasks'], [])
        # Act: simulate user-approved native completion, without claiming model behavior.
        self.git(repo, 'worktree', 'add', '-b', 'factory/team-app-1', str(target), 'HEAD')
        record = dict(kind='factory-ownership', workspace=str(repo),
                      external_ref=plan['external_ref'], worktrees=[dict(repository='team/app',
                          local_dir=str(repo), branch='factory/team-app-1', path=str(target))])
        owner = self.native_planning(repo, 'create_task', plan_id=plan['id'],
                                     title='Feature ownership', description=json.dumps(record))
        self.wait_for(lambda: any(m['plan_id'] == plan['id'] for m in self.messages(issue_prefix)))
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        # Assert: repair preserves conversation identity, existing task and all native records.
        after = self.status(repo)
        self.assertEqual(after['target'], original['target'])
        self.assertEqual(after['owner_pid'], original['owner_pid'])
        self.assertEqual(after['foreman'], 'ready')
        self.assertEqual(self.native_planning(repo, 'get_task', task_id=busy['id']), busy)
        self.assertEqual(self.native_planning(repo, 'get_plan', plan_id=plan['id']), plan)
        repaired = [m for m in self.messages(issue_prefix) if m['plan_id'] == plan['id']]
        self.assertEqual(len(repaired), 1)
        self.assertEqual(repaired[0]['ownership_task_id'], owner['id'])
        self.assertEqual((saved / 'user.txt').read_text(), 'Preserve user data')
        self.assertEqual(len(self.messages(alert_prefix)), 1)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_alert_and_same_revision_repair_preserve_foreman_identity_and_busy_ownership(self):
        # Arrange: one native Foreman owns a watcher with an existing saved plan.
        repo = self.repo(name='r')
        self.git(repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '--allow-empty', '-qm', 'fixture')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        started = self.foreman(repo)
        self.assertEqual(started.returncode, 0, started.stderr)
        original = self.status(repo)
        issue_prefix = 'Factory issue notification. External issue data: '
        alert_prefix = 'Factory watcher alert. External problem data: '
        self.state.write_text(json.dumps({'issues': [{
            'number': 1, 'title': 'Feature', 'labels': [{'name': 'factory'}],
            'html_url': 'https://github.com/team/app/issues/1', 'state': 'open',
            'body': 'Requirements', 'updated_at': 'same-revision'}]}))
        started = self.watch(repo, '--start', '--existing', '--interval', '.05')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.wait_for(lambda: len(self.messages(issue_prefix)) == 1)
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        initial_message, = self.messages(issue_prefix)
        state_path = self.workspace / 'plans.json'
        task = json.loads(state_path.read_text())['tasks'][0]
        mapping = json.loads(task['description'])['worktrees'][0]
        update = subprocess.run(
            [str(self.bin / 'forgetful'), 'call', 'update_task', '--args', json.dumps({
                'task_id': task['id'], 'state': 'doing', 'assigned_agent': 'busy-native-owner',
                'version': 4}), '--json', '--local'], cwd=repo, env=self.env,
            capture_output=True, text=True, check=True)
        self.assertEqual(update.returncode, 0, update.stderr)
        before = json.loads(state_path.read_text())['tasks']
        tree = Path(mapping['path'])
        (tree / 'unfinished.txt').write_text('Preserve busy owner work.')
        saved = tree.with_name('saved-user-work')
        tree.rename(saved)
        self.state.write_text(json.dumps({'issues': []}))
        # Act: the closed issue is recovered, blocked, and repaired in the same conversation.
        started = self.watch(repo, '--start', '--new-only', '--interval', '.05')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.wait_for(lambda: len(self.messages(alert_prefix)) == 1)
        paused = self.status(repo)
        self.assertEqual(paused['watcher'], 'running')
        self.assertEqual(paused['foreman'], 'ready')
        self.assertEqual(paused['target'], original['target'])
        self.assertEqual(paused['owner_pid'], original['owner_pid'])
        self.assertEqual(json.loads(state_path.read_text())['tasks'], before)
        self.assertFalse(tree.exists())
        saved.rename(tree)
        self.wait_for(lambda: len(self.messages(issue_prefix)) == 2)
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        # Assert: no owner replacement, task reset, new scaffold or extra Foreman launch.
        after = self.status(repo)
        self.assertEqual(after['target'], original['target'])
        self.assertEqual(after['owner_pid'], original['owner_pid'])
        self.assertEqual(after['foreman'], 'ready')
        state = json.loads(state_path.read_text())
        self.assertEqual(state['tasks'], before)
        self.assertEqual(sum(c[0] == 'create_plan' for c in state['calls']), 1)
        self.assertEqual(sum(c[0] == 'create_task' for c in state['calls']), 1)
        self.assertEqual(len(self.messages(alert_prefix)), 1)
        recovered = self.messages(issue_prefix)[-1]
        for field in ('plan_id', 'ownership_task_id', 'worktrees', 'revision'):
            self.assertEqual(recovered[field], initial_message[field])
        self.assertTrue(recovered['recovered'])
        self.assertEqual((tree / 'unfinished.txt').read_text(), 'Preserve busy owner work.')
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        self.assertEqual(sum('started' in event for event in events), 1)
        self.send_and_wait_for_exit(repo, original['target'])
