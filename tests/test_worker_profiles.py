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

    def test_execution_guidance_carries_required_workflow_and_worker_boundaries(self):
        # Arrange
        repo = self.repo()
        settings = worker_settings(self)
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *settings)
        # Assert: public editable role files are the product's workflow instructions.
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        owner = ' '.join(
            (agents / 'feature-owner/skills/feature-owner/SKILL.md').read_text().split())
        implementation = ' '.join(
            (agents / 'implementation/skills/implementation/SKILL.md').read_text().split())
        reviewer = ' '.join((agents / 'review/skills/review/SKILL.md').read_text().split())
        foreman = ' '.join((agents / 'foreman/skills/foreman/SKILL.md').read_text().split())
        for required in ('actual changes', 'acceptance criteria', 'required tests',
                         'without a mandatory plan-approval', 'repository requires approval',
                         'configured names and descriptions', 'absolute SKILL.md',
                         'cwd=', 'full role briefing', 'native session ID',
                         'claim_task', 'transition_task', '--match-head-commit',
                         'ADRs', 'merged', 'retained worktrees', 'waiting'):
            self.assertIn(required, owner)
        for required in ('TDD', 'commit', 'push', 'exact commit', 'CI run', 'task IDs',
                         'Do not use Forgetful', 'waiting', 'repository instructions'):
            self.assertIn(required, implementation)
        for required in ('independent', 'GitHub', 'task IDs', 'Do not use Forgetful',
                         'repository instructions'):
            self.assertIn(required, reviewer)
        for content in (owner, foreman):
            self.assertIn('get_current_user', content)
            self.assertIn('Deployment and E2E', content)
        self.assertNotIn('This slice stops at a reviewable plan.', owner)
        self.assertNotIn('Implementation/review execution, commits, PR creation', foreman)

    def test_init_assigns_pr_creation_to_implementation_and_keeps_owner_review_and_merge(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        # Assert: inspect the role instructions a new factory actually receives.
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        implementation = ' '.join(
            (agents / 'implementation/skills/implementation/SKILL.md').read_text().split())
        owner = ' '.join(
            (agents / 'feature-owner/skills/feature-owner/SKILL.md').read_text().split())
        foreman = ' '.join((agents / 'foreman/skills/foreman/SKILL.md').read_text().split())
        for required in ('Open or reuse the repository PR', 'head branch and base branch',
                         'before waiting for PR-triggered CI', 'do not blindly create another',
                         'designated PR-opening task', 'rather than compete to create one',
                         'reuse a matching open PR', 'closed or merged PR',
                         'not automatic reuse or reopening', 'PR URL',
                         'when all required checks pass', 'An open PR is not completion',
                         'Draft status follows repository rules and owner guidance',
                         'not a factory-wide requirement', 'Do not approve or merge PRs'):
            self.assertIn(required, implementation)
        for obsolete in ('open/merge PRs', 'do not open PRs yourself', 'Always open it as a draft'):
            self.assertNotIn(obsolete, implementation)
        for required in ('Implementation agents open or reuse the repository PR',
                         'one feature PR per affected repository',
                         'name the PR-opening task in their briefings', 'PR content expectations',
                         'Verify the returned PR', 'repository-specific PR URLs in plan context',
                         'required checks must still pass before implementation is complete',
                         'no factory-wide draft-only requirement',
                         'PR creation gives the worker no approval or merge authority',
                         'Only after verified implementation evidence',
                         'Launch an independent reviewer', '--match-head-commit'):
            self.assertIn(required, owner)
        self.assertNotIn('Open a separate PR', owner)
        self.assertIn('Implementation agents open or reuse PRs', foreman)
        self.assertIn('opening a PR does not mean implementation is complete', foreman)
        self.assertNotIn('verifies exact-commit CI, opens PRs', foreman)

    def test_native_contract_limits_and_evidence_rules_are_explicit_in_role_guidance(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        owner = ' '.join(
            (agents / 'feature-owner/skills/feature-owner/SKILL.md').read_text().split())
        reviewer = ' '.join((agents / 'review/skills/review/SKILL.md').read_text().split())
        for required in ('verify_criterion', 'todo -> doing', 'doing -> waiting',
                         'Codex resume', 'approval/sandbox', 'commit_id', 'exit zero',
                         'workflow/event', 'attempt', 'merge revision'):
            self.assertIn(required, owner)
        for required in ('commit_id', 'COMMENT', 'external approvals', 'AGENTS.md'):
            self.assertIn(required, reviewer)

    def test_dispatch_guidance_records_launch_intent_without_requiring_an_early_job_id(self):
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(result.returncode, 0, result.stderr)
        path = repo / '.factory/agents/feature-owner/skills/feature-owner/SKILL.md'
        guidance = ' '.join(path.read_text().split())
        self.assertIn('worktree before launch', guidance)
        self.assertIn('After dispatch, record a transient Job ID only if returned', guidance)
        self.assertIn('inline result may return only the final native session ID', guidance)
        self.assertIn('never invent a Job ID', guidance)

    def test_review_fixes_cleanup_reconciliation_and_native_prerequisites_are_explicit(self):
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *worker_settings(self))
        self.assertEqual(result.returncode, 0, result.stderr)
        agents = repo / '.factory/agents'
        owner = ' '.join(
            (agents / 'feature-owner/skills/feature-owner/SKILL.md').read_text().split())
        reviewer = ' '.join((agents / 'review/skills/review/SKILL.md').read_text().split())
        foreman = ' '.join((agents / 'foreman/skills/foreman/SKILL.md').read_text().split())
        for requirement in ('feature-specific review-fix task',
                            'Keep completed implementation tasks done', 'Keep review pending',
                            'never omit cwd', 'native-valid metadata',
                            'does not provision browser or computer-use tools',
                            'pull_request_url', 'merge_commit', 'pending', 'removed',
                            'update_task', 'before native removal', 'registration is absent',
                            'Do not dispatch workers into removed or pending worktrees'):
            self.assertIn(requirement, owner)
        self.assertIn('temporary directory outside the assigned worktree', reviewer)
        self.assertIn('removed or pending', foreman)
        self.assertIn('historical', foreman)
        self.assertIn('do not recreate', foreman)
        # CI remains the completion gate even though the worker can now open the PR first.
        self.assertLess(owner.index('Only after verified implementation evidence'),
                        owner.index('Launch an independent reviewer'))
