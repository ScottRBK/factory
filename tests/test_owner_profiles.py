import json

from test_init import INIT_SETTINGS, InitFixture


class OwnerProfileTests(InitFixture):
    def test_lowercase_depth_setting_provisions_141_without_changing_preferences(self):
        # Arrange: the shared profile uses the extension 1.4.1 spelling.
        repo = self.repo()
        preferences = self.workspace / 'native pi/extensions/agentshell.json'
        original = '{"silent": true, "max_sub_agent_depth": 1}'
        preferences.write_text(original)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        extension = repo / '.factory/agents/foreman/resources/agentshell'
        self.assertEqual(json.loads((extension / 'package.json').read_text())['version'], '1.4.1')
        self.assertEqual(preferences.read_text(), original)

    def test_insufficient_native_depth_is_reported_without_changing_preferences(self):
        # Arrange
        repo = self.repo()
        preferences = self.workspace / 'native pi/extensions/agentshell.json'
        preferences.write_text('{"max_sub_agent_depth": 0}')
        before = preferences.read_bytes()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('max_sub_agent_depth', result.stderr)
        self.assertEqual(preferences.read_bytes(), before)

    def test_stale_or_edited_extension_is_refused_without_overwrite(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/foreman/resources/agentshell/config.ts'
        original = path.read_text() + '\n// user edit to preserve\n'
        path.write_text(original)
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reconcile', result.stderr)
        self.assertEqual(path.read_text(), original)

    def test_roles_select_children_and_preserve_shared_login_and_grill_source(self):
        # Arrange
        from pathlib import Path
        repo = self.repo()
        skill = self.workspace / 'grill-me.md'
        original = ('---\nname: grill-me\ndescription: Ask frontier questions.\n'
                    'disable-model-invocation: true\n---\nResearch with subagents.\n')
        skill.write_text(original)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--grill-me-skill', str(skill))
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        foreman = json.loads((agents / 'foreman/roster.json').read_text())['roster']
        owner = foreman['roles'][0]
        self.assertEqual(owner['name'], 'feature-owner')
        self.assertEqual(owner['cwd'], str(agents / 'feature-owner'))
        self.assertEqual(owner['roster_file'], str(agents / 'feature-owner/roster.json'))
        resources = owner['resources']
        self.assertIn(str(skill), resources['skills'])
        for field in ('packages', 'plugins', 'mcp_servers'):
            self.assertEqual(resources[field], [])
        for field in ('inherit_personal_resources', 'inherit_project_resources',
                      'include_home_system_prompt'):
            self.assertIs(resources[field], False)
        self.assertIs(resources['include_instruction_files'], True)
        children = json.loads(Path(owner['roster_file']).read_text())['roster']['roles']
        self.assertEqual([r['name'] for r in children], ['research'])
        self.assertEqual(children[0]['resources']['extensions'], [])
        leaf = json.loads(Path(children[0]['roster_file']).read_text())
        self.assertIs(leaf['roster']['enabled'], False)
        self.assertEqual(skill.read_text(), original)
        for role in ('foreman', 'feature-owner', 'research'):
            self.assertTrue((agents / role / 'AGENTS.md').is_file())

    def test_native_max_effort_is_saved_for_both_coordinators_and_research(self):
        # Arrange
        from forgetful_factory.configuration import load_configuration
        repo = self.repo()
        settings = list(INIT_SETTINGS)
        settings[settings.index('--foreman-effort') + 1] = 'max'
        # Act
        result = self.run_cli(repo, '--repo', '.', *settings,
                              '--feature-owner-effort', 'max')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.foreman_agent_effort, 'max')
        self.assertEqual(config.feature_owner_agent_effort, 'max')
        for role in ('foreman', 'feature-owner'):
            roster = json.loads((repo / f'.factory/agents/{role}/roster.json').read_text())
            self.assertEqual(roster['roster']['roles'][0]['effort'], 'max')

    def test_non_native_effort_is_rejected_before_setup(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--feature-owner-effort', 'not-a-pi-effort')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('off, minimal, low, medium, high, xhigh', result.stderr)
        self.assertFalse((repo / '.factory').exists())

    def test_owner_model_effort_and_grill_source_are_persisted(self):
        # Arrange
        from forgetful_factory.configuration import load_configuration
        repo = self.repo()
        self.env['PROFILE_MODELS'] = (
            'provider  model  context  max-out  thinking  images\n'
            'provider  model  128000  8192  yes  yes\n'
            'provider  owner  128000  8192  yes  yes')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--feature-owner-model', 'provider/owner',
                              '--feature-owner-effort', 'xhigh')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.feature_owner_agent_model, 'provider/owner')
        self.assertEqual(config.feature_owner_agent_effort, 'xhigh')
        self.assertEqual(config.feature_owner_agent_harness, 'pi')
    def test_init_provisions_audited_worker_supporting_role_resources(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        extension = repo / '.factory/agents/foreman/resources/agentshell'
        self.assertEqual(json.loads((extension / 'package.json').read_text())['version'], '1.4.1')
        self.assertIn('agent-shell-py==0.5.0', (extension / 'python/pyproject.toml').read_text())
