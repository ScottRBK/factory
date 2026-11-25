"""Run the AgentTeam contract against the Pi agent team."""
import os
import tempfile
import unittest
from pathlib import Path

from contracts.agents import AgentTeamContract

from forgetful_factory.agents.adapters.pi.agent_team import PiAgentTeam


class PiAgentTeamContractTests(AgentTeamContract, unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.workspace = Path(directory.name) / 'factory'
        self.workspace.mkdir()
        self.home = str(Path(directory.name) / 'native pi')
        Path(self.home).mkdir()

    def team(self):
        return PiAgentTeam(self.workspace, role_environment=lambda connection, home: dict(
            os.environ), missing_tools=lambda connection: [])
