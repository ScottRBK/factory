"""Setup recovery through the public CLI; package managers are external command doubles."""
import json
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture


class ProfileRecoveryTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.log = self.workspace / 'install.jsonl'
        self.env['PROFILE_INSTALL_LOG'] = str(self.log)

    def test_partial_role_install_is_retried_and_deleted_package_is_repaired(self):
        # Arrange: uv creates the environment but fails before installing its package.
        repo = self.repo()
        self.env['PROFILE_INSTALL_FAIL'] = 'sync'
        # Act
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        del self.env['PROFILE_INSTALL_FAIL']
        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(len(events(self.log)), 2)
        # Arrange: installed package was subsequently removed.
        package = repo / '.factory/agents/foreman/resources/agentshell/python/.venv/bin'
        (package / '.fixture-package').unlink()
        # Act
        repaired = self.run_cli(repo)
        unchanged = self.run_cli(repo)
        # Assert
        self.assertEqual(repaired.returncode, 0, repaired.stderr)
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
        self.assertEqual(len(events(self.log)), 3)

    def test_edited_role_lock_is_preserved_but_does_not_authorize_unreviewed_install(self):
        # Arrange
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(result.returncode, 0, result.stderr)
        lock = repo / '.factory/agents/foreman/resources/agentshell/python/uv.lock'
        edited = lock.read_text() + '\n# User edit\n'
        lock.write_text(edited)
        # Act
        retry = self.run_cli(repo)
        # Assert
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('lock', retry.stderr.lower())
        self.assertEqual(lock.read_text(), edited)
        self.assertEqual(len(events(self.log)), 1)

    def test_managed_forgetful_partial_install_cannot_be_accepted_on_retry(self):
        # Arrange: partial managed install shadows an otherwise available host executable.
        repo = self.repo()
        managed = repo / '.factory/runtime/forgetful/bin/forgetful'
        managed.parent.mkdir(parents=True)
        managed.write_text((self.bin / 'forgetful').read_text())
        managed.chmod(0o755)
        self.env['PROFILE_INSTALL_FAIL'] = 'pip'
        # Act
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertFalse((managed.parent.parent / '.factory-sync').exists())
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
        # Arrange
        del self.env['PROFILE_INSTALL_FAIL']
        # Act
        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual([e['args'][0] for e in events(self.log)],
                         ['venv', 'pip', 'venv', 'pip', 'sync'])

    def watch(self, repo):
        import subprocess
        return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                               '--workspace', str(repo), '--new-only'], cwd=repo, env=self.env,
                              capture_output=True, text=True, timeout=5)

    def install_terminal_double(self):
        from test_watch import SHELL, TMUX
        package = self.workspace / 'external/agent_shell'
        (package / 'models').mkdir(parents=True)
        (package / '__init__.py').write_text('')
        (package / 'shell.py').write_text(SHELL)
        (package / 'tmux.py').write_text(TMUX)
        (package / 'models/__init__.py').write_text('')
        (package / 'models/resources.py').write_text(
            'class SessionResources:\n'
            '    def __init__(self, **kwargs): self.__dict__.update(kwargs)\n')
        (package / 'models/agent.py').write_text('class AgentType:\n    PI = "pi"\n')
        self.terminal_log = self.workspace / 'terminal.jsonl'
        self.env.update(PYTHONPATH=str(package.parent) + ':' + self.env['PYTHONPATH'],
                        WATCH_TERMINAL_LOG=str(self.terminal_log), WATCH_EXIT_DELAY='0.1')

    def test_native_cli_setup_needs_no_wrapper_and_preserves_old_user_files(self):
        # Arrange
        self.install_terminal_double()
        repo = self.repo()
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--forgetful-method', 'cli')
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        old_files = (role / 'bin/factory-forgetful', role / 'resources/forgetful_cli.py',
                     role / 'resources/factory-status.ts')
        for path in old_files:
            self.assertFalse(path.exists())
        # Arrange: existing edited resources belong to the user, including old generated files.
        for path in old_files:
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(b'User content\xff')
        settings = role / 'resources.json'
        custom = json.loads(settings.read_text())
        custom['extensions'].append('resources/factory-status.ts')
        settings.write_text(json.dumps(custom))
        # Act
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(json.loads(settings.read_text()), custom)
        for path in old_files:
            self.assertEqual(path.read_bytes(), b'User content\xff')
            path.unlink()
        # Act: old files are not factory launch prerequisites; the user refreshes Pi settings.
        custom['extensions'].remove('resources/factory-status.ts')
        settings.write_text(json.dumps(custom))
        self.assertEqual(self.run_cli(repo).returncode, 0)
        self.watch(repo)
        # Assert
        self.assertTrue(any(e['kind'] == 'launch' for e in events(self.terminal_log)))

    def skill_command(self, repo, fragment):
        import re
        skill = repo / '.factory/agents/foreman/skills/foreman/SKILL.md'
        commands = [code for code in re.findall(r'```bash\n(.*?)```', skill.read_text(), re.S)
                    if fragment in code]
        self.assertEqual(len(commands), 1, f'Missing/ambiguous native example: {fragment}')
        return ('set -e\n' + commands[0]
                + '\nprintf "CONFIG=%s\\nCWD=%s\\n" "$XDG_CONFIG_HOME" "$PWD"')

    def test_generated_skill_uses_native_local_and_remote_cli_in_launch_environment(self):
        # Arrange
        self.install_terminal_double()
        executable = self.bin / 'custom forgetful'
        executable.write_text((self.bin / 'forgetful').read_text())
        executable.chmod(0o755)
        log = self.workspace / 'native.jsonl'
        personal = str(self.workspace / 'personal config')
        self.env.update(PROFILE_LOG=str(log), XDG_CONFIG_HOME=personal,
                        FORGETFUL_TOKEN='TOP_SECRET', FORGETFUL_SERVER='https://personal.example',
                        DATABASE='Postgres', SQLITE_PATH='/wrong/personal.db')
        for instance in ('local', 'server'):
            with self.subTest(instance=instance):
                repo = self.repo('repo ' + instance)
                (repo / '.env').write_text('FORGETFUL_SERVER=https://repository.example\n')
                (repo / 'docker').mkdir()
                (repo / 'docker/.env').write_text('DATABASE=Postgres\n')
                extra = () if instance == 'local' else (
                    '--forgetful-server', 'https://memory.example/mcp', '--check-connection')
                setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                     '--forgetful-method', 'cli', '--forgetful-instance', instance,
                                     '--forgetful-executable', str(executable), *extra)
                self.assertEqual(setup.returncode, 0, setup.stderr)
                target = '--local' if instance == 'local' else '--server'
                self.env['WATCH_SKILL_COMMANDS'] = json.dumps([
                    self.skill_command(repo, 'project list ' + target)])
                log.unlink(missing_ok=True)
                # Act: run the generated example inside the controller's actual inherited env.
                self.watch(repo)
                # Assert
                calls = [e for e in events(log) if e['args'][:2] == ['project', 'list']]
                self.assertEqual(len(calls), 1)
                call = calls[0]
                expected = (['--local'] if instance == 'local' else
                            ['--server', 'https://memory.example/mcp'])
                self.assertEqual(call['args'], ['project', 'list', *expected, '--json'])
                self.assertEqual(call['configured_executable'], str(executable))
                self.assertEqual(call['cwd'], str(repo / '.factory/agents/foreman'))
                self.assertEqual(call['config_home'],
                                 str(repo / '.factory/agents/foreman/cli-config'))
                self.assertFalse(call['has_token'])
                self.assertEqual(call['server'], '' if instance == 'local'
                                 else 'https://memory.example/mcp')
                if instance == 'local':
                    self.assertEqual(call['database'], str(repo / '.factory/data/forgetful.db'))
                    self.assertEqual(call['database_type'], 'SQLite')
                command = next(e for e in events(self.terminal_log) if e['kind'] == 'skill-command')
                self.assertEqual(command['code'], 0)
                self.assertEqual(command['stdout'].splitlines()[-2:],
                                 ['CONFIG=' + personal,
                                  'CWD=' + str(repo / '.factory/agents/foreman')])
                self.terminal_log.unlink()

    def test_generated_skill_keeps_native_auth_arguments_and_role_config_isolation(self):
        # Arrange: only external CLI doubles are executed, including all auth commands.
        self.install_terminal_double()
        repo = self.repo()
        log = self.workspace / 'native-auth.jsonl'
        personal = str(self.workspace / 'personal config')
        self.env.update(PROFILE_LOG=str(log), XDG_CONFIG_HOME=personal,
                        FORGETFUL_TOKEN='TOP_SECRET')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--forgetful-method', 'cli', '--forgetful-instance', 'server',
                             '--forgetful-server', 'https://memory.example/mcp',
                             '--check-connection')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        log.unlink(missing_ok=True)
        self.env['WATCH_SKILL_COMMANDS'] = json.dumps([
            self.skill_command(repo, 'auth ' + operation)
            for operation in ('login', 'status', 'logout')])
        # Act
        self.watch(repo)
        # Assert
        calls = [e for e in events(log) if e['args'][:1] == ['auth']]
        self.assertEqual([call['args'] for call in calls], [
            ['auth', 'login', '--server', 'https://memory.example/mcp'],
            ['auth', 'status'], ['auth', 'logout']])
        for call in calls:
            self.assertEqual(call['configured_executable'], 'forgetful')
            self.assertEqual(call['config_home'],
                             str(repo / '.factory/agents/foreman/cli-config'))
            self.assertFalse(call['has_token'])
            self.assertEqual(call['cwd'], str(repo / '.factory/agents/foreman'))
            self.assertEqual(call['server'], 'https://memory.example/mcp')
        for command in (e for e in events(self.terminal_log) if e['kind'] == 'skill-command'):
            self.assertEqual(command['code'], 0)
            self.assertEqual(command['stdout'].splitlines()[-2:],
                             ['CONFIG=' + personal, 'CWD=' + str(repo / '.factory/agents/foreman')])

    def test_local_native_auth_overrides_saved_remote_default_with_empty_server(self):
        # Arrange: status/logout have no --local flag; process env must defeat saved defaults.
        self.install_terminal_double()
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--forgetful-method', 'cli')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        saved = role / 'cli-config/forgetful/.env'
        saved.parent.mkdir(parents=True, exist_ok=True)
        saved.write_text('FORGETFUL_SERVER=https://previous.example/mcp\n')
        log = self.workspace / 'native-local-auth.jsonl'
        self.env.update(PROFILE_LOG=str(log), FORGETFUL_SERVER='https://personal.example')
        self.env['WATCH_SKILL_COMMANDS'] = json.dumps([
            self.skill_command(repo, 'auth ' + operation) for operation in ('status', 'logout')])
        # Act
        self.watch(repo)
        # Assert
        calls = [e for e in events(log) if e['args'][:1] == ['auth']]
        self.assertEqual([call['args'] for call in calls], [['auth', 'status'], ['auth', 'logout']])
        for call in calls:
            self.assertEqual(call['server'], '')
            self.assertEqual(call['cwd'], str(role))
            self.assertEqual(call['config_home'], str(role / 'cli-config'))
        self.assertEqual(saved.read_text(), 'FORGETFUL_SERVER=https://previous.example/mcp\n')

    def test_edited_relative_cli_path_resolves_before_init_check_and_skill_change_directory(self):
        # Arrange: user-edited configuration uses a workspace-relative path containing spaces.
        self.install_terminal_double()
        repo = self.repo('repo space')
        executable = self.bin / 'custom forgetful'
        executable.write_text((self.bin / 'forgetful').read_text())
        executable.chmod(0o755)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--forgetful-method', 'cli')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = repo / '.factory/factory.toml'
        edited = config.read_text().replace('executable = "forgetful"',
                                           'executable = "../bin/custom forgetful"')
        config.write_text(edited)
        log = self.workspace / 'relative-native.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['WATCH_SKILL_COMMANDS'] = json.dumps([
            self.skill_command(repo, 'project list --local')])
        # Act
        retry = self.run_cli(repo)
        self.watch(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        calls = [e for e in events(log) if e['name'] != 'pi']
        self.assertGreaterEqual(len(calls), 2)
        for call in calls:
            self.assertEqual(call['name'], 'custom forgetful')
            self.assertEqual(call['configured_executable'], str(executable))
            self.assertEqual(call['cwd'], str(repo / '.factory/agents/foreman'))
            self.assertEqual(call['server'], '')
        self.assertEqual(config.read_text(), edited)

    def missing_pi(self):
        import shutil

        from profile_support import INSTALLER

        self.install_terminal_double()
        (self.bin / 'pi').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        npm = self.bin / 'npm'
        npm.write_text(INSTALLER)
        npm.chmod(0o755)
        self.env['PATH'] = str(self.bin)

    def test_partial_managed_pi_install_blocks_retry_and_watch_until_sync_succeeds(self):
        # Arrange: a complete role must not hide a later partial managed Pi installation.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.missing_pi()
        self.env['PROFILE_INSTALL_FAIL'] = 'ci'
        # Act
        failed = self.run_cli(repo, input='y\n')
        retry = self.run_cli(repo, input='y\n')
        watch = self.watch(repo)
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertNotEqual(retry.returncode, 0)
        self.assertEqual([e['args'][0] for e in events(self.log)], ['sync', 'ci', 'ci'])
        self.assertIn('rerun init', watch.stderr)
        self.assertEqual(events(self.terminal_log), [])
        # Act
        del self.env['PROFILE_INSTALL_FAIL']
        repaired = self.run_cli(repo, input='y\n')
        unchanged = self.run_cli(repo)
        self.watch(repo)
        # Assert
        self.assertEqual(repaired.returncode, 0, repaired.stderr)
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
        self.assertEqual([e['args'][0] for e in events(self.log)], ['sync', 'ci', 'ci', 'ci'])
        self.assertTrue(any(e['kind'] == 'launch' for e in events(self.terminal_log)))

    def test_managed_pi_rejects_changed_install_inputs_and_a_broken_executable(self):
        # Arrange
        self.missing_pi()
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        runtime = repo / '.factory/runtime/pi'
        for relative in ('package.json', 'package-lock.json', 'node_modules/.bin/pi'):
            with self.subTest(changed=relative):
                path = runtime / relative
                original = path.read_bytes()
                changed = b'#!/bin/sh\nexit 9\n' if path.name == 'pi' else original + b'\n'
                path.write_bytes(changed)
                try:
                    # Act
                    watch = self.watch(repo)
                    # Assert
                    self.assertIn('rerun init', watch.stderr)
                    self.assertEqual(events(self.terminal_log), [])
                    self.assertEqual(path.read_bytes(), changed)
                finally:
                    path.write_bytes(original)
                    self.terminal_log.unlink(missing_ok=True)

    def test_failed_and_declined_setup_block_watch_then_successful_retry_launches(self):
        # Arrange
        self.install_terminal_double()
        for outcome in ('declined', 'failed'):
            with self.subTest(outcome=outcome):
                repo = self.repo(outcome)
                self.env['PROFILE_INSTALL_FAIL'] = 'sync' if outcome == 'failed' else ''
                # Act
                setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                     input='n\n', role_defaults=outcome == 'failed')
                watch = self.watch(repo)
                # Assert
                self.assertNotEqual(setup.returncode, 0)
                self.assertIn('run init first', watch.stderr)
                self.assertEqual(events(self.terminal_log), [])
                # Act
                self.env.pop('PROFILE_INSTALL_FAIL')
                retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
                self.watch(repo)
                # Assert
                self.assertEqual(retry.returncode, 0, retry.stderr)
                self.assertTrue(any(e['kind'] == 'launch' for e in events(self.terminal_log)))
                self.terminal_log.unlink()

    def test_watch_rejects_missing_resources_and_target_drift_without_changing_files(self):
        # Arrange
        self.install_terminal_double()
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        for relative in ('resources.json', 'resources/hide-tools/index.ts',
                         'skills/foreman/SKILL.md', 'resources/agentshell/python/uv.lock',
                         'resources/agentshell/python/.venv/bin/.fixture-package',
                         'resources/agentshell/python/.venv/pyvenv.cfg',
                         'resources/agentshell/python/.venv/.factory-sync', 'model-selection.json'):
            with self.subTest(missing=relative):
                path = role / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    # Act
                    watch = self.watch(repo)
                    # Assert
                    self.assertIn('rerun init', watch.stderr)
                    self.assertFalse(path.exists())
                    self.assertEqual(events(self.terminal_log), [])
                finally:
                    path.write_bytes(original)
                    self.terminal_log.unlink(missing_ok=True)
        # Arrange
        config = repo / '.factory/factory.toml'
        config.write_text(config.read_text().replace('provider/model', 'provider/other'))
        original = (role / 'model-selection.json').read_bytes()
        # Act
        watch = self.watch(repo)
        # Assert
        self.assertIn('model setup', watch.stderr)
        self.assertEqual(events(self.terminal_log), [])
        self.assertEqual((role / 'model-selection.json').read_bytes(), original)

    def test_remote_checked_setup_rechecks_planning_without_explicit_auth_login(self):
        # Arrange
        self.install_terminal_double()
        repo = self.repo()
        commands = self.workspace / 'commands.jsonl'
        self.env['PROFILE_LOG'] = str(commands)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--forgetful-instance', 'server',
                             '--forgetful-server', 'https://memory.example/mcp',
                             '--check-connection')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        commands.unlink()
        # Act
        self.watch(repo)
        # Assert
        self.assertTrue(any(e['kind'] == 'launch' for e in events(self.terminal_log)))
        calls = events(commands)
        self.assertTrue(any(e['args'][:2] == ['call', 'get_project'] for e in calls))
        self.assertFalse(any(e['args'][:2] == ['auth', 'login'] for e in calls))

    def test_reinit_preserves_stricter_ignores_and_does_not_duplicate_managed_block(self):
        # Arrange
        repo = self.repo()
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(first.returncode, 0, first.stderr)
        ignore = repo / '.factory/.gitignore'
        original = ignore.read_text()
        custom = original + '\n# My stricter policy\n/agents/*/mcp.json\n'
        ignore.write_text(custom)
        # Act
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(ignore.read_text(), custom)
        self.assertEqual(original.count('/runtime/'), 1)
        for relative in ('mcp.json', 'auth.json', 'mcp-auth.json',
                         'resources/agentshell/python/.venv/.factory-sync'):
            self.assertEqual(self.git(repo, 'check-ignore', '.factory/agents/foreman/' + relative),
                             '.factory/agents/foreman/' + relative)

    def test_old_mcp_and_native_settings_are_preserved_while_role_selection_is_separate(self):
        # Arrange
        self.install_terminal_double()
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        project = repo / '.pi'
        project.mkdir()
        originals = {project / 'settings.json': '{"skills": ["./skills"]}',
                     project / 'mcp.json': '{"mcpServers": {"old": {"command": "old-tool"}}}',
                     repo / '.factory/agents/foreman/settings.json': '{"custom": true}'}
        for path, value in originals.items():
            path.write_text(value)
        # Act
        self.watch(repo)
        # Assert
        self.assertTrue(any(e['kind'] == 'launch' for e in events(self.terminal_log)))
        for path, value in originals.items():
            self.assertEqual(path.read_text(), value)

    def test_role_install_has_its_own_uv_workspace_boundary(self):
        # Arrange
        import tomllib
        repo = self.repo()
        parent = repo / 'pyproject.toml'
        parent.write_text('[tool.uv.workspace]\nmembers = [".factory/agents/foreman/resources/'
                          'agentshell/python"]\n')
        original = parent.read_bytes()
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert: uv receives a standalone project, independent of repository workspace sources.
        self.assertEqual(setup.returncode, 0, setup.stderr)
        sync = [e for e in events(self.log) if e['args'][0] == 'sync'][0]
        metadata = tomllib.loads(sync['project_metadata'])
        self.assertEqual(metadata['tool']['uv'].get('workspace'), {'members': []})
        self.assertEqual(parent.read_bytes(), original)

    def test_pi_model_store_is_ignored_but_editable_role_settings_are_available(self):
        # Arrange
        import subprocess
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = '.factory/agents/foreman/'
        # Act / Assert
        self.assertEqual(self.git(repo, 'check-ignore', role + 'models-store.json'),
                         role + 'models-store.json')
        result = subprocess.run(['git', '-C', str(repo), 'check-ignore', role + 'resources.json'],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_pi_trust_crash_and_download_state_are_ignored(self):
        # Arrange
        import subprocess
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        paths = ['.factory/agents/foreman/' + relative for relative in
                 ('trust.json', 'crashes.json', 'tmp/session', 'tools/tool',
                  'npm/package', 'git/checkout')]
        # Act
        result = subprocess.run(['git', '-C', str(repo), 'check-ignore', *paths],
                                capture_output=True, text=True)
        # Assert
        self.assertEqual(result.stdout.splitlines(), paths)

    def test_consented_nonroot_tmux_install_uses_stdin_for_sudo_authentication(self):
        # Arrange
        import os
        import platform
        import shutil

        from profile_support import COMMAND
        release = platform.freedesktop_os_release()
        if (os.geteuid() == 0 or release.get('ID') != 'ubuntu'
                or release.get('VERSION_ID') != '24.04'):
            self.skipTest('Reviewed non-root tmux recipe requires Ubuntu 24.04')
        repo = self.repo()
        (self.bin / 'tmux').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        apt = self.bin / 'apt-get'
        apt.write_text('#!/bin/sh\necho "0 upgraded, 1 newly installed, 0 to remove"\n')
        apt.chmod(0o755)
        sudo_log = self.workspace / 'sudo.json'
        sudo = self.bin / 'sudo'
        sudo.write_text(f'#!{sys.executable}\nimport json,sys\nfrom pathlib import Path\n'
                        f'Path({str(sudo_log)!r}).write_text(json.dumps(sys.argv[1:]))\n'
                        f'p=Path({str(self.bin / "tmux")!r})\n'
                        f'p.write_text({COMMAND!r})\np.chmod(0o755)\n')
        sudo.chmod(0o755)
        self.env['PATH'] = str(self.bin)
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertEqual(json.loads(sudo_log.read_text())[:2], ['--stdin', 'apt-get'])
