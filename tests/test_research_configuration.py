"""Independent research configuration through public init and config loading."""
import json

from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration
from forgetful_factory.domain.models import FactoryError


class ResearchConfigurationTests(InitFixture):
    def test_research_typo_can_be_corrected_without_stale_rosters(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  model  128000  8192  yes  yes\n'
            'research  exact/model  128000  8192  yes  yes')
        # Act
        rejected = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                '--research-model', 'research/exact/modle')
        # Assert
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('Research model', rejected.stderr)
        self.assertFalse((repo / '.factory/agents/feature-owner/roster.json').exists())
        self.assertFalse((repo / '.factory/factory.toml').exists())
        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--research-model', 'research/exact/model')
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(load_configuration(repo).research_agent_model, 'research/exact/model')

    def test_rejected_owner_and_research_flags_preserve_readiness_without_external_calls(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        saved = receipt.read_bytes()
        log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.state.write_text('{}')
        for flag in ('--research-effort', '--feature-owner-effort'):
            with self.subTest(flag=flag):
                # Act
                refused = self.run_cli(repo, flag, 'low')
                # Assert
                self.assertNotEqual(refused.returncode, 0)
                self.assertIn('conflict', refused.stderr)
                self.assertTrue(receipt.exists(), refused.stderr)
                self.assertEqual(receipt.read_bytes(), saved)
                self.assertFalse(log.exists())
                self.assertEqual(json.loads(self.state.read_text()), {})

    def test_supported_apps_report_specific_upstream_limits_in_configuration_loader(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        original = path.read_text()
        for app, limitation in (('opencode', 'optional effort'),
                                ('cursor', 'optional effort'),
                                ('copilot_cli', 'native selected skills'),
                                ('grok', 'native selected skills'),
                                ('codex', 'native selected skills'),
                                ('claude_code', 'native selected skills')):
            with self.subTest(app=app):
                path.write_text(f'research_agent_harness = "{app}"\n'
                                'research_agent_model = "exact-native-model"\n'
                                'research_agent_effort = "high"\n' + original)
                # Act / Assert
                with self.assertRaisesRegex(FactoryError, limitation):
                    load_configuration(repo)

    def test_research_pi_settings_roundtrip_and_reach_owner_roster(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  model  128000  8192  yes  yes\n'
            'research  exact/model  128000  8192  yes  yes')

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--research-harness', 'pi', '--research-model',
                              'research/exact/model', '--research-effort', 'low')

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.research_agent_model, 'research/exact/model')
        self.assertEqual(config.research_agent_harness, 'pi')
        self.assertEqual(config.research_agent_effort, 'low')
        self.assertEqual(config.feature_owner_agent_model, 'provider/model')
        roster = repo / '.factory/agents/feature-owner/roster.json'
        research = json.loads(roster.read_text())['roster']['roles'][0]
        self.assertEqual(research['model'], 'research/exact/model')
        self.assertEqual(research['effort'], 'low')
        saved = (repo / '.factory/factory.toml').read_bytes()
        retry = self.run_cli(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual((repo / '.factory/factory.toml').read_bytes(), saved)
