import json
import os
from pathlib import Path
import selectors
import subprocess
import time
import uuid

from forgetful_factory.domain.models import FactoryError


class AgentShellTerminal:
    """Keep AgentShell in its own installed interpreter, including inside uvx isolation."""

    def __init__(self, python: str):
        self.python = python
        self.process: subprocess.Popen | None = None
        self.buffer = b''
        self.session_name = f'factory-foreman-{uuid.uuid4().hex[:12]}'

    def startup_hint(self) -> str:
        return f'Attach during startup: tmux attach-session -t {self.session_name}'

    def _write(self, value: dict, timeout: float) -> None:
        data = memoryview((json.dumps(value) + '\n').encode())
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdin, selectors.EVENT_WRITE)
            while data:
                if not selector.select(max(0, deadline - time.monotonic())):
                    raise FactoryError('AgentShell send timed out; delivery may be incomplete.')
                try:
                    data = data[os.write(self.process.stdin.fileno(), data):]
                except BlockingIOError:
                    continue
                except OSError as error:
                    raise FactoryError('AgentShell input closed; Pi delivery failed.') from error

    def _read(self, timeout: float, expected: str) -> dict:
        deadline = time.monotonic() + timeout
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout, selectors.EVENT_READ)
            while b'\n' not in self.buffer:
                if not selector.select(max(0, deadline - time.monotonic())):
                    if expected == 'ready':
                        raise FactoryError(
                            'Pi did not become ready before the startup deadline '
                            f'({self.session_name}). Watcher is stopping. '
                            'Check any cleanup errors before retrying. Restart watch, then '
                            'promptly use the new tmux attach-session command shown at startup '
                            'to resolve any trust dialog.')
                    raise FactoryError('Pi send response timed out; submission is uncertain. '
                                       'Check the Pi terminal before restarting watch.')
                chunk = os.read(self.process.stdout.fileno(), 65536)
                if not chunk:
                    raise FactoryError('AgentShell controller exited; check its error output.')
                self.buffer += chunk
        line, self.buffer = self.buffer.split(b'\n', 1)
        try:
            reply = json.loads(line)
            if not isinstance(reply, dict):
                raise ValueError('Expected an object')
        except ValueError as error:
            raise FactoryError('Invalid AgentShell controller response.') from error
        if reply.get('kind') == 'error':
            raise FactoryError(f'AgentShell: {reply.get("message", "terminal failed")}')
        if reply.get('kind') != expected:
            raise FactoryError(f'AgentShell stopped before {expected} acknowledgement; '
                               'watcher stopped without assuming success.')
        return reply

    def start(self, cwd: str, model: str, effort: str) -> None:
        helper = Path(__file__).with_name('controller.py').resolve()
        try:
            self.process = subprocess.Popen(
                [self.python, '-u', str(helper)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                # Library diagnostics stay on stderr, separate from the protocol and user stdin.
                stderr=None, start_new_session=True,
            )
        except OSError as error:
            raise FactoryError('Cannot run AgentShell Python; check --agentshell-python: '
                               f'{error}') from error
        os.set_blocking(self.process.stdin.fileno(), False)
        self._write({'cwd': cwd, 'model': model, 'effort': effort,
                     'session_name': self.session_name}, 10)
        self._read(35, 'ready')

    def send(self, message: str) -> None:
        self._write({'text': message}, 10)
        self._read(20, 'sent')

    def wait(self, interval: float) -> None:
        with selectors.DefaultSelector() as selector:
            selector.register(self.process.stdout, selectors.EVENT_READ)
            deadline = time.monotonic() + interval
            while (remaining := deadline - time.monotonic()) > 0:
                if selector.select(min(remaining, 60)):
                    self._read(1, 'error')

    def close(self) -> None:
        if self.process is None:
            return
        process, self.process = self.process, None
        process.stdin.close()
        process.stdin = None
        try:
            output, _ = process.communicate(timeout=10)
        except subprocess.TimeoutExpired as error:
            process.terminate()
            try:
                process.communicate(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
            raise FactoryError(f'Pi cleanup timed out; check session {self.session_name}.') \
                from error
        finally:
            process.stdout.close()
        for line in (self.buffer + output).splitlines():
            try:
                reply = json.loads(line)
            except ValueError as error:
                raise FactoryError('Invalid AgentShell cleanup response.') from error
            if reply.get('kind') == 'error':
                raise FactoryError(f'AgentShell: {reply.get("message", "failed")}')
