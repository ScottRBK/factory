"""Foreman Forgetful memory setup through the public init command."""
import json
import os
import shutil

from lifecycle_support import LifecycleFixture
from test_init import INIT_SETTINGS, InitFixture


class ForemanMemorySetupTests(InitFixture):
    def test_explicit_opt_in_saves_role_scoped_automatic_memory_preferences(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Foreman automatic memory enabled for the configured Forgetful server.',
                      result.stdout)
        preferences = json.loads(
            (repo / '.factory/agents/foreman/forgetful.json').read_text()
        )
        self.assertEqual(preferences, {
            'enabled': True,
            'capture_mode': 'auto',
            'model': 'provider/model',
        })

    def test_help_describes_memory_as_server_only(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(repo, '--help')

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Enable Foreman recall/capture for a Forgetful server',
                      ' '.join(result.stdout.split()))
        self.assertFalse((repo / '.factory').exists())

    def test_local_automatic_memory_fails_before_setup_writes(self):
        # Arrange
        enabled_repo = self.repo()

        # Act
        enabled = self.run_cli(
            enabled_repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
        )

        # Assert
        self.assertNotEqual(enabled.returncode, 0)
        self.assertIn('automatic memory requires a Forgetful server', enabled.stderr)
        self.assertIn('Local CLI planning remains available', enabled.stderr)
        self.assertFalse((enabled_repo / '.factory/factory.toml').exists())
        self.assertFalse((enabled_repo / '.factory/agents/foreman/forgetful.json').exists())

    def test_unmappable_server_automatic_memory_fails_before_setup_writes(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/custom-endpoint',
        )

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('automatic memory cannot derive the server REST endpoint', result.stderr)
        self.assertIn('Native CLI planning can still use this server URL', result.stderr)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertFalse((repo / '.factory/agents/foreman/forgetful.json').exists())

    def test_local_planning_remains_available_when_automatic_memory_is_off(self):
        # Arrange
        planning_repo = self.repo('planning', 'git@github.com:team/planning.git')

        # Act
        planning = self.run_cli(planning_repo, '--repo', '.', *INIT_SETTINGS)

        # Assert
        self.assertEqual(planning.returncode, 0, planning.stderr)
        self.assertIn('selected project and planning permissions verified', planning.stdout)

    def test_manual_setup_offers_automatic_memory_and_numbered_model_choices(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  model  128000  8192  yes  yes\n'
            'provider  research  128000  8192  yes  yes'
        )
        answers = '\n'.join((
            '1',  # Manual setup.
            '1', '5',  # Owner: provider/model, high effort.
            '2', '3',  # Research: provider/research, low effort.
            '1', '1', '5',  # Implementation: Pi, provider/model, high effort.
            '1', '2', '4',  # Review: Pi, provider/research, medium effort.
            '2', '2',  # Automatic memory preference, provider/research.
            '',  # Submit the final answer.
        ))

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
            worker_defaults=False,
            input=answers,
            connection_defaults=False,
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Foreman automatic memory choices:', result.stdout)
        self.assertIn('Automatic recall and capture', result.stdout)
        self.assertIn('Foreman memory model choices:', result.stdout)
        preferences = json.loads(
            (repo / '.factory/agents/foreman/forgetful.json').read_text()
        )
        self.assertEqual(preferences, {
            'enabled': True,
            'capture_mode': 'auto',
            'model': 'provider/research',
        })

    def test_fully_specified_setup_defaults_memory_off_without_a_model(self):
        # Arrange
        default_repo = self.repo()
        disabled_repo = self.repo('disabled', 'git@github.com:team/disabled.git')

        # Act
        default = self.run_cli(default_repo, '--repo', '.', *INIT_SETTINGS)
        disabled = self.run_cli(
            disabled_repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
        )

        # Assert
        for result, repo in ((default, default_repo), (disabled, disabled_repo)):
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('Foreman automatic memory choices:', result.stdout)
            self.assertIn('memory extension reports unavailable for local Forgetful',
                          result.stdout)
            definition = json.loads(
                (repo / '.factory/agents/foreman/agent.json').read_text()
            )
            self.assertIn('../../resources/pi-forgetful/factory.ts',
                          definition['agent']['resources']['extensions'])
            preferences = json.loads(
                (repo / '.factory/agents/foreman/forgetful.json').read_text()
            )
            self.assertEqual(preferences, {
                'enabled': False,
                'capture_mode': 'off',
                'model': None,
            })

    def test_server_setup_loads_foreman_planning_when_automatic_memory_is_off(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/factory/mcp',
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        foreman = json.loads((agents / 'foreman/agent.json').read_text())
        managed = '../../resources/pi-forgetful/factory.ts'
        self.assertIn(managed, foreman['agent']['resources']['extensions'])
        for role in ('feature-owner', 'research'):
            child = json.loads((agents / role / 'agent.json').read_text())
            self.assertNotIn(managed, child['agent']['resources']['extensions'])
        self.assertIn('plans against the selected Forgetful project even when automatic memory '
                      'is off', ' '.join(result.stdout.split()))
        self.assertIn('forgetful-auth.json', result.stdout)
        self.assertIn('token_env', result.stdout)
        self.assertIn('native CLI login is separate', result.stdout)
        self.assertFalse((agents / 'foreman/forgetful-auth.json').exists())

    def test_unmappable_server_memory_off_keeps_cli_planning_without_rest_guessing(self):
        # Arrange
        repo = self.repo()
        log = self.workspace / 'unmappable-planning.jsonl'
        self.env['PROFILE_LOG'] = str(log)

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/custom-endpoint',
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('managed Foreman extension reports unavailable', result.stdout)
        self.assertIn('Native Factory CLI planning remains available', result.stdout)
        self.assertIn('no REST target was guessed', result.stdout)
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        planning = [call for call in calls if call['name'] == 'forgetful']
        self.assertTrue(planning)
        self.assertTrue(all(call['server'] == 'https://memory.example/custom-endpoint'
                            for call in planning))

    def test_unmappable_server_keeps_native_planning_when_managed_extension_is_unselected(self):
        # Arrange: model a completed legacy root without silently adding the new extension.
        repo = self.repo()
        log = self.workspace / 'legacy-planning.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['PROFILE_FAIL'] = 'forgetful'
        first = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/custom-endpoint',
        )
        self.assertNotEqual(first.returncode, 0)
        del self.env['PROFILE_FAIL']
        definition = repo / '.factory/agents/foreman/agent.json'
        document = json.loads(definition.read_text())
        managed = '../../resources/pi-forgetful/factory.ts'
        document['agent']['resources']['extensions'].remove(managed)
        definition.write_text(json.dumps(document))
        shutil.rmtree(repo / '.factory/resources/pi-forgetful', ignore_errors=True)
        preferences = repo / '.factory/agents/foreman/forgetful.json'
        before = {definition: definition.read_bytes(), preferences: preferences.read_bytes()}
        log.unlink(missing_ok=True)

        # Act
        finalized = self.run_cli(repo, '--finalize', connection_defaults=False)
        rerun = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--no-foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/custom-endpoint',
        )

        # Assert
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        self.assertEqual(rerun.returncode, 0, rerun.stderr)
        self.assertIn('managed Foreman extension is not selected', finalized.stdout)
        self.assertIn('Native Factory CLI planning remains available', finalized.stdout)
        self.assertIn('no REST target was guessed', finalized.stdout)
        calls = [json.loads(line) for line in log.read_text().splitlines()]
        planning = [call for call in calls if call['name'] == 'forgetful']
        self.assertTrue(planning)
        self.assertTrue(all(call['server'] == 'https://memory.example/custom-endpoint'
                            for call in planning))
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_model_alone_is_retained_without_enabling_memory(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory-model', 'provider/model',
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        preferences = json.loads(
            (repo / '.factory/agents/foreman/forgetful.json').read_text()
        )
        self.assertEqual(preferences, {
            'enabled': False,
            'capture_mode': 'off',
            'model': 'provider/model',
        })

    def test_enabled_memory_requires_a_model_and_explicit_models_match_catalog(self):
        # Arrange
        missing = self.repo('missing')
        unlisted = self.repo('unlisted', 'git@github.com:team/unlisted.git')

        # Act
        without_model = self.run_cli(
            missing,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
        )
        invalid_model = self.run_cli(
            unlisted,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory-model', 'provider/not-listed',
        )

        # Assert
        self.assertNotEqual(without_model.returncode, 0)
        self.assertIn('requires a memory model', without_model.stderr)
        self.assertNotEqual(invalid_model.returncode, 0)
        self.assertIn('not selectable', invalid_model.stderr)
        for repo in (missing, unlisted):
            self.assertFalse((repo / '.factory/factory.toml').exists())
            self.assertFalse((repo / '.factory/agents/foreman/forgetful.json').exists())

    def test_unsafe_or_connection_bearing_preference_files_are_preserved_and_refused(self):
        for kind in ('symlink', 'fifo', 'connection'):
            with self.subTest(kind=kind):
                # Arrange: these are existing public safety rules, not new failure claims.
                repo = self.repo(kind, f'git@github.com:team/{kind}.git')
                path = repo / '.factory/agents/foreman/forgetful.json'
                path.parent.mkdir(parents=True)
                target = self.workspace / f'{kind}-user-data.json'
                target.write_text('{"user_data":"preserve"}\n')
                original = target.read_bytes()
                preference = {'enabled': False, 'capture_mode': 'off', 'model': None,
                              'server': 'https://wrong.example'}
                if kind == 'symlink':
                    path.symlink_to(target)
                elif kind == 'fifo':
                    os.mkfifo(path, 0o600)
                else:
                    path.write_text(json.dumps(preference))

                # Act: bounded public CLI invocation, no internal reader replacement.
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)

                # Assert: no setup completion, target mutation or blocked FIFO read.
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertEqual(target.read_bytes(), original)
                if kind == 'symlink':
                    self.assertTrue(path.is_symlink())
                elif kind == 'fifo':
                    self.assertTrue(path.is_fifo())
                else:
                    self.assertEqual(json.loads(path.read_text()), preference)
                    self.assertIn('memory preferences differ', result.stderr)

    def test_partial_retry_preserves_matching_format_and_refuses_changed_preferences(self):
        # Arrange
        repo = self.repo()
        conflict_repo = self.repo('conflict', 'git@github.com:team/conflict.git')
        self.state.write_text(json.dumps({'fail_create': 'factory'}))
        failed = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
        )
        self.assertNotEqual(failed.returncode, 0)
        path = repo / '.factory/agents/foreman/forgetful.json'
        path.write_text(
            '{"model":"provider/model","capture_mode":"auto","enabled":true}\n'
        )
        preserved = path.read_bytes()
        conflict_failed = self.run_cli(
            conflict_repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
        )
        self.assertNotEqual(conflict_failed.returncode, 0)
        conflict_path = conflict_repo / '.factory/agents/foreman/forgetful.json'
        conflict_preserved = conflict_path.read_bytes()
        self.state.write_text('{}')

        # Act
        matching = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--foreman-memory',
            '--foreman-memory-model', 'provider/model',
            '--forgetful-instance', 'server',
            '--forgetful-server', 'https://memory.example/mcp',
        )
        changed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        conflict = self.run_cli(conflict_repo, '--repo', '.', *INIT_SETTINGS)

        # Assert
        self.assertEqual(matching.returncode, 0, matching.stderr)
        self.assertEqual(path.read_bytes(), preserved)
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertEqual(path.read_bytes(), preserved)
        self.assertNotEqual(conflict.returncode, 0)
        self.assertIn('memory preferences differ', conflict.stderr)
        self.assertEqual(conflict_path.read_bytes(), conflict_preserved)


class AssistedForemanMemorySetupTests(LifecycleFixture):
    def test_assisted_setup_can_leave_memory_off_without_hidden_choices(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(
            repo,
            '--repo', '.',
            *INIT_SETTINGS,
            '--assisted',
            timeout=20,
        )

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('Foreman automatic memory choices:', result.stdout)
        preferences = json.loads(
            (repo / '.factory/agents/foreman/forgetful.json').read_text()
        )
        self.assertEqual(preferences, {
            'enabled': False,
            'capture_mode': 'off',
            'model': None,
        })
        self.send(self.status(repo)['target'], 'EXIT_FAKE')
