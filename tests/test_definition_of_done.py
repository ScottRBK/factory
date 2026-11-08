"""Agreement persistence through public setup; no model-compliance claims."""
import subprocess
import sys
import time

from test_init import INIT_SETTINGS, InitFixture


class DefinitionOfDoneTests(InitFixture):
    def run_cli(self, cwd, *args, **kwargs):
        kwargs.setdefault('agreement_input', '')
        return super().run_cli(cwd, *args, **kwargs)

    def test_confirmed_merge_agreement_is_saved_outside_feature_worktrees(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='1\ny\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        agreement = repo / '.factory/definition_of_done.md'
        self.assertTrue(agreement.is_file(), result.stdout)
        text = agreement.read_text()
        self.assertIn('team/app', text)
        self.assertIn('Independent review', text)
        self.assertIn('Deployment and deployed E2E are not completion requirements', text)
        self.assertIn(text, result.stdout, 'Show the agreement before saving it')
        self.assertTrue((repo / '.factory/setup-complete.json').is_file())

    def test_agreement_created_during_confirmation_is_preserved_not_silently_accepted(self):
        # Arrange: hold public CLI input at confirmation, then emulate a concurrent user save.
        repo = self.repo()
        output = self.workspace / 'setup-output.txt'
        args = [sys.executable, '-m', 'forgetful_factory', 'init', '--repo', '.',
                *INIT_SETTINGS, '--planning-only', '--share-pi-profile', '--install-role-runtime',
                '--forgetful-instance', 'local', '--forgetful-project', '12',
                '--grill-me-skill', str(self.grill_skill)]
        with output.open('w') as stream, subprocess.Popen(
                args, cwd=repo, env=dict(self.env, PYTHONUNBUFFERED='1'), stdin=subprocess.PIPE,
                stdout=stream, stderr=stream, text=True) as process:
            try:
                process.stdin.write('1\n')
                process.stdin.flush()
                deadline = time.monotonic() + 10
                while 'Save this Definition of Done' not in output.read_text():
                    self.assertIsNone(process.poll(), output.read_text())
                    self.assertLess(time.monotonic(), deadline, output.read_text())
                    time.sleep(0.01)
                path = repo / '.factory/definition_of_done.md'
                saved = '# Other agreement\n\nUser is still discussing completion.\n'
                path.write_text(saved)
                # Act
                process.communicate('y\n', timeout=10)
                # Assert
                self.assertNotEqual(process.returncode, 0, output.read_text())
                self.assertEqual(path.read_text(), saved)
                self.assertFalse((repo / '.factory/setup-complete.json').exists())
            finally:
                if process.poll() is None:
                    process.kill()
                    process.communicate()

    def test_deployment_preset_excludes_e2e_and_requires_revision_evidence(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              input='2\nstaging\nDelivery\ny\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (repo / '.factory/definition_of_done.md').read_text()
        self.assertIn('actual merged revision', text)
        self.assertIn('Deployed E2E is not a completion requirement', text)
        self.assertIn('staging', text)
        self.assertIn('Delivery', text)
        self.assertIn('environment', result.stdout)
        self.assertIn('missing', result.stdout)
        self.assertIn(text, result.stdout)

    def test_e2e_preset_names_deployment_and_tested_revision_combination(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                              input='3\nisolated-e2e\nDeploy and test\ny\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (repo / '.factory/definition_of_done.md').read_text()
        self.assertIn('isolated-e2e', text)
        self.assertIn('Deploy and test', text)
        self.assertIn('deployed repository combination', text)
        self.assertIn('after deployment succeeds', text)
        self.assertNotIn('E2E is not', text)
        self.assertIn(text, result.stdout)

    def test_no_selection_or_rejected_agreement_never_selects_merge_only(self):
        for name, answer in (('eof', ''), ('blank', '\n'), ('invalid', '9\n'),
                             ('declined', '1\nn\n')):
            with self.subTest(name=name):
                # Arrange
                repo = self.repo(name)
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input=answer)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((repo / '.factory/definition_of_done.md').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())
                self.assertTrue((repo / '.factory/factory.toml').is_file())

    def test_finalization_can_confirm_missing_agreement_without_reprovisioning_agents(self):
        # Arrange: interruption after config save is the existing first-init recovery boundary.
        repo = self.repo()
        incomplete = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertNotEqual(incomplete.returncode, 0)
        files = [repo / '.factory/factory.toml',
                 *sorted((repo / '.factory/agents').rglob('*'))]
        before = {path: path.read_bytes() for path in files if path.is_file()}
        # Act
        finalized = self.run_cli(repo, '--finalize', input='1\ny\n')
        # Assert
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        self.assertTrue((repo / '.factory/definition_of_done.md').is_file())
        self.assertTrue((repo / '.factory/setup-complete.json').is_file())

    def test_existing_custom_agreement_and_guidance_survive_setup_and_repeated_init(self):
        # Arrange
        repo = self.repo()
        path = repo / '.factory/definition_of_done.md'
        path.parent.mkdir()
        text = b'# Programme delivery\n\nAPI: deploy. Library: publish verified package.\n'
        path.write_bytes(text)
        guidance = repo / '.factory/agents/foreman/skills/foreman/SKILL.md'
        guidance.parent.mkdir(parents=True)
        guidance.write_text('---\nname: foreman\ndescription: Custom team guidance.\n'
                            '---\nKeep this.\n')
        saved_guidance = guidance.read_bytes()
        # Act
        first = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        repeated = self.run_cli(repo, '--assisted', input='4\n')
        finalized = self.run_cli(repo, '--finalize')
        # Assert
        for result in (first, repeated, finalized):
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('Select Definition of Done', result.stdout)
        self.assertEqual(path.read_bytes(), text)
        self.assertEqual(guidance.read_bytes(), saved_guidance)

    def test_older_ready_workspace_does_not_gain_an_agreement_during_repeated_init(self):
        # Arrange: an old receipt is not evidence that a completion policy was agreed.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='1\ny\n')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/definition_of_done.md'
        path.unlink()
        # Act
        repeated = self.run_cli(repo, input='1\ny\n')
        # Assert
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertFalse(path.exists())
        self.assertNotIn('Select Definition of Done', repeated.stdout)

    def test_agreement_symlink_is_preserved_and_cannot_overwrite_an_external_file(self):
        # Arrange
        repo = self.repo()
        outside = self.workspace / 'keep.md'
        saved = b'# Keep this external agreement\n'
        outside.write_bytes(saved)
        path = repo / '.factory/definition_of_done.md'
        path.parent.mkdir()
        path.symlink_to(outside)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='1\ny\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlinks', result.stderr)
        self.assertTrue(path.is_symlink())
        self.assertEqual(outside.read_bytes(), saved)
        self.assertFalse((repo / '.factory/setup-complete.json').exists())

    def test_eof_with_complete_flags_requires_terminal_agreement_and_finalize(self):
        # Arrange / Act: all settings flags are supplied by this public setup fixture.
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='')
        # Assert: flags cannot answer the human agreement prompt.
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('terminal session', result.stderr)
        self.assertIn('init --finalize', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertTrue((repo / '.factory/factory.toml').is_file())
        self.assertFalse((repo / '.factory/definition_of_done.md').exists())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
