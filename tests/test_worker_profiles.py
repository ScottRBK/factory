"""Native worker selections provisioned by public init."""
import json

from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class WorkerProfileTests(InitFixture):
    def test_worker_definitions_preserve_dynamic_worktree_and_native_harness_contract(self):
        # Arrange / Act
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        roster = json.loads((agents / 'feature-owner/agent.json').read_text())['roster']['roles']
        self.assertEqual(roster, [{'agent_file': f'../{role}/agent.json'}
                                  for role in ('research', 'implementation', 'review')])
        for role, harness, model, effort in (('implementation', 'codex', 'gpt-5.4', 'xhigh'),
                                             ('review', 'claude_code', 'opus', 'high')):
            document = json.loads((agents / role / 'agent.json').read_text())
            entry = document['agent']
            self.assertEqual(entry['agent_type'], harness)
            self.assertEqual(entry['model'], model)
            self.assertEqual(entry['effort'], effort)
            self.assertNotIn('cwd', entry)
            self.assertEqual(set(entry['resources']), {'skills'})
            self.assertIn(str(self.workspace / 'standards/SKILL.md'), entry['resources']['skills'])
            self.assertIn('./skills', entry['resources']['skills'])
            self.assertEqual(document['roster'], {'enabled': False, 'roles': []})
            self.assertTrue((agents / role / f'skills/{role}/SKILL.md').is_file())
        foreman = json.loads((agents / 'foreman/agent.json').read_text())['roster']['roles']
        self.assertEqual(foreman, [{'agent_file': '../feature-owner/agent.json'}])
        self.assertEqual((self.workspace / 'tdd/SKILL.md').read_text(),
                         '---\nname: tdd\ndescription: Sequential TDD.\n---\nTest first.\n')

    def test_pi_worker_uses_explicit_skills_and_disabled_child_roster_without_fixed_cwd(self):
        # Arrange / Act
        repo = self.repo()
        settings = worker_settings(self, harness='pi', model='provider/model', effort='high')
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        document = json.loads((repo / '.factory/agents/implementation/agent.json').read_text())
        entry = document['agent']
        self.assertEqual(entry['agent_type'], 'pi')
        self.assertNotIn('cwd', entry)
        self.assertEqual(entry['resources']['extensions'], [])
        self.assertIs(entry['resources']['include_instruction_files'], True)
        self.assertIs(entry['resources']['inherit_project_resources'], False)
        self.assertIn(str(self.workspace / 'tdd/SKILL.md'), entry['resources']['skills'])
        self.assertEqual(document['roster'], {'enabled': False, 'roles': []})
