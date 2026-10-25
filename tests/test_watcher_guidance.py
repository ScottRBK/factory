"""Public watch setup exposes alert guidance; this does not prove model compliance."""

from test_watch import WatchFixture


class WatcherGuidanceTests(WatchFixture):
    def test_native_duplicate_retirement_guidance_preserves_records_and_claims(self):
        # Public setup provisions this selected starter skill; no model action is claimed.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        self.assertEqual(self.stop(process)[0], 130)
        text = (self.workspace / '.factory/agents/foreman/skills/foreman/SKILL.md').read_text()
        for phrase in ('Duplicate ownership records', 'user approval', 'change BOTH',
                       'not compare-and-swap', 'transition_task', 'running', 'pinned task',
                       'Fresh issue preflight', 'config edits need restart'):
            self.assertIn(phrase, text)

    def test_interrupted_setup_guidance_requires_approved_native_completion(self):
        # Arrange/Act: public setup provisions the selected skill and watch loads its directory.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, errors = self.stop(process)
        # Assert: this is instruction delivery evidence, not model behavior.
        self.assertEqual(code, 130, errors)
        text = (self.workspace / '.factory/agents/foreman/skills/foreman/SKILL.md').read_text()
        for instruction in ('Interrupted first-time setup', 'user approval', 'get_plan',
                            'query_tasks', 'get_task', 'create_task', 'factory-ownership',
                            'local_dir', 'read-only', 'deliberately restart', 'pinned task'):
            self.assertIn(instruction, text)

    def test_selected_foreman_has_alert_guidance_without_overwriting_user_edits(self):
        # Arrange: the public setup fixture provisions the selected Foreman's skill.
        skill = self.workspace / ".factory/agents/foreman/skills/foreman/SKILL.md"
        original = skill.read_text() + "\nKeep my local escalation preferences.\n"
        skill.write_text(original)
        # Act
        process = self.start("--new-only")
        self.wait_until(process, lambda: any(e["kind"] == "ready" for e in self.events()))
        code, _, errors = self.stop(process)
        # Assert: inspect delivered instructions, not hypothetical agent behaviour.
        self.assertEqual(code, 130, errors)
        self.assertEqual(skill.read_text(), original)
        (launch,) = [e for e in self.events() if e["kind"] == "launch"]
        self.assertEqual(launch["cwd"], str(skill.parents[2]))
        self.assertIn(str(skill.parents[1]), launch["resources"]["skills"])
        for instruction in (
            "Factory watcher alert.",
            "Discuss the problem with the user",
            "An alert is not a work notification",
            "does not pause an already-running owner",
            "Never repeat an uncertain write",
            "Existing user-edited skills are preserved",
        ):
            with self.subTest(instruction=instruction):
                self.assertIn(instruction, original)
