"""Normalized Factory lifecycle through public CLI, real tmux and fake native Pi."""
import json
import shutil

from lifecycle_support import LifecycleFixture
from test_init import INIT_SETTINGS


class NormalizedLifecycleTests(LifecycleFixture):
    def test_legacy_root_preserves_edits_and_keeps_unselected_memory_inactive(self):
        # Arrange: finish an older edited root without selecting the optional managed extension.
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertNotEqual(first.returncode, 0)
        del self.env['PROFILE_FAIL']
        definition = repo / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        managed = '../../resources/pi-forgetful/factory.ts'
        document['agent']['name'] = 'dispatch-lead'
        document['agent']['resources']['extensions'].remove(managed)
        custom = definition.parent / 'custom-extension.ts'
        custom.write_text('// Existing user-managed extension.\n')
        document['agent']['resources']['extensions'].append('./custom-extension.ts')
        definition.write_text(json.dumps(document))
        shutil.rmtree(repo / '.factory/resources/pi-forgetful', ignore_errors=True)
        finalized = self.run_cli(repo, '--finalize')
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        preferences = definition.with_name('forgetful.json')
        before = {definition: definition.read_bytes(), custom: custom.read_bytes(),
                  preferences: preferences.read_bytes()}

        # Act: ordinary rerun and launch must use the edited definition without repairing it.
        rerun = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        started = self.foreman(repo)

        # Assert
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertIn('managed Foreman extension is not selected', started.stdout)
        self.assertIn('saved automatic-memory preferences are inactive', started.stdout)
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        state = self.status(repo)
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        self.assertIn(str(custom), launch['args'])
        self.assertNotIn('pi-forgetful/factory.ts', ' '.join(launch['args']))
        self.send_and_wait_for_exit(repo, state['target'])

        # Arrange / Act / Assert: an old enabled preference remains saved but stays inactive.
        enabled = {'enabled': True, 'capture_mode': 'auto', 'model': 'provider/model'}
        preferences.write_text(json.dumps(enabled))
        enabled_before = preferences.read_bytes()
        restarted = self.foreman(repo)
        self.assertEqual(restarted.returncode, 0, restarted.stderr)
        self.assertIn('saved automatic-memory preferences are inactive', restarted.stdout)
        self.assertEqual(preferences.read_bytes(), enabled_before)
        self.assertNotIn('pi-forgetful/factory.ts', ' '.join(
            json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[-1])['args']))
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])

    def test_foreman_keeps_extension_auth_separate_from_native_cli_auth(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/factory/mcp',
        )
        self.assertEqual(setup.returncode, 0, setup.stderr)
        auth = repo / '.factory/agents/foreman/forgetful-auth.json'
        auth.write_text('{"token_env":"FACTORY_EXTENSION_TOKEN"}\n')
        before = auth.read_bytes()
        self.env['FORGETFUL_TOKEN'] = 'native-fixture-token'
        self.env['FACTORY_EXTENSION_TOKEN'] = 'extension-fixture-token'

        # Act
        started = self.foreman(repo)

        # Assert
        self.assertEqual(started.returncode, 0, started.stderr)
        state = self.status(repo)
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        self.assertFalse(launch['has_native_forgetful_token'])
        self.assertTrue(launch['has_extension_token'])
        self.assertEqual(auth.read_bytes(), before)
        self.send_and_wait_for_exit(repo, state['target'])

    def test_relocated_foreman_receives_its_absolute_definition_without_changing_children(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        factory = repo / '.factory'
        original = factory / 'agents/foreman'
        relocated = factory / 'coordinators/dispatch'
        relocated.parent.mkdir()
        original.rename(relocated)
        definition = relocated / 'agent.json'
        document = json.loads(definition.read_text())
        document['agent']['resources']['extensions'] = [
            '../../resources/agentshell/extensions/agentshell.ts',
            '../../resources/hide-tools/index.ts',
            '../../resources/pi-forgetful/factory.ts',
        ]
        document['roster']['roles'] = [{'agent_file': '../../agents/feature-owner/agent.json'}]
        definition.write_text(json.dumps(document))
        config = factory / 'factory.toml'
        config.write_text(config.read_text().replace(
            'agents/foreman/agent.json', 'coordinators/dispatch/agent.json'))
        child = factory / 'agents/feature-owner/agent.json'
        child_before = child.read_bytes()

        # Act
        started = self.foreman(repo)

        # Assert
        self.assertEqual(started.returncode, 0, started.stderr)
        state = self.status(repo)
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        self.assertEqual(launch['foreman_file'], str(definition.absolute()))
        self.assertEqual(launch['roster'], str(definition.absolute()))
        self.assertEqual(child.read_bytes(), child_before)
        self.send_and_wait_for_exit(repo, state['target'])

    def test_standalone_start_attach_and_borrowed_watcher_keep_original_foreman(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)

        # Act
        started = self.foreman(repo)

        # Assert: start/attach does not poll or duplicate, managed watcher borrows the same owner.
        self.assertEqual(started.returncode, 0, started.stderr)
        original = self.status(repo)
        self.assertEqual((original['foreman'], original['watcher']), ('ready', 'stopped'))
        self.assertFalse((self.workspace / 'plans.json').exists())
        attached = self.foreman(repo, '--attach')
        self.assertEqual(attached.returncode, 0, attached.stderr)
        self.assertIn('attach-session', attached.stdout)
        self.assertEqual(self.status(repo)['target'], original['target'])
        duplicate = self.foreman(repo)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn('--attach', duplicate.stderr)
        plain = self.watch(repo, '--new-only')
        self.assertNotEqual(plain.returncode, 0)
        watch = self.watch(repo, '--start', '--new-only', '--interval', '0.1')
        self.assertEqual(watch.returncode, 0, watch.stderr)
        stopped = self.watch(repo, '--stop')
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        self.assertEqual(self.status(repo)['target'], original['target'])
        self.assertEqual(self.status(repo)['foreman'], 'ready')
        events = (self.workspace / 'pi.jsonl').read_text().splitlines()
        starts = [json.loads(line) for line in events if 'started' in json.loads(line)]
        self.assertEqual(len(starts), 1)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_root_resource_choices_reach_native_pi_through_the_real_sdk(self):
        # Arrange: edit native resource options after completed first setup.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        definition = repo / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        document['agent']['resources'].update(
            mcp_servers=None, inherit_personal_resources=True,
            inherit_project_resources=True, include_home_system_prompt=True)
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()

        # Act: the real SDK starts only the fixture's fake native Pi in its private tmux server.
        started = self.foreman(repo)

        # Assert: the former forced flags are absent, but selected local skills still arrive.
        self.assertEqual(started.returncode, 0, started.stderr)
        original = self.status(repo)
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        for flag in ('--no-extensions', '--no-skills', '--no-mcp', '--system-prompt'):
            self.assertNotIn(flag, launch['args'])
        self.assertIn('--skill', launch['args'])
        self.assertIn(str(definition.parent / 'skills'), launch['args'])
        self.assertEqual(definition.read_bytes(), before)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_project_prompt_guard_follows_the_selected_home_prompt_option(self):
        # Arrange: the starter excludes the home prompt; a project override then needs review.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        definition = repo / '.factory/agents/foreman/agent.json'
        project_prompt = definition.parent / '.pi/SYSTEM.md'
        project_prompt.parent.mkdir()
        project_prompt.write_text('Disposable project instructions; no model is invoked.\n')
        blocked = self.foreman(repo)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn('.pi/SYSTEM.md', blocked.stderr)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        document = json.loads(definition.read_text())
        document['agent']['resources']['include_home_system_prompt'] = True
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()

        # Act: explicitly choosing native prompt handling removes the exclusion conflict.
        started = self.foreman(repo)

        # Assert: native Pi keeps its normal prompt handling; Factory never rewrites instructions.
        self.assertEqual(started.returncode, 0, started.stderr)
        original = self.status(repo)
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        self.assertNotIn('--system-prompt', launch['args'])
        self.assertIn('--no-extensions', launch['args'])
        self.assertEqual(project_prompt.read_text(),
                         'Disposable project instructions; no model is invoked.\n')
        self.assertEqual(definition.read_bytes(), before)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_assisted_first_finalization_keeps_full_team_and_same_conversation(self):
        # Arrange: assisted setup still provisions all explicitly selected starter workers.
        repo = self.repo()
        workers = []
        for role in ('implementation', 'review'):
            workers.extend((f'--{role}-harness', 'pi', f'--{role}-model', 'provider/model',
                            f'--{role}-effort', 'high'))
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *workers,
                             '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        factory = repo / '.factory'
        paths = [factory / f'agents/{role}/agent.json' for role in (
            'foreman', 'feature-owner', 'research', 'implementation', 'review')]
        self.assertTrue(all(path.is_file() for path in paths))
        before = {path: path.read_bytes() for path in paths}
        self.assertEqual(original['setup'], 'incomplete')
        self.assertFalse((factory / 'runtime/foreman/roster.json').exists())
        blocked = self.watch(repo, '--start', '--new-only')
        self.assertNotEqual(blocked.returncode, 0)

        # Act
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')

        # Assert: validate in place without replay, replacement or definition synchronization.
        self.assertEqual(final.returncode, 0, final.stderr)
        self.assertIn('/reload', final.stdout)
        after = self.status(repo)
        self.assertEqual(after['setup'], 'complete')
        self.assertEqual(after['target'], original['target'])
        self.assertEqual({path: path.read_bytes() for path in paths}, before)
        self.assertEqual(json.loads((factory / 'setup-complete.json').read_text()),
                         {'complete': True})
        self.assertEqual(self.watch(repo, '--start', '--new-only').returncode, 0)
        self.assertEqual(self.watch(repo, '--stop').returncode, 0)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_unknown_owner_and_failed_start_never_replace_or_replay(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        definition = repo / '.factory/agents/foreman/agent.json'
        before = definition.read_bytes()

        # Act: preflight failure must leave no launched owner.
        failed = self.foreman(repo, '--agentshell-python', str(self.bin / 'missing-python'))

        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('preflight failed', failed.stderr)
        self.assertIn('retry foreman', failed.stderr)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        state = repo / '.factory/runtime/foreman/owner.json'
        self.assertFalse(state.exists())
        state.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        contents = json.dumps({'workspace': str(repo), 'run_id': 'uncertain-fixture',
                               'foreman': 'unknown', 'watcher': 'stopped', 'target': None})
        state.write_text(contents)
        retry = self.foreman(repo)
        attach = self.foreman(repo, '--attach')
        self.assertNotEqual(retry.returncode, 0)
        self.assertNotEqual(attach.returncode, 0)
        self.assertIn('uncertain', retry.stderr)
        self.assertEqual(state.read_text(), contents)
        self.assertEqual(definition.read_bytes(), before)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        self.assertFalse((self.workspace / 'plans.json').exists())

    def test_owner_lock_conflict_preserves_lock_and_names_standalone_attach(self):
        import fcntl

        # Arrange: hold this fixture's owner lease, with no claim that a native session exists.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        runtime = repo / '.factory/runtime/foreman'
        runtime.mkdir(parents=True, mode=0o700)
        lock = runtime / 'owner.lock'
        with lock.open('w') as stream:
            lock.chmod(0o600)
            inode = lock.stat().st_ino
            fcntl.flock(stream, fcntl.LOCK_EX)
            # Act
            started = self.foreman(repo)
            # Assert
            self.assertNotEqual(started.returncode, 0)
            self.assertIn('already exists', started.stderr)
            self.assertIn('use foreman --attach', started.stderr)
            self.assertEqual(lock.stat().st_ino, inode)
            self.assertFalse((self.workspace / 'pi.jsonl').exists())

    def test_watcher_runtime_prerequisite_timeout_preserves_foreman_and_startup_guidance(self):
        import sys
        import time

        # Arrange: freeze only the fixture runtime probe's calling watcher before borrowed ready.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        started = self.foreman(repo)
        self.assertEqual(started.returncode, 0, started.stderr)
        original = self.status(repo)
        probe = repo / '.factory/resources/agentshell/python/.venv/bin/python'
        self.assertFalse(probe.is_symlink(), 'Never replace a real interpreter through a symlink')
        original_probe = probe.read_text()
        self.assertIn('.fixture-package', original_probe)
        invoked = self.workspace / 'runtime-probe-invoked'
        probe.write_text(
            f'#!{sys.executable}\nimport os, signal\n'
            'from pathlib import Path\n'
            f'Path({str(invoked)!r}).write_text(str(os.getppid()))\n'
            'os.kill(os.getppid(), signal.SIGSTOP)\n')
        # Act: exercise the existing timeout unchanged; no new retry or recovery behavior.
        began = time.monotonic()
        try:
            failed = self.watch(repo, '--start', '--new-only', timeout=45)
        finally:
            probe.write_text(original_probe)
        # Assert
        self.assertGreaterEqual(time.monotonic() - began, 30)
        self.assertTrue(invoked.is_file(), 'The external runtime prerequisite was not probed')
        self.assertNotEqual(int(invoked.read_text()), original['owner_pid'])
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('startup timed out', failed.stderr)
        self.assertIn('native sign-in', failed.stderr)
        self.assertIn('init --finalize', failed.stderr)
        after = self.status(repo)
        self.assertEqual(after['target'], original['target'])
        self.assertEqual(after['owner_pid'], original['owner_pid'])
        self.assertEqual(after['foreman'], 'ready')
        self.send_and_wait_for_exit(repo, original['target'])
