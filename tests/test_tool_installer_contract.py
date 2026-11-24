"""Run the ToolInstaller contract against each tool Factory can install."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from contracts.tools import ToolInstallerContract

from forgetful_factory.agents.adapters.agentshell.runtime_install import AgentShellRuntimeInstall
from forgetful_factory.agents.adapters.pi.runtime_install import PiInstall
from forgetful_factory.factory.services.initialise_factory import missing_tools
from forgetful_factory.planning.adapters.forgetful.install import ForgetfulInstall
from forgetful_factory.planning.model import ForgetfulConnection
from forgetful_factory.runtime.adapters.tmux import TmuxInstall
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


class ProbeTimingTests(HostFixture):
    """Probes keep the old timing when the host changes between two lookups."""

    def test_forgetful_found_absent_is_not_also_offered_as_unready(self):
        # Arrange: the first lookup misses; the second finds a half-installed managed CLI.
        install = ForgetfulInstall(self.workspace, ForgetfulConnection())
        managed = str(self.workspace / '.factory/runtime/forgetful/bin/forgetful')
        module = 'forgetful_factory.planning.adapters.forgetful.install'
        with (patch(f'{module}.shutil.which', side_effect=[None, managed]) as which,
              patch(f'{module}.runtime_ready', return_value=False) as ready):
            # Act
            missing = missing_tools([install])
        # Assert: one offer, as the old check skipped the probe for a missing executable;
        # it still looked the executable up twice.
        self.assertEqual(missing, ['forgetful'])
        self.assertEqual(which.call_count, 2)
        ready.assert_not_called()

    def test_managed_pi_probe_reads_the_saved_home_again(self):
        # Arrange: the old check read the saved home once for the folder, once for the probe.
        install = PiInstall(self.workspace)
        managed = str(self.workspace / '.factory/runtime/pi/node_modules/.bin/pi')
        module = 'forgetful_factory.agents.adapters.pi.runtime_install'
        homes = [str(self.workspace), str(self.workspace / 'later')]
        with (patch(f'{module}.shutil.which', return_value=managed),
              patch(f'{module}.saved_pi_home', side_effect=homes),
              patch.object(PiInstall, 'ready', return_value=False) as ready):
            # Act
            missing = install.unready()
        # Assert
        self.assertEqual(missing, ['pi'])
        ready.assert_called_once_with(homes[1])
