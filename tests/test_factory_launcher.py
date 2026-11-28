"""The launcher in FACTORY_COMMAND: one path that runs the Factory that started the Foreman.

The Foreman runs Factory commands through it. One path works with or without quotes, on any
machine and for any install method; a multi-word command breaks when a model quotes it.
"""
import os
import shlex
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from forgetful_factory.agents.adapters.agentshell.foreman_runtime import factory_launcher


class FactoryLauncherTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.workspace = self.root / 'workspace'
        self.workspace.mkdir()

    def run_launcher(self, launcher, *arguments):
        return subprocess.run([str(launcher), *arguments], capture_output=True, text=True,
                              timeout=60)

    def test_one_private_path_runs_this_factory(self):
        # Act
        launcher = factory_launcher(self.workspace, sys.executable)
        result = self.run_launcher(launcher, 'watch', '--help')
        # Assert
        self.assertEqual(launcher, self.workspace / '.factory/runtime/foreman/forgetful-factory')
        self.assertEqual(stat.S_IMODE(launcher.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(launcher.parent.stat().st_mode), 0o700)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--chat-interval', result.stdout)

    def test_an_interpreter_path_with_spaces_and_quotes_still_runs(self):
        # Arrange
        folder = self.root / "it's a folder"
        folder.mkdir()
        # A wrapper, not a link: a link to a virtual environment's Python loses the environment.
        python = folder / 'python'
        python.write_text(f'#!/bin/sh\nexec {shlex.quote(sys.executable)} "$@"\n')
        python.chmod(0o700)
        # Act
        launcher = factory_launcher(self.workspace, str(python))
        result = self.run_launcher(launcher, '--help')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('usage: forgetful-factory', result.stdout)

    def test_each_start_writes_the_launcher_again(self):
        # Arrange: an older Factory wrote the launcher, then a newer one starts.
        older = factory_launcher(self.workspace, '/old/python')
        # Act
        launcher = factory_launcher(self.workspace, sys.executable)
        # Assert
        self.assertEqual(launcher, older)
        self.assertNotIn('/old/python', launcher.read_text())
        self.assertIn(sys.executable, launcher.read_text())
        self.assertEqual(sorted(path.name for path in launcher.parent.iterdir()),
                         ['forgetful-factory'])

    def test_a_shared_runtime_folder_is_refused(self):
        # Arrange
        runtime = self.workspace / '.factory/runtime/foreman'
        runtime.mkdir(parents=True)
        runtime.chmod(0o755)
        # Act / Assert
        with self.assertRaisesRegex(Exception, 'private owned directory'):
            factory_launcher(self.workspace, sys.executable)
        self.assertFalse((runtime / 'forgetful-factory').exists())

    def test_a_link_in_place_of_the_launcher_is_replaced_not_followed(self):
        # Arrange
        target = self.root / 'elsewhere'
        target.write_text('keep')
        runtime = self.workspace / '.factory/runtime/foreman'
        runtime.mkdir(parents=True, mode=0o700)
        (runtime / 'forgetful-factory').symlink_to(target)
        # Act
        launcher = factory_launcher(self.workspace, sys.executable)
        # Assert
        self.assertEqual(target.read_text(), 'keep')
        self.assertFalse(launcher.is_symlink())
        self.assertTrue(os.access(launcher, os.X_OK))


if __name__ == '__main__':
    unittest.main()
