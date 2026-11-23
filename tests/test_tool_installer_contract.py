"""Run the ToolInstaller contract against each tool Factory can install."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from contracts.tools import ToolInstallerContract

from forgetful_factory.agents.adapters.agentshell.runtime_install import AgentShellRuntimeInstall
from forgetful_factory.agents.adapters.agentshell.tmux_install import TmuxInstall
from forgetful_factory.agents.adapters.pi.runtime_install import PiInstall
from forgetful_factory.planning.adapters.forgetful.install import ForgetfulInstall
from forgetful_factory.planning.model import ForgetfulConnection
from forgetful_factory.shared.installation import SYNC_RECEIPT, sync_fingerprint


class HostFixture(unittest.TestCase):
    """A workspace and a PATH that holds only the commands a test puts there."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.workspace = Path(directory.name) / 'factory'
        self.workspace.mkdir()
        self.bin = Path(directory.name) / 'bin'
        self.bin.mkdir()
        environment = patch.dict(os.environ, {'PATH': str(self.bin)})
        environment.start()
        self.addCleanup(environment.stop)

    def command(self, name):
        path = self.bin / name
        path.write_text('#!/bin/sh\nexit 0\n')
        path.chmod(0o755)


class PiInstallContractTests(ToolInstallerContract, HostFixture):
    missing_on_bare_host = ('pi',)

    def installer(self):
        return PiInstall(self.workspace)

    def arrange_installed(self):
        self.command('pi')


class TmuxInstallContractTests(ToolInstallerContract, HostFixture):
    missing_on_bare_host = ('tmux',)

    def installer(self):
        return TmuxInstall(self.workspace)

    def arrange_installed(self):
        self.command('tmux')


class ForgetfulInstallContractTests(ToolInstallerContract, HostFixture):
    missing_on_bare_host = ('forgetful',)

    def installer(self):
        connection = ForgetfulConnection(database=str(self.workspace / 'forgetful.db'))
        return ForgetfulInstall(self.workspace, connection)

    def arrange_installed(self):
        self.command('forgetful')


class AgentShellRuntimeInstallContractTests(ToolInstallerContract, HostFixture):
    missing_on_bare_host = ('agentshell-runtime',)

    def installer(self):
        return AgentShellRuntimeInstall(self.workspace)

    def arrange_installed(self):
        # A finished locked sync: the receipt matches the inputs and the probe succeeds.
        project = self.workspace / '.factory/resources/agentshell/python'
        runtime = project / '.venv'
        (runtime / 'bin').mkdir(parents=True)
        inputs = (project / 'pyproject.toml', project / 'uv.lock')
        for path in inputs:
            path.write_text(path.name)
        (runtime / 'pyvenv.cfg').write_text('home = test-fixture')
        (runtime / SYNC_RECEIPT).write_text(sync_fingerprint(inputs))
        python = runtime / 'bin/python'
        python.write_text('#!/bin/sh\nexit 0\n')
        python.chmod(0o755)
