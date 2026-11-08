"""Discussion setup through public CLI, native tmux and fixture-owned Pi without inference."""
import json

from lifecycle_support import LifecycleFixture
from test_init import INIT_SETTINGS


class AgreementDiscussionTests(LifecycleFixture):
    def test_saved_incomplete_setup_can_start_discussion_without_a_default_policy(self):
        # Arrange
        repo = self.repo()
        incomplete = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, agreement_input='')
        self.assertNotEqual(incomplete.returncode, 0)
        # Act
        discussion = self.run_cli(repo, '--finalize', agreement_input='4\n', timeout=20)
        # Assert
        self.assertEqual(discussion.returncode, 0, discussion.stderr)
        self.assertFalse((repo / '.factory/definition_of_done.md').exists())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        state = self.status(repo)
        self.assertEqual(state['foreman'], 'ready')
        self.send_and_wait_for_exit(repo, state['target'])

    def test_discussion_retains_incomplete_setup_until_agreement_is_saved(self):
        # Arrange
        repo = self.repo()
        # Act
        discussed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                                 agreement_input='4\n', timeout=20)
        # Assert: discussion is not an invented fourth completion policy.
        self.assertEqual(discussed.returncode, 0, discussed.stderr)
        self.assertFalse((repo / '.factory/definition_of_done.md').exists())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        original = self.status(repo)
        self.assertEqual(original['foreman'], 'ready')
        events = [json.loads(line)
                  for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        launch, = [event for event in events if 'started' in event]
        self.assertEqual(launch['workspace'], str(repo))
        blocked = self.watch(repo, '--start', '--existing')
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse((self.workspace / 'plans.json').exists())
        # Act: unresolved finalization must not launch a second Foreman.
        still_discussing = self.run_cli(repo, '--finalize', '--delegated-work-stopped',
                                        agreement_input='4\n')
        # Assert
        self.assertNotEqual(still_discussing.returncode, 0)
        self.assertIn('init --attach', still_discussing.stderr)
        self.assertEqual(self.status(repo)['target'], original['target'])
        # Arrange: emulate the user-confirmed conversation save, not model compliance.
        agreement = repo / '.factory/definition_of_done.md'
        text = '# Package delivery\n\nReview, required checks, merge and a verified package.\n'
        agreement.write_text(text)
        # Act
        finalized = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        # Assert
        self.assertEqual(finalized.returncode, 0, finalized.stderr)
        self.assertEqual(agreement.read_text(), text)
        self.assertEqual(self.status(repo)['target'], original['target'])
        self.assertTrue((repo / '.factory/setup-complete.json').is_file())
        self.send_and_wait_for_exit(repo, original['target'])
