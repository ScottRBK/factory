"""Run the Channel contract against the terminal channel on the tmux host."""
import unittest

from contracts.channels import ChannelContract

from forgetful_factory.channels.adapters.terminal import TerminalChannel
from forgetful_factory.runtime.adapters.tmux import TmuxHost


class TerminalChannelContractTests(ChannelContract, unittest.TestCase):
    target = {'socket_path': '/tmp/tmux-1000/default', 'pane_id': '%7', 'server_pid': 10,
              'server_started': 20, 'pane_pid': 30}

    def channel(self):
        return TerminalChannel(TmuxHost())
