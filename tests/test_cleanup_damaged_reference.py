"""A completed plan whose saved reference is damaged is reported, never cleaned up."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from forgetful_factory.factory.services.cleanup_completed import CleanupCompleted
from forgetful_factory.factory.services.factory_records import FactoryRecords
from forgetful_factory.forge.adapters.github import GitHubForge
from forgetful_factory.ticketing.adapters.github import GitHubTicketing
from forgetful_factory.ticketing.model import TicketSource


class DamagedReferenceTests(unittest.TestCase):
    def poll(self, key: str) -> tuple[int, list[str]]:
        """Poll cleanup once for a completed plan saved with this key; no Git is touched."""
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            source = TicketSource('github', 'team/app')
            repository = SimpleNamespace(local_dir=str(workspace),
                                         remote='git@github.com:team/app.git',
                                         work_source=source)
            config = SimpleNamespace(repository=(repository,))
            reference = f'github:team/app#{key}'
            context = {'workspace': str(workspace), 'issue': {
                'source': {'provider': 'github', 'reference': 'team/app'}, 'key': key,
                'title': 'Title', 'url': 'https://github.com/team/app/issues/12', 'body': '',
                'revision': 'r1', 'epic': False}}
            plan = dict(id=1, status='completed', project_id=1, external_ref=reference,
                        context=json.dumps(context))
            mapping = dict(repository='team/app', local_dir=str(workspace),
                           branch='factory/team-app-12', target_branch='main',
                           path=str(workspace / '.factory/worktrees/team-app-12'))
            record = {'kind': 'factory-ownership', 'workspace': str(workspace),
                      'external_ref': reference, 'worktrees': [mapping]}
            planning = Mock()
            planning.plans.return_value = [plan]
            planning.get_plan.return_value = plan
            planning.tasks.return_value = [dict(id=2, plan_id=1, title='Feature ownership',
                                                description=json.dumps(record))]
            planning.owns.return_value = True
            planning.backend_identity.return_value = 'local:fixture'
            repositories = Mock()
            repositories.origin.return_value = repository.remote
            ticketing = GitHubTicketing()
            records = FactoryRecords(planning, workspace, config, repositories, GitHubForge(),
                                     ticketing)
            worktrees = Mock()
            worktrees.repository_identity.return_value = 'fixture'
            receipts = Mock()
            receipts.load.return_value = set()
            alerts = Mock()
            cleanup = CleanupCompleted(records, worktrees, receipts, ticketing)
            cleanup.poll(alerts, lambda text: None)
            return (worktrees.dispose.call_count,
                    [call.kwargs['code'] for call in alerts.send.call_args_list])

    def test_sound_reference_is_cleaned_up(self):
        # Control: the same plan with a key GitHub writes reaches disposal.
        self.assertEqual(self.poll('12'), (1, []))

    def test_non_ascii_digits_are_reported_not_cleaned_up(self):
        # Before keys were text, the scope took any digits and the saved number then failed.
        self.assertEqual(self.poll('1٢'), (0, ['plan_recovery_invalid']))

    def test_number_python_cannot_read_is_never_cleaned_up(self):
        # The old saved number failed to load past Python's digit limit; it was never disposed.
        disposed, alerts = self.poll('1' * (sys.get_int_max_str_digits() + 1))
        self.assertEqual(disposed, 0)
        self.assertEqual(len(alerts), 1)
