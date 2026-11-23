"""The terminal channel: a person reaches the Foreman in their own terminal, through the host.

Composition supplies the session host; this channel does not import a host adapter.
"""
from forgetful_factory.runtime.ports import SessionHost


class TerminalChannel:
    def __init__(self, host: SessionHost):
        self.host = host

    def how_to_reach(self, session_name: str) -> str:
        return self.host.how_to_attach(session_name)

    def open(self, target: dict) -> None:
        self.host.enter(target)
