import time

from test_planning_watch import PlanningWatchFixture


class WatchIssueChangesTests(PlanningWatchFixture):
    def test_timestamp_only_is_silent_and_comments_and_content_notify(self):
        # Arrange: start a watcher with one eligible issue.
        issue = self.issue(updated_at='one')
        self.script({'team/app': [[[issue]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        # Act and assert: timestamp-only updates stay silent; comments and content notify.
        issue['updated_at'] = 'two'
        self.script({'team/app': [[[issue]]]})
        self.wait_until(process, lambda: self.polls() >= 3)
        time.sleep(0.15)
        self.assertEqual(len(self._messages()), 1)
        comment = {'id': 5, 'body': 'A reply', 'updated_at': 'c1',
                   'user': {'login': 'automation[bot]', 'type': 'Bot'},
                   'issue_url': 'https://api.github.com/repos/team/app/issues/1'}
        self.script({'team/app': [[[issue]]]}, {'team/app': [[comment]]})
        self.wait_until(process, lambda: len(self._messages()) == 2)
        comment['body'] = 'Edited reply'
        comment['updated_at'] = 'c2'
        self.script({'team/app': [[[issue]]]}, {'team/app': [[comment]]})
        self.wait_until(process, lambda: len(self._messages()) == 3)
        issue['body'] = 'Changed requirements'
        self.script({'team/app': [[[issue]]]}, {'team/app': [[comment]]})
        self.wait_until(process, lambda: len(self._messages()) == 4)
        # Assert: the final notification carries the updated content.
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
        self.assertEqual(self._messages()[-1]['body'], 'Changed requirements')

    def test_failed_comment_read_retries_without_consuming_change(self):
        # Arrange: establish an issue notification before the comment read fails.
        issue = self.issue(updated_at='one')
        self.script({'team/app': [[[issue]]]})
        process = self.start('--existing')
        self.wait_until(process, lambda: len(self._messages()) == 1)
        comment = {'id': 5, 'body': 'Answer', 'updated_at': 'c1',
                   'issue_url': 'https://api.github.com/repos/team/app/issues/1'}
        # Act: fail the comment read, then restore it with a new comment.
        self.script({'team/app': [[[issue]]]}, {'team/app': 'temporary failure'})
        self.wait_until(process, lambda: bool(self.alerts()))
        self.assertEqual(len(self._messages()), 1)
        self.script({'team/app': [[[issue]]]}, {'team/app': [[comment]]})
        self.wait_until(process, lambda: len(self._messages()) == 2)
        # Assert: the watcher survives and delivers the pending change.
        code, _, errors = self.stop(process)
        self.assertEqual(code, 130, errors)
