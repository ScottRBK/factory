"""Assisted setup through public init/watch/config, with controlled external commands."""
import json

from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration


class FinalizationTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.env['HOME'] = str(self.workspace)

    def test_manual_role_catalog_rejects_symlinks_before_running_external_command(self):
        for role in ('feature-owner', 'research'):
            with self.subTest(role=role):
                # Arrange
                repo = self.repo(name=role)
                outside = self.workspace / f'outside-{role}'
                outside.mkdir()
                directory = repo / '.factory/agents' / role
                directory.parent.mkdir(parents=True)
                directory.symlink_to(outside, target_is_directory=True)
                log = self.workspace / f'{role}-catalog.jsonl'
                log.touch()
                self.env['PROFILE_LOG'] = str(log)

                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      worker_defaults=False, input='1\n1\n5\n1\n5\n')

                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('symlink', result.stderr)
                commands = [json.loads(line) for line in log.read_text().splitlines()]
                self.assertFalse(any(call['cwd'] == str(outside) for call in commands))
                self.assertTrue(directory.is_symlink())
                self.assertEqual(list(outside.iterdir()), [])

    def test_manual_unsupported_research_app_fails_before_pi_catalog_prompt(self):
        # Arrange / Act
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--research-harness', 'codex',
                              worker_defaults=False, input='1\n1\n5\n1\n5\n')

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('research', result.stderr.lower())
        self.assertIn('Pi', result.stderr)
        self.assertNotIn('Research model choices', result.stdout)

    def test_first_finalization_validates_definition_without_reconciling_legacy_roster(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        initial = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertNotEqual(initial.returncode, 0)
        del self.env['PROFILE_FAIL']
        config = repo / '.factory/factory.toml'
        config.write_text('# Preserve this comment.\n' + config.read_text())
        before = config.read_bytes()
        definition = repo / '.factory/agents/foreman/agent.json'
        saved = definition.read_bytes()
        legacy = repo / '.factory/runtime/foreman/roster.json'
        legacy.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        legacy.write_text('{"roster":{"enabled":false,"roles":[]}}')
        old = legacy.read_bytes()
        # Act
        result = self.run_cli(repo, '--finalize')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(definition.read_bytes(), saved)
        self.assertEqual(legacy.read_bytes(), old)
        self.assertEqual(config.read_bytes(), before)
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})
        self.assertIn('reload or restart', result.stdout)
        self.assertNotIn('Launch factory now?', result.stdout)

    def test_legacy_runtime_roster_symlink_cannot_authorize_writes_during_first_finalization(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        initial = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertNotEqual(initial.returncode, 0)
        del self.env['PROFILE_FAIL']
        legacy = repo / '.factory/runtime/foreman/roster.json'
        legacy.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        target = self.workspace / 'keep.json'
        target.write_text('Keep this edit.')
        legacy.symlink_to(target)
        # Act
        finalized = self.run_cli(repo, '--finalize')
        # Assert: no runtime roster is published; this obsolete path is never write authority.
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        self.assertEqual(target.read_text(), 'Keep this edit.')
        self.assertTrue(legacy.is_symlink())
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})

    def test_manual_route_numbers_owner_research_and_workers(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  model  128000  8192  yes  yes\n'
            'provider  research  128000  8192  yes  yes')
        # Manual; owner model/effort; research model/effort; both workers app/model/effort.
        answers = '1\n1\n5\n2\n3\n1\n1\n5\n1\n2\n4\n'

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              worker_defaults=False, input=answers)

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(
            'How would you like to set up your factory?\n'
            '  1. Manual — Choose agents, models and settings through step-by-step prompts.\n'
            '  2. Foreman-assisted — Chat with Foreman, your coordinating AI agent, '
            'to finish setup together.\n'
            'Select 1 or 2: ', result.stdout)
        self.assertIn('Feature-owner model', result.stdout)
        self.assertIn('Research model', result.stdout)
        config = load_configuration(repo)
        agents = repo / '.factory/agents'
        owner = json.loads((agents / 'feature-owner/agent.json').read_text())['agent']
        research = json.loads((agents / 'research/agent.json').read_text())['agent']
        self.assertEqual(owner['model'], 'provider/model')
        self.assertEqual(research['model'], 'provider/research')
        self.assertEqual(research['effort'], 'low')
        self.assertTrue(config.execution_enabled)

    def test_new_foreman_guidance_gates_dispatch_and_explains_same_session_finalization(self):
        # Arrange / Act
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        directory = repo / '.factory/agents/foreman'
        instructions = (directory / 'AGENTS.md').read_text()
        maintenance = (directory / 'skills/factory-maintenance/SKILL.md').read_text()
        self.assertIn('Setup is incomplete', instructions)
        self.assertIn('do not dispatch', instructions)
        self.assertIn('FACTORY_COMMAND', maintenance)
        self.assertIn('--finalize --delegated-work-stopped', maintenance)
        self.assertIn('watch --start', maintenance)
        self.assertIn('watch --stop', maintenance)
        self.assertIn('same conversation', maintenance)
        self.assertIn('Pi and OpenCode support skill paths', maintenance)
        self.assertIn('Claude Code, Copilot CLI and Cursor support native plugins', maintenance)
        self.assertIn('Broader Factory app support is a separate phase', maintenance)
        self.assertNotIn('Copilot/Grok need native', maintenance)
        self.assertNotIn('A dedicated Foreman-first setup mode is not yet available', maintenance)

    def test_finalize_missing_configuration_fails_without_prompting_or_writing(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(repo, '--finalize')

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('saved configuration', result.stderr)
        self.assertIn('terminal', result.stderr)
        self.assertNotIn('Select repositories', result.stdout)
        self.assertFalse((repo / '.factory').exists())

    def test_runtime_directory_permissions_are_checked_before_completion(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        runtime = repo / '.factory/runtime/foreman'
        runtime.mkdir(parents=True, exist_ok=True, mode=0o700)
        runtime.chmod(0o755)

        # Act
        result = self.run_cli(repo, '--finalize')

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('private', result.stderr)
        self.assertEqual(runtime.stat().st_mode & 0o777, 0o755)

    def test_assisted_preserves_old_guidance_and_requires_setup_gate_reconciliation(self):
        # Arrange
        repo = self.repo()
        instructions = repo / '.factory/agents/foreman/AGENTS.md'
        instructions.parent.mkdir(parents=True)
        text = 'Existing team guidance: immediately dispatch incoming work.\n'
        instructions.write_text(text)

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('setup guidance', result.stderr)
        self.assertIn('Stale testing guidance', result.stderr)
        self.assertIn('preserved', result.stderr)
        self.assertEqual(instructions.read_text(), text)
        self.assertFalse((repo / '.factory/runtime/foreman/owner.json').exists())
