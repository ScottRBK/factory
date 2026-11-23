"""Run the planning contracts against the Forgetful adapters and stateful native fakes."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from contracts.planning import PlanningSetupContract, PlanStoreContract
from planning_support import PLANNING
from profile_support import COMMAND

from forgetful_factory.planning.adapters.forgetful.plan_store import ForgetfulPlanStore
from forgetful_factory.planning.adapters.forgetful.setup import ForgetfulSetup
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


class ForgetfulSetupContractTests(PlanningSetupContract, unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.workspace = Path(directory.name)
        (self.workspace / '.factory').mkdir()
        self.executable = self.workspace / 'forgetful'
        self.executable.write_text(COMMAND)
        self.executable.chmod(0o755)
        projects = self.workspace / 'projects.json'
        projects.write_text('[]')
        environment = patch.dict(os.environ, {'PROFILE_PROJECTS_FILE': str(projects)})
        environment.start()
        self.addCleanup(environment.stop)

    def setup(self):
        return ForgetfulSetup(self.workspace)

    def connection(self, project_id=None):
        return ForgetfulConnection(executable=str(self.executable),
                                   database=str(self.workspace / '.factory/data/forgetful.db'),
                                   project_id=project_id)
