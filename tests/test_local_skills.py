"""Selected local skills remain editable; repeated public init never reconciles them."""
import json

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class LocalSkillTests(InitFixture):
    def setup_team(self, name='app', *flags):
        repo = self.repo(name)
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *flags)
        self.assertEqual(result.returncode, 0, result.stderr)
        return repo, repo / '.factory/agents'

    def assert_preserved_by_init(self, repo):
        factory = repo / '.factory'
        paths = [p for p in factory.rglob('*') if p.is_file() or p.is_symlink()]
        before = {p: p.readlink() if p.is_symlink() else p.read_bytes() for p in paths}
        receipt = factory / 'setup-complete.json'
        receipt_stat = receipt.stat()
        log = self.workspace / 'repeat.jsonl'
        log.unlink(missing_ok=True)
        self.env.update(PROFILE_LOG=str(log), PROFILE_FAIL='pi')
        self.state.write_text('{}')
        # Act
        result = self.run_cli(repo, worker_defaults=False)
        # Assert: preservation is positive evidence against existing files, not removed sidecars.
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('reload or restart', result.stdout)
        self.assertEqual({p: p.readlink() if p.is_symlink() else p.read_bytes() for p in paths},
                         before)
        self.assertEqual((receipt.stat().st_ino, receipt.stat().st_mtime_ns),
                         (receipt_stat.st_ino, receipt_stat.st_mtime_ns))
        self.assertEqual(events(log), [])
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.env.pop('PROFILE_FAIL')

    def add_skill(self, agents, role='research', name='team', content='# Team guidance.\n'):
        skill = agents / role / 'skills' / name / 'SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text(content)
        return skill

    def test_local_names_do_not_replace_external_selections(self):
        # Arrange
        repo, agents = self.setup_team()
        self.add_skill(agents, 'feature-owner', 'team-grill',
                       '---\nname: grill-me\ndescription: Team grilling.\n---\n')
        selected = json.loads((agents / 'feature-owner/agent.json').read_text())
        self.assertIn(str(self.grill_skill), selected['agent']['resources']['skills'])
        self.assertIn('./skills', selected['agent']['resources']['skills'])
        self.assert_preserved_by_init(repo)

    def test_local_skill_can_share_another_roles_folder_name(self):
        # Arrange
        repo, agents = self.setup_team()
        self.add_skill(agents, name='review')
        self.assert_preserved_by_init(repo)

    def test_legacy_receipt_cannot_authorize_reordering_manual_selections(self):
        # Arrange: obsolete metadata is inert user content, never migration authority.
        repo, agents = self.setup_team()
        selected = json.loads((agents / 'feature-owner/agent.json').read_text())
        skills = selected['agent']['resources']['skills']
        receipt = {'version': 1, 'managed': {}, 'pending': {'feature-owner': {
            'before': skills, 'after': list(reversed(skills)), 'parent_before': None}}}
        (agents / 'skill-registration.json').write_text(json.dumps(receipt))
        self.assert_preserved_by_init(repo)

    def test_removed_local_skill_preserves_custom_explicit_selection(self):
        # Arrange
        repo, agents = self.setup_team()
        custom = self.workspace / 'custom/SKILL.md'
        custom.parent.mkdir()
        custom.write_text('# Keep custom guidance.\n')
        path = agents / 'research/agent.json'
        document = json.loads(path.read_text())
        document['agent']['resources']['skills'].append(str(custom))
        path.write_text(json.dumps(document))
        self.add_skill(agents).unlink()
        self.assert_preserved_by_init(repo)
        self.assertEqual(custom.read_text(), '# Keep custom guidance.\n')

    def test_repeated_init_preserves_legacy_receipt_and_skill_symlinks(self):
        # Arrange
        repo, agents = self.setup_team()
        skill = self.add_skill(agents)
        outside = self.workspace / 'outside'
        outside.write_text('Preserve target bytes')
        skill.unlink()
        skill.symlink_to(outside)
        (agents / 'skill-registration.json').symlink_to(outside)
        self.assert_preserved_by_init(repo)
        self.assertEqual(outside.read_text(), 'Preserve target bytes')

    def test_malformed_legacy_receipts_cannot_authorize_selection_writes(self):
        # Arrange
        repo, agents = self.setup_team()
        outside = self.workspace / 'outside'
        outside.write_text('preserve outside file')
        for content in ('{broken', '[]', '{"version":true}',
                        json.dumps({'managed': {'research': [str(outside)]}}),
                        '{"pending":{"../outside":{}}}'):
            with self.subTest(content=content):
                (agents / 'skill-registration.json').write_text(content)
                self.assert_preserved_by_init(repo)
                self.assertEqual(outside.read_text(), 'preserve outside file')

    def test_missing_explicit_child_skill_is_not_pruned_or_recursively_validated_by_init(self):
        # Arrange: native child loading owns the error; init preserves the user's selection.
        repo, agents = self.setup_team()
        skill = self.add_skill(agents)
        path = agents / 'research/agent.json'
        document = json.loads(path.read_text())
        document['agent']['resources']['skills'].append(str(skill))
        path.write_text(json.dumps(document))
        skill.unlink()
        self.assert_preserved_by_init(repo)

    def test_parent_and_child_edits_remain_independent_after_interrupted_manual_edit(self):
        # Arrange
        repo, agents = self.setup_team()
        parent = agents / 'feature-owner/agent.json'
        document = json.loads(parent.read_text())
        document['roster']['roles'] = [{'agent_file': '../research/agent.json'}]
        parent.write_text(json.dumps(document))
        child = agents / 'research/agent.json'
        child.write_text('{partially edited')
        self.assert_preserved_by_init(repo)

    def test_edits_to_added_and_starter_skill_contents_are_preserved(self):
        # Arrange
        repo, agents = self.setup_team()
        self.add_skill(agents, content='---\nname: team\ndescription: 123\n---\n')
        (agents / 'research/skills/research/SKILL.md').write_text('# Manual research briefing.\n')
        self.assert_preserved_by_init(repo)

    def test_read_only_parent_needs_no_reconciliation_when_child_skills_change(self):
        # Arrange
        repo, agents = self.setup_team()
        self.add_skill(agents)
        owner = agents / 'feature-owner'
        owner.chmod(0o500)
        try:
            self.assert_preserved_by_init(repo)
        finally:
            owner.chmod(0o700)

    def test_deleted_and_renamed_local_skills_do_not_rewrite_selected_directories(self):
        # Arrange
        repo, agents = self.setup_team()
        for role in ('foreman', 'feature-owner', 'research'):
            skill = self.add_skill(agents, role)
            if role == 'research':
                skill.parent.rename(skill.parent.with_name('renamed'))
            else:
                skill.unlink()
                skill.parent.rmdir()
        self.assert_preserved_by_init(repo)
        self.assertTrue((agents / 'research/skills/renamed/SKILL.md').is_file())

    def test_init_does_not_interpret_new_skill_contents(self):
        # Arrange
        repo, agents = self.setup_team()
        skill = self.add_skill(agents, content='This skill has no YAML header.\n')
        skill.write_bytes(b'Native harness validates this content\xff')
        self.assert_preserved_by_init(repo)

    def test_harness_resolves_duplicate_skill_names(self):
        # Arrange
        repo, agents = self.setup_team()
        for name in ('team-a', 'team-b'):
            self.add_skill(agents, name=name,
                           content='---\nname: team\ndescription: Team context.\n---\n')
        self.assert_preserved_by_init(repo)

    def test_pi_worker_local_directory_and_tdd_selection_remain_authoritative(self):
        # Arrange
        flags = worker_settings(self, harness='pi', model='provider/model', effort='high')
        repo, agents = self.setup_team('app', *flags)
        self.add_skill(agents, 'implementation')
        document = json.loads((agents / 'implementation/agent.json').read_text())
        self.assertEqual(document['agent']['resources']['skills'],
                         ['./skills', str(self.workspace / 'tdd/SKILL.md'),
                          str(self.workspace / 'standards/SKILL.md')])
        self.assert_preserved_by_init(repo)

    def test_drop_in_worker_skills_preserve_pi_and_codex_authoritative_selections(self):
        for harness, model, effort in (('pi', 'provider/model', 'high'),
                                       ('codex', 'gpt-5.4', 'xhigh')):
            with self.subTest(harness=harness):
                # Arrange
                flags = worker_settings(self, harness=harness, model=model, effort=effort)[:12]
                repo, agents = self.setup_team(harness, *flags)
                for role in ('implementation', 'review'):
                    self.add_skill(agents, role)
                    selected = json.loads((agents / role / 'agent.json').read_text())
                    self.assertIn('./skills', selected['agent']['resources']['skills'])
                    self.assertEqual(selected['roster'], {'enabled': False, 'roles': []})
                self.assert_preserved_by_init(repo)

    def test_unavailable_child_skill_does_not_trigger_registration_or_completion_rewrite(self):
        # Arrange
        repo, agents = self.setup_team()
        invalid = agents / 'research/skills/team/SKILL.md'
        invalid.mkdir(parents=True)
        self.assert_preserved_by_init(repo)
        self.assertTrue(invalid.is_dir())

    def test_additions_across_team_preserve_references_comments_and_completion(self):
        # Arrange
        repo, agents = self.setup_team()
        for role in ('foreman', 'feature-owner', 'research'):
            self.add_skill(agents, role)
        config = repo / '.factory/factory.toml'
        config.write_text('# Preserve this comment.\n' + config.read_text())
        self.assert_preserved_by_init(repo)
        for parent, child in (('foreman', 'feature-owner'), ('feature-owner', 'research')):
            document = json.loads((agents / parent / 'agent.json').read_text())
            self.assertIn({'agent_file': f'../{child}/agent.json'}, document['roster']['roles'])
