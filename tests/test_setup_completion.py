"""Completion and profile compatibility through the public init/watch CLI."""
import json
import subprocess
import sys
from pathlib import Path

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture


class SetupCompletionTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(self.log)

    def assert_watch_stopped(self, repo, message):
        self.state.write_text('{}')
        self.log.unlink(missing_ok=True)
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(repo),
             '--new-only'], cwd=repo, env=self.env, capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual(events(self.log), [])

    def test_failed_local_check_never_completes_fresh_setup(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
        self.assert_watch_stopped(repo, 'incomplete')

    def test_connection_drift_blocks_watch_until_successful_recheck(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        # Act / Assert: each connection field contributes to completion evidence.
        for old, new in [('forgetful.db', 'other.db'),
                         ('executable = "forgetful"', 'executable = "other-forgetful"'),
                         ('instance = "local"',
                          'instance = "server"\nserver = "https://memory.example/mcp"')]:
            with self.subTest(change=new):
                changed = original.replace(old, new)
                if old == 'instance = "local"':
                    changed = '\n'.join(line for line in changed.splitlines()
                                        if not line.startswith('database = ')) + '\n'
                path.write_text(changed)
                self.assert_watch_stopped(repo, 'incomplete or changed')

    def test_failed_reinitialization_invalidates_previous_completion(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        self.assertTrue((role / 'model-selection.json').is_file())
        self.env['PROFILE_FAIL'] = 'forgetful'
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((role / 'model-selection.json').exists())
        self.assert_watch_stopped(repo, 'incomplete')

    def test_failed_automatic_server_check_has_no_completion_receipt(self):
        for failure in ('login', 'permission', 'external_ref'):
            with self.subTest(failure=failure):
                # Arrange
                repo = self.repo(failure)
                self.env['PROFILE_PLANNING_FAILURE'] = failure
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      '--forgetful-instance', 'server', '--forgetful-server',
                                      'https://memory.example/mcp')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Forgetful planning check failed', result.stderr)
                self.assertNotIn('TOP_SECRET', result.stdout + result.stderr)
                calls = [e for e in events(self.log) if e['name'] == 'forgetful']
                self.assertEqual(calls[0]['args'][:2], ['call', 'get_project'])
                self.assertTrue((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
                self.assert_watch_stopped(repo, 'incomplete')

    def test_interrupted_automatic_server_check_preserves_config_and_blocks_watch(self):
        # Arrange
        import os
        repo = self.repo()
        self.env['PROFILE_INTERRUPT'] = 'forgetful'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'server', '--forgetful-server',
                              'https://memory.example/mcp')
        # Assert
        self.assertEqual(result.returncode, 130, result.stderr)
        self.assertIn('interrupted', result.stderr)
        self.assertTrue((repo / '.factory/factory.toml').exists())
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
        call = events(self.log)[-1]
        self.assertEqual(call['args'][:2], ['call', 'get_project'])
        with self.assertRaises(ProcessLookupError):
            os.kill(call['pid'], 0)
        self.assert_watch_stopped(repo, 'incomplete')

    def test_successful_rerun_replaces_generated_receipt_without_touching_linked_snapshot(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        previous = self.workspace / 'previous-receipt.json'
        previous.hardlink_to(receipt)
        original = previous.read_bytes()
        config = repo / '.factory/factory.toml'
        config.write_text(config.read_text().replace('foreman_agent_model = "provider/model"',
                                                 'foreman_agent_model = "provider/next"'))
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  next  128000  8192  yes  yes\n'
            'provider  model  128000  8192  yes  yes')
        # An external check can leave an older generated receipt. Completion replaces it.
        command = self.bin / 'forgetful'
        command.write_text(command.read_text() + '\nfrom pathlib import Path\n'
                           + f'Path({str(receipt)!r}).write_text("{{}}")\n')
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(receipt.read_text())['model'], 'provider/next')
        self.assertEqual(previous.read_bytes(), original)
        self.assertEqual(receipt.stat().st_mode & 0o777, 0o600)

    def test_symlinked_receipt_is_refused_without_following_or_replacing_it(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        target = self.workspace / 'keep-receipt.json'
        receipt.rename(target)
        original = target.read_bytes()
        receipt.symlink_to(target)
        # Act / Assert
        self.assert_watch_stopped(repo, 'symlink')
        retry = self.run_cli(repo)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('symlink', retry.stderr)
        self.assertTrue(receipt.is_symlink())
        self.assertEqual(target.read_bytes(), original)

    def test_restored_legacy_skill_requires_manual_reconciliation_and_is_preserved(self):
        # Arrange: restore the old shipped skill, as an existing installation can do.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        path = role / 'skills/foreman/SKILL.md'
        old = (Path(__file__).parent / 'fixtures/legacy_foreman_skill.md').read_bytes()
        path.write_bytes(old)
        # Act / Assert
        self.assert_watch_stopped(repo, 'manual reconciliation')
        retry = self.run_cli(repo)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('manual reconciliation', retry.stderr)
        self.assertIn('skills/foreman/SKILL.md', retry.stderr)
        self.assertEqual(path.read_bytes(), old)
        self.assertFalse((role / 'model-selection.json').exists())
        self.assertEqual(events(self.log), [])
        self.assert_watch_stopped(repo, 'manual reconciliation')

    def test_obsolete_role_prompt_commands_require_manual_reconciliation(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/foreman/APPEND_SYSTEM.md'
        original = path.read_text()
        for command in ('XDG_CONFIG_HOME="${PI_CODING_AGENT_DIR}/cli-config" forgetful auth status',
                        'Use `/mcp login forgetful` when asked to sign in.',
                        'Run `pi mcp login forgetful` to sign in.',
                        'cd "$PI_CODING_AGENT_DIR" && forgetful project list --local --json'):
            with self.subTest(command=command):
                path.write_text(command)
                # Act / Assert
                self.assert_watch_stopped(repo, 'manual reconciliation')
                retry = self.run_cli(repo)
                self.assertNotEqual(retry.returncode, 0)
                self.assertIn('APPEND_SYSTEM.md', retry.stderr)
                self.assertEqual(path.read_text(), command)
                self.assertEqual(events(self.log), [])
                path.write_text(original)
                setup = self.run_cli(repo)
                self.assertEqual(setup.returncode, 0, setup.stderr)

    def test_unlisted_supplied_model_changes_no_config_or_labels_and_can_be_corrected(self):
        # Arrange
        repo = self.repo()
        settings = list(INIT_SETTINGS)
        settings[settings.index('--foreman-model') + 1] = 'provider/missing'
        # Act
        failed = self.run_cli(repo, '--repo', '.', *settings)
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('not selectable', failed.stderr)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
        self.assertEqual([e['args'] for e in events(self.log) if e['name'] == 'pi'],
                         [['--no-approve', '--list-models']])
        # Act: correct the supplied value without manually repairing a saved config.
        self.log.unlink()
        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual([e['args'] for e in events(self.log) if e['name'] == 'pi'],
                         [['--no-approve', '--list-models']])

    def test_missing_explicit_pi_home_is_rejected_before_pi_or_writes(self):
        # Arrange
        repo = self.repo()
        chosen = self.workspace / 'misspelled home'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--pi-agent-dir', str(chosen))
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('native Pi', result.stderr)
        self.assertIn('/login', result.stderr)
        self.assertIn(str(chosen), result.stderr)
        self.assertEqual(events(self.log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertFalse((repo / '.factory').exists())
        self.assertFalse(chosen.exists())

    def test_missing_default_home_allows_consented_install_but_never_invokes_pi(self):
        # Arrange: installer and Pi remain external-command doubles.
        import shutil

        from profile_support import INSTALLER
        repo = self.repo()
        self.env.pop('PI_CODING_AGENT_DIR')
        self.env['HOME'] = str(self.workspace / 'new native user')
        (self.bin / 'pi').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        npm = self.bin / 'npm'
        npm.write_text(INSTALLER)
        npm.chmod(0o755)
        install_log = self.workspace / 'install.jsonl'
        self.env.update(PATH=str(self.bin), PROFILE_INSTALL_LOG=str(install_log))
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('/login', result.stderr)
        self.assertIn('incomplete', result.stderr)
        self.assertIn(str(repo / '.factory/runtime/pi/node_modules/.bin/pi'), result.stderr)
        self.assertTrue(any(e['name'] == 'npm' for e in events(install_log)))
        self.assertFalse(any(e['name'] == 'pi' for e in events(self.log)))
        self.assertFalse((Path(self.env['HOME']) / '.pi/agent').exists())
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

    def test_mistyped_environment_home_explains_how_to_reset_saved_consent(self):
        # Arrange
        repo = self.repo()
        self.env['PI_CODING_AGENT_DIR'] = str(self.workspace / 'mistyped native home')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('pi-profile.json', result.stderr)
        self.assertIn('PI_CODING_AGENT_DIR', result.stderr)
        self.assertIn('saved consent', result.stderr)
        self.assertFalse(any(e['name'] == 'pi' for e in events(self.log)))
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

    def test_non_utf8_role_guidance_is_cleanly_rejected_and_preserved(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/foreman/APPEND_SYSTEM.md'
        path.write_bytes(b'Instructions\xff')
        # Act / Assert
        self.assert_watch_stopped(repo, 'valid UTF-8')
        retry = self.run_cli(repo)
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('valid UTF-8', retry.stderr)
        self.assertIn('APPEND_SYSTEM.md', retry.stderr)
        self.assertNotIn('Traceback', retry.stderr)
        self.assertEqual(path.read_bytes(), b'Instructions\xff')
        self.assertEqual(events(self.log), [])

    def test_generated_profile_metadata_is_git_ignored(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('pi-profile.json', 'model-selection.json'):
            with self.subTest(name=name):
                path = '.factory/agents/foreman/' + name
                ignored = subprocess.run(['git', '-C', str(repo), 'check-ignore', path],
                                         text=True, capture_output=True)
                self.assertEqual(ignored.returncode, 0, ignored.stderr)
                self.assertEqual(ignored.stdout.strip(), path)

    def test_malformed_persisted_json_is_cleanly_rejected_without_launch_or_poll(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        for name, message in (('pi-profile.json', 'consent'),
                              ('model-selection.json', 'incomplete'),
                              ('resources.json', 'resources.json')):
            path = role / name
            original = path.read_bytes()
            for malformed in (b'{broken', b'null', b'[]', b'{"agent_directory": []}', b'\xff'):
                with self.subTest(name=name, malformed=malformed):
                    path.write_bytes(malformed)
                    # Act / Assert
                    self.assert_watch_stopped(repo, message)
                    self.assertEqual(path.read_bytes(), malformed)
                    if name != 'model-selection.json':
                        retry = self.run_cli(repo)
                        self.assertNotEqual(retry.returncode, 0)
                        self.assertNotIn('Traceback', retry.stderr)
                        self.assertEqual(path.read_bytes(), malformed)
                        path.write_bytes(original)
                        setup = self.run_cli(repo)
                        self.assertEqual(setup.returncode, 0, setup.stderr)
            path.write_bytes(original)

    def test_conflicting_arguments_preserve_completion_but_preflight_failure_invalidates_it(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        original = receipt.read_bytes()
        for args in (('--foreman-model', 'provider/other'),
                     ('--forgetful-database', str(self.workspace / 'other.db')),
                     ('--pi-agent-dir', str(self.workspace / 'other home'))):
            with self.subTest(args=args):
                self.log.unlink(missing_ok=True)
                self.state.write_text('{}')
                # Act
                result = self.run_cli(repo, *args)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('conflict', result.stderr)
                self.assertEqual(receipt.read_bytes(), original)
                self.assertEqual(events(self.log), [])
                self.assertEqual(json.loads(self.state.read_text()), {})
        # Arrange: a genuine re-init must invalidate completion even before external checks finish.
        self.state.write_text(json.dumps({'denied': 'team/app'}))
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(receipt.exists())
        self.assert_watch_stopped(repo, 'incomplete')

    def test_completion_refuses_symlink_created_during_external_check(self):
        # Arrange
        repo = self.repo()
        target = self.workspace / 'untouched.json'
        target.write_text('Keep this file')
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        command = self.bin / 'forgetful'
        command.write_text(command.read_text() + '\nfrom pathlib import Path\n'
                           + f'if not Path({str(receipt)!r}).is_symlink():\n'
                           + f'    Path({str(receipt)!r}).symlink_to({str(target)!r})\n')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlink', result.stderr)
        self.assertEqual(target.read_text(), 'Keep this file')
        self.assertTrue(receipt.is_symlink())
        self.assert_watch_stopped(repo, 'symlink')

    def test_changed_server_requires_successful_automatic_recheck_on_every_init(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--forgetful-instance', 'server', '--forgetful-server',
                             'https://memory.example/mcp', '--check-connection')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = repo / '.factory/factory.toml'
        config.write_text(config.read_text().replace('memory.example', 'other.example'))
        # Act / Assert
        self.assert_watch_stopped(repo, 'incomplete or changed')
        checked = self.run_cli(repo, connection_defaults=False)
        self.assertEqual(checked.returncode, 0, checked.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        self.assertEqual(json.loads(receipt.read_text())['forgetful']['server'],
                         'https://other.example/mcp')
        self.log.unlink()
        retry = self.run_cli(repo, connection_defaults=False)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        calls = [e for e in events(self.log) if e['name'] == 'forgetful']
        self.assertEqual(calls[0]['args'][:2], ['call', 'get_project'])
        self.assertTrue(receipt.exists())
        self.env['PROFILE_FAIL'] = 'forgetful'
        failed = self.run_cli(repo, connection_defaults=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('Forgetful planning check failed', failed.stderr)
        self.assertFalse(receipt.exists())
        self.assert_watch_stopped(repo, 'incomplete')
