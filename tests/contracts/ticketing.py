"""Promises every Ticketing adapter keeps, and a non-GitHub fake that keeps them.

A new ticketing adapter is done when a subclass of TicketingContract passes for it.
"""
import hashlib
import json
import re
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.model import Label, Ticket, TicketSource


class TicketingContract:
    """Mix into unittest.TestCase. The subclass supplies the adapter and provider data."""

    source: TicketSource
    invalid_references: tuple[str, ...]
    keys: tuple[str, str, str]
    non_keys: tuple[str, ...]

    def adapter(self):
        raise NotImplementedError

    def publish(self, tickets: list[dict]) -> None:
        """Make these tickets the provider's current tickets for self.source."""
        raise NotImplementedError

    def ticket(self, key, *, labels=('factory',), body='Body', state='open'):
        return {'key': key, 'title': f'Ticket {key}', 'body': body, 'labels': list(labels),
                'state': state}

    def test_lists_open_tickets_with_a_watched_label(self):
        # Arrange
        a, b, c = self.keys
        self.publish([self.ticket(a), self.ticket(b, labels=('Other',)),
                      self.ticket(c, state='closed')])
        # Act
        tickets = self.adapter().list_open(self.source, ('FACTORY',))
        # Assert: label matching ignores case; the id is the source prefix plus the key.
        self.assertEqual([ticket.key for ticket in tickets], [a])
        ticket, = tickets
        self.assertIsInstance(ticket, Ticket)
        self.assertEqual(ticket.source, self.source)
        self.assertEqual(ticket.id, self.source.id_prefix + a)
        self.assertEqual((ticket.title, ticket.body, ticket.epic), (f'Ticket {a}', 'Body', False))
        self.assertTrue(ticket.url)

    def test_star_lists_every_open_ticket(self):
        a, b, _ = self.keys
        self.publish([self.ticket(a), self.ticket(b, labels=())])
        tickets = self.adapter().list_open(self.source, ('*',))
        self.assertEqual(sorted(ticket.key for ticket in tickets), sorted([a, b]))

    def test_epic_label_marks_an_epic(self):
        a, _, _ = self.keys
        self.publish([self.ticket(a, labels=('factory', 'Epic'))])
        ticket, = self.adapter().list_open(self.source, ('factory',))
        self.assertTrue(ticket.epic)

    def test_listed_keys_are_text_keys(self):
        adapter = self.adapter()
        self.publish([self.ticket(key) for key in self.keys])
        for ticket in adapter.list_open(self.source, ('factory',)):
            with self.subTest(key=ticket.key):
                self.assertIsInstance(ticket.key, str)
                self.assertTrue(adapter.is_key(ticket.key))
        for text in ('', ' ', *self.non_keys):
            with self.subTest(text=text):
                self.assertFalse(adapter.is_key(text))

    def test_revision_changes_with_content_only(self):
        a, _, _ = self.keys
        adapter = self.adapter()
        self.publish([self.ticket(a)])
        first, = adapter.list_open(self.source, ('factory',))
        same, = adapter.list_open(self.source, ('factory',))
        self.publish([self.ticket(a, body='Changed')])
        changed, = adapter.list_open(self.source, ('factory',))
        self.assertTrue(first.revision)
        self.assertEqual(first.revision, same.revision)
        self.assertNotEqual(first.revision, changed.revision)

    def test_validates_sources(self):
        adapter = self.adapter()
        adapter.validate_source(self.source)
        for reference in self.invalid_references:
            with self.subTest(reference=reference):
                with self.assertRaises(FactoryError):
                    adapter.validate_source(TicketSource(self.source.provider, reference))

    def test_refuses_another_providers_source(self):
        with self.assertRaises(FactoryError):
            self.adapter().validate_source(TicketSource('another-provider', self.source.reference))

    def test_created_label_is_listed(self):
        adapter = self.adapter()
        adapter.create_label(self.source, Label('factory-new'))
        self.assertIn('factory-new', [label.name for label in adapter.list_labels(self.source)])

    def test_ready_with_access(self):
        adapter = self.adapter()
        adapter.check_ready()
        adapter.check_access(self.source)


class FakeTicketing:
    """A non-GitHub provider: its own name, URLs and text keys such as ENG-123.

    State lives in a JSON file, so a watcher in another process can use the same fake:
    {"tickets": {source: [ticket, ...]}, "labels": {source: [name, ...]}}.
    """

    def __init__(self, state: Path):
        self.state = state

    def _load(self) -> dict:
        if not self.state.exists():
            return {'tickets': {}, 'labels': {}}
        return json.loads(self.state.read_text())

    def publish(self, source: TicketSource, tickets: list[dict]) -> None:
        state = self._load()
        state['tickets'][source.reference.casefold()] = tickets
        self.state.write_text(json.dumps(state))

    def check_ready(self) -> None:
        pass

    def validate_source(self, source: TicketSource) -> None:
        if source.provider != 'tracker':
            raise FactoryError(f'Unsupported work-tracking provider {source.provider!r}.')
        if re.fullmatch(r'[a-z][a-z0-9-]*', source.reference.casefold()) is None:
            raise FactoryError(f'Invalid tracker team {source.reference!r}.')

    def is_key(self, text: str) -> bool:
        return re.fullmatch(r'[A-Z][A-Z0-9]*-[1-9][0-9]*', text) is not None

    def check_access(self, source: TicketSource) -> None:
        self.validate_source(source)

    def list_labels(self, source: TicketSource) -> tuple[Label, ...]:
        names = self._load()['labels'].get(source.reference.casefold(), [])
        return tuple(Label(name) for name in names)

    def create_label(self, source: TicketSource, label: Label) -> None:
        state = self._load()
        state['labels'].setdefault(source.reference.casefold(), []).append(label.name)
        self.state.write_text(json.dumps(state))

    def list_open(self, source: TicketSource, labels: tuple[str, ...]) -> tuple[Ticket, ...]:
        watched = {name.casefold() for name in labels}
        result = []
        for item in self._load()['tickets'].get(source.reference.casefold(), []):
            names = {name.casefold() for name in item['labels']}
            if item['state'] != 'open' or not ('*' in watched or names & watched):
                continue
            content = json.dumps([item['title'], item['body'], sorted(names)])
            result.append(Ticket(source, item['key'], item['title'],
                                 f'https://tracker.example/{item["key"]}', item['body'],
                                 hashlib.sha256(content.encode()).hexdigest(), 'epic' in names))
        return tuple(result)
