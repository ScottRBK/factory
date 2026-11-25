"""Run the PersistentForeman contract against the AgentShell owner client, without live owners."""
import json
import tempfile
import unittest
from pathlib import Path

from contracts.agents import PersistentForemanContract

from forgetful_factory.agents.adapters.agentshell.owner_client import AgentShellOwner
from forgetful_factory.runtime.adapters.tmux import TmuxHost


class AgentShellOwnerContractTests(PersistentForemanContract, unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name).resolve()
        self.runtime = self.workspace / '.factory/runtime/foreman'

    def owner(self):
        return AgentShellOwner(self.workspace, 'python3', host=TmuxHost())

    def save_unreadable_record(self):
        self.runtime.mkdir(parents=True, mode=0o700)
        (self.runtime / 'owner.json').write_text('{unreadable')

    def save_silent_owner(self, foreman: str):
        self.runtime.mkdir(parents=True, mode=0o700)
        (self.runtime / 'owner.json').write_text(json.dumps({
            'workspace': str(self.workspace), 'run_id': 'run', 'foreman': foreman,
            'watcher': 'stopped', 'target': None}))
