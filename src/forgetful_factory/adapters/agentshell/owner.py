"""One detached Foreman owner. Control stays local; delivery stays in AgentShell."""
import asyncio
import contextlib
import fcntl
import json
import math
import os
import shlex
import signal
import socket
import stat
import sys
import uuid
from pathlib import Path

from forgetful_factory.adapters.agentshell.owner_client import read_state
from forgetful_factory.adapters.filesystem.foreman_runtime import runtime_directory
from forgetful_factory.adapters.filesystem.resource_files import replace_generated_json
from forgetful_factory.deadlines import AgentShellLifecycleDeadlines
from forgetful_factory.domain.models import FactoryError

_CONTROLLER_KINDS = {
    'launched', 'ready', 'sent', 'exited', 'stopped', 'closed', 'error', 'send_error',
    'uncertain',
}


def _validate_target(target) -> None:
    if (not isinstance(target, dict)
            or not isinstance(target.get('pane_id'), str)
            or not isinstance(target.get('socket_path'), str)
            or any(type(target.get(key)) is not int
                   for key in ('server_pid', 'server_started', 'pane_pid'))):
        raise ValueError('Invalid terminal identity')


def _controller_event(line: bytes) -> dict:
    value = json.loads(line)
    if not isinstance(value, dict):
        raise ValueError('Expected an object')
    kind = value.get('kind')
    if kind not in _CONTROLLER_KINDS:
        raise ValueError('Unknown controller event')
    if kind in ('error', 'send_error', 'uncertain') and not isinstance(
            value.get('message'), str):
        raise ValueError('Missing diagnostic')
    if kind == 'exited' and type(value.get('code')) is not int:
        raise ValueError('Missing exit status')
    if kind == 'launched':
        _validate_target(value.get('target'))
    return value


def _watcher_request(line: bytes) -> dict:
    value = json.loads(line)
    if (not isinstance(value, dict) or value.get('operation') not in ('ready', 'send')
            or (value['operation'] == 'send' and not isinstance(value.get('text'), str))):
        raise FactoryError('Invalid watcher request.')
    return value


def _acquire_owner_lock(directory: Path, workspace: Path) -> int:
    descriptor = os.open(directory / 'owner.lock',
                         os.O_CREAT | os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(descriptor).st_mode):
            raise FactoryError('Foreman owner lock must be a regular file; preserved.')
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise FactoryError('Foreman owner already exists; use foreman --attach '
                               f'--workspace {shlex.quote(str(workspace))}.') from error
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _prepare_owner_startup(workspace: Path) -> tuple[Path, Path, int]:
    directory = runtime_directory(workspace, create=True)
    descriptor = _acquire_owner_lock(directory, workspace)
    try:
        previous = read_state(workspace)
        if previous and previous.get('foreman') != 'stopped':
            raise FactoryError('Previous Foreman state is uncertain. Preserve its terminal '
                               'and owner files; reconcile before a new assisted launch.')
        endpoint = directory / 'control.sock'
        if len(os.fsencode(endpoint)) > 100:
            raise FactoryError('Workspace path is too long for the Foreman control socket.')
        if previous:
            if endpoint.exists() or endpoint.is_symlink():
                info = endpoint.lstat()
                if (not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid()
                        or stat.S_IMODE(info.st_mode) & 0o077):
                    raise FactoryError('Invalid old Foreman socket; preserved for review.')
            endpoint.unlink(missing_ok=True)
        return directory, endpoint, descriptor
    except BaseException:
        os.close(descriptor)
        raise


