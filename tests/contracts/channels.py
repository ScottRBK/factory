"""Promises every Channel adapter keeps.

A new channel (for example Slack) is done when a subclass of ChannelContract passes for it.
"""
import io
from contextlib import redirect_stdout
from unittest.mock import patch


class ChannelContract:
    """Mix into unittest.TestCase. The subclass supplies the channel and one launched target."""

    target: dict

    def channel(self):
        raise NotImplementedError

    def test_how_to_reach_names_the_session(self):
        self.assertIn('factory-foreman-0123456789ab',
                      self.channel().how_to_reach('factory-foreman-0123456789ab'))

    def test_open_without_a_terminal_only_prints_how_to_reach(self):
        with redirect_stdout(io.StringIO()) as output, patch('sys.stdin', io.StringIO()):
            self.channel().open(self.target)
        self.assertTrue(output.getvalue().strip())
