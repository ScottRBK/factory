"""Foreman maintenance guidance is provisioned through public setup, not a hidden helper."""
import json
import subprocess
import sys
from pathlib import Path

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class FactoryMaintenanceTests(InitFixture):
    def test_init_selects_editable_maintenance_skill_and_reinit_preserves_it(self):
        # Arrange
        repo = self.repo()
        # Act
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        selection = json.loads((role / 'resources.json').read_text())
        self.assertIn('skills/factory-maintenance', selection['skills'])
        skill = role / 'skills/factory-maintenance/SKILL.md'
        guidance = skill.read_text()
        self.assertIn('name: factory-maintenance', guidance)
        self.assertIn('description:', guidance)
        self.assertNotIn('disable-model-invocation: true', guidance)
        self.assertIn('Init registers role-local skill files', guidance)
        self.assertIn('feature-owner/roster.json', guidance)
        self.assertIn('Do not run init from the watcher-owned Foreman', guidance)
        self.assertIn('init holds the workspace lease', guidance)
        self.assertIn('--research-model', guidance)
        self.assertIn('skills/factory-maintenance/SKILL.md', (role / 'AGENTS.md').read_text())
        # Arrange / Act: local instructions remain editable, even after setup is rerun.
        edited = guidance + '\nAsk our team before changing selected review models.\n'
        skill.write_text(edited)
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(skill.read_text(), edited)
        self.assertEqual(json.loads((role / 'resources.json').read_text()), selection)

    def test_missing_maintenance_selection_blocks_init_and_watch_without_overwriting_edits(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        path = role / 'resources.json'
        selection = json.loads(path.read_text())
        selection['skills'] = ['skills/foreman']
        path.write_text(json.dumps(selection))
        saved = path.read_bytes()
        log = self.workspace / 'maintenance-profile.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.state.write_text('{}')
        # Act
        watch = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                                '--workspace', str(repo), '--new-only'],
                               cwd=repo, env=self.env, capture_output=True, text=True, timeout=5)
        calls = events(log)
        state = json.loads(self.state.read_text())
        retry = self.run_cli(repo)
        # Assert
        for result in (watch, retry):
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('factory-maintenance', result.stderr)
            self.assertIn('resources.json', result.stderr)
            self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(calls, [])
        self.assertEqual(state, {})
        self.assertEqual(path.read_bytes(), saved)

    def test_pre_maintenance_profile_files_require_selection_and_keep_old_guidance(self):
        # Arrange: a resource fixture from before the maintenance skill existed.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        skill = role / 'skills/factory-maintenance/SKILL.md'
        skill.unlink()
        skill.parent.rmdir()
        selection = role / 'resources.json'
        before = json.dumps({
            'skills': ['skills/foreman'],
            'extensions': ['resources/agentshell/extensions/agentshell.ts',
                           'resources/hide-tools/index.ts'],
        })
        selection.write_text(before)
        old_agents = (Path(__file__).parent / 'fixtures/foreman-before-maintenance.md').read_text()
        (role / 'AGENTS.md').write_text(old_agents)
        config = repo / '.factory/factory.toml'
        saved_config = config.read_bytes()
        # Act: re-init provisions the missing skill, but cannot replace preserved selections.
        retry = self.run_cli(repo)
        # Assert
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('factory-maintenance', retry.stderr)
        self.assertIn('resources.json', retry.stderr)
        self.assertTrue(skill.is_file())
        self.assertEqual(selection.read_text(), before)
        self.assertEqual((role / 'AGENTS.md').read_text(), old_agents)
        self.assertEqual(config.read_bytes(), saved_config)
        self.assertFalse((role / 'model-selection.json').exists())
        # Act: follow the documented selection correction and rerun public init.
        selected = json.loads(before)
        selected['skills'].append('skills/factory-maintenance')
        selection.write_text(json.dumps(selected))
        corrected = self.run_cli(repo)
        # Assert
        self.assertEqual(corrected.returncode, 0, corrected.stderr)
        self.assertTrue((role / 'model-selection.json').is_file())
        self.assertEqual(json.loads(selection.read_text()), selected)
        self.assertEqual((role / 'AGENTS.md').read_text(), old_agents)
        self.assertNotIn('factory-maintenance', old_agents)
        self.assertEqual(config.read_bytes(), saved_config)

    def test_pi_worker_skill_update_also_requires_the_parent_roster_selection(self):
        # Arrange
        repo = self.repo()
        flags = worker_settings(self, harness='pi', model='provider/model', effort='high')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *flags)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        extra = agents / 'implementation/skills/local-style/SKILL.md'
        extra.parent.mkdir(parents=True)
        extra.write_text('---\nname: local-style\ndescription: Local coding style.\n---\n')
        config = repo / '.factory/factory.toml'
        standard = json.dumps(str(self.workspace / 'standards/SKILL.md'))
        original = f'implementation_skills = [{standard}]'
        self.assertIn(original, config.read_text())
        config.write_text(config.read_text().replace(
            original, f'implementation_skills = [{standard}, {json.dumps(str(extra))}]'))
        selection = agents / 'implementation/resources.json'
        selected = json.loads(selection.read_text())
        selected['skills'].append(str(extra))
        selection.write_text(json.dumps(selected))
        # Act: the native Pi launch selection in the owner's roster is still stale.
        incomplete = self.run_cli(repo, worker_defaults=False)
        # Assert
        roster = agents / 'feature-owner/roster.json'
        self.assertNotEqual(incomplete.returncode, 0)
        self.assertIn(str(roster), incomplete.stderr)
        self.assertFalse((agents / 'foreman/model-selection.json').exists())
        # Act: complete the Pi-specific step from the maintenance skill.
        roles = json.loads(roster.read_text())
        implementation = next(r for r in roles['roster']['roles'] if r['name'] == 'implementation')
        implementation['resources']['skills'].append(str(extra))
        roster.write_text(json.dumps(roles))
        corrected = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(corrected.returncode, 0, corrected.stderr)
        self.assertEqual(json.loads(selection.read_text()), selected)
        self.assertEqual(json.loads(roster.read_text()), roles)
        self.assertTrue((agents / 'foreman/model-selection.json').is_file())
