from typing import Protocol

from forgetful_factory.domain.models import FactoryError


class WorktreeReadError(FactoryError):
    """A Git/path read failed before any worktree creation was attempted."""


class WorktreeProblem(FactoryError):
    """A deterministic, read-only safety check failed; adapter knows no plan identity."""

    def __init__(self, code: str, diagnostic: str, path: str | None = None):
        super().__init__(diagnostic)
        self.code = code
        self.paths = (path,) if path else ()


class Worktrees(Protocol):
    def inspect(self, repository: str, branch: str, path: str, *, remote: str) -> None: ...

    def ensure(self, repository: str, branch: str, path: str, *, recorded: bool,
               remote: str) -> None: ...

    def verify_removed(self, repository: str, branch: str, path: str, *, remote: str) -> None: ...
