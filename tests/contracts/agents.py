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


class PersistentForemanContract:
    """Mix into unittest.TestCase. The subclass supplies the owner and ways to save its records.

    Starting a real owner needs a live session; the lifecycle tests cover start and status.
    """

    def owner(self):
        raise NotImplementedError

    def save_unreadable_record(self):
        raise NotImplementedError

    def save_silent_owner(self, foreman: str):
        """Save an owner record whose owner does not answer."""
        raise NotImplementedError

    def test_no_owner_gives_no_record_no_report_and_no_status(self):
        owner = self.owner()
        self.assertIsNone(owner.saved())
        self.assertIsNone(owner.report())
        with self.assertRaises(FactoryError):
            owner.status()

    def test_unreadable_record_is_reported_unknown_with_a_warning(self):
        self.save_unreadable_record()
        report = self.owner().report()
        self.assertEqual(report['observation'], 'unavailable')
        self.assertEqual(report['foreman'], 'unknown')
        self.assertTrue(report['warning'])
        with self.assertRaises(FactoryError):
            self.owner().saved()

    def test_silent_owner_is_history_never_a_live_observation(self):
        self.save_silent_owner('ready')
        report = self.owner().report()
        self.assertEqual(report['observation'], 'saved')
        self.assertEqual(report['process'], 'unknown')
        self.assertEqual(report['recorded_foreman'], 'ready')
        self.assertTrue(report['warning'])
        self.assertEqual(self.owner().saved()['foreman'], 'ready')

    def test_silent_stopped_owner_needs_no_recovery(self):
        self.save_silent_owner('stopped')
        report = self.owner().report()
        self.assertEqual(report['observation'], 'saved')
        self.assertNotIn('warning', report)
        self.assertNotIn('recovery', report)
