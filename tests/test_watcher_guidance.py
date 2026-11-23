"""Public watch setup preserves the selected Foreman skill and loads its directory."""

from test_watch import WatchFixture


class WatcherGuidanceTests(WatchFixture):
    def test_selected_foreman_skill_loads_without_overwriting_user_edits(self):
        # Arrange: the public setup fixture provisions the selected Foreman's skill.
        skill = self.workspace / ".factory/agents/foreman/skills/foreman/SKILL.md"
        original = skill.read_text() + "\nKeep my local escalation preferences.\n"
        skill.write_text(original)
        # Act
        process = self.start("--new-only")
        self.wait_until(process, lambda: any(e["kind"] == "ready" for e in self.events()))
        code, _, errors = self.stop(process)
        # Assert
        self.assertEqual(code, 130, errors)
        self.assertEqual(skill.read_text(), original)
        (launch,) = [e for e in self.events() if e["kind"] == "launch"]
        self.assertEqual(launch["cwd"], str(skill.parents[2]))
        self.assertIn(str(skill.parents[1]), launch["resources"]["skills"])
