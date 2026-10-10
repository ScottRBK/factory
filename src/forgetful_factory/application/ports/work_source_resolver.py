from typing import Protocol

from forgetful_factory.domain.models import WorkSource


class WorkSourceResolver(Protocol):
    """Map an origin to the work source used by this initialization integration."""

    def source_from_remote(self, remote: str) -> WorkSource: ...
