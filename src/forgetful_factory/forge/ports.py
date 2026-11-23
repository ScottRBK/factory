from typing import Protocol

from forgetful_factory.forge.model import RepositoryRef


class Forge(Protocol):
    """One code forge: hosts repositories and their change requests."""

    def repository(self, remote: str) -> RepositoryRef:
        """The repository a Git remote names; refuse a remote this forge does not host."""

    def is_change_request(self, repository: RepositoryRef, url: str) -> bool:
        """Whether url is the canonical address of a change request in repository."""
