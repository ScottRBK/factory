import json
import tomllib

from test_init import INIT_SETTINGS, InitFixture


class ForemanIssueIntakeTests(InitFixture):
    def test_new_foreman_reads_configured_labels_and_asks_before_issue_intake(self):
        # Arrange: use two non-default labels and a repository outside the role cwd.
        repo = self.repo()
        settings = list(INIT_SETTINGS)
        settings[settings.index('--label') + 1] = 'Ready for Factory'

        # Act: provision through the public CLI without a model or live GitHub call.
        result = self.run_cli(repo, '--repo', '.', *settings, '--label', 'Expedite')

        # Assert: the saved config remains authoritative.
        self.assertEqual(result.returncode, 0, result.stderr)
        config = tomllib.loads((repo / '.factory/factory.toml').read_text())
        self.assertEqual(config['watcher_label'], ['Ready for Factory', 'Expedite'])
        self.assertEqual(config['repository'][0]['source'], 'team/app')
        # Init may ensure label definitions, but must not create issues.
        calls = json.loads(self.state.read_text())['calls']
        self.assertFalse(any('/issues' in call[1] for call in calls))

    def test_watch_all_guidance_does_not_offer_an_unlabelled_opt_out(self):
        # Arrange: watch all issues rather than a concrete label.
        repo = self.repo()
        settings = list(INIT_SETTINGS)
        settings[settings.index('--label') + 1] = '*'

        # Act
        result = self.run_cli(repo, '--repo', '.', *settings)

        # Assert: no literal wildcard label, and explicit consent before issue creation.
        self.assertEqual(result.returncode, 0, result.stderr)
        config = tomllib.loads((repo / '.factory/factory.toml').read_text())
        self.assertEqual(config['watcher_label'], ['*'])
        self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])

    def test_repeat_init_preserves_edited_issue_intake_guidance(self):
        # Arrange: local edits remain the user's responsibility, not a template-sync target.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        paths = [role / 'AGENTS.md', role / 'skills/foreman/SKILL.md']
        for path in paths:
            path.write_text(path.read_text() + '\nLocal issue triage requires a user discussion.\n')
        before = {path: path.read_bytes() for path in paths}
        config = repo / '.factory/factory.toml'
        saved_config = config.read_bytes()
        calls = self.state.read_bytes()

        # Act
        result = self.run_cli(repo)

        # Assert: no silent adoption, backend writes or watched-label configuration changes.
        self.assertEqual(result.returncode, 0, result.stderr)
        for path in paths:
            self.assertEqual(path.read_bytes(), before[path])
        self.assertEqual(config.read_bytes(), saved_config)
        self.assertEqual(self.state.read_bytes(), calls)
