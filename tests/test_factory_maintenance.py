"""Maintenance guidance and authoritative selections through public setup and runtime."""
import json
import subprocess
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class FactoryMaintenanceTests(InitFixture):
    def test_completion_explains_direct_skill_selection_and_reload_without_registration(self):
        # Arrange / Act
        repo = self.repo("team's app")
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        self.assertIn('Agent settings live in agent.json', setup.stdout)
        self.assertIn('reload or restart affected agents', setup.stdout)
        self.assertIn(str(repo / '.factory/agents/research/skills'), setup.stdout)
        self.assertNotIn('Launch factory now?', setup.stdout)
        role = repo / '.factory/agents/research'
        skill = role / 'skills/team-notes/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: team-notes\ndescription: Research notes.\n---\n')
        definition = role / 'agent.json'
        before = definition.read_bytes()
        # Act: ordinary repeated init from another directory leaves selected discovery intact.
        repeated = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'init',
                                   '--workspace', str(repo)], cwd=self.workspace, env=self.env,
                                  input='', capture_output=True, text=True, timeout=10)
        # Assert
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(definition.read_bytes(), before)
        self.assertIn('./skills', json.loads(before)['agent']['resources']['skills'])
        self.assertNotIn('Select repositories', repeated.stdout)

    def test_init_selects_editable_maintenance_skill_and_reinit_preserves_it(self):
        # Arrange / Act
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        # Assert
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/foreman'
        definition = role / 'agent.json'
        before = definition.read_bytes()
        self.assertIn('./skills', json.loads(before)['agent']['resources']['skills'])
        skill = role / 'skills/factory-maintenance/SKILL.md'
        guidance = skill.read_text()
        for required in ('name: factory-maintenance', 'description:', 'agent.json',
                         'Setup does not ask for skill paths', 'after setup', 'TDD',
                         'foreman --attach', 'init --finalize', 'uncertain delivery',
                         'read-before-work', 'full briefing', 'absolute SKILL.md'):
            self.assertIn(required, guidance)
        self.assertNotIn('disable-model-invocation: true', guidance)
        self.assertIn('skills/factory-maintenance/SKILL.md', (role / 'AGENTS.md').read_text())
        # Act
        edited = guidance + '\nAsk our team before changing selected review models.\n'
        skill.write_text(edited)
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(skill.read_text(), edited)
        self.assertEqual(definition.read_bytes(), before)

    def test_missing_maintenance_selection_blocks_watch_and_preserves_direct_edit(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        path = repo / '.factory/agents/foreman/agent.json'
        definition = json.loads(path.read_text())
        definition['agent']['resources']['skills'] = ['skills/foreman']
        path.write_text(json.dumps(definition))
        saved = path.read_bytes()
        log = self.workspace / 'maintenance-profile.jsonl'
        self.env['PROFILE_LOG'] = str(log)
        self.state.write_text('{}')
        # Act
        watch = subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                                '--workspace', str(repo), '--new-only'],
                               cwd=repo, env=self.env, capture_output=True, text=True, timeout=5)
        retry = self.run_cli(repo)
        # Assert
        self.assertNotEqual(watch.returncode, 0)
        self.assertIn('factory-maintenance', watch.stderr)
        self.assertNotIn('Traceback', watch.stderr)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(events(log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertEqual(path.read_bytes(), saved)

    def test_first_finalization_requires_guidance_and_preserves_edits_until_manual_repair(self):
        # Arrange: first setup saves the team but fails its external access check.
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertNotEqual(setup.returncode, 0)
        del self.env['PROFILE_FAIL']
        role = repo / '.factory/agents/foreman'
        skill = role / 'skills/factory-maintenance/SKILL.md'
        original = skill.read_bytes()
        skill.unlink()
        config = repo / '.factory/factory.toml'
        saved_config = config.read_bytes()
        definition = role / 'agent.json'
        saved = definition.read_bytes()
        # Act
        repeated = self.run_cli(repo)
        failed = self.run_cli(repo, '--finalize')
        # Assert
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('factory-maintenance', failed.stderr)
        self.assertFalse(skill.exists())
        self.assertEqual(definition.read_bytes(), saved)
        self.assertEqual(config.read_bytes(), saved_config)
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        # Act: user restores the selected guidance; explicit first finalization validates it.
        skill.write_bytes(original)
        corrected = self.run_cli(repo, '--finalize')
        # Assert
        self.assertEqual(corrected.returncode, 0, corrected.stderr)
        self.assertEqual(json.loads((repo / '.factory/setup-complete.json').read_text()),
                         {'complete': True})
        self.assertEqual(definition.read_bytes(), saved)

    def test_worker_skill_edit_requires_only_its_own_definition(self):
        # Arrange
        repo = self.repo()
        flags = worker_settings(self, harness='pi', model='provider/model', effort='high')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *flags)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        extra = self.workspace / 'local-style/SKILL.md'
        extra.parent.mkdir()
        extra.write_text('# Local coding style.\n')
        worker = agents / 'implementation/agent.json'
        selected = json.loads(worker.read_text())
        selected['agent']['resources']['skills'].append(str(extra))
        worker.write_text(json.dumps(selected))
        saved = worker.read_bytes()
        parent = agents / 'feature-owner/agent.json'
        before = parent.read_bytes()
        self.assertIn({'agent_file': '../implementation/agent.json'},
                      json.loads(before)['roster']['roles'])
        # Act
        repeated = self.run_cli(repo, worker_defaults=False)
        # Assert
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(worker.read_bytes(), saved)
        self.assertEqual(parent.read_bytes(), before)
        self.assertIn(str(self.workspace / 'tdd/SKILL.md'),
                      selected['agent']['resources']['skills'])
