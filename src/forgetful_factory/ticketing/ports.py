from typing import Protocol

from forgetful_factory.ticketing.model import Label, Ticket, TicketSource


class Ticketing(Protocol):
    """One ticketing provider: where work requests come from."""

    def check_ready(self) -> None:
        """Check local tools before watching; no remote request."""

    def validate_source(self, source: TicketSource) -> None:
        """Refuse a source reference this provider cannot use."""

    def is_key(self, text: str) -> bool:
        """Whether text is a ticket key exactly as this provider writes it."""

    def could_be_key(self, text: str) -> bool:
        """Whether text has the rough shape of a key. Every key passes; a damaged one may too.

        Cleanup uses it to find a plan's reference, so a damaged record is reported, not skipped.
        """

    def check_access(self, source: TicketSource) -> None: ...

    def list_labels(self, source: TicketSource) -> tuple[Label, ...]: ...

    def create_label(self, source: TicketSource, label: Label) -> None: ...

    def list_open(self, source: TicketSource, labels: tuple[str, ...]) -> tuple[Ticket, ...]:
        """Open tickets with any of the labels; '*' matches every ticket."""
