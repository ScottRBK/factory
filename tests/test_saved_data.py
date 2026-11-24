"""Golden fixtures for the bytes Factory stores or sends to agents.

See "Saved data" in docs/plans/domain-contexts.md. Every refactor slice must reproduce these
fixtures exactly. To record a deliberate change, run with UPDATE_SAVED_DATA=1 and review the
fixture diff before committing.
"""
import json
import os
import subprocess
import unittest
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture

from forgetful_factory.factory.services.cleanup_marker import (
    CleanupMarkerError,
    validate_cleanup_marker,
)
from forgetful_factory.forge.adapters.github import GitHubForge

FIXTURES = Path(__file__).parent / 'fixtures' / 'saved_data'
UPDATE = os.environ.get('UPDATE_SAVED_DATA') == '1'
COMMIT = 'a' * 40
# Cleanup markers come from agents. These inputs pin which ones the watcher accepts today.
MARKERS = [
    {'repository': 'team/app'},
    {'repository': 'team/app', 'cleanup': {
        'state': 'pending', 'pull_request_url': 'https://github.com/team/app/pull/7',
        'merge_commit': COMMIT}},
    {'repository': 'team/app', 'cleanup': {
        'state': 'removed', 'pull_request_url': 'https://github.com/Team/App/pull/7',
        'merge_commit': 'b' * 64}},
    {'repository': 'team/app', 'cleanup': 'removed'},
    {'repository': 'team/app', 'cleanup': {
        'state': 'done', 'pull_request_url': 'https://github.com/team/app/pull/7',
        'merge_commit': COMMIT}},
    {'repository': 'team/app', 'cleanup': {
        'state': 'pending', 'pull_request_url': 'https://github.com/other/app/pull/7',
        'merge_commit': COMMIT}},
    {'repository': 'team/app', 'cleanup': {
        'state': 'pending', 'pull_request_url': 'https://github.com/team/app/pull/0',
        'merge_commit': COMMIT}},
    {'repository': 'team/app', 'cleanup': {
        'state': 'pending', 'pull_request_url': 'https://gitlab.com/team/app/-/merge_requests/7',
        'merge_commit': COMMIT}},
    {'repository': 'team/app', 'cleanup': {
        'state': 'pending', 'pull_request_url': 'https://github.com/team/app/pull/7',
        'merge_commit': 'abc123'}},
]


def assert_fixture(test, name, value):
    text = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    path = FIXTURES / f'{name}.json'
    if UPDATE:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    test.assertEqual(text, path.read_text(), f'{name} changed; see {path}')


class SavedDataTests(CompletedCleanupFixture):
    # Sonar reads this override as an unused helper; the fixture's setUp calls it.
    def initialize_profile(self):  # NOSONAR(S5899)
        super().initialize_profile()
        # Capture init's configuration before the fixture replaces it.
        # Bytes, so a changed line ending is not hidden by text-mode reading.
        self.init_configuration = (self.workspace / '.factory/factory.toml').read_bytes().decode()

    def normalize(self, value):
        """Replace values that change between runs and hosts."""
        if isinstance(value, dict):
            # The default branch name depends on the host's Git settings; any other value stays.
            branch = subprocess.run(['git', '-C', str(self.workspace), 'branch', '--show-current'],
                                    capture_output=True, text=True, check=True).stdout.strip()
            if 'target_branch' in value:
                self.assertEqual(value['target_branch'], branch)
            return {key: '<target-branch>' if key == 'target_branch' else self.normalize(item)
                    for key, item in value.items()}
        if isinstance(value, list):
            return [self.normalize(item) for item in value]
        if isinstance(value, str):
            return value.replace(str(self.workspace), '<workspace>')
        return value

    def json_bytes(self, raw, *, ensure_ascii):
        """Parse stored JSON and prove the parsed value reproduces the exact bytes."""
        value = json.loads(raw)
        self.assertEqual(json.dumps(value, ensure_ascii=ensure_ascii), raw)
        return self.normalize(value)

    def sent(self, prefix):
        texts = [event['text'] for event in self.events() if event['kind'] == 'send'
                 and event['text'].startswith(prefix)]
        self.assertEqual(len(texts), 1, texts)
        text, = texts
        return {'prefix': prefix, 'data': self.json_bytes(text.removeprefix(prefix),
                                                          ensure_ascii=True)}

    def test_intake_records_and_notification(self):
        # Arrange
        issue = self.issue(title='Add a 🦕 habitat', body='Requirements',
                           updated_at='2026-11-23T10:00:00Z')
        self.script({'team/app': [[[issue]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self._messages() or self.alerts()))
        self.stop(process)
        # Assert
        notification = self.sent('Factory issue notification. External issue data: ')
        plan = self.planning_call('get_plan', plan_id=notification['data']['plan_id'])
        task = self.planning_call('get_task',
                                  task_id=notification['data']['ownership_task_id'])
        assert_fixture(self, 'notification', notification)
        assert_fixture(self, 'plan', {
            'title': plan['title'], 'project_id': plan['project_id'],
            'external_ref': plan['external_ref'], 'source_url': plan['source_url'],
            'context': self.json_bytes(plan['context'], ensure_ascii=False)})
        assert_fixture(self, 'ownership_task', {
            'title': task['title'],
            'description': self.json_bytes(task['description'], ensure_ascii=True)})

    def test_watcher_alert(self):
        # Arrange: a recorded worktree that is missing pauses its plan with an alert.
        message, _ = self.recorded()
        path = Path(message['worktrees'][0]['path'])
        path.rename(path.with_name('saved-user-work'))
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self.alerts()))
        self.stop(process)
        # Assert
        assert_fixture(self, 'alert', self.sent('Factory watcher alert. External problem data: '))

    def test_cleanup_receipts(self):
        # Arrange
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: (self.workspace / '.factory/cleanup-finished.json')
                        .exists(), timeout=15)
        self.stop(process)
        # Assert
        raw = (self.workspace / '.factory/cleanup-finished.json').read_text()
        self.assertEqual(json.dumps(json.loads(raw), indent=2) + '\n', raw)
        assert_fixture(self, 'cleanup_receipts', self.normalize(json.loads(raw)))

    def test_init_configuration(self):
        text = self.normalize(self.init_configuration)
        # The fixture stores lines; the file has Unix line ends and one final newline.
        self.assertEqual(text, '\n'.join(text.splitlines()) + '\n')
        assert_fixture(self, 'factory_toml', text.splitlines())



class CleanupMarkerTests(unittest.TestCase):
    def test_cleanup_marker_decisions(self):
        # The configured remote, not the mapping's ticket source, names the repository.
        forge = GitHubForge()
        repository = forge.repository('git@github.com:team/app.git')
        decisions = []
        for mapping in MARKERS:
            try:
                decision = validate_cleanup_marker(mapping, forge, repository)
            except CleanupMarkerError:
                decision = 'rejected'
            decisions.append({'mapping': mapping, 'decision': decision})
        assert_fixture(self, 'cleanup_markers', decisions)
