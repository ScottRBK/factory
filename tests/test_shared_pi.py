"""Shared native Pi onboarding through public init/watch commands only."""
import json
from pathlib import Path

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.cli.numbered_selection import parse_numbered_selection
from forgetful_factory.domain.models import FactoryError


class SharedPiTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(self.log)

    def test_declining_shared_home_stops_before_pi_or_github(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              pi_defaults=False, input='n\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Shared Pi profile consent declined', result.stderr)
        self.assertIn('Use your existing Pi login', result.stdout)
        self.assertIn(self.env['PI_CODING_AGENT_DIR'], result.stdout)
        self.assertIn('settings and history remain shared', result.stdout)
        self.assertIn('skips your personal SYSTEM.md', result.stdout)
        self.assertIn('AGENTS.md and APPEND_SYSTEM.md can still apply', result.stdout)
        self.assertIn('Listing models can run your installed Pi extensions', result.stdout)
        self.assertIn('may incur charges', result.stdout)
        self.assertIn('Use this Pi profile? [y/N]', result.stdout)
        self.assertNotIn('auth-only isolation', result.stdout)
        self.assertTrue(all(len(line) <= 100 for line in result.stdout.splitlines()))
        self.assertEqual(events(self.log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})

    def test_shared_home_consent_and_exact_model_are_persisted_without_credentials(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        role = repo / '.factory/agents/foreman'
        choice = json.loads((repo / '.factory/pi-profile.json').read_text())
        self.assertEqual(choice, {'agent_directory': self.env['PI_CODING_AGENT_DIR'],
                                  'shared_profile_consent': True})
        receipt = json.loads((repo / '.factory/setup-complete.json').read_text())
        self.assertEqual(receipt, {'complete': True})
        agent = json.loads((role / 'agent.json').read_text())['agent']
        self.assertEqual(agent['model'], 'provider/model')
        calls = [e for e in events(self.log) if e['name'] == 'pi']
        self.assertEqual([e['args'] for e in calls], [['--no-approve', '--list-models']])
        self.assertEqual(calls[0]['agent_dir'], self.env['PI_CODING_AGENT_DIR'])
        self.assertIn('access unverified', result.stdout)
        self.assertFalse((role / 'auth.json').exists())

    def test_numbered_models_are_grouped_and_save_exact_native_identifier(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'z-provider  special/model  128000  8192  yes  yes\n'
            'a-provider  first  128000  8192  yes  yes')
        # Act
        result = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                              '--foreman-effort', 'high', input='2\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('a-provider:', result.stdout)
        self.assertIn('z-provider:', result.stdout)
        self.assertIn('2. z-provider/special/model', result.stdout)
        selected = json.loads((repo / '.factory/agents/foreman/agent.json').read_text())
        self.assertEqual(selected['agent']['model'], 'z-provider/special/model')

    def test_numbered_foreman_effort_is_saved_and_used_as_owner_default(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', '--label', 'factory', input='1\n5\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('1. off\n  2. minimal\n  3. low\n  4. medium\n  5. high\n'
                      '  6. xhigh\n  7. max', result.stdout)
        self.assertIn('Select Foreman effort number:', result.stdout)
        for role in ('foreman', 'feature-owner'):
            agent = json.loads((repo / f'.factory/agents/{role}/agent.json').read_text())['agent']
            self.assertEqual(agent['model'], 'provider/model')
            self.assertEqual(agent['effort'], 'high')

    def test_numbered_selection_preserves_all_foreman_answer_results(self):
        # Arrange: preserve every answer from the former CLI matrix.
        prompts = (('Foreman model', 1, '2', 'provider/model'),
                   ('Foreman effort', 7, '8', 'high'))
        for label, choice_count, upper, old_name in prompts:
            invalid = (('', 'number'), ('not-a-number', 'number'), ('0', 'range'),
                       ('-1', 'range'), (upper, 'range'), (old_name, 'number'))
            for answer, failure in invalid:
                with self.subTest(label=label, answer=answer):
                    expected = (f'{label}: select a number from 1 to {choice_count}.'
                                if failure == 'number' else
                                f'{label} selection is out of range; '
                                f'select a number from 1 to {choice_count}.')
                    # Act / Assert
                    with self.assertRaises(FactoryError) as raised:
                        parse_numbered_selection(label, answer, choice_count)
                    self.assertEqual(str(raised.exception), expected)
        # Act / Assert: both valid endpoints retain their one-based menu positions.
        self.assertEqual(parse_numbered_selection('Foreman model', '1', 1), 1)
        self.assertEqual(parse_numbered_selection('Foreman effort', '1', 7), 1)
        self.assertEqual(parse_numbered_selection('Foreman effort', '7', 7), 7)

    def test_invalid_foreman_numbers_stop_before_config_or_label_changes(self):
        # Keep one non-number model case and one out-of-range effort case at the real CLI.
        for field, prefix, answer in (('model', '', 'provider/model'),
                                      ('effort', '1\n', '8')):
            with self.subTest(field=field):
                # Arrange
                repo = self.repo(field)
                self.state.write_text('{}')
                # Act
                result = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                                      input=prefix + answer + '\n')
                # Assert
                self.assertEqual(result.returncode, 1)
                self.assertIn(f'Foreman {field}', result.stderr)
                self.assertIn('select a number from 1 to', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())
                self.assertEqual(json.loads(self.state.read_text()), {})

    def test_no_models_gives_native_login_in_chosen_home_and_allows_recheck(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = 'No models available'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='r\nn\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('/login', result.stdout)
        self.assertIn(self.env['PI_CODING_AGENT_DIR'], result.stdout)
        self.assertIn('another terminal', result.stdout)
        calls = [e['args'] for e in events(self.log) if e['name'] == 'pi']
        self.assertEqual(calls, [['--no-approve', '--list-models']] * 2)
        self.assertFalse((repo / '.factory/setup-complete.json').exists())

    def test_saved_home_is_preserved_when_environment_and_repeated_init_flags_change(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        choice = repo / '.factory/pi-profile.json'
        original = choice.read_bytes()
        self.env['PI_CODING_AGENT_DIR'] = str(self.workspace / 'different home')
        self.log.unlink()
        # Act
        retry = self.run_cli(repo, pi_defaults=False)
        ignored = self.run_cli(repo, '--pi-agent-dir', self.env['PI_CODING_AGENT_DIR'])
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(ignored.returncode, 0, ignored.stderr)
        self.assertEqual(choice.read_bytes(), original)
        self.assertEqual(events(self.log), [])
        # Explicit first-setup validation cannot silently switch the approved shared home.
        conflict = self.run_cli(repo, '--finalize', '--pi-agent-dir',
                                self.env['PI_CODING_AGENT_DIR'])
        self.assertNotEqual(conflict.returncode, 0)
        self.assertIn('conflicts with saved consent', conflict.stderr)
        self.assertIn('init --finalize', conflict.stderr)
        self.assertEqual(choice.read_bytes(), original)

    def watch(self, repo):
        import subprocess
        import sys
        return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                               '--workspace', str(repo), '--new-only'], cwd=repo, env=self.env,
                              capture_output=True, text=True, timeout=5)

    def test_watch_rejects_missing_consent_and_model_receipt_before_polling(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        for name, message in (('pi-profile.json', 'consent'),
                              ('setup-complete.json', 'incomplete')):
            with self.subTest(missing=name):
                path = repo / '.factory' / name
                original = path.read_bytes()
                path.unlink()
                self.state.write_text('{}')
                self.log.unlink(missing_ok=True)
                # Act
                result = self.watch(repo)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertEqual(json.loads(self.state.read_text()), {})
                self.assertEqual(events(self.log), [])
                path.write_bytes(original)

    def test_selected_resources_must_be_provisioned_local_paths(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        path = role / 'agent.json'
        original = path.read_bytes()
        for selection in ({'extensions': ['npm:unreviewed']},
                          {'skills': ['https://example.com/skill']},
                          {'skills': ['missing-skill']}, {'packages': ['npm:package']},
                          {'inherit_personal_resources': 'true'}):
            with self.subTest(selection=selection):
                document = json.loads(original)
                document['agent']['resources'].update(selection)
                path.write_text(json.dumps(document))
                self.state.write_text('{}')
                self.log.unlink(missing_ok=True)
                # Act
                result = self.watch(repo)
                state_after_watch = json.loads(self.state.read_text())
                retry = self.run_cli(repo)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(retry.returncode, 0, retry.stderr)
                self.assertRegex(result.stderr, 'resource|audited local')
                self.assertEqual(state_after_watch, {})
                self.assertEqual(events(self.log), [])
                self.assertEqual(json.loads(path.read_text()), document)
                path.write_bytes(original)
                setup = self.run_cli(repo)
                self.assertEqual(setup.returncode, 0, setup.stderr)

    def test_actual_agentshell_launch_uses_shared_home_and_selected_resources(self):
        # Arrange: replace only external commands, using the real installed AgentShell.
        import signal
        import subprocess
        import sys
        import time

        from agentshell_support import PI_INTERACTIVE, TMUX, stop_terminal_fixture
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        (role / 'APPEND_SYSTEM.md').write_text('Discuss only. Custom role guidance.')
        skill = role / 'skills/foreman/SKILL.md'
        edited_skill = skill.read_text() + '\nExplain decisions with short examples.\n'
        skill.write_text(edited_skill)
        extra = repo / 'repository-skill'
        extra.mkdir()
        (extra / 'SKILL.md').write_text('---\nname: repo\ndescription: repo\n---\nRepo skill')
        selection = role / 'agent.json'
        document = json.loads(selection.read_text())
        resources = document['agent']['resources']
        resources['skills'].append(str(extra))
        selection.write_text(json.dumps(document))
        retry = self.run_cli(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(skill.read_text(), edited_skill)
        self.assertEqual((role / 'APPEND_SYSTEM.md').read_text(),
                         'Discuss only. Custom role guidance.')
        (self.bin / 'tmux').write_text(TMUX)
        pi = self.bin / 'pi'
        pi.write_text(pi.read_text() + PI_INTERACTIVE)
        self.env['TERMINAL_FIXTURE'] = str(self.workspace / 'terminal')
        self.addCleanup(stop_terminal_fixture, self.workspace / 'terminal')
        self.env['PI_CODING_AGENT_DIR'] = str(self.workspace / 'wrong home')
        self.log.unlink()
        # Act
        process = subprocess.Popen([sys.executable, '-m', 'forgetful_factory', 'watch',
                                    '--workspace', str(repo), '--new-only'],
                                   env=self.env, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 8
            while time.monotonic() < deadline and process.poll() is None:
                if any('--extension' in e['args'] for e in events(self.log)):
                    time.sleep(0.2)
                    break
                time.sleep(0.02)
            process.send_signal(signal.SIGINT)
            stdout, stderr = process.communicate(timeout=12)
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate(timeout=12)
        # Assert
        self.assertEqual(process.returncode, 130, stderr)
        launches = [e for e in events(self.log) if e['name'] == 'pi']
        self.assertEqual(len(launches), 1)
        launch = launches[0]
        self.assertEqual(launch['agent_dir'], str(self.workspace / 'native pi'))
        self.assertEqual(launch['role_dir'], str(repo / '.factory'))
        args = launch['args']
        for flag in ('--no-extensions', '--no-skills', '--no-mcp', '--offline'):
            self.assertIn(flag, args)
        self.assertIn('--system-prompt', args)
        self.assertEqual(args[args.index('--system-prompt') + 1], '')
        for flag in ('--no-context-files', '--tools', '--no-approve'):
            self.assertNotIn(flag, args)
        self.assertIn(str(role / 'skills'), args)
        self.assertIn(str(extra), args)
        self.assertIn(str(repo / '.factory/resources/hide-tools/index.ts'), args)
        self.assertNotIn('Discuss only. Custom role guidance.', args)
        self.assertEqual(launch['cwd'], str(role))
        self.assertIn('APPEND_SYSTEM.md', (role / 'AGENTS.md').read_text())
        self.assertIn('session ready', stdout)
        self.assertNotIn('model access verified', stdout)

    def test_project_system_prompt_blocks_init_and_watch_without_modifying_instructions(self):
        # Arrange: AgentShell cannot retain a project SYSTEM.md while excluding the home one.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        project_prompt = repo / '.factory/agents/foreman/.pi/SYSTEM.md'
        project_prompt.parent.mkdir()
        project_prompt.write_text('Keep these repository instructions unchanged.\n')
        self.log.unlink()
        self.state.write_text('{}')
        # Act
        watch = self.watch(repo)
        watch_calls = events(self.log)
        watch_state = json.loads(self.state.read_text())
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        for result in (watch,):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('.pi/SYSTEM.md', result.stderr)
            self.assertIn('AgentShell', result.stderr)
            self.assertIn('AGENTS.md', result.stderr)
        self.assertEqual(watch_calls, [])
        self.assertEqual(watch_state, {})
        self.assertEqual(events(self.log), [])
        self.assertEqual(project_prompt.read_text(),
                         'Keep these repository instructions unchanged.\n')
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})

    def test_unlisted_explicit_model_cannot_complete_setup_or_watch(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  available  128000  8192  yes  yes')
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.state.write_text('{}')
        self.log.unlink()
        watch = self.watch(repo)
        # Assert
        self.assertNotEqual(setup.returncode, 0)
        self.assertIn('not selectable', setup.stderr)
        self.assertIn('provider/available', setup.stdout)
        self.assertIn('run init first', watch.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual(events(self.log), [])

    def test_default_native_home_comes_from_home_when_environment_is_unset(self):
        # Arrange
        repo = self.repo()
        self.env.pop('PI_CODING_AGENT_DIR')
        self.env['HOME'] = str(self.workspace / 'disposable home')
        native = Path(self.env['HOME']) / '.pi/agent'
        (native / 'extensions').mkdir(parents=True)
        (native / 'extensions/agentshell.json').write_text('{"max_sub_agent_depth":1}')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        choice = json.loads((repo / '.factory/pi-profile.json').read_text())
        self.assertEqual(choice['agent_directory'], self.env['HOME'] + '/.pi/agent')
        self.assertFalse((repo / '.factory/agents/foreman/auth.json').exists())

    def test_managed_pi_metadata_probe_uses_saved_home_without_auth_commands(self):
        # Arrange: installation and Pi are external command doubles.
        import shutil
        import sys

        from profile_support import INSTALLER
        repo = self.repo()
        chosen = str(self.workspace / 'chosen native home')
        (Path(chosen) / 'extensions').mkdir(parents=True)
        (Path(chosen) / 'extensions/agentshell.json').write_text('{"max_sub_agent_depth":1}')
        (self.bin / 'pi').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        npm = self.bin / 'npm'
        npm.write_text(INSTALLER)
        npm.chmod(0o755)
        self.env.update(PATH=str(self.bin), FORGETFUL_TOKEN='TOP_SECRET')
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--pi-agent-dir', chosen, input='y\n')
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        calls = [e for e in events(self.log) if e['name'] == 'pi']
        self.assertTrue(any(e['args'] == ['--version'] for e in calls))
        for call in calls:
            self.assertEqual(call['agent_dir'], chosen)
            self.assertFalse(call['has_token'])
        self.log.unlink()
        self.env['PI_CODING_AGENT_DIR'] = str(self.workspace / 'different native home')
        # Act: startup may check the managed executable version, never auth or model discovery.
        self.watch(repo)
        # Assert
        calls = [e for e in events(self.log) if e['name'] == 'pi']
        self.assertEqual([e['args'] for e in calls], [['--version']])
        self.assertEqual(calls[0]['agent_dir'], chosen)
        self.assertFalse(calls[0]['has_token'])
