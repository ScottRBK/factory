"""Observation of a plain watch invocation, without owning or controlling another process."""
import json
import os
import socket
import stat
import struct
import threading
import time
import uuid
from collections.abc import Callable, Iterator
from contextlib import contextmanager, suppress
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    replace_generated_json,
)
from forgetful_factory.application.ports.foreman_terminal import ForemanTerminal
from forgetful_factory.domain.models import FactoryError

_LIMIT = 16384
_TIMEOUT = 0.5
_IDENTITY = ('workspace', 'run_id', 'watcher_pid', 'process_started')


def _observation_json(data: bytes) -> object:
    try:
        return json.loads(data)
    except RecursionError as error:
        raise ValueError('Observation JSON exceeds the parser depth limit') from error


def _discovery_path(workspace: Path) -> Path:
    return workspace / '.factory/runtime/watch/status.json'


def _endpoint(run_id: str) -> str:
    # Linux abstract sockets avoid workspace path-length limits and stale socket unlinking.
    return f'\0factory-watch-{os.getuid()}-{run_id}'


def _frame(connection: socket.socket) -> dict:
    deadline = time.monotonic() + _TIMEOUT
    data = b''
    while b'\n' not in data:
        connection.settimeout(max(0.001, deadline - time.monotonic()))
        chunk = connection.recv(_LIMIT + 1 - len(data))
        data += chunk
        if not chunk or len(data) > _LIMIT or time.monotonic() >= deadline:
            raise ValueError('Missing, oversized or timed out observation frame')
    value = _observation_json(data)
    if not isinstance(value, dict):
        raise ValueError('Observation must be an object')
    return value


def _peer(connection: socket.socket) -> tuple[int, int]:
    pid, uid, _ = struct.unpack('3i', connection.getsockopt(
        socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')))
    return pid, uid


def _read_discovery(workspace: Path) -> dict:
    path = _discovery_path(workspace)
    check_real_path(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) & 0o077):
            raise ValueError('Observation record must be a private owned regular file')
        data = stream.read(_LIMIT + 1)
    if len(data) > _LIMIT:
        raise ValueError('Oversized observation record')
    value = _observation_json(data)
    if (not isinstance(value, dict) or value.get('workspace') != str(workspace)
            or not isinstance(value.get('run_id'), str) or len(value['run_id']) != 32
            or any(c not in '0123456789abcdef' for c in value['run_id'])
            or type(value.get('watcher_pid')) is not int or value['watcher_pid'] <= 0
            or not isinstance(value.get('process_started'), str)
            or not value['process_started']):
        raise ValueError('Invalid observation identity')
    return value


def unknown_status(source: str = 'none', observation: str = 'unavailable') -> dict:
    return {'source': source, 'observation': observation, 'process': 'unknown', 'phase': 'unknown',
            'foreman': 'unknown', 'watcher': 'unknown', 'target': None, 'health': 'not_checked',
            'evidence': 'not_observed'}


def plain_watch_status(workspace: Path) -> dict | None:
    """A saved identity locates a read-only endpoint; it never authorizes process operations."""
    try:
        saved = _read_discovery(workspace)
    except FileNotFoundError:
        return None
    except (FactoryError, OSError, ValueError) as error:
        return {**unknown_status('plain_watch'), 'warning': str(error)}
    try:
        with socket.socket(socket.AF_UNIX) as connection:
            connection.settimeout(_TIMEOUT)
            connection.connect(_endpoint(saved['run_id']))
            if _peer(connection) != (saved['watcher_pid'], os.getuid()):
                raise ValueError('Observation peer identity changed')
            connection.sendall((json.dumps({'operation': 'status',
                                            'run_id': saved['run_id']}) + '\n').encode())
            observed = _frame(connection)
        latest = _read_discovery(workspace)
        if (any(observed.get(key) != saved[key] for key in _IDENTITY)
                or any(latest[key] != saved[key] for key in _IDENTITY)):
            raise ValueError('Observation identity changed during query')
        if (observed.get('phase') not in ('starting', 'watching', 'stopping', 'stopped')
                or observed.get('foreman') not in ('starting', 'ready', 'stopping',
                                                  'stopped', 'unknown')
                or observed.get('watcher') not in ('starting', 'running', 'stopping', 'stopped')):
            raise ValueError('Invalid lifecycle observation')
        return {**observed, 'source': 'plain_watch', 'observation': 'live',
                'process': 'present', 'health': 'not_checked', 'process_role': 'watcher'}
    except (FactoryError, OSError, ValueError) as error:
        return {**unknown_status('plain_watch', 'saved'),
                'run_id': saved['run_id'], 'watcher_pid': saved['watcher_pid'],
                'recorded_foreman': saved.get('foreman'),
                'recorded_watcher': saved.get('watcher'),
                'recorded_phase': saved.get('phase'),
                'recorded_evidence': saved.get('evidence'), 'warning': str(error)}


class PlainWatchObservation:
    """One bounded observer thread inside the foreground watcher; no separate daemon."""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.lock = threading.Lock()
        self.finished = threading.Event()
        self.listener = None
        self.thread = None
        # Read only this process's identity. No handles are opened from persisted PIDs.
        started = Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19]
        boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
        self.state = {**unknown_status('plain_watch'), 'workspace': str(workspace),
                      'run_id': uuid.uuid4().hex, 'watcher_pid': os.getpid(),
                      'process_started': f'{boot}:{started}', 'phase': 'starting',
                      'watcher': 'starting', 'foreman': 'unknown'}

    def update(self, **fields) -> None:
        with self.lock:
            self.state = {**self.state, **fields, 'updated_at': time.time()}
            # Readers see the transition after its one publication attempt has completed.
            self._publish_history(dict(self.state))

    def snapshot(self) -> dict:
        with self.lock:
            return dict(self.state)

    def _publish_history(self, current: dict) -> None:
        # One bounded-size attempt, without retries or authority to replace another identity.
        # History is optional after startup; failure must preserve the watcher's result.
        try:
            saved = _read_discovery(self.workspace)
            if all(saved[key] == current[key] for key in _IDENTITY):
                replace_generated_json(_discovery_path(self.workspace), current)
        except (FactoryError, OSError, ValueError):
            pass

    def __enter__(self):
        directory = _discovery_path(self.workspace).parent
        check_real_path(directory)
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        info = directory.stat()
        if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise FactoryError('Watch observation directory must be private and owned.')
        self.listener = socket.socket(socket.AF_UNIX)
        try:
            self.listener.bind(_endpoint(self.state['run_id']))
            self.listener.listen(4)
            self.listener.settimeout(0.1)
            replace_generated_json(_discovery_path(self.workspace), self.snapshot())
            self.thread = threading.Thread(target=self._serve, daemon=True,
                                           name='watch-observation')
            self.thread.start()
        except BaseException:
            with suppress(FactoryError, OSError, ValueError, RuntimeError):
                self._close_resources()
                self.update(phase='unknown', watcher='unknown', foreman='unknown',
                            evidence='observer_startup_failed')
            raise
        return self

    def _serve(self) -> None:
        while not self.finished.is_set():
            try:
                connection, _ = self.listener.accept()
            except TimeoutError:
                continue
            except OSError:
                return
            with connection:
                try:
                    if _peer(connection)[1] != os.getuid():
                        continue
                    request = _frame(connection)
                    if request != {'operation': 'status', 'run_id': self.state['run_id']}:
                        continue
                    connection.sendall((json.dumps(self.snapshot()) + '\n').encode())
                except (OSError, ValueError):
                    continue

    def _close_resources(self) -> None:
        self.finished.set()
        if self.listener is not None:
            self.listener.close()
        if self.thread is not None and self.thread.is_alive():
            self.thread.join(timeout=1)

    def __exit__(self, *_):
        self._close_resources()
        # Historical evidence only. An unavailable endpoint never establishes current absence.
        # The workspace lease still excludes the next normal watcher. Preserve any discovery
        # replaced outside that lease instead of publishing this invocation over another one.
        current = self.snapshot()
        if current['phase'] != 'stopped':
            self.update(phase='stopped', watcher='stopped', foreman='unknown',
                        evidence='exited_before_session')
        else:
            self._publish_history(current)


