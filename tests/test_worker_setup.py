"""Execution setup failures stop public watch before external work."""
import json
import subprocess
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class WorkerSetupTests(InitFixture):
    def watch(self, repo):
        self.state.write_text('{}')
        log = self.workspace / 'profile.jsonl'
        log.unlink(missing_ok=True)
        self.env['PROFILE_LOG'] = str(log)
        result = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                                 '--workspace', str(repo), '--new-only'], cwd=repo, env=self.env,
                                capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual(events(log), [])
        return result

    def test_root_watch_does_not_recursively_preflight_workers_or_native_worker_accounts(self):
        # Arrange: child loading and native startup checks belong to the extension.
        from test_profile_recovery import ProfileRecoveryTests
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        ProfileRecoveryTests.install_terminal_double(self)
        agents = repo / '.factory/agents'
        for path in (self.workspace / 'tdd/SKILL.md', self.workspace / 'standards/SKILL.md',
                     agents / 'implementation/skills/implementation/SKILL.md',
                     self.bin / 'codex', self.bin / 'claude'):
            path.unlink()
        definition = agents / 'review/agent.json'
        definition.write_text('{unfinished child edit')
        root = agents / 'foreman/agent.json'
        before = root.read_bytes()
        # Act
        result = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                                 '--workspace', str(repo), '--new-only'], cwd=repo, env=self.env,
                                capture_output=True, text=True, timeout=5)
        # Assert: this proves root startup only, not native child/model compliance.
        self.assertNotIn('Traceback', result.stderr)
        launch, = [e for e in events(self.terminal_log) if e['kind'] == 'launch']
        self.assertEqual(launch['roster'], str(root))
        self.assertEqual(root.read_bytes(), before)
        self.assertEqual(definition.read_text(), '{unfinished child edit')

    def test_rerun_preserves_edited_worker_files_without_content_fingerprints(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/implementation/skills/implementation/SKILL.md'
        content = path.read_text() + '\nAdditional team instruction.\n'
        path.write_text(content)
        # Act
        retry = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(path.read_text(), content)
        receipt = json.loads((repo / '.factory/setup-complete.json').read_text())
        self.assertEqual(receipt, {'complete': True})

    def test_stale_planning_guidance_blocks_first_execution_setup_without_overwriting_edits(self):
        stale = {
            'feature-owner/skills/feature-owner/SKILL.md':
                'This slice stops at a reviewable plan. Do not run implementation agents.',
            'feature-owner/AGENTS.md': 'Implementation agents are not available in this slice.',
            'foreman/skills/foreman/SKILL.md':
                'Implementation/review execution, commits, PR creation remain for Slice 6.',
            'foreman/APPEND_SYSTEM.md': 'Implementation and review execution remain for Slice 6.',
        }
        for index, (relative, obsolete) in enumerate(stale.items()):
            with self.subTest(relative=relative):
                # Arrange: an incomplete first setup with preexisting user instructions.
                repo = self.repo(str(index))
                path = repo / '.factory/agents' / relative
                path.parent.mkdir(parents=True)
                path.write_text(obsolete + '\nPreserve this team edit.\n')
                before = path.read_bytes()
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('reconciliation', result.stderr)
                self.assertEqual(path.read_bytes(), before)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())

    def test_repeated_init_cannot_enable_workers_or_rewrite_planning_definitions(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = repo / '.factory/factory.toml'
        owner = repo / '.factory/agents/feature-owner/agent.json'
        before = config.read_bytes(), owner.read_bytes()
        # Act
        result = self.run_cli(repo, *worker_settings(self), worker_defaults=False)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((config.read_bytes(), owner.read_bytes()), before)
        self.assertEqual(json.loads(owner.read_text())['roster']['roles'],
                         [{'agent_file': '../research/agent.json'}])
        self.assertFalse((repo / '.factory/agents/implementation').exists())

    def test_existing_planning_only_role_edits_survive_without_enabling_workers(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        path = agents / 'feature-owner/skills/feature-owner/SKILL.md'
        old_guidance = ('This slice stops at a reviewable plan.\n'
                        'Keep this existing planning-only team guidance.\n')
        path.write_text(old_guidance)
        config = repo / '.factory/factory.toml'
        before = config.read_bytes()
        # Act
        result = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(config.read_bytes(), before)
        self.assertEqual(path.read_text(), old_guidance)
        self.assertFalse((agents / 'implementation').exists())
        receipt = json.loads((repo / '.factory/setup-complete.json').read_text())
        self.assertEqual(receipt, {'complete': True})

    def test_execution_requires_verification_permission_before_init_completion(self):
        repo = self.repo()
        settings = worker_settings(self)
        log = self.workspace / 'permissions.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('planning check failed', result.stderr)
        receipt = repo / '.factory/setup-complete.json'
        self.assertFalse(receipt.exists())
        calls = [e['args'][:2] for e in events(log) if e['name'] == 'forgetful']
        self.assertEqual(calls, [['call', 'get_project'], ['tools', 'list']])
        del self.env['PROFILE_PLANNING_FAILURE']
        setup = self.run_cli(repo, '--finalize', worker_defaults=False)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertEqual(json.loads(receipt.read_text()), {'complete': True})

    def test_planning_only_init_retains_twelve_permission_access(self):
        repo = self.repo()
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_first_setup_refuses_to_write_through_worker_definition_symlink(self):
        # Arrange
        repo = self.repo()
        selection = repo / '.factory/agents/implementation/agent.json'
        selection.parent.mkdir(parents=True)
        target = self.workspace / 'preserve.json'
        target.write_text('Keep target bytes')
        selection.symlink_to(target)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlink', result.stderr)
        self.assertTrue(selection.is_symlink())
        self.assertEqual(target.read_text(), 'Keep target bytes')
        self.assertFalse((repo / '.factory/factory.toml').exists())

    def test_invalid_external_skills_create_no_worker_metadata_and_corrected_init_succeeds(self):
        settings = worker_settings(self)
        review_failure_repo = None
        for index, (flag, bad) in enumerate((
                ('--tdd-skill', self.workspace / 'tdd/SKIL.md'),
                ('--implementation-skill', self.workspace / 'standards'),
                ('--review-skill', self.workspace / 'missing.md'))):
            with self.subTest(flag=flag):
                repo = self.repo(f'bad-skill-{index}')
                invalid = list(settings)
                invalid[invalid.index(flag) + 1] = str(bad)
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *invalid)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/agents/feature-owner/agent.json').exists())
                if flag == '--review-skill':
                    review_failure_repo = repo

        # Retry the case that left partial implementation resources, regardless of tuple order.
        self.assertIsNotNone(review_failure_repo)
        corrected = self.run_cli(review_failure_repo, '--repo', '.', *INIT_SETTINGS, *settings)
        self.assertEqual(corrected.returncode, 0, corrected.stderr)

    def test_relative_worker_skill_edit_is_preserved_without_reconciliation(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        definition = repo / '.factory/agents/implementation/agent.json'
        document = json.loads(definition.read_text())
        document['agent']['resources']['skills'] = ['./skills']
        definition.write_text(json.dumps(document))
        before = definition.read_bytes()
        config = repo / '.factory/factory.toml'
        saved = config.read_bytes()
        # Act
        result = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(definition.read_bytes(), before)
        self.assertEqual(config.read_bytes(), saved)

    def test_repeated_init_preserves_partial_owner_edits_without_disclosing_contents(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/feature-owner/agent.json'
        path.write_text('TOP_SECRET invalid JSON; keep these edits')
        config = repo / '.factory/factory.toml'
        saved = path.read_bytes(), config.read_bytes()
        # Act
        result = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('TOP_SECRET', result.stdout + result.stderr)
        self.assertEqual((path.read_bytes(), config.read_bytes()), saved)
