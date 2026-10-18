"""Project selection through public init with an external Forgetful CLI double."""
import json
import subprocess
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture

from forgetful_factory.configuration import load_configuration


class ProjectOnboardingTests(InitFixture):
    def setUp(self):
        super().setUp()
        self.projects = self.workspace / 'projects.json'
        self.projects.write_text('[]')
        self.log = self.workspace / 'commands.jsonl'
        self.env.update(PROFILE_PROJECTS_FILE=str(self.projects), PROFILE_LOG=str(self.log))

    def init(self, repo, answers):
        return subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--planning-only',
             '--repo', '.', *INIT_SETTINGS,
             '--forgetful-instance', 'local', '--share-pi-profile', '--install-role-runtime',
             '--grill-me-skill', str(self.grill_skill)], cwd=repo, env=self.env,
            input=answers, capture_output=True, text=True, timeout=10)

    def creates(self):
        return [event for event in events(self.log)
                if event['name'] == 'forgetful' and event['args'][:2] == ['call', 'create_project']]

    def test_empty_account_offers_creation_with_workspace_name_and_saves_returned_id(self):
        # Arrange
        repo = self.repo('new-factory')
        # Act: accept the suggested name, then explicitly approve creation.
        result = self.init(repo, '\ny\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('No Forgetful projects found.', result.stdout)
        self.assertIn('Project name [new-factory]:', result.stdout)
        self.assertNotIn('Select Forgetful project ID', result.stdout)
        config = load_configuration(repo)
        self.assertEqual(config.forgetful.project_id, 31)
        saved = json.loads(self.projects.read_text())
        self.assertEqual(saved, [{'id': 31, 'name': 'new-factory',
                                 'description': 'Factory plans and knowledge for new-factory.',
                                 'project_type': 'development'}])
        self.assertEqual(len(self.creates()), 1)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        self.assertEqual(json.loads(receipt.read_text())['forgetful']['project_id'], 31)

    def test_failed_create_is_not_retried_and_lists_committed_project_on_rerun(self):
        for failure in ('denied', 'lost'):
            with self.subTest(failure=failure):
                # Arrange
                repo = self.repo(failure)
                self.projects.write_text('[]')
                self.log.unlink(missing_ok=True)
                self.env['PROFILE_CREATE_FAILURE'] = failure
                # Act
                result = self.init(repo, '\ny\n')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Project creation could not be confirmed', result.stderr)
                self.assertIn('check the project list', result.stderr)
                self.assertNotIn('TOP_SECRET', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(len(self.creates()), 1)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
                self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
                self.env.pop('PROFILE_CREATE_FAILURE')
                if failure == 'lost':
                    # Act: choose the committed project on retry, not a second create.
                    retry = self.init(repo, '31\n')
                    # Assert
                    self.assertEqual(retry.returncode, 0, retry.stderr)
                    self.assertEqual(len(self.creates()), 1)
                    self.assertEqual(load_configuration(repo).forgetful.project_id, 31)
                    self.assertEqual(len(json.loads(self.projects.read_text())), 1)

    def test_interrupted_create_warns_about_saved_project_and_retry_reuses_it(self):
        # Arrange: the CLI commits, then interrupts init before returning its response.
        repo = self.repo('interrupted')
        self.env['PROFILE_CREATE_FAILURE'] = 'interrupt'
        # Act
        result = self.init(repo, '\ny\n')
        # Assert
        self.assertEqual(result.returncode, 130, result.stderr)
        self.assertIn('Init interrupted', result.stderr)
        self.assertIn('may already exist', result.stderr)
        self.assertIn('check the project list before creating another', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(len(self.creates()), 1)
        self.assertEqual(len(json.loads(self.projects.read_text())), 1)
        self.assertFalse((repo / '.factory/factory.toml').exists())
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
        self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
        # Act: rerun init and choose the committed project.
        self.env.pop('PROFILE_CREATE_FAILURE')
        retry = self.init(repo, '31\n')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(load_configuration(repo).forgetful.project_id, 31)
        self.assertEqual(len(self.creates()), 1)
        self.assertEqual(len(json.loads(self.projects.read_text())), 1)

    def test_malformed_create_response_keeps_setup_incomplete_with_recovery_guidance(self):
        for project_id in (None, True, '31', 0, -1):
            with self.subTest(project_id=project_id):
                # Arrange
                repo = self.repo(f'response-{project_id}')
                self.projects.write_text('[]')
                self.log.unlink(missing_ok=True)
                self.env['PROFILE_CREATE_RESPONSE'] = json.dumps({'id': project_id})
                # Act
                result = self.init(repo, '\ny\n')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Project creation could not be confirmed', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(len(self.creates()), 1)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

    def test_existing_projects_offer_creation_and_allow_a_custom_name(self):
        # Arrange
        repo = self.repo()
        self.projects.write_text('[{"id":12,"name":"Other project"}]')
        # Act
        result = self.init(repo, 'c\n  Shared workspace  \ny\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('12. Other project', result.stdout)
        self.assertIn('c. Create new project', result.stdout)
        self.assertEqual(load_configuration(repo).forgetful.project_id, 31)
        self.assertEqual(json.loads(self.projects.read_text())[-1]['name'], 'Shared workspace')
        self.assertEqual(len(self.creates()), 1)
        # Act: re-init reuses the saved choice without asking or creating.
        retry = self.init(repo, '')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertNotIn('Project name', retry.stdout)
        self.assertNotIn('Select Forgetful project', retry.stdout)
        self.assertEqual(len(self.creates()), 1)

    def test_select_existing_does_not_create_or_require_creation_permission(self):
        # Arrange
        repo = self.repo()
        self.projects.write_text('[{"id":12,"name":"Existing project"}]')
        self.env['PROFILE_CREATE_FAILURE'] = 'denied'
        # Act
        result = self.init(repo, '12\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(load_configuration(repo).forgetful.project_id, 12)
        self.assertEqual(self.creates(), [])

    def test_declining_creation_or_ending_input_creates_nothing(self):
        for answers in ('\nn\n', '\n\n', '', '\n'):
            with self.subTest(answers=answers):
                # Arrange
                repo = self.repo(f'cancel-{len(list(self.workspace.glob("cancel-*")))}')
                # Act
                result = self.init(repo, answers)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(self.creates(), [])
                self.assertEqual(json.loads(self.projects.read_text()), [])
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())
                self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])

    def test_invalid_choice_or_skip_is_rejected_without_creating(self):
        for choice in ('skip', '', '0', '99', '-1'):
            with self.subTest(choice=choice):
                # Arrange
                repo = self.repo(f'choice-{choice or "empty"}')
                self.projects.write_text('[{"id":12,"name":"Existing project"}]')
                # Act
                result = self.init(repo, choice + '\n')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Select a listed project ID or c', result.stderr)
                self.assertEqual(self.creates(), [])
                self.assertFalse((repo / '.factory/factory.toml').exists())

    def test_invalid_project_listing_is_not_treated_as_an_empty_account(self):
        for listing in ([{}], [{'id': True, 'name': 'Wrong'}], [{'id': 1}], [None]):
            with self.subTest(listing=listing):
                # Arrange
                repo = self.repo(f'listing-{len(list(self.workspace.glob("listing-*")))}')
                self.projects.write_text(json.dumps(listing))
                # Act
                result = self.init(repo, '\ny\n')
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Forgetful returned invalid projects', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertNotIn('Create Forgetful project', result.stdout)
                self.assertEqual(self.creates(), [])
                self.assertFalse((repo / '.factory/factory.toml').exists())
