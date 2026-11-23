from typing import Protocol


class SessionHost(Protocol):
    """Where an interactive agent session runs. Launch data and targets are plain dicts."""

    def spec(self) -> dict:
        """The host as plain data for the launch JSON, with a 'kind' the controller knows."""

    def how_to_attach(self, session_name: str) -> str:
        """The command a person runs to watch a session that is starting."""

    def enter(self, target: dict) -> None:
        """Take this terminal into a launched target, or print how to enter it."""
