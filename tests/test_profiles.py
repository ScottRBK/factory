import json

from profile_support import INSTALLER, events, install_commands
from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration


class ProfileTests(InitFixture):
    def setUp(self):
        super().setUp()
        install_commands(self.bin)
        self.log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(self.log)

    def test_init_defaults_to_shared_local_cli_and_installs_editable_foreman(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        connection = load_configuration(repo).forgetful
        self.assertEqual(connection.method, 'cli')
        self.assertEqual(connection.database, str(repo / '.factory/data/forgetful.db'))
        profile = repo / '.factory/agents/foreman'
        document = json.loads((profile / 'agent.json').read_text())
        settings = document['agent']['resources']
        self.assertEqual(settings['skills'], ['./skills'])
        self.assertFalse((profile / 'mcp.json').exists())
        self.assertTrue((profile / 'skills/foreman/SKILL.md').is_file())
        self.assertIn('Additional Foreman guidance',
                      (profile / 'APPEND_SYSTEM.md').read_text())
        self.assertTrue((repo / '.factory/agents/feature-owner/AGENTS.md').exists())
        self.assertFalse((profile / 'auth.json').exists())
        self.assertFalse((profile / 'mcp-auth.json').exists())

    def test_reinit_preserves_edited_profile_and_connection(self):
        # Arrange
        repo = self.repo()
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--forgetful-instance', 'local')
        self.assertEqual(first.returncode, 0, first.stderr)
        profile = repo / '.factory/agents/foreman'
        original = (repo / '.factory/factory.toml').read_bytes()
        (profile / 'APPEND_SYSTEM.md').write_text('My edited Foreman instructions')
        document = json.loads((profile / 'agent.json').read_text())
        settings = document['agent']['resources']
        extra = repo / 'extra-skill'
        extra.mkdir()
        (extra / 'SKILL.md').write_text('My extra skill')
        settings['skills'].append(str(extra))
        (profile / 'agent.json').write_text(json.dumps(document))
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((repo / '.factory/factory.toml').read_bytes(), original)
        self.assertEqual((profile / 'APPEND_SYSTEM.md').read_text(),
                         'My edited Foreman instructions')
        self.assertEqual(json.loads((profile / 'agent.json').read_text()), document)

    def test_local_cli_uses_database_and_isolated_configuration(self):
        # Arrange
        repo = self.repo()
        self.env.update(DATABASE='Postgres', SQLITE_PATH='/wrong/personal.db',
                        FORGETFUL_SERVER='https://personal.example/mcp')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-method', 'cli', '--forgetful-instance', 'local')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Forgetful: connected', result.stdout)
        calls = [e for e in events(self.log) if e['name'] == 'forgetful']
        self.assertTrue(calls)
        self.assertEqual(calls[-1]['args'],
                         ['tools', 'list', '--local', '--json'])
        self.assertEqual(calls[-1]['database'], str(repo / '.factory/data/forgetful.db'))
        self.assertEqual(calls[-1]['database_type'], 'SQLite')
        self.assertEqual(calls[-1]['config_home'],
                         str(repo / '.factory/cli-config'))
        self.assertFalse((repo / '.factory/agents/foreman/mcp.json').exists())

    def test_failed_cli_check_never_claims_ready_and_can_be_retried(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        # Act
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertNotIn('Forgetful: connected', failed.stdout)
        self.assertNotIn('TOP_SECRET', failed.stdout + failed.stderr)
        self.assertIn('init --finalize', failed.stderr)
        self.assertTrue((repo / '.factory/factory.toml').exists())
        # Arrange
        del self.env['PROFILE_FAIL']
        # Act
        retry = self.run_cli(repo, '--finalize')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertIn('Forgetful: connected', retry.stdout)

    def test_explicit_mcp_init_is_rejected_before_external_effects(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--forgetful-method', 'mcp')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('MCP configuration is unsupported', result.stderr)
        self.assertEqual(events(self.log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})

    def test_remote_setup_checks_access_without_extra_flags_or_explicit_login(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'server',
                              '--forgetful-server', 'https://memory.example/custom-endpoint')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Checking Forgetful connection and planning access', result.stdout)
        self.assertNotIn('If your browser opens', result.stdout)
        calls = [e for e in events(self.log) if e['name'] == 'forgetful']
        self.assertEqual(calls[0]['args'][:2], ['call', 'get_project'])
        self.assertTrue(any(e['args'][:2] == ['call', 'get_project'] for e in calls))
        self.assertTrue(any(e['args'][:2] == ['tools', 'list'] for e in calls))
        self.assertFalse(any(e['args'][:2] == ['auth', 'login'] for e in calls))
        self.assertTrue(all(e['config_home'] == str(repo / '.factory/cli-config')
                            for e in calls))
        self.assertTrue((repo / '.factory/setup-complete.json').exists())

    def test_explicit_remote_login_uses_the_role_credentials_then_checks_connection(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'server',
                              '--forgetful-server', 'https://memory.example/custom-endpoint',
                              '--login')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [e for e in events(self.log) if e['name'] == 'forgetful']
        self.assertEqual(calls[0]['args'],
                         ['auth', 'login', '--server', 'https://memory.example/custom-endpoint'])
        self.assertEqual(calls[1]['args'][:2], ['call', 'get_project'])
        self.assertTrue(any(e['args'][:2] == ['tools', 'list'] for e in calls))
        self.assertTrue(all(e['config_home'] == str(repo / '.factory/cli-config')
                            for e in calls))

    def test_cli_login_failure_is_incomplete_and_never_changes_personal_defaults(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-method', 'cli', '--forgetful-instance', 'server',
                              '--forgetful-server', 'https://memory.example/custom-endpoint',
                              '--login')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        calls = [e for e in events(self.log) if e['name'] == 'forgetful']
        self.assertEqual(calls[0]['args'],
                         ['auth', 'login', '--server', 'https://memory.example/custom-endpoint'])
        self.assertEqual(calls[0]['config_home'],
                         str(repo / '.factory/cli-config'))
        self.assertNotIn('Forgetful: connected', result.stdout)
        self.assertIn('init --finalize', result.stderr)

    def test_role_extensions_are_installed_offline_and_preserved_on_rerun(self):
        # Arrange
        repo = self.repo()
        # Act
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--forgetful-instance', 'local')
        # Assert
        self.assertEqual(first.returncode, 0, first.stderr)
        profile = repo / '.factory/agents/foreman'
        document = json.loads((profile / 'agent.json').read_text())
        settings = document['agent']['resources']
        self.assertIn('../../resources/agentshell/extensions/agentshell.ts', settings['extensions'])
        self.assertIn('../../resources/hide-tools/index.ts', settings['extensions'])
        self.assertFalse(any('forgetful-extension' in item for item in settings['extensions']))
        extension = repo / '.factory/resources/hide-tools/index.ts'
        self.assertIn('hide-tools', extension.read_text())
        self.assertTrue((repo / '.factory/resources/agentshell/python/.venv/bin/python').exists())
        # Arrange
        extension.write_text('// my edited extension')
        # Act
        retry = self.run_cli(repo, '--finalize')
        # Assert
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('reconcile', retry.stderr)
        self.assertEqual(extension.read_text(), '// my edited extension')

    def test_runtime_credentials_logs_and_cli_state_are_git_ignored(self):
        # Arrange
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = '.factory/agents/foreman/'
        # Act
        ignored = self.git(repo, 'check-ignore',
                           *[profile + p for p in ('auth.json', 'mcp-auth.json', 'mcp.log',
                             'cli-config/forgetful/.env', 'sessions/session.jsonl')])
        # Assert
        self.assertEqual(len(ignored.splitlines()), 5)
        self.assertTrue((repo / '.factory/agents/foreman/agent.json').exists())

    def test_missing_executable_declined_or_unresolved_never_claims_complete(self):
        # Arrange
        repo = self.repo()
        for answer in ('n\n', 'y\n\n'):
            with self.subTest(answer=answer):
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      '--forgetful-instance', 'local',
                                      '--forgetful-executable', '/missing/forgetful', input=answer)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('missing', result.stderr.lower())
                self.assertIn('install', result.stdout.lower())
                self.assertNotIn('Forgetful: connected', result.stdout)

    def test_profile_includes_only_requested_third_party_extensions(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        profile = repo / '.factory/agents/foreman'
        document = json.loads((profile / 'agent.json').read_text())
        settings = document['agent']['resources']
        self.assertEqual(settings['extensions'], [
            '../../resources/agentshell/extensions/agentshell.ts',
            '../../resources/hide-tools/index.ts'])
        self.assertFalse((profile / 'resources/factory-status.ts').exists())
        self.assertTrue((profile / 'skills/foreman/SKILL.md').is_file())


    def test_changed_cli_target_uses_saved_config_and_preserves_old_mcp_file(self):
        # Arrange
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(result.returncode, 0, result.stderr)
        config = repo / '.factory/factory.toml'
        config.write_text(config.read_text().replace('data/forgetful.db', 'data/replacement.db'))
        mcp = repo / '.factory/agents/foreman/mcp.json'
        original = b'old edited MCP content'
        mcp.write_bytes(original)
        # Act
        result = self.run_cli(repo, '--finalize')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(events(self.log)[-1]['database'],
                         str(repo / '.factory/data/replacement.db'))
        self.assertEqual(mcp.read_bytes(), original)

    def test_custom_gitignore_keeps_edits_and_still_excludes_credentials(self):
        # Arrange
        repo = self.repo()
        ignore = repo / '.factory/.gitignore'
        ignore.parent.mkdir()
        ignore.write_text('# My custom exclusion\n/custom-cache/\n')
        # Act: the first setup adds necessary exclusions while preserving the user's policy.
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('/custom-cache/', ignore.read_text())
        self.assertEqual(self.git(repo, 'check-ignore', '.factory/agents/foreman/mcp-auth.json'),
                         '.factory/agents/foreman/mcp-auth.json')

    def test_profile_symlink_is_rejected_without_writing_through_it(self):
        # Arrange
        repo = self.repo()
        outside = self.workspace / 'outside'
        outside.mkdir()
        (repo / '.factory/agents').mkdir(parents=True)
        (repo / '.factory/agents/foreman').symlink_to(outside)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'local')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])

    def test_missing_pi_installer_requires_consent_and_failure_is_not_success(self):
        # Arrange
        repo = self.repo()
        (self.bin / 'pi').unlink()
        # Keep only test executables and necessary existing tools on PATH.
        import shutil
        import sys
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable),
                             ('node', shutil.which('node'))):
            (self.bin / name).symlink_to(target)
        npm = self.bin / 'npm'
        npm.write_text('#!/bin/sh\necho installer-failed >&2\nexit 9\n')
        npm.chmod(0o755)
        self.env['PATH'] = str(self.bin)
        # Act
        declined = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertNotEqual(declined.returncode, 0)
        self.assertIn('declined', declined.stderr.lower())
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('installation failed', failed.stderr.lower())
        self.assertNotIn('Forgetful: connected', failed.stdout)
        self.assertTrue((repo / '.factory/runtime/pi/package-lock.json').exists())

    def test_approved_workspace_install_uses_frozen_recipes_and_does_not_repeat(self):
        # Arrange
        import shutil
        import sys
        repo = self.repo()
        for name in ('pi', 'forgetful'):
            (self.bin / name).unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        for name in ('npm', 'uv'):
            manager = self.bin / name
            manager.write_text(INSTALLER)
            manager.chmod(0o755)
        log = self.workspace / 'install.jsonl'
        self.env.update(PATH=str(self.bin), PROFILE_INSTALL_LOG=str(log),
                        UV_NO_VERIFY_HASHES='1', UV_INDEX_URL='https://unreviewed.invalid',
                        NPM_CONFIG_IGNORE_SCRIPTS='false',
                        PIP_INDEX_URL='https://unreviewed.invalid',
                        NODE_OPTIONS='--invalid-option')
        # Act
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\ny\n')
        second = self.run_cli(repo)
        # Assert
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        calls = events(log)
        self.assertEqual(len(calls), 4)
        self.assertTrue(all(not call['node_options'] for call in calls))
        self.assertTrue(all(call['config_env'] == [] for call in calls[:3]))
        self.assertEqual(calls[3]['config_env'], ['UV_PROJECT_ENVIRONMENT'])
        self.assertEqual(calls[0]['args'],
                         ['ci', '--ignore-scripts', '--no-audit', '--no-fund', '--engine-strict',
                          '--userconfig=/dev/null', '--globalconfig=/dev/null',
                          '--registry=https://registry.npmjs.org'])
        self.assertIn('--no-python-downloads', calls[1]['args'])
        self.assertIn('--allow-existing', calls[1]['args'])
        self.assertEqual(calls[1]['args'][calls[1]['args'].index('--python') + 1],
                         str(self.bin / 'installed python3.12'))
        self.assertIn('--require-hashes', calls[2]['args'])
        self.assertIn('--only-binary', calls[2]['args'])
        self.assertIn(':all:', calls[2]['args'])
        self.assertTrue((repo / '.factory/runtime/forgetful/bin/forgetful').is_file())
        self.assertEqual(self.git(repo, 'check-ignore', '.factory/runtime/forgetful/bin/forgetful'),
                         '.factory/runtime/forgetful/bin/forgetful')

    def test_interactive_connection_defaults_choose_local_cli(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='\n\n',
                              connection_defaults=False)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(load_configuration(repo).forgetful.method, 'cli')
        self.assertEqual(load_configuration(repo).forgetful.instance, 'local')
        self.assertNotIn('Forgetful access [mcp', result.stdout)
        self.assertIn('Forgetful instance', result.stdout)

    def test_local_checks_default_to_offline_resources_and_do_not_import_bearer_tokens(self):
        # Arrange
        repo = self.repo()
        self.env['FORGETFUL_TOKEN'] = 'TOP_SECRET'
        self.env.pop('PI_OFFLINE', None)
        self.env.pop('HF_HUB_OFFLINE', None)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-method', 'cli')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        call = events(self.log)[-1]
        self.assertFalse(call['has_token'])
        self.assertEqual(call['pi_offline'], '1')
        self.assertEqual(call['models_offline'], '1')
        self.assertNotIn('TOP_SECRET', (repo / '.factory/factory.toml').read_text())

    def test_interrupted_login_leaves_retryable_setup_and_stops_auth_process(self):
        # Arrange
        import os
        repo = self.repo()
        self.env['PROFILE_INTERRUPT'] = 'forgetful'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-instance', 'server',
                              '--forgetful-server', 'https://memory.example/custom-endpoint',
                              '--login')
        # Assert
        self.assertEqual(result.returncode, 130, result.stderr)
        self.assertIn('incomplete', result.stderr)
        self.assertIn('init --finalize', result.stderr)
        self.assertNotIn('Forgetful: connected', result.stdout)
        self.assertTrue((repo / '.factory/factory.toml').exists())
        with self.assertRaises(ProcessLookupError):
            os.kill(events(self.log)[-1]['pid'], 0)

    def test_missing_tmux_offers_pinned_distro_install_and_reports_failure(self):
        # Arrange
        import platform
        import shutil
        import sys
        release = platform.freedesktop_os_release()
        if release.get('ID') != 'ubuntu' or release.get('VERSION_ID') != '24.04':
            self.skipTest('Automatic tmux recipe is audited for Ubuntu 24.04 only')
        repo = self.repo()
        (self.bin / 'tmux').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        for name in ('sudo', 'apt-get'):
            tool = self.bin / name
            tool.write_text('#!/bin/sh\nexit 9\n')
            tool.chmod(0o755)
        self.env['PATH'] = str(self.bin)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('tmux 3.4-1ubuntu0.1', result.stdout)
        self.assertIn('installation failed', result.stderr.lower())
        self.assertNotIn('Forgetful: connected', result.stdout)

    def test_tmux_install_refuses_an_apt_transaction_that_would_upgrade_dependencies(self):
        # Arrange
        import platform
        import shutil
        import sys
        release = platform.freedesktop_os_release()
        if release.get('ID') != 'ubuntu' or release.get('VERSION_ID') != '24.04':
            self.skipTest('Automatic tmux recipe is audited for Ubuntu 24.04 only')
        repo = self.repo()
        (self.bin / 'tmux').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        apt = self.bin / 'apt-get'
        apt.write_text('#!/bin/sh\necho "1 upgraded, 1 newly installed, 0 to remove"\n')
        apt.chmod(0o755)
        sudo = self.bin / 'sudo'
        sudo.write_text('#!/bin/sh\necho ACTUAL_INSTALL_ATTEMPT >&2\nexit 9\n')
        sudo.chmod(0o755)
        self.env['PATH'] = str(self.bin)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('upgrade', result.stderr)
        self.assertNotIn('Forgetful: connected', result.stdout)

    def test_relative_executable_path_is_saved_as_absolute_for_role_subprocesses(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-executable', '../bin/forgetful')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(load_configuration(repo).forgetful.executable, str(self.bin / 'forgetful'))

    def test_agentshell_runtime_install_is_consent_gated_and_uses_upstream_lock(self):
        # Arrange
        repo = self.repo()
        log = self.workspace / 'role-install.jsonl'
        self.env['PROFILE_INSTALL_LOG'] = str(log)
        # Act
        declined = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n',
                                role_defaults=False)
        approved = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                input='y\n', role_defaults=False)
        # Assert
        self.assertNotEqual(declined.returncode, 0)
        self.assertIn('declined', declined.stderr.lower())
        self.assertEqual(approved.returncode, 0, approved.stderr)
        calls = events(log)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]['args'][0], 'sync')
        for flag in ('--locked', '--no-build', '--no-dev', '--no-python-downloads', '--no-config'):
            self.assertIn(flag, calls[0]['args'])
        runtime = repo / '.factory/resources/agentshell/python/.venv'
        self.assertTrue((runtime / 'pyvenv.cfg').exists())

    def test_legacy_config_without_forgetful_is_rejected_before_any_external_effects(self):
        # Arrange
        repo = self.repo()
        initialized = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        path = repo / '.factory/factory.toml'
        old = path.read_text().split('[forgetful]')[0]
        path.write_text(old)
        self.state.write_text('{}')
        self.log.unlink()
        # Act
        result = self.run_cli(repo, '--finalize')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('migration is not supported', result.stderr)
        self.assertEqual(path.read_text(), old)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual(events(self.log), [])
