"""What the factory's own workflows need from storage and tool installs."""
from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import Protocol

from forgetful_factory.factory.model.configuration import FactoryConfiguration


class ConfigurationStore(Protocol):
    def load(self) -> FactoryConfiguration | None: ...

    def save(self, configuration: FactoryConfiguration) -> None: ...


class WatchLease(Protocol):
    def hold(self) -> AbstractContextManager[None]: ...


@dataclass(frozen=True)
class CleanupSet:
    workspace: str
    backend: str
    plan_id: int
    external_ref: str
    repository: str
    local_dir: str
    branch: str
    path: str

    def overlaps(self, other: 'CleanupSet') -> bool:
        return ((self.workspace, self.plan_id) == (other.workspace, other.plan_id) and
                (self.path == other.path or
                 (self.branch == other.branch and
                  (self.local_dir == other.local_dir or self.repository == other.repository))))


class CleanupReceipts(Protocol):
    """Terminal confirmation for a resource set, never progress through deletion steps."""

    def load(self) -> set[CleanupSet]: ...

    def confirm(self, resource: CleanupSet) -> None: ...


class ToolInstaller(Protocol):
    """Installs one tool that the factory needs. Each context implements its own tools."""

    def absent(self) -> list[str]:
        """Names of the tool's executables that are not on the factory PATH."""

    def unready(self) -> list[str]:
        """Names of tools that are present, but whose managed copy is not usable."""

    def describe(self, name: str) -> str | None:
        """The consent question for a reviewed install; None means install it manually."""

    def install(self, name: str) -> None: ...