class ForemanOwner:
    def __init__(self, workspace: Path, python: str, directory: Path):
        self.workspace = workspace
        self.python = python
        self.directory = directory
        self.state = {'workspace': str(workspace), 'run_id': uuid.uuid4().hex,
                      'foreman': 'starting', 'target': None, 'watcher': 'stopped'}
        self.controller = None
        self.ready = asyncio.get_running_loop().create_future()
        self.stopped = asyncio.Event()
        self.watcher = None
        self.watcher_done = None
        self.watcher_ready = None
        self.channel = None
        self.delivery = asyncio.Lock()
        self.sent = None
        self.delivery_error = None
        self.spawned = None
        self.deadlines = AgentShellLifecycleDeadlines()

    def save(self):
        replace_generated_json(self.directory / 'owner.json', self.state)

    def _validate_readiness(self, value) -> None:
        if value['kind'] != 'ready':
            return
        if not self.state['target'] or self.ready.done():
            raise ValueError('Unexpected readiness')
        if 'warning' in value and not isinstance(value['warning'], str):
            raise ValueError('Invalid readiness warning')

    async def _reject_controller_event(self, error) -> None:
        message = f'Invalid controller message; terminal state uncertain: {error}'
        print(message, file=sys.stderr, flush=True)
        self.state['foreman'] = 'unknown'
        self.state['warning'] = message
        if not self.ready.done():
            self.ready.set_exception(FactoryError(message))
        else:
            await self.stop_watcher()
        self.save()

    async def _apply_controller_problem(self, value) -> None:
        print(value['message'], file=sys.stderr, flush=True)
        if value['kind'] == 'send_error':
            self.delivery_error = (
                value['message'] + '. Inspect Foreman for the possible message, '
                'then deliberately exit Foreman and relaunch with foreman '
                f'--workspace {shlex.quote(str(self.workspace))}. '
                'This failed send cannot be acknowledged or retried in this session.')
            value['message'] = self.delivery_error
            if self.sent and not self.sent.done():
                self.sent.set_exception(FactoryError(self.delivery_error))
        self.state['warning'] = value['message']
        if not self.ready.done():
            self.ready.set_exception(FactoryError(value['message']))
        elif value['kind'] in ('send_error', 'uncertain'):
            if value['kind'] == 'uncertain':
                self.state['foreman'] = 'unknown'
            await self.stop_watcher()
            self.state['warning'] = value['message']
        self.save()

    async def _apply_controller_event(self, value) -> None:
        kind = value['kind']
        if kind == 'launched':
            self.state['target'] = value['target']
            self.save()
        elif kind == 'ready':
            self.state['foreman'] = 'unknown' if value.get('warning') else 'ready'
            if value.get('warning'):
                self.state['warning'] = value['warning']
            self.save()
            self.ready.set_result(None)
        elif kind == 'sent' and self.sent and not self.sent.done():
            self.sent.set_result(None)
        elif kind in ('exited', 'stopped'):
            self.state['foreman'] = 'stopped'
        elif kind in ('error', 'send_error', 'uncertain'):
            await self._apply_controller_problem(value)

    def _finish_observation(self) -> None:
        if not self.ready.done():
            self.ready.set_exception(FactoryError('Foreman exited before startup readiness.'))
        if self.state['foreman'] != 'stopped':
            self.state['foreman'] = 'unknown'
        self.save()
        self.stopped.set()
        if self.sent and not self.sent.done():
            self.sent.set_exception(FactoryError('Foreman exited during delivery.'))

    async def observe(self):
        try:
            while line := await self.controller.stdout.readline():
                try:
                    value = _controller_event(line)
                    self._validate_readiness(value)
                except (ValueError, TypeError) as error:
                    await self._reject_controller_event(error)
                    continue
                await self._apply_controller_event(value)
        except (ValueError, OSError) as error:
            message = f'Invalid controller message or disconnected stream: {error}'
            print(message, file=sys.stderr, flush=True)
            self.state['warning'] = message
            if not self.ready.done():
                self.ready.set_exception(FactoryError(message))
        finally:
            self._finish_observation()

    async def _relay_request(self, value) -> None:
        if self.state['foreman'] != 'ready':
            raise FactoryError('Foreman is not ready.')
        if value['operation'] == 'ready':
            if not self.watcher_ready.done():
                self.watcher_ready.set_result(None)
            self.state['watcher'] = 'running'
            return
        async with self.delivery:
            self.sent = asyncio.get_running_loop().create_future()
            self.sent.add_done_callback(
                lambda future: None if future.cancelled() else future.exception())
            self.controller.stdin.write(
                (json.dumps({'text': value['text']}) + '\n').encode())
            await self.controller.stdin.drain()
            async with asyncio.timeout(22):
                await asyncio.shield(self.sent)

    async def relay(self, reader, writer):
        try:
            while line := await reader.readline():
                await self._relay_request(_watcher_request(line))
                writer.write(b'{"kind":"ok"}\n')
                await writer.drain()
        except (OSError, ValueError, FactoryError, TimeoutError):
            with contextlib.suppress(Exception):
                writer.write(b'{"kind":"error"}\n')
                await writer.drain()
        finally:
            writer.close()

    async def reap_watcher(self, child, relay):
        code = await child.wait()
        relay.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await relay
        if not self.watcher_ready.done():
            self.watcher_ready.set_exception(FactoryError(
                'Watcher startup failed; setup may be incomplete or the workspace lease busy. '
                'Inspect .factory/runtime/foreman/owner.log; retry after correction.'))
        self.state['watcher'] = 'stopped' if code in (0, 130) else 'failed'

    async def start_watcher(self, value):
        if self.state['foreman'] != 'ready':
            raise FactoryError('Foreman is not ready; no watcher started.')
        if self.delivery_error:
            raise FactoryError(self.delivery_error)
        if self.sent and not self.sent.done():
            raise FactoryError('Previous delivery is still unacknowledged. Inspect Foreman '
                               'and retry after it resolves; no new watcher started.')
        if self.state['watcher'] in ('starting', 'running', 'stopping'):
            raise FactoryError('Watcher already starting or running; existing process preserved.')
        interval = value.get('interval')
        if (type(interval) not in (int, float) or not math.isfinite(interval) or interval <= 0
                or type(value.get('existing')) is not bool):
            raise FactoryError('Invalid watcher startup options.')
        self.state['watcher'] = 'starting'
        self.spawned = asyncio.get_running_loop().create_future()
        self.watcher_ready = asyncio.get_running_loop().create_future()
        parent, child = socket.socketpair()
        try:
            self.watcher = await asyncio.create_subprocess_exec(
                sys.executable, '-m', 'forgetful_factory', 'watch',
                '--workspace', str(self.workspace), '--owner-fd', str(child.fileno()),
                '--existing' if value['existing'] else '--new-only', '--interval', str(interval),
                pass_fds=(child.fileno(),), stdin=asyncio.subprocess.DEVNULL,
                start_new_session=True)
            reader, writer = await asyncio.open_connection(sock=parent)
            self.channel = writer
            relay = asyncio.create_task(self.relay(reader, writer))
            self.watcher_done = asyncio.create_task(self.reap_watcher(self.watcher, relay))
        except BaseException:
            parent.close()
            self.state['watcher'] = 'failed'
            raise
        finally:
            child.close()
            self.spawned.set_result(None)
        try:
            async with asyncio.timeout(self.deadlines.owner_watcher_start):
                await asyncio.shield(self.watcher_ready)
        except TimeoutError as error:
            await self.stop_watcher()
            raise FactoryError('Watcher startup timed out and was stopped; external checks '
                               'may be uncertain. Complete native sign-in in an attended terminal, '
                               'then retry watch --start. Use init --finalize for incomplete '
                               'first setup.') \
                from error

    async def stop_watcher(self):
        if self.spawned and not self.spawned.done():
            async with asyncio.timeout(self.deadlines.owner_watcher_stop):
                await asyncio.shield(self.spawned)
        if self.watcher is None or (self.watcher_done and self.watcher_done.done()):
            self.state['watcher'] = 'stopped'
            return
        self.state['watcher'] = 'stopping'
        if self.watcher.returncode is None:
            self.watcher.terminate()
        try:
            async with asyncio.timeout(self.deadlines.owner_watcher_stop):
                await asyncio.shield(self.watcher_done)
        except TimeoutError:
            if self.watcher.returncode is None:
                self.watcher.kill()
            async with asyncio.timeout(self.deadlines.owner_watcher_stop):
                await asyncio.shield(self.watcher_done)
            self.state['warning'] = ('Watcher forced to stop; delivery/external work uncertain. '
                                     'External helpers may need inspection; no PID scanning.')
        self.state['watcher'] = 'stopped'
        if self.sent and not self.sent.done():
            self.state['warning'] = ('Watcher stopped; its last delivery is still in progress. '
                                     'Foreman was preserved; do not assume receipt.')

    async def control(self, reader, writer):
        try:
            async with asyncio.timeout(5):
                value = json.loads(await reader.readline())
            if (not isinstance(value, dict)
                    or value.get('operation') not in ('start', 'stop', 'status')):
                raise FactoryError('Invalid Foreman control request; expected a command object.')
            if (value.get('run_id') != self.state['run_id']
                    or value.get('workspace') != str(self.workspace)):
                raise FactoryError('Foreman identity mismatch; no action performed.')
            if value.get('operation') == 'start':
                await self.start_watcher(value)
            elif value.get('operation') == 'stop':
                await self.stop_watcher()
            elif value.get('operation') != 'status':
                raise FactoryError('Unsupported Foreman operation.')
            response = {**self.state, 'owner_pid': os.getpid()}
        except (FactoryError, ValueError, TimeoutError, OSError) as error:
            response = {'run_id': self.state['run_id'], 'error': str(error)}
        try:
            writer.write((json.dumps(response) + '\n').encode())
            await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    async def _start_controller(self, reader):
        async with asyncio.timeout(5):
            launch = json.loads(await reader.readline())
        self.deadlines = AgentShellLifecycleDeadlines(**launch.get('deadlines', {}))
        launch['report_target'] = True
        self.controller = await asyncio.create_subprocess_exec(
            self.python, '-u', str(Path(__file__).with_name('controller.py')),
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
            stderr=None, start_new_session=True)
        self.controller.stdin.write((json.dumps(launch) + '\n').encode())
        await self.controller.stdin.drain()
        return asyncio.create_task(self.observe()), asyncio.create_task(reader.readline())

    async def _await_readiness(self, disconnected) -> None:
        async with asyncio.timeout(self.deadlines.owner_ready):
            done, _ = await asyncio.wait((self.ready, disconnected),
                                         return_when=asyncio.FIRST_COMPLETED)
            if disconnected in done:
                raise FactoryError('Init disconnected before Foreman handover.')
            await self.ready

    async def _complete_handover(self, writer, disconnected) -> None:
        writer.write((json.dumps(self.state) + '\n').encode())
        await writer.drain()
        async with asyncio.timeout(5):
            if await disconnected != b'adopt\n':
                raise FactoryError('Init did not accept Foreman handover.')
        writer.write(b'adopted\n')
        await writer.drain()
        writer.close()

    async def _close_controller(self, observer) -> None:
        if not self.controller:
            return
        self.controller.stdin.close()
        try:
            # Controller EOF cleanup allows eight seconds for open and eight for close.
            async with asyncio.timeout(self.deadlines.owner_controller_close):
                await self.controller.wait()
        except TimeoutError:
            self.controller.terminate()
            async with asyncio.timeout(5):
                await self.controller.wait()
        if observer:
            await observer
        self.save()

    def _remove_control_socket(self, server, endpoint, socket_identity) -> None:
        if not server:
            return
        with contextlib.suppress(FileNotFoundError):
            info = endpoint.lstat()
            if (stat.S_ISSOCK(info.st_mode)
                    and (info.st_dev, info.st_ino) == socket_identity):
                endpoint.unlink()

    async def _cleanup(self, server, endpoint, socket_identity, observer, disconnected) -> None:
        if server:
            server.close()
            await server.wait_closed()
        if self.state['foreman'] == 'ready':
            self.state['foreman'] = 'stopping'
        await self.stop_watcher()
        if disconnected:
            disconnected.cancel()
        await self._close_controller(observer)
        self._remove_control_socket(server, endpoint, socket_identity)

    async def run(self, handover, endpoint):
        reader, writer = await asyncio.open_connection(sock=handover)
        server = observer = disconnected = None
        socket_identity = None
        try:
            self.save()
            server = await asyncio.start_unix_server(self.control, path=str(endpoint))
            endpoint.chmod(0o600)
            info = endpoint.lstat()
            socket_identity = (info.st_dev, info.st_ino)
            observer, disconnected = await self._start_controller(reader)
            await self._await_readiness(disconnected)
            await self._complete_handover(writer, disconnected)
            await self.stopped.wait()
        except (Exception, asyncio.CancelledError) as error:
            with contextlib.suppress(Exception):
                writer.write((json.dumps({'error': str(error) or 'Foreman startup cancelled'})
                              + '\n').encode())
                await writer.drain()
            if isinstance(error, asyncio.CancelledError):
                raise
        finally:
            await self._cleanup(server, endpoint, socket_identity, observer, disconnected)
            writer.close()


async def main(workspace, python, directory, endpoint, handover):
    owner = ForemanOwner(workspace, python, directory)
    task = asyncio.create_task(owner.run(handover, endpoint))
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, task.cancel)
    with contextlib.suppress(asyncio.CancelledError):
        await task


def _report_startup_error(handover, error) -> None:
    with handover, contextlib.suppress(OSError):
        message = str(error) or 'Foreman startup cancelled'
        handover.sendall((json.dumps({'error': message}) + '\n').encode())


def entrypoint() -> None:
    workspace = Path(sys.argv[1])
    handover = socket.socket(fileno=int(sys.argv[3]))
    try:
        directory, endpoint, descriptor = _prepare_owner_startup(workspace)
    except Exception as error:
        _report_startup_error(handover, error)
        return
    try:
        asyncio.run(main(workspace, sys.argv[2], directory, endpoint, handover))
    finally:
        os.close(descriptor)


if __name__ == '__main__':
    entrypoint()
