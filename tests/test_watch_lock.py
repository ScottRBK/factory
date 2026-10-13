import subprocess
import unittest

import test_watch


class WatchLockTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_watch.WatchCliTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)

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
