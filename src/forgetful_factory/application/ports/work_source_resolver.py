from typing import Protocol

from forgetful_factory.ticketing.model import TicketSource


class WorkSourceResolver(Protocol):
    """Map an origin to the work source used by this integration."""

    def source_from_remote(self, remote: str) -> TicketSource: ...
