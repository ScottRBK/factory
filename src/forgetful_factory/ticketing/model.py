"""Tickets: the work requests Factory watches, from any ticketing provider."""
from dataclasses import dataclass


@dataclass(frozen=True)
class TicketSource:
    provider: str
    reference: str

    @property
    def id_prefix(self) -> str:
        """Every ticket id from this source starts with this text."""
        return f'{self.provider}:{self.reference.casefold()}#'


@dataclass(frozen=True)
class Label:
    name: str


@dataclass(frozen=True)
class Ticket:
    source: TicketSource
    key: str
    title: str
    url: str
    body: str = ''
    revision: str = ''
    epic: bool = False

    @property
    def id(self) -> str:
        return self.source.id_prefix + self.key
