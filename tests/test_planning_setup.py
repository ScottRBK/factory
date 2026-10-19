import json
import subprocess
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration


class PlanningSetupTests(InitFixture):
    def test_fresh_interactive_project_choice_is_saved_with_completion(self):
        # Arrange
        repo = self.repo()
        # Act: no fixture-supplied --forgetful-project argument.
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--planning-only',
             '--repo', '.', *INIT_SETTINGS,
             '--forgetful-instance', 'local', '--share-pi-profile', '--install-role-runtime',
             '--grill-me-skill', str(self.grill_skill)], cwd=repo, env=self.env,
            input='12\n', capture_output=True, text=True, timeout=10)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Select Forgetful project ID or c to create:', result.stdout)
        self.assertEqual(load_configuration(repo).forgetful.project_id, 12)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        self.assertEqual(json.loads(receipt.read_text())['forgetful']['project_id'], 12)

    def test_existing_config_requires_project_edit_before_interactive_or_explicit_init(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config_path = repo / '.factory/factory.toml'
        edited = config_path.read_text().replace('project_id = 12\n', '')
        edited += '\n# Preserve these user notes.\n[custom]\nsetting = "keep"\n'
        config_path.write_text(edited)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        previous = receipt.read_bytes()
        gh_state = self.state.read_bytes()
        log = self.workspace / 'project-selection.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        for arguments in ((), ('--forgetful-project', '12')):
            with self.subTest(arguments=arguments):
                log.unlink(missing_ok=True)
                # Act: bypass fixture defaults, which normally supply the project argument.
                result = subprocess.run(
                    [sys.executable, '-m', 'forgetful_factory', 'init', '--planning-only',
                     '--share-pi-profile',
                     '--install-role-runtime', *arguments], cwd=repo, env=self.env,
                    input='12\n', capture_output=True, text=True, timeout=10)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('.factory/factory.toml', result.stderr)
                self.assertIn('[forgetful]', result.stderr)
                self.assertIn('project_id', result.stderr)
                self.assertIn('rerun init', result.stderr)
                self.assertEqual(result.stdout, '', 'Reject before prompting or reporting success')
                self.assertEqual(events(log), [], 'Reject before external setup calls')
                self.assertEqual(config_path.read_text(), edited)
                self.assertEqual(receipt.read_bytes(), previous)
                self.assertEqual(self.state.read_bytes(), gh_state)
                self.assertIsNone(load_configuration(repo).forgetful.project_id)
        # Act: follow the edit guidance, then retry with explicit arguments.
        corrected = edited.replace('[forgetful]', '[forgetful]\nproject_id = 12')
        config_path.write_text(corrected)
        retry = self.run_cli(repo, '--forgetful-project', '12')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(config_path.read_text(), corrected)
        self.assertEqual(load_configuration(repo).forgetful.project_id, 12)
        self.assertEqual(json.loads(receipt.read_text())['forgetful']['project_id'], 12)

    def test_init_rejects_missing_foreman_selections_and_preserves_edits(self):
        for missing in ('both', 'skill', 'agentshell'):
            with self.subTest(missing=missing):
                # Arrange
                repo = self.repo(missing)
                setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
                self.assertEqual(setup.returncode, 0, setup.stderr)
                role = repo / '.factory/agents/foreman'
                path = role / 'resources.json'
                settings = json.loads(path.read_text())
                if missing in ('both', 'skill'):
                    settings['skills'] = []
                if missing in ('both', 'agentshell'):
                    settings['extensions'] = []
                edited = json.dumps(settings, indent=2) + '\n'
                path.write_text(edited)
                guidance = role / 'APPEND_SYSTEM.md'
                guidance.write_text('Keep my additional guidance.\n')
                # Act
                result = self.run_cli(repo)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('resources.json', result.stderr)
                self.assertIn('skills/foreman', result.stderr)
                self.assertIn('resources/agentshell/extensions/agentshell.ts', result.stderr)
                self.assertIn('rerun init', result.stderr)
                self.assertEqual(path.read_text(), edited)
                self.assertEqual(guidance.read_text(), 'Keep my additional guidance.\n')
                self.assertFalse((role / 'model-selection.json').exists())
                watch = subprocess.run(
                    [sys.executable, '-m', 'forgetful_factory', 'watch', '--new-only'],
                    cwd=repo, env=self.env, capture_output=True, text=True, timeout=5)
                self.assertNotEqual(watch.returncode, 0)
                self.assertIn('resources.json', watch.stderr)

    def test_init_accepts_essential_foreman_resources_without_optional_hide_tools(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        path = role / 'resources.json'
        edited = json.dumps({'skills': [str(role / 'skills/foreman/SKILL.md'),
                                       str(role / 'skills/factory-maintenance/SKILL.md')],
                             'extensions': ['resources/agentshell/extensions/agentshell.ts']})
        path.write_text(edited)
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(path.read_text(), edited)
        self.assertTrue((role / 'model-selection.json').exists())

    def test_init_records_project_access_without_requesting_a_user_profile(self):
        # Arrange: the command double rejects user-profile requests.
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-project', '12')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads((repo / '.factory/agents/foreman/model-selection.json').read_text())
        self.assertEqual(receipt['forgetful']['project_id'], 12)
        self.assertNotIn('principal', receipt)

    def test_old_backend_or_wrong_project_leaves_setup_incomplete(self):
        for failure in ('external_ref', 'permission', 'project', 'login'):
            with self.subTest(failure=failure):
                # Arrange
                repo = self.repo(failure)
                self.env['PROFILE_PLANNING_FAILURE'] = failure
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                      '--forgetful-project', '12')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('planning check failed', result.stderr)
                self.assertNotIn('TOP_SECRET', result.stderr)
                receipt = repo / '.factory/agents/foreman/model-selection.json'
                self.assertFalse(receipt.exists())

    def test_bulk_catalog_still_requires_every_planning_permission_and_both_reference_fields(self):
        required = ('create_plan', 'list_plans', 'get_plan', 'update_plan', 'create_task',
                    'query_tasks', 'get_task', 'update_task', 'claim_task', 'transition_task',
                    'add_criterion', 'add_dependency')
        catalog = [{'name': name, 'parameters': {'external_ref': {'type': 'string'}}}
                   for name in required]
        cases = [('missing-' + name, {'plan': [t for t in catalog if t['name'] != name]})
                 for name in required]
        for name in ('create_plan', 'list_plans'):
            for parameters in ({}, [], None, 'external_ref'):
                cases.append((name, {'plan': [dict(t, parameters=parameters)
                                              if t['name'] == name else t for t in catalog]}))
        cases.extend([('not-object', []), ('bad-group', {'plan': {}}),
                      ('bad-entry', {'plan': [None]}), ('bad-name', {'plan': [{'name': 1}]}),
                      ('duplicate', {'plan': [*catalog, catalog[0]]})])
        for index, (name, groups) in enumerate(cases):
            with self.subTest(name=name, index=index):
                # Arrange
                repo = self.repo(f'app-{index}')
                self.env['PROFILE_TOOL_CATALOG'] = json.dumps({'tools_by_category': groups})
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('planning check failed', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

    def test_connection_preflight_only_checks_project_and_tool_catalog(self):
        # Arrange
        repo = self.repo()
        log = self.workspace / 'planning.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = [e['args'][:2] for e in events(log) if e['name'] == 'forgetful']
        self.assertEqual(calls, [['call', 'get_project'], ['tools', 'list']])

    def test_init_checks_selected_project_permissions_under_native_login(self):
        # Arrange
        repo = self.repo()
        log = self.workspace / 'planning.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              '--forgetful-project', '12')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = load_configuration(repo)
        self.assertEqual(config.forgetful.project_id, 12)
        receipt = json.loads((repo / '.factory/agents/foreman/model-selection.json').read_text())
        self.assertEqual(receipt['forgetful']['project_id'], 12)
        calls = [e['args'] for e in events(log) if e['name'] == 'forgetful']
        self.assertTrue(any(c[:2] == ['tools', 'list'] for c in calls))
        self.assertFalse(any(c[:2] == ['call', 'get_current_user'] for c in calls))
        self.assertTrue(any(c[:2] == ['call', 'get_project'] for c in calls))
