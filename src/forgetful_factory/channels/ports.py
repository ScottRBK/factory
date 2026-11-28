from typing import Protocol

from forgetful_factory.channels.model import ChatMessage, Delivery


class Channel(Protocol):
    """How a person talks to the Foreman. Targets are the session host's plain dicts."""

    def how_to_reach(self, session_name: str) -> str:
        """What a person does to reach a session that is starting."""

    def open(self, target: dict) -> None:
        """Take the person to a launched session, or print how to reach it."""


class ChatChannel(Protocol):
    """A chat room linked to the Foreman. A chat problem never stops the caller: methods
    report it as a warning and do not raise, and the room is then left out."""

    name: str

    def start(self) -> None:
        """Begin to connect. Does not wait for the chat room."""

    def online(self) -> None:
        """Say that the Foreman is ready."""

    def post(self, text: str) -> None:
        """Post text from the Foreman."""

    def receive(self) -> list[ChatMessage]:
        """Messages for the Foreman that came since the last call. Never waits."""

    def mark(self, message_id: str, delivery: Delivery) -> None:
        """Show what happened to a message."""

    def close(self, reason: str) -> None:
        """Say why watch stopped, then end the link."""
