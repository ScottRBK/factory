"""Watcher borrows its parent's held AgentShell session through one inherited private channel."""
import json
import selectors
import socket

from forgetful_factory.domain.models import FactoryError


class BorrowedForemanTerminal:
    def __init__(self, descriptor: int):
        self.connection = socket.socket(fileno=descriptor)
        self.connection.settimeout(25)
        self.reader = self.connection.makefile('rb')

    def startup_hint(self) -> str:
        return 'Watcher borrows the setup Foreman; stopping watch leaves Foreman alive.'

    def _request(self, value: dict) -> None:
        try:
            self.connection.sendall((json.dumps(value) + '\n').encode())
            line = self.reader.readline(65537)
            if len(line) > 65536 or not line.endswith(b'\n'):
                raise ValueError('Invalid Foreman reply frame')
            reply = json.loads(line)
            if not isinstance(reply, dict) or reply.get('kind') != 'ok':
                raise FactoryError('Foreman unavailable or submission uncertain; watcher stopped.')
        except (OSError, ValueError) as error:
            raise FactoryError('Foreman owner disconnected; watcher stopped without replacement.') \
                from error

    def start(self) -> None:
        self._request({'operation': 'ready'})

    def send(self, message: str) -> None:
        self._request({'operation': 'send', 'text': message})

    def wait(self, interval: float) -> None:
        with selectors.DefaultSelector() as selector:
            selector.register(self.connection, selectors.EVENT_READ)
            if selector.select(interval):
                raise FactoryError('Foreman owner disconnected; watcher stopped.')

    def close(self) -> None:
        self.reader.close()
        self.connection.close()
