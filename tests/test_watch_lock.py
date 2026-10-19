import subprocess
import sys
import time
import unittest

import test_watch


class WatchLockTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_watch.WatchCliTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

    def test_watch_rejects_active_init_before_reading_incomplete_setup(self):
        # Arrange: block only the external Forgetful check in a real public init.
        fixture = self.fixture
        (fixture.bin / 'gh').write_text(test_watch.INIT_GH)
        fixture.env['GH_STATE'] = str(fixture.workspace / 'init-gh.json')
        marker = fixture.workspace / 'checking'
        gate = fixture.workspace / 'finish-check'
        command = fixture.bin / 'forgetful'
        original = command.read_text()
        command.write_text(original.replace(
            'import sys', 'import sys\nimport time\nfrom pathlib import Path\n'
            f'Path({str(marker)!r}).touch()\n'
            f'while not Path({str(gate)!r}).exists(): time.sleep(0.01)', 1))
        process = subprocess.Popen(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--workspace',
             str(fixture.workspace)], env=fixture.env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(fixture.cleanup_process, process)
        deadline = time.monotonic() + 5
        while not marker.exists() and process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(marker.exists())

        # Act
        watcher = fixture.start('--new-only')
        _, stderr = watcher.communicate(timeout=5)
        gate.touch()
        _, setup_error = process.communicate(timeout=5)

        # Assert
        self.assertEqual(watcher.returncode, 1, stderr)
        self.assertIn('already running', stderr)
        self.assertNotIn('incomplete', stderr)
        self.assertEqual(process.returncode, 0, setup_error)
        self.assertEqual(fixture.events(), [])

    def test_init_preserves_readiness_and_files_while_watcher_holds_workspace(self):
        # Arrange
        fixture = self.fixture
        first = fixture.start('--existing')
        fixture.wait_until(first, lambda: any(e['kind'] == 'ready' for e in fixture.events()))
        directory = fixture.workspace / '.factory'
        receipt = directory / 'agents/foreman/model-selection.json'
        original = receipt.read_bytes()
        config = (directory / 'factory.toml').read_bytes()

        # Act
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--workspace',
             str(fixture.workspace)], env=fixture.env, input='', text=True,
            capture_output=True, timeout=5)

        # Assert
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('already running', result.stderr)
        self.assertEqual(receipt.read_bytes(), original)
        self.assertEqual((directory / 'factory.toml').read_bytes(), config)
        self.assertIsNone(first.poll())
        self.assertEqual(sum(e['kind'] == 'launch' for e in fixture.events()), 1)
        fixture.stop(first)

    def test_second_watcher_is_rejected_and_stopping_first_allows_restart(self):
        # Arrange
        fixture = self.fixture
        first = fixture.start('--existing')
        fixture.wait_until(first, lambda: any(e['kind'] == 'ready' for e in fixture.events()))

        # Act
        second = fixture.start(input='e\n')
        try:
            stdout, stderr = second.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            fixture.stop(second)
            self.fail('A second watcher launched instead of rejecting the occupied workspace.')

        # Assert
        self.assertEqual(second.returncode, 1, stderr)
        self.assertIn('already running', stderr.lower())
        self.assertNotIn('tmux attach', stdout)
        self.assertNotIn('Forward existing', stdout)
        self.assertIsNone(first.poll(), 'The existing watcher must remain untouched.')
        self.assertEqual(sum(e['kind'] == 'launch' for e in fixture.events()), 1)

        # Act: release ownership, then start again
        code, _, stderr = fixture.stop(first)
        self.assertEqual(code, 130, stderr)
        restarted = fixture.start('--existing')
        fixture.wait_until(restarted, lambda: sum(e['kind'] == 'ready'
                                                  for e in fixture.events()) == 2)
        code, _, stderr = fixture.stop(restarted)

        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertEqual(sum(e['kind'] == 'launch' for e in fixture.events()), 2)
        self.assertEqual(sum(e['kind'] == 'close' for e in fixture.events()), 2)


if __name__ == '__main__':
    unittest.main()
