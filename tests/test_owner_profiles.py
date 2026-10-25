import json

from test_init import INIT_SETTINGS, InitFixture


class OwnerProfileTests(InitFixture):
    def test_foreman_delegates_unless_user_explicitly_requests_direct_work(self):
        # Arrange: provision a new factory through the public CLI, without inference.
        repo = self.repo()

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)

        # Assert: both entry guidance and the selected skill carry the delegation policy.
        self.assertEqual(result.returncode, 0, result.stderr)
        role = repo / '.factory/agents/foreman'
        for relative in ('AGENTS.md', 'skills/foreman/SKILL.md'):
            with self.subTest(guidance=relative):
                guidance = ' '.join((role / relative).read_text().split())
                for required in (
                    'Delegate feature work by default.',
                    'Only do that work yourself when the user explicitly asks you '
                    'in this conversation to do it directly.',
                    'A request to get work done is not permission to do it yourself.',
                    'Route feature investigation, implementation and review through '
                    'the configured feature-owner and its workers.',
                    'Routine status checks, coordination, user communication and '
                    'approved Factory maintenance remain your responsibility.',
                    'If delegation is blocked, report the blocker instead of taking over.',
                    'User permission does not bypass setup, ownership or safety checks.',
                ):
                    self.assertIn(required, guidance)

    def test_lowercase_depth_setting_provisions_150_without_changing_preferences(self):
        # Arrange: the shared profile uses the supported lowercase depth key.
        repo = self.repo()
        preferences = self.workspace / 'native pi/extensions/agentshell.json'
        original = '{"silent": true, "max_sub_agent_depth": 1}'
        preferences.write_text(original)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        extension = repo / '.factory/resources/agentshell'
        self.assertEqual(json.loads((extension / 'package.json').read_text())['version'], '1.5.0')
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
        path = repo / '.factory/resources/agentshell/config.ts'
        original = path.read_text() + '\n// user edit to preserve\n'
        path.write_text(original)
        # Act
        result = self.run_cli(repo, '--finalize')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reconcile', result.stderr)
        self.assertEqual(path.read_text(), original)

    def test_roles_reference_child_definitions_and_preserve_shared_login_and_grill_source(self):
        # Arrange
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
        foreman = json.loads((agents / 'foreman/agent.json').read_text())
        self.assertEqual(foreman['roster'], {'enabled': True, 'roles': [
            {'agent_file': '../feature-owner/agent.json'}]})
        owner = json.loads((agents / 'feature-owner/agent.json').read_text())
        self.assertEqual(owner['agent']['name'], 'feature-owner')
        self.assertEqual(owner['agent']['cwd'], '.')
        resources = owner['agent']['resources']
        self.assertIn(str(skill), resources['skills'])
        self.assertIn('./skills', resources['skills'])
        for field in ('packages', 'plugins', 'mcp_servers'):
            self.assertEqual(resources[field], [])
        for field in ('inherit_personal_resources', 'inherit_project_resources',
                      'include_home_system_prompt'):
            self.assertIs(resources[field], False)
        self.assertIs(resources['include_instruction_files'], True)
        self.assertEqual(owner['roster']['roles'], [{'agent_file': '../research/agent.json'}])
        leaf = json.loads((agents / 'research/agent.json').read_text())
        self.assertEqual(leaf['agent']['resources']['extensions'], [])
        self.assertEqual(leaf['roster'], {'enabled': False, 'roles': []})
        self.assertEqual(skill.read_text(), original)
        for role in ('foreman', 'feature-owner', 'research'):
            self.assertTrue((agents / role / 'AGENTS.md').is_file())

    def test_native_max_effort_is_saved_for_both_coordinators_and_research(self):
        # Arrange
        repo = self.repo()
        settings = list(INIT_SETTINGS)
        settings[settings.index('--foreman-effort') + 1] = 'max'
        # Act
        result = self.run_cli(repo, '--repo', '.', *settings,
                              '--feature-owner-effort', 'max')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        for role in ('foreman', 'feature-owner', 'research'):
            selected = json.loads((repo / f'.factory/agents/{role}/agent.json').read_text())
            self.assertEqual(selected['agent']['effort'], 'max')

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
        selected = json.loads((repo / '.factory/agents/feature-owner/agent.json').read_text())
        self.assertEqual(selected['agent']['model'], 'provider/owner')
        self.assertEqual(selected['agent']['effort'], 'xhigh')
        self.assertEqual(selected['agent']['agent_type'], 'pi')
        self.assertIn(str(self.grill_skill), selected['agent']['resources']['skills'])

    def test_init_provisions_audited_worker_supporting_role_resources(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        extension = repo / '.factory/resources/agentshell'
        self.assertEqual(json.loads((extension / 'package.json').read_text())['version'], '1.5.0')
        self.assertIn('agent-shell-py==0.5.0', (extension / 'python/pyproject.toml').read_text())
