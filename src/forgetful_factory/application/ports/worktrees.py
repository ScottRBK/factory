from typing import Protocol


class Worktrees(Protocol):
    def ensure(self, repository: str, branch: str, path: str, *, recorded: bool,
               remote: str) -> None: ...

    def verify_removed(self, repository: str, branch: str, path: str, *, remote: str) -> None: ...