@contextmanager
def observe_plain_watch(workspace: Path, report_unavailable: Callable[[str], None]
                        ) -> Iterator[PlainWatchObservation | None]:
    """Optional observation only: body/admission errors retain their original outcome."""
    observation = None
    try:
        candidate = PlainWatchObservation(workspace)
        candidate.__enter__()
        observation = candidate
    except (FactoryError, OSError, ValueError, RuntimeError) as error:
        with suppress(OSError):
            report_unavailable(str(error))
    try:
        yield observation
    finally:
        if observation is not None:
            try:
                observation.__exit__(None, None, None)
            except (FactoryError, OSError, ValueError, RuntimeError) as error:
                with suppress(OSError):
                    report_unavailable(str(error))


class ObservedTerminal:
    """Observe port lifecycle calls; all terminal ownership and I/O stay in the wrapped adapter."""

    def __init__(self, terminal: ForemanTerminal, observation: PlainWatchObservation):
        self.terminal = terminal
        self.observation = observation

    def startup_hint(self) -> str:
        return self.terminal.startup_hint()

    def start(self) -> None:
        self.observation.update(foreman='starting', evidence='awaiting_session_ready')
        self.terminal.start()
        self.observation.update(foreman='ready', watcher='running', phase='watching',
                                evidence='session_ready')

    def send(self, message: str) -> None:
        self.terminal.send(message)

    def wait(self, interval: float) -> None:
        self.terminal.wait(interval)

    def close(self) -> None:
        self.observation.update(phase='stopping', watcher='stopping', foreman='unknown')
        evidence = 'cleanup_uncertain'
        try:
            self.terminal.close()
            evidence = 'watcher_cleanup_finished'
        finally:
            self.observation.update(phase='stopped', watcher='stopped',
                                    evidence=evidence)
