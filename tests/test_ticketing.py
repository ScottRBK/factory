"""Ticket identity, GitHub key and source rules, and ticketing selection in composition."""
import unittest
from types import SimpleNamespace

from forgetful_factory.cli.bootstrap import select_ticketing
from forgetful_factory.factory.model.watcher_problems import ScaffoldProblem
from forgetful_factory.factory.services.factory_records import FactoryRecords
from forgetful_factory.factory.services.scaffold_issue import worktree_name
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.adapters.github import GitHubTicketing
from forgetful_factory.ticketing.model import Ticket, TicketSource


def ticket(provider, reference, key):
    return Ticket(TicketSource(provider, reference), key, 'Title', 'https://tickets.example/1')


class TicketIdentityTests(unittest.TestCase):
    def test_github_id_keeps_the_saved_format(self):
        self.assertEqual(ticket('github', 'Team/App', '42').id, 'github:team/app#42')

    def test_text_key_keeps_its_case(self):
        self.assertEqual(ticket('linear', 'Platform', 'ENG-123').id, 'linear:platform#ENG-123')

    def test_worktree_name_keeps_github_bytes_and_makes_other_keys_branch_safe(self):
        cases = {('team/app', '42'): 'team-app-42',
                 ('team/app', 'ENG-123'): 'team-app-ENG-123',
                 ('team/app', 'a/b c~1'): 'team-app-a-b-c-1'}
        for (reference, key), expected in cases.items():
            with self.subTest(key=key):
                self.assertEqual(worktree_name(ticket('github', reference, key)), expected)


class SavedTicketTests(unittest.TestCase):
    def snapshot(self, **issue):
        saved = dict(source={'provider': 'github', 'reference': 'team/app'}, title='Title',
                     url='https://github.com/team/app/issues/7', body='', revision='r1',
                     epic=False, **issue)
        records = FactoryRecords(None, None, None, None, None, GitHubTicketing())
        return records.snapshot({'issue': saved}, f'github:team/app#{issue.get("key", 7)}')

    def test_saved_text_key_restores_the_ticket(self):
        self.assertEqual(self.snapshot(key='7').key, '7')

    def test_plan_saved_by_an_older_build_needs_reconciliation(self):
        # Decision 6: there is no reader for the integer "number" shape.
        cases = {'number field': {'number': 7}, 'integer key': {'key': 7}, 'empty key': {'key': ''}}
        for name, issue in cases.items():
            with self.subTest(name):
                with self.assertRaises(ScaffoldProblem) as raised:
                    self.snapshot(**issue)
                self.assertEqual(raised.exception.code, 'plan_recovery_invalid')

    def test_saved_key_the_provider_never_writes_needs_reconciliation(self):
        # Before keys were text, a saved number had to be a positive integer, so its reference
        # had ASCII digits and no leading zero. A completed plan must not authorize cleanup else.
        for key in ('0', '07', '1\u0662', 'ENG-1'):
            with self.subTest(key=key):
                with self.assertRaises(ScaffoldProblem) as raised:
                    self.snapshot(key=key)
                self.assertEqual(raised.exception.code, 'plan_recovery_invalid')


class GitHubTicketingRulesTests(unittest.TestCase):
    def test_keys_are_positive_issue_numbers(self):
        github = GitHubTicketing()
        for key in ('1', '42', '1000'):
            with self.subTest(key=key):
                self.assertTrue(github.is_key(key))
        for key in ('', '0', '01', '-1', ' 1', '1 ', 'ENG-1', '٣', '1\u0662'):
            with self.subTest(key=key):
                self.assertFalse(github.is_key(key))

    def test_sources_are_owner_and_repository(self):
        github = GitHubTicketing()
        for reference in ('team/app', 'Team/App.js', 'a-b/c_d.e', 'team/app.GIT'):
            with self.subTest(reference=reference):
                github.validate_source(TicketSource('github', reference))
        for reference in ('team', 'team/app.git', 'team/.', 'team/..', 'team/app/x',
                          'a b/c', '/app', 'team/'):
            with self.subTest(reference=reference):
                with self.assertRaisesRegex(FactoryError, 'Invalid GitHub work source'):
                    github.validate_source(TicketSource('github', reference))


class TicketingSelectionTests(unittest.TestCase):
    def config(self, *providers):
        return SimpleNamespace(repository=[
            SimpleNamespace(work_source=TicketSource(provider, f'team/app{index}'))
            for index, provider in enumerate(providers)])

    def test_github_sources_select_github_ticketing(self):
        self.assertIsInstance(select_ticketing(self.config('github', 'github'), 30),
                              GitHubTicketing)

    def test_unknown_provider_is_refused_clearly(self):
        with self.assertRaisesRegex(FactoryError,
                                    "Unsupported work-tracking provider 'linear'; "
                                    'watch supports github only.'):
            select_ticketing(self.config('github', 'linear'), 30)

    def test_repositories_are_checked_in_order_provider_then_source(self):
        # The first repository's fault is reported, as before the ticketing registry.
        config = SimpleNamespace(repository=[
            SimpleNamespace(work_source=TicketSource('github', 'team/app.git')),
            SimpleNamespace(work_source=TicketSource('gitlab', 'team/b'))])
        with self.assertRaisesRegex(FactoryError, "Invalid GitHub work source 'team/app.git'"):
            select_ticketing(config, 30)

    def test_invalid_source_is_refused_before_watching(self):
        config = SimpleNamespace(repository=[
            SimpleNamespace(work_source=TicketSource('github', 'team/app.git'))])
        with self.assertRaisesRegex(FactoryError, "Invalid GitHub work source 'team/app.git'"):
            select_ticketing(config, 30)
