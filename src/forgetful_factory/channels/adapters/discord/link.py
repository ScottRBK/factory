"""watch's side of the Discord relay: find the token, start the relay child and exchange JSON
lines with it over a socket pair. A Discord problem never stops watch: the link prints a
warning and then does nothing, so watch and the tmux terminal work as before."""
import json
import os
import socket
import subprocess
import sys
import time
from collections.abc import Callable, Mapping
from pathlib import Path

from forgetful_factory.channels.model import ChatMessage, Delivery, DiscordSettings
from forgetful_factory.shared.env_file import find_secret

RELAY = (sys.executable, '-m', 'forgetful_factory.channels.adapters.discord.relay')
# What Python, TLS and proxies need. The token goes over the socket, not in the environment.
PASSED = ('PATH', 'HOME', 'LANG', 'LC_ALL', 'LC_CTYPE', 'TMPDIR', 'TZ', 'PYTHONPATH',
          'SSL_CERT_FILE', 'SSL_CERT_DIR', 'HTTP_PROXY', 'HTTPS_PROXY', 'NO_PROXY',
          'http_proxy', 'https_proxy', 'no_proxy')
BACKLOG = 1 << 20  # bytes the relay has not taken; more means it is stuck
CLOSE_WAIT = 10.0  # seconds for the relay to post its last messages when watch stops


class DiscordLink:
    name = 'Discord'

    def __init__(self, settings: DiscordSettings, env_file: Path, *, explicit_env_file: bool,
                 warn: Callable[[str], None], command: tuple[str, ...] | list[str] = RELAY,
                 environment: Mapping[str, str] = os.environ, close_wait: float = CLOSE_WAIT):
        self.settings = settings
        self.env_file = env_file
        self.explicit_env_file = explicit_env_file
        self.warn = warn
        self.command = list(command)
        self.environment = environment
        self.close_wait = close_wait
        self.process: subprocess.Popen | None = None
        self.connection: socket.socket | None = None
        self.outgoing = b''
        self.incoming = b''
        self.inbox: list[ChatMessage] = []
        # True once the relay gave its final problem, or watch is closing: an exit is expected.
        self.finished = False

    def start(self) -> None:
        token, problem = find_secret(self.settings.token_variable, self.env_file,
                                     explicit=self.explicit_env_file,
                                     environment=self.environment)
        if token is None:
            self.warn(f'Discord is off: {problem} Watch continues without Discord.')
            return
        parent, child = socket.socketpair()
        try:
            self.process = subprocess.Popen(
                [*self.command, str(child.fileno())], pass_fds=(child.fileno(),),
                env={name: self.environment[name] for name in PASSED if name in self.environment},
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                # Its own session: Ctrl-C in the watch terminal must not stop the last posts.
                start_new_session=True)
        except OSError as error:
            parent.close()
            self.warn(f'Discord is off: cannot start the relay: {error}. '
                      'Watch continues without Discord.')
            return
        finally:
            child.close()
        parent.setblocking(False)
        self.connection = parent
        self._send({'kind': 'start', 'token': token,
                    'token_variable': self.settings.token_variable,
                    'channel_id': self.settings.channel_id,
                    'allowed_users': list(self.settings.allowed_users)})

    def online(self) -> None:
        self._send({'kind': 'online'})

    def post(self, text: str) -> None:
        self._send({'kind': 'post', 'text': text})

    def mark(self, message_id: str, delivery: Delivery) -> None:
        self._send({'kind': 'mark', 'id': message_id, 'delivery': delivery.value})

    def receive(self) -> list[ChatMessage]:
        self._pump()
        messages, self.inbox = self.inbox, []
        return messages

    def close(self, reason: str) -> None:
        self._send({'kind': 'stopped', 'reason': reason})
        if self.connection is None:
            return
        self.finished = True
        deadline = time.monotonic() + self.close_wait
        try:
            self.connection.settimeout(self.close_wait)
            self.connection.sendall(self.outgoing)
            self.connection.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        self.outgoing = b''
        try:
            # Read the relay's last problems until it closes its side.
            while (remaining := deadline - time.monotonic()) > 0:
                self.connection.settimeout(remaining)
                if not self._read(self.connection.recv(65536)):
                    break
        except OSError:
            pass
        self._end(deadline)

    def _send(self, value: dict) -> None:
        if self.connection is None:
            return
        self.outgoing += (json.dumps(value) + '\n').encode()
        self._pump()

    def _pump(self) -> None:
        """Move bytes both ways without waiting."""
        while self.connection is not None and self.outgoing:
            try:
                sent = self.connection.send(self.outgoing)
            except BlockingIOError:
                break
            except OSError:
                # The relay has gone. Read what it sent before it went, such as its last problem.
                self.outgoing = b''
                break
            self.outgoing = self.outgoing[sent:]
        if self.connection is not None and len(self.outgoing) > BACKLOG:
            self.finished = True
            self.warn('Discord relay is not keeping up; it was stopped. '
                      'Watch continues without Discord.')
            self.process.kill()
            self._end(time.monotonic() + 5)
            return
        while self.connection is not None:
            try:
                data = self.connection.recv(65536)
            except BlockingIOError:
                return
            except OSError:
                data = b''
            if not self._read(data):
                self._lost()

    def _read(self, data: bytes) -> bool:
        """Handle relay lines; False at the end of the relay's output."""
        if not data:
            return False
        self.incoming += data
        while b'\n' in self.incoming:
            line, self.incoming = self.incoming.split(b'\n', 1)
            try:
                value = json.loads(line)
                if value['kind'] == 'problem':
                    self.finished = self.finished or value.get('fatal') is True
                    self.warn(f'Discord: {value["text"]}')
                elif value['kind'] == 'message':
                    self.inbox.append(ChatMessage(str(value['id']), str(value['author']),
                                                  str(value['text'])))
            except (ValueError, KeyError, TypeError):
                self.warn('Discord relay sent an invalid line; it was ignored.')
        return True

    def _lost(self) -> None:
        status = self._end(time.monotonic() + 5)
        if not self.finished:
            self.warn(f'Discord relay ended unexpectedly (exit status {status}). '
                      'Watch continues without Discord.')
        self.finished = True

    def _end(self, deadline: float) -> int | None:
        connection, self.connection = self.connection, None
        if connection is not None:
            connection.close()
        process, self.process = self.process, None
        if process is None:
            return None
        try:
            return process.wait(timeout=max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
            if self.finished:
                self.warn('Discord relay did not finish in time and was stopped. '
                          'The last Discord posts may be missing.')
            return process.returncode
