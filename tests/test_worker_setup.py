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

    def test_worker_sources_selections_and_executables_are_checked_before_watch(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        paths = [self.workspace / 'tdd/SKILL.md', self.workspace / 'standards/SKILL.md',
                 agents / 'implementation/skills/implementation/SKILL.md',
                 agents / 'review/resources.json', self.bin / 'codex', self.bin / 'claude']
        for path in paths:
            original = path.read_bytes()
            mode = path.stat().st_mode
            with self.subTest(path=path):
                path.unlink()
                # Act / Assert
                result = self.watch(repo)
                self.assertRegex(result.stderr, 'worker|skill|incomplete')
                path.write_bytes(original)
                path.chmod(mode)
        for path in paths[:3]:
            original = path.read_bytes()
            with self.subTest(edited=path):
                path.write_bytes(original + b'\nChanged selection content\n')
                # Act / Assert
                result = self.watch(repo)
                self.assertIn('changed', result.stderr)
                path.write_bytes(original)

    def test_rerun_preserves_edited_worker_files_and_binds_selected_sources(self):
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
        receipt = json.loads((repo / '.factory/agents/foreman/model-selection.json').read_text())
        self.assertIn('workers', receipt['profiles'])

    def test_stale_planning_guidance_blocks_execution_and_is_preserved_on_reinit(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        stale = {
            'feature-owner/skills/feature-owner/SKILL.md':
                'This slice stops at a reviewable plan. '
                'Do not run implementation or review agents.',
            'feature-owner/AGENTS.md':
                'Implementation, review execution, commits, pushes, PRs '
                'and merges belong to Slice 6 '
                'and are not\navailable in this slice.',
            'foreman/skills/foreman/SKILL.md':
                'Implementation/review execution, commits, PR creation '
                'and merges remain for Slice 6.',
            'foreman/APPEND_SYSTEM.md': 'Implementation and review\nexecution remain for Slice 6.',
        }
        for relative, obsolete in stale.items():
            path = agents / relative
            original = path.read_text()
            with self.subTest(relative=relative):
                path.write_text(obsolete + '\nPreserve this team edit.\n')
                before = path.read_bytes()
                # Act / Assert
                result = self.watch(repo)
                self.assertIn('reconciliation', result.stderr)
                retry = self.run_cli(repo, worker_defaults=False)
                self.assertNotEqual(retry.returncode, 0)
                self.assertIn('reconciliation', retry.stderr)
                self.assertEqual(path.read_bytes(), before)
                self.assertFalse((agents / 'foreman/model-selection.json').exists())
                path.write_text(original)
                restored = self.run_cli(repo, worker_defaults=False)
                self.assertEqual(restored.returncode, 0, restored.stderr)

    def test_enabling_workers_never_rewrites_the_existing_planning_roster(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/factory.toml'
        old_config = path.read_text()
        roster = repo / '.factory/agents/feature-owner/roster.json'
        original_roster = roster.read_bytes()
        worker_settings(self)
        additions = {
            'implementation_agent_model': 'gpt-5.4', 'implementation_agent_harness': 'codex',
            'implementation_agent_effort': 'xhigh', 'review_agent_model': 'opus',
            'review_agent_harness': 'claude_code', 'review_agent_effort': 'high',
            'tdd_skill': str(self.workspace / 'tdd/SKILL.md'),
        }
        path.write_text(''.join(f'{key} = {json.dumps(value)}\n'
                                for key, value in additions.items()) + old_config)
        before = path.read_bytes()
        # Act
        result = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('reconcile', result.stderr)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(roster.read_bytes(), original_roster)
        self.assertFalse((repo / '.factory/agents/foreman/model-selection.json').exists())

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
        receipt = json.loads((agents / 'foreman/model-selection.json').read_text())
        self.assertNotIn('workers', receipt['profiles'])

    def test_execution_requires_verification_permission_at_init_and_watch(self):
        repo = self.repo()
        settings = worker_settings(self)
        log = self.workspace / 'permissions.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('planning check failed', result.stderr)
        receipt = repo / '.factory/agents/foreman/model-selection.json'
        self.assertFalse(receipt.exists())
        calls = [e['args'][:2] for e in events(log) if e['name'] == 'forgetful']
        self.assertEqual(calls, [['call', 'get_project'], ['tools', 'list']])
        del self.env['PROFILE_PLANNING_FAILURE']
        setup = self.run_cli(repo, worker_defaults=False)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        log.unlink()
        self.state.write_text('{}')
        result = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                                 '--new-only'], cwd=repo, env=self.env, capture_output=True,
                                text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('planning check failed', result.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual([(e['name'], e['args'][:2]) for e in events(log)],
                         [('forgetful', ['call', 'get_project']),
                          ('forgetful', ['tools', 'list'])])

    def test_planning_only_init_retains_twelve_permission_access(self):
        repo = self.repo()
        self.env['PROFILE_PLANNING_FAILURE'] = 'verification'
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_worker_metadata_symlink_is_rejected_before_reading_its_target(self):
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(setup.returncode, 0, setup.stderr)
        selection = repo / '.factory/agents/implementation/resources.json'
        selection.unlink()
        selection.symlink_to(self.workspace, target_is_directory=True)
        result = self.watch(repo)
        self.assertIn('symlink', result.stderr)
        self.assertTrue(selection.is_symlink())
        self.assertEqual(selection.readlink(), self.workspace)

    def test_invalid_external_skills_create_no_worker_metadata_and_corrected_init_succeeds(self):
        settings = worker_settings(self)
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
                for role in ('implementation', 'review'):
                    self.assertFalse((repo / f'.factory/agents/{role}/resources.json').exists())
                corrected = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
                self.assertEqual(corrected.returncode, 0, corrected.stderr)

    def test_relative_saved_skill_is_rejected_before_new_metadata_and_config_is_preserved(self):
        repo = self.repo()
        settings = worker_settings(self)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        config = repo / '.factory/factory.toml'
        edited = config.read_text().replace(str(self.workspace / 'tdd/SKILL.md'), 'tdd/SKILL.md')
        config.write_text(edited)
        resource = repo / '.factory/agents/implementation/resources.json'
        resource.unlink()
        result = self.run_cli(repo, worker_defaults=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('absolute readable regular file', result.stderr)
        self.assertFalse(resource.exists())
        self.assertEqual(config.read_text(), edited)

    def test_conflicting_preserved_owner_selection_names_the_file_without_disclosing_contents(self):
        settings = worker_settings(self)
        for kind in ('roster', 'resources'):
            with self.subTest(kind=kind):
                repo = self.repo(kind)
                setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
                self.assertEqual(setup.returncode, 0, setup.stderr)
                config = repo / '.factory/factory.toml'
                path = repo / f'.factory/agents/feature-owner/{kind}.json'
                if kind == 'roster':
                    config.write_text(config.read_text().replace(
                        'review_agent_effort = "high"', 'review_agent_effort = "low"'))
                else:
                    path.write_text('TOP_SECRET invalid JSON; keep these edits')
                saved_config, saved_selection = config.read_bytes(), path.read_bytes()
                result = self.run_cli(repo, worker_defaults=False)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(str(path), result.stderr)
                self.assertIn('reconcile', result.stderr)
                self.assertIn('Back up', result.stderr)
                self.assertNotIn('TOP_SECRET', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(config.read_bytes(), saved_config)
                self.assertEqual(path.read_bytes(), saved_selection)
