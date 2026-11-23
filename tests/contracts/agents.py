"""Promises every AgentTeam adapter keeps about consent and setup completion.

A new agent team adapter is done when a subclass of AgentTeamContract passes for it.
"""
from forgetful_factory.shared.errors import FactoryError


class AgentTeamContract:
    """Mix into unittest.TestCase. The subclass supplies the team and an existing native home."""

    home: str

    def team(self):
        raise NotImplementedError

    def test_declined_home_stops_setup_and_saves_nothing(self):
        team = self.team()
        with self.assertRaises(FactoryError):
            team.choose_pi_home(self.home, lambda home: False)
        team.save_pi_choice()
        with self.assertRaises(FactoryError):
            self.team().pi_home()

    def test_accepted_home_is_kept_once_saved(self):
        team = self.team()
        self.assertEqual(team.choose_pi_home(self.home, lambda home: True), self.home)
        team.save_pi_choice()
        self.assertEqual(self.team().pi_home(), self.home)

    def test_setup_is_incomplete_until_completion_is_recorded(self):
        team = self.team()
        team.begin_setup()
        with self.assertRaises(FactoryError):
            team.validate_completion()

    def test_no_memory_notice_before_a_launch_is_selected(self):
        self.assertIsNone(self.team().managed_memory_notice())
