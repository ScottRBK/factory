"""Run the PlanStore contract against the Forgetful adapter and a stateful native fake."""
import tempfile
import unittest
from pathlib import Path

from contracts.planning import PlanStoreContract
from planning_support import PLANNING

from forgetful_factory.planning.adapters.forgetful.plan_store import ForgetfulPlanStore
from forgetful_factory.planning.model import ForgetfulConnection

FORGETFUL = ('#!/usr/bin/env python3\nimport json, os, sys\nfrom pathlib import Path\n'
             'args = sys.argv[1:]\nif True:\n' + PLANNING + "    sys.exit('unsupported call')\n")


class ForgetfulPlanStoreContractTests(PlanStoreContract, unittest.TestCase):
    project_id = 12

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.workspace = Path(directory.name)
        (self.workspace / '.factory').mkdir()
        self.executable = self.workspace / 'forgetful'
        self.executable.write_text(FORGETFUL)
        self.executable.chmod(0o755)

    def store(self):
        connection = ForgetfulConnection(instance='server', executable=str(self.executable),
                                         server='https://memory.example/test',
                                         project_id=self.project_id)
        return ForgetfulPlanStore(self.workspace, connection, execution_enabled=False)
