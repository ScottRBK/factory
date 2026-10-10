from pathlib import Path
from typing import Protocol


class LocalRepositories(Protocol):
    def origin(self, path: Path) -> str: ...

    def discover(self, workspace: Path) -> list[Path]: ...
