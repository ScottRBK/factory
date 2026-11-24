from dataclasses import dataclass

from forgetful_factory.ticketing.model import TicketSource


@dataclass(frozen=True)
class RepositoryReference:
    local_dir: str
    remote: str
    work_source: TicketSource
