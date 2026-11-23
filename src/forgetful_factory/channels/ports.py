from typing import Protocol


class Channel(Protocol):
    """How a person talks to the Foreman. Targets are the session host's plain dicts."""

    def how_to_reach(self, session_name: str) -> str:
        """What a person does to reach a session that is starting."""

    def open(self, target: dict) -> None:
        """Take the person to a launched session, or print how to reach it."""
