"""Terminal confirmation for a resource set, never progress through deletion steps."""
from dataclasses import dataclass
from typing import Protocol


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
    def load(self) -> set[CleanupSet]: ...

    def confirm(self, resource: CleanupSet) -> None: ...
