"""Role-local skill registration through public init."""
import json

from test_init import INIT_SETTINGS, InitFixture
from worker_support import worker_settings


class LocalSkillTests(InitFixture):
    def test_local_names_do_not_replace_external_selections(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        skill = agents / 'feature-owner/skills/team-grill/SKILL.md'
        skill.parent.mkdir()
        content = '---\nname: grill-me\ndescription: Team grilling.\n---\n'
        skill.write_text(content)
        selected = agents / 'feature-owner/resources.json'
        previous = json.loads(selected.read_text())['skills']
        # Act
        registered = self.run_cli(repo)
        # Assert: native name resolution does not change Factory's path selections.
        self.assertEqual(registered.returncode, 0, registered.stderr)
        expected = [*previous, str(skill)]
        self.assertEqual(json.loads(selected.read_text())['skills'], expected)
        roster = json.loads((agents / 'foreman/roster.json').read_text())
        self.assertEqual(roster['roster']['roles'][0]['resources']['skills'], expected)
        self.assertEqual(skill.read_text(), content)

    def test_local_skill_can_share_another_roles_folder_name(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        role = repo / '.factory/agents/research'
        skill = role / 'skills/review/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: review\ndescription: Review research notes.\n---\n')
        # Act
        registered = self.run_cli(repo)
        # Assert
        self.assertEqual(registered.returncode, 0, registered.stderr)
        self.assertIn(str(skill), json.loads((role / 'resources.json').read_text())['skills'])

    def test_receipt_cannot_authorize_reordering_manual_selections(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        selected = agents / 'foreman/resources.json'
        before = selected.read_bytes()
        skills = json.loads(before)['skills']
        receipt = {'version': 1, 'managed': {}, 'pending': {'foreman': {
            'before': skills, 'after': list(reversed(skills)), 'parent_before': None}}}
        (agents / 'skill-registration.json').write_text(json.dumps(receipt))
        # Act
        rejected = self.run_cli(repo)
        # Assert
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('registration', rejected.stderr)
        self.assertEqual(selected.read_bytes(), before)

    def test_automatic_removal_preserves_custom_selection_and_accepts_child_already_repaired(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        custom = self.workspace / 'team-guidance/SKILL.md'
        custom.parent.mkdir()
        custom.write_text('# Custom guidance, preserved without metadata migration.\n')
        selected = agents / 'research/resources.json'
        data = json.loads(selected.read_text())
        data['skills'].append(str(custom))
        selected.write_text(json.dumps(data))
        roster = agents / 'feature-owner/roster.json'
        data = json.loads(roster.read_text())
        data['roster']['roles'][0]['resources']['skills'].append(str(custom))
        roster.write_text(json.dumps(data))
        automatic = agents / 'research/skills/team-context/SKILL.md'
        automatic.parent.mkdir()
        automatic.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        registered = self.run_cli(repo)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        automatic.unlink()
        data = json.loads(selected.read_text())
        data['skills'].remove(str(automatic))
        selected.write_text(json.dumps(data))
        before_selected = selected.read_bytes()
        # Act
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertEqual(selected.read_bytes(), before_selected)
        skills = json.loads(roster.read_text())['roster']['roles'][0]['resources']['skills']
        self.assertEqual(skills, data['skills'])
        self.assertIn(str(custom), skills)
        self.assertEqual(custom.read_text(),
                         '# Custom guidance, preserved without metadata migration.\n')

    def test_registration_rejects_receipt_and_managed_skill_symlinks(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        skill = agents / 'research/skills/team-context/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        self.assertEqual(self.run_cli(repo).returncode, 0)
        receipt = agents / 'skill-registration.json'
        selected = agents / 'research/resources.json'
        roster = agents / 'feature-owner/roster.json'
        before = selected.read_bytes(), roster.read_bytes()
        for target in (receipt, skill):
            with self.subTest(target=target):
                original = target.read_bytes()
                outside = self.workspace / 'outside'
                outside.write_bytes(original)
                target.unlink()
                target.symlink_to(outside)
                try:
                    # Act
                    rejected = self.run_cli(repo)
                    # Assert
                    self.assertNotEqual(rejected.returncode, 0)
                    self.assertIn('symlink', rejected.stderr)
                    self.assertEqual((selected.read_bytes(), roster.read_bytes()), before)
                    self.assertEqual(outside.read_bytes(), original)
                finally:
                    target.unlink()
                    target.write_bytes(original)

    def test_malformed_registration_receipts_cannot_authorize_selection_writes(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        receipt = agents / 'skill-registration.json'
        selected = agents / 'research/resources.json'
        roster = agents / 'feature-owner/roster.json'
        before = selected.read_bytes(), roster.read_bytes()
        outside = self.workspace / 'outside.json'
        outside.write_text('preserve outside file')
        skills = json.loads(selected.read_text())['skills']
        cases = ['{broken', '[]', json.dumps({'version': True, 'managed': {}, 'pending': {}}),
                 json.dumps({'version': 1, 'managed': {'research': [str(outside)]},
                             'pending': {}}),
                 json.dumps({'version': 1, 'managed': {}, 'pending': {'research': {
                     'before': skills, 'after': [*skills, str(outside)],
                     'parent_before': skills}}}),
                 json.dumps({'version': 1, 'managed': {}, 'pending': {'../outside': {}}})]
        for content in cases:
            with self.subTest(content=content):
                receipt.write_text(content)
                # Act
                rejected = self.run_cli(repo)
                # Assert
                self.assertNotEqual(rejected.returncode, 0)
                self.assertNotIn('Traceback', rejected.stderr)
                self.assertIn('registration', rejected.stderr)
                self.assertEqual((selected.read_bytes(), roster.read_bytes()), before)
                self.assertEqual(outside.read_text(), 'preserve outside file')
                self.assertEqual(receipt.read_text(), content)

    def test_untracked_local_selection_is_never_pruned_as_automatic(self):
        # Arrange: a user selected this file before Factory's first registration receipt.
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        skill = agents / 'research/skills/manual-context/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('# Manually selected team guidance, without native metadata.\n')
        selected = agents / 'research/resources.json'
        data = json.loads(selected.read_text())
        data['skills'].append(str(skill))
        selected.write_text(json.dumps(data))
        roster = agents / 'feature-owner/roster.json'
        data = json.loads(roster.read_text())
        data['roster']['roles'][0]['resources']['skills'].append(str(skill))
        roster.write_text(json.dumps(data))
        accepted = self.run_cli(repo)
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        before = selected.read_bytes(), roster.read_bytes()
        skill.unlink()
        # Act
        rejected = self.run_cli(repo)
        # Assert
        self.assertNotEqual(rejected.returncode, 0)
        self.assertEqual((selected.read_bytes(), roster.read_bytes()), before)

    def test_interrupted_registration_does_not_overwrite_a_conflicting_parent_edit(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        skill = agents / 'research/skills/team-context/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        owner = agents / 'feature-owner'
        owner.chmod(0o500)
        try:
            interrupted = self.run_cli(repo)
        finally:
            owner.chmod(0o700)
        self.assertNotEqual(interrupted.returncode, 0)
        roster = owner / 'roster.json'
        data = json.loads(roster.read_text())
        data['roster']['roles'][0]['resources']['skills'].append('/manual-selection')
        roster.write_text(json.dumps(data))
        before = roster.read_bytes()
        selected = agents / 'research/resources.json'
        before_selected = selected.read_bytes()
        # Act
        rejected = self.run_cli(repo)
        # Assert
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('registration', rejected.stderr)
        self.assertEqual(roster.read_bytes(), before)
        self.assertEqual(selected.read_bytes(), before_selected)
        self.assertFalse((agents / 'foreman/model-selection.json').exists())

    def test_edits_to_managed_and_manual_skill_contents_are_preserved(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        role = repo / '.factory/agents/research'
        managed = role / 'skills/team-context/SKILL.md'
        managed.parent.mkdir()
        managed.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        self.assertEqual(self.run_cli(repo).returncode, 0)
        manual = role / 'skills/research/SKILL.md'
        manual_content = '# Preserve this manually edited research guidance.\n'
        managed_content = '---\nname: team-context\ndescription: 123\n---\n'
        manual.write_text(manual_content)
        managed.write_text(managed_content)
        before = (role / 'resources.json').read_bytes()
        # Act
        refreshed = self.run_cli(repo)
        # Assert
        self.assertEqual(refreshed.returncode, 0, refreshed.stderr)
        self.assertEqual((role / 'resources.json').read_bytes(), before)
        self.assertEqual(manual.read_text(), manual_content)
        self.assertEqual(managed.read_text(), managed_content)
        self.assertTrue((role.parent / 'foreman/model-selection.json').exists())

    def test_interrupted_registration_repairs_parent_roster_on_retry(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        skill = agents / 'research/skills/team-context/SKILL.md'
        skill.parent.mkdir()
        skill.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        owner = agents / 'feature-owner'
        selected = agents / 'research/resources.json'
        roster = owner / 'roster.json'
        before = roster.read_bytes()
        owner.chmod(0o500)
        try:
            # Act: resources can be written but the parent roster cannot.
            failed = self.run_cli(repo)
        finally:
            owner.chmod(0o700)
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn(str(skill), json.loads(selected.read_text())['skills'])
        self.assertEqual(roster.read_bytes(), before)
        self.assertFalse((agents / 'foreman/model-selection.json').exists())
        retry = self.run_cli(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        research = json.loads(roster.read_text())['roster']['roles'][0]
        self.assertEqual(research['resources']['skills'],
                         json.loads(selected.read_text())['skills'])

    def test_deleted_and_renamed_automatic_skills_reconcile_on_init(self):
        # Arrange
        repo = self.repo()
        self.assertEqual(self.run_cli(repo, '--repo', '.', *INIT_SETTINGS).returncode, 0)
        agents = repo / '.factory/agents'
        for role in ('foreman', 'feature-owner', 'research'):
            path = agents / role / 'skills/team-context/SKILL.md'
            path.parent.mkdir()
            path.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        registered = self.run_cli(repo)
        self.assertEqual(registered.returncode, 0, registered.stderr)
        for role in ('foreman', 'feature-owner', 'research'):
            folder = agents / role / 'skills/team-context'
            if role == 'research':
                folder.rename(folder.with_name('team-renamed'))
            else:
                (folder / 'SKILL.md').unlink()
                folder.rmdir()
        # Act
        retry = self.run_cli(repo)
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        for role in ('foreman', 'feature-owner', 'research'):
            selected = json.loads((agents / role / 'resources.json').read_text())['skills']
            self.assertFalse(any('team-context' in value for value in selected))
        selected = json.loads((agents / 'research/resources.json').read_text())['skills']
        self.assertIn(str(agents / 'research/skills/team-renamed/SKILL.md'), selected)
        roster = json.loads((agents / 'feature-owner/roster.json').read_text())
        self.assertEqual(roster['roster']['roles'][0]['resources']['skills'], selected)

    def test_init_registers_skills_without_interpreting_contents(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/research'
        skill = role / 'skills/team-context/SKILL.md'
        skill.parent.mkdir()
        contents = ('# Plain guidance without a header.\n',
                    '---\nname: team-context\ndescription: "unclosed\n---\n',
                    '---\nname: team-context\ndescription: 123\n---\n',
                    '---\nname: team-context\ncontext: &team Team notes.\n'
                    'description: *team\n---\n')
        for content in contents:
            with self.subTest(content=content):
                skill.write_text(content)
                # Act
                result = self.run_cli(repo)
                # Assert: registration forwards paths; the harness interprets the file.
                self.assertEqual(result.returncode, 0, result.stderr)
                selected = json.loads((role / 'resources.json').read_text())['skills']
                self.assertEqual(selected.count(str(skill)), 1)
                roster = json.loads((role.parent / 'feature-owner/roster.json').read_text())
                self.assertEqual(roster['roster']['roles'][0]['resources']['skills'], selected)
                self.assertEqual(skill.read_text(), content)

    def test_harness_resolves_duplicate_skill_names(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        role = repo / '.factory/agents/research'
        skills = []
        content = '---\nname: team\ndescription: Team context.\n---\n'
        for folder in ('team-a', 'team-b'):
            path = role / 'skills' / folder / 'SKILL.md'
            path.parent.mkdir()
            path.write_text(content)
            skills.append(path)
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        selected = json.loads((role / 'resources.json').read_text())['skills']
        for path in skills:
            self.assertIn(str(path), selected)
            self.assertEqual(path.read_text(), content)

    def test_init_registers_worker_local_skills_without_rewriting_config(self):
        # Arrange
        repo = self.repo()
        flags = worker_settings(self, harness='pi', model='provider/model', effort='high')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, *flags)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        extra = agents / 'implementation/skills/team-context/SKILL.md'
        extra.parent.mkdir(parents=True)
        extra.write_text('---\nname: team-context\ndescription: Team context.\n---\n')
        config = repo / '.factory/factory.toml'
        saved = config.read_bytes()

        # Act
        result = self.run_cli(repo, worker_defaults=False)

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        resources = json.loads((agents / 'implementation/resources.json').read_text())
        self.assertIn(str(extra), resources['skills'])
        self.assertIn(str(self.workspace / 'tdd/SKILL.md'), resources['skills'])
        roster = json.loads((agents / 'feature-owner/roster.json').read_text())
        worker = next(r for r in roster['roster']['roles'] if r['name'] == 'implementation')
        self.assertIn(str(extra), worker['resources']['skills'])
        self.assertEqual(config.read_bytes(), saved)
        retry = self.run_cli(repo, worker_defaults=False)
        self.assertEqual(retry.returncode, 0, retry.stderr)

    def test_unavailable_skill_file_preserves_selections_and_blocks_completion(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        extra = agents / 'research/skills/team-context/SKILL.md'
        extra.mkdir(parents=True)
        selected = agents / 'research/resources.json'
        saved = selected.read_bytes()
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(str(extra), result.stderr)
        self.assertIn('regular file', result.stderr)
        self.assertEqual(selected.read_bytes(), saved)
        self.assertFalse((agents / 'foreman/model-selection.json').exists())
        extra.rmdir()
        extra.write_text('# Contents are for the harness to read.\n')
        extra.chmod(0o000)
        try:
            unreadable = self.run_cli(repo)
        finally:
            extra.chmod(0o600)
        self.assertNotEqual(unreadable.returncode, 0)
        self.assertIn('readable', unreadable.stderr)
        self.assertEqual(selected.read_bytes(), saved)

    def test_init_registers_local_skills_and_parent_rosters_preserving_edits(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        agents = repo / '.factory/agents'
        contents = '---\nname: team-context\ndescription: Team context.\n---\nKeep our edits.\n'
        for role in ('foreman', 'feature-owner', 'research'):
            path = agents / role / 'skills/team-context/SKILL.md'
            path.parent.mkdir(parents=True)
            path.write_text(contents)
        config = repo / '.factory/factory.toml'
        config.write_text('# Preserve this comment.\n' + config.read_text())
        saved = config.read_bytes()

        # Act
        result = self.run_cli(repo)

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        for role in ('foreman', 'feature-owner', 'research'):
            directory = agents / role
            skill = directory / 'skills/team-context/SKILL.md'
            selected = json.loads((directory / 'resources.json').read_text())['skills']
            self.assertIn(str(skill), selected)
            self.assertEqual(skill.read_text(), contents)
        for parent, child in (('foreman', 'feature-owner'), ('feature-owner', 'research')):
            roster = json.loads((agents / parent / 'roster.json').read_text())
            entry = next(r for r in roster['roster']['roles'] if r['name'] == child)
            self.assertIn(str(agents / child / 'skills/team-context/SKILL.md'),
                          entry['resources']['skills'])
        self.assertEqual(config.read_bytes(), saved)
        self.assertIn('.factory/agents/<role>/skills/<name>/SKILL.md', result.stdout)
        self.assertIn('/reload', result.stdout)
