from typing import Protocol


class ToolInstaller(Protocol):
    """Installs one tool that the factory needs. Each context implements its own tools."""

    def absent(self) -> list[str]:
        """Names of the tool's executables that are not on the factory PATH."""

    def unready(self) -> list[str]:
        """Names of tools that are present, but whose managed copy is not usable."""

    def describe(self, name: str) -> str | None:
        """The consent question for a reviewed install; None means install it manually."""

    def install(self, name: str) -> None: ...
