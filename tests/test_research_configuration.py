"""Independent research configuration through public init and config loading."""
import json

from test_init import INIT_SETTINGS, InitFixture


class ResearchConfigurationTests(InitFixture):
    def agent(self, repo, role):
        return json.loads((repo / f'.factory/agents/{role}/agent.json').read_text())['agent']

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
        self.assertFalse((repo / '.factory/agents/feature-owner/agent.json').exists())
        self.assertFalse((repo / '.factory/factory.toml').exists())
        retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--research-model', 'research/exact/model')
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(self.agent(repo, 'research')['model'], 'research/exact/model')

    def test_repeated_owner_and_research_flags_preserve_readiness_without_external_calls(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/setup-complete.json'
        saved = receipt.read_bytes()
        log = self.workspace / 'profile.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.state.write_text('{}')
        for flag in ('--research-effort', '--feature-owner-effort'):
            with self.subTest(flag=flag):
                # Act
                refused = self.run_cli(repo, flag, 'low')
                # Assert
                self.assertEqual(refused.returncode, 0, refused.stderr)
                self.assertTrue(receipt.exists(), refused.stderr)
                self.assertEqual(receipt.read_bytes(), saved)
                self.assertFalse(log.exists())
                self.assertEqual(json.loads(self.state.read_text()), {})

    def test_first_research_setup_reports_current_factory_app_scope(self):
        # Arrange: this wizard provisions Pi research; broader apps are a separate phase.
        for app in ('opencode', 'cursor', 'copilot_cli', 'grok', 'codex', 'claude_code'):
            with self.subTest(app=app):
                repo = self.repo(app)
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      '--research-harness', app,
                                      '--research-model', 'exact-native-model')
                # Assert: no claim about another harness lacking native skill support.
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('research', result.stderr.lower())
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertNotIn('Traceback', result.stderr)

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
        self.assertEqual(self.agent(repo, 'research')['model'], 'research/exact/model')
        self.assertEqual(self.agent(repo, 'research')['agent_type'], 'pi')
        self.assertEqual(self.agent(repo, 'research')['effort'], 'low')
        self.assertEqual(self.agent(repo, 'feature-owner')['model'], 'provider/model')
        roster = repo / '.factory/agents/feature-owner/agent.json'
        self.assertEqual(json.loads(roster.read_text())['roster']['roles'],
                         [{'agent_file': '../research/agent.json'}])
        research = self.agent(repo, 'research')
        self.assertEqual(research['model'], 'research/exact/model')
        self.assertEqual(research['effort'], 'low')
        saved = (repo / '.factory/factory.toml').read_bytes()
        retry = self.run_cli(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual((repo / '.factory/factory.toml').read_bytes(), saved)
