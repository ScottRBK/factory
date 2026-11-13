import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from forgetful_factory.adapters.github.work_tracking import GitHubWorkTracking
from forgetful_factory.domain.models import WorkSource


class GitHubIssueChangesTests(unittest.TestCase):
    def test_reads_comments_only_for_eligible_issues_and_attributes_them(self):
        # Arrange: historical and unrelated comments are not available to the adapter.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gh = root / 'gh'
            gh.write_text('''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
endpoint = sys.argv[2]
with Path(os.environ['GH_CALLS']).open('a') as calls:
    calls.write(endpoint + '\\n')
responses = json.loads(Path(os.environ['GH_RESPONSES']).read_text())
if endpoint not in responses:
    sys.exit('unexpected endpoint')
print(json.dumps(responses[endpoint]))
''')
            gh.chmod(0o755)
            calls, responses = root / 'calls', root / 'responses'
            def issue(number, labels):
                return {'number': number, 'title': f'Issue {number}', 'body': '',
                        'html_url': f'https://github.com/team/app/issues/{number}',
                        'state': 'open', 'labels': [{'name': label} for label in labels]}
            def comment(number, body):
                return {'id': number, 'body': body, 'updated_at': 't1',
                        'issue_url': f'https://api.github.com/repos/Team/App/issues/{number}'}
            issue_endpoint = 'repos/team/app/issues?state=open&per_page=100'
            first_endpoint = 'repos/team/app/issues/1/comments?per_page=100'
            second_endpoint = 'repos/team/app/issues/2/comments?per_page=100'
            data = {issue_endpoint: [[issue(1, ['factory']), issue(2, ['factory']),
                                      issue(3, ['other'])]],
                    first_endpoint: [[comment(1, 'First')]],
                    second_endpoint: [[comment(2, 'Second')]]}
            responses.write_text(json.dumps(data))
            adapter = GitHubWorkTracking()
            source = WorkSource('github', 'team/app')
            env = {'PATH': f'{root}:{os.environ["PATH"]}', 'GH_CALLS': str(calls),
                   'GH_RESPONSES': str(responses)}
            # Act: read both eligible issues, edit only the second, then exclude all.
            with patch.dict(os.environ, env):
                first = adapter.list_issues(source, ('factory',))
                data[second_endpoint][0][0]['body'] = 'Edited second'
                responses.write_text(json.dumps(data))
                second = adapter.list_issues(source, ('factory',))
                empty = adapter.list_issues(source, ('absent',))
            # Assert: only issue 2 changes, and no unrelated comment request is made.
            self.assertEqual(len(first), 2)
            self.assertEqual(first[0].revision, second[0].revision)
            self.assertNotEqual(first[1].revision, second[1].revision)
            self.assertEqual(empty, ())
            self.assertEqual(calls.read_text().splitlines(), [
                issue_endpoint, first_endpoint, second_endpoint,
                issue_endpoint, first_endpoint, second_endpoint, issue_endpoint])

    def test_timestamp_only_does_not_change_revision_but_content_does(self):
        # Arrange: a controlled gh program serves one eligible issue without comments.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gh = root / 'gh'
            gh.write_text('''#!/usr/bin/env python3
import os
from pathlib import Path
import sys
print('[[]]' if '/comments?' in sys.argv[2]
      else Path(os.environ['GH_REPLY']).read_text())
''')
            gh.chmod(0o755)
            reply = root / 'reply.json'
            issue = {'number': 1, 'title': 'Feature', 'body': 'Original',
                     'html_url': 'https://github.com/team/app/issues/1', 'state': 'open',
                     'labels': [{'name': 'factory'}], 'updated_at': 'first'}
            adapter = GitHubWorkTracking()
            source = WorkSource('github', 'team/app')
            with patch.dict(os.environ, {'PATH': f'{root}:{os.environ["PATH"]}',
                                        'GH_REPLY': str(reply)}):
                # Act: compare timestamps, content, and assignee changes.
                reply.write_text(json.dumps([[issue]]))
                first, = adapter.list_issues(source, ('factory',))
                issue['updated_at'] = 'second'
                reply.write_text(json.dumps([[issue]]))
                unchanged, = adapter.list_issues(source, ('factory',))
                issue['body'] = 'Changed'
                issue['updated_at'] = 'third'
                reply.write_text(json.dumps([[issue]]))
                changed, = adapter.list_issues(source, ('factory',))
                issue['assignees'] = [{'login': 'alice'}]
                reply.write_text(json.dumps([[issue]]))
                assigned, = adapter.list_issues(source, ('factory',))
                issue['title'] = 'New title'
                reply.write_text(json.dumps([[issue]]))
                titled, = adapter.list_issues(source, ('factory',))
                issue['labels'].append({'name': 'epic'})
                reply.write_text(json.dumps([[issue]]))
                epic, = adapter.list_issues(source, ('factory',))
                issue['labels'].reverse()
                reply.write_text(json.dumps([[issue]]))
                reordered, = adapter.list_issues(source, ('factory',))
            # Assert
            self.assertEqual(first.revision, unchanged.revision)
            self.assertNotEqual(first.revision, changed.revision)
            self.assertNotEqual(changed.revision, assigned.revision)
            self.assertNotEqual(assigned.revision, titled.revision)
            self.assertNotEqual(titled.revision, epic.revision)
            self.assertTrue(epic.epic)
            self.assertEqual(epic.revision, reordered.revision)

    def test_comments_are_paginated_order_independent_and_fail_closed(self):
        from forgetful_factory.domain.models import FactoryError

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gh = root / 'gh'
            # Arrange: multiple comment pages contain human and bot comments.
            gh.write_text('''#!/usr/bin/env python3
import os
from pathlib import Path
import sys
if '/comments?' in sys.argv[2] and not {'--paginate', '--slurp'} <= set(sys.argv):
    sys.exit('pagination flags missing')
name = 'GH_COMMENTS' if '/comments?' in sys.argv[2] else 'GH_REPLY'
value = Path(os.environ[name]).read_text()
if value == 'FAIL':
    sys.exit('read failed')
print(value)
''')
            gh.chmod(0o755)
            reply, comments = root / 'issue', root / 'comments'
            issue = {'number': 1, 'title': 'Feature', 'body': 'Original',
                     'html_url': 'https://github.com/team/app/issues/1', 'state': 'open',
                     'labels': [{'name': 'factory'}], 'updated_at': 'same'}
            reply.write_text(json.dumps([[issue]]))
            first = {'id': 1, 'body': 'One', 'updated_at': 't1',
                     'user': {'login': 'person', 'type': 'User'},
                     'issue_url': 'https://api.github.com/repos/Team/App/issues/1'}
            second = {**first, 'id': 2, 'body': 'Two',
                      'user': {'login': 'robot[bot]', 'type': 'Bot'}}
            adapter = GitHubWorkTracking()
            source = WorkSource('github', 'team/app')
            env = {'PATH': f'{root}:{os.environ["PATH"]}', 'GH_REPLY': str(reply),
                   'GH_COMMENTS': str(comments)}
            with patch.dict(os.environ, env):
                # Act and assert: reordering is stable, editing changes the revision.
                comments.write_text(json.dumps([[first], [second]]))
                original, = adapter.list_issues(source, ('factory',))
                comments.write_text(json.dumps([[second], [first]]))
                reordered, = adapter.list_issues(source, ('factory',))
                self.assertEqual(original.revision, reordered.revision)
                second['body'] = 'Edited'
                second['updated_at'] = 't2'
                comments.write_text(json.dumps([[first], [second]]))
                edited, = adapter.list_issues(source, ('factory',))
                self.assertNotEqual(original.revision, edited.revision)
                wrong_issue = {**first, 'issue_url':
                               'https://api.github.com/repos/team/app/issues/9'}
                for invalid in ('FAIL', '[]', json.dumps([[first], [{'id': 3}]]),
                                json.dumps([[wrong_issue]])):
                    comments.write_text(invalid)
                    with self.assertRaises(FactoryError):
                        adapter.list_issues(source, ('factory',))
                comments.write_text(json.dumps([[first], [second]]))
                retried, = adapter.list_issues(source, ('factory',))
                self.assertEqual(edited.revision, retried.revision)
