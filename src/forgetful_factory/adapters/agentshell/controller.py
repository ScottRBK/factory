"""Run by the selected AgentShell interpreter using this installed file's absolute path."""
import asyncio
import contextlib
import ctypes
import json
import math
import os
import select
import signal
import sys
from dataclasses import asdict, dataclass


async def ready(session) -> None:
    async with contextlib.aclosing(session.events()) as events:
        async for event in events:
            if event.type == 'system' and event.session_id:
                return
    raise RuntimeError('Pi exited before its session-ready event.')


async def interact(session, reader, reply, name, deadlines, *, persistent=False,
                   startup_warning=None) -> None:
    try:
        async with asyncio.timeout(deadlines['controller_ready']):
            await ready(session)
    except TimeoutError as error:
        raise RuntimeError('Pi did not become ready within '
                           f'{deadlines["controller_ready"]:g} seconds ({name}). '
                           'Watcher is stopping. Check any cleanup errors before retrying. '
                           'Restart watch, then promptly use the new tmux attach-session '
                           'command shown at startup to resolve any trust dialog.') from error
    reply({'kind': 'ready', **({'warning': startup_warning} if startup_warning else {})})
    while line := await reader.readline():
        try:
            request = json.loads(line)
            if not isinstance(request, dict) or not isinstance(request.get('text'), str):
                raise ValueError('Invalid Foreman send request; expected text in an object.')
            async with asyncio.timeout(deadlines['controller_send']):
                await session.terminal.send_text(request['text'], submit=True)
        except Exception as error:
            if persistent:
                reply({'kind': 'send_error', 'message':
                       'Foreman send failed; delivery uncertain: '
                       f'{str(error) or type(error).__name__}'})
                continue
            if not isinstance(error, TimeoutError):
                raise
            raise RuntimeError('Pi send timed out after '
                               f'{deadlines["controller_send"]:g} seconds; '
                               'submission is uncertain. Watcher stopped.') from error
        reply({'kind': 'sent'})


async def retain_identity(session, reply) -> None:
    """Owned wait detects exit; compare identity too, since a pane ID can be respawned."""
    from agent_shell.tmux import TmuxTarget

    target = session.terminal.target
    while True:
        try:
            async with asyncio.timeout(5):
                current = await TmuxTarget.capture(target.pane_id, socket_path=target.socket_path)
        except Exception as error:
            reply({'kind': 'uncertain', 'message':
                   'Foreman identity query unavailable; terminal state uncertain: '
                   f'{str(error) or type(error).__name__}'})
            return
        if current != target:
            raise RuntimeError('Captured Foreman terminal identity changed; replacement refused.')
        await asyncio.sleep(1)


async def pin_worker(target) -> int:
    """Pin a live launch target, then revalidate it; never use saved owner metadata."""
    from agent_shell.tmux import TmuxTarget

    if hasattr(os, 'pidfd_open'):
        descriptor = os.pidfd_open(target.pane_pid)
    else:
        # Python 3.13 builds may omit os.pidfd_open. This Linux fallback needs glibc 2.36+
        # and a kernel supporting pidfd_open (5.3+); unsupported hosts remain uncertain.
        function = ctypes.CDLL(None, use_errno=True).pidfd_open
        function.argtypes = [ctypes.c_int, ctypes.c_uint]
        function.restype = ctypes.c_int
        descriptor = function(target.pane_pid, 0)
        if descriptor < 0:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error))
    try:
        async with asyncio.timeout(5):
            current = await TmuxTarget.capture(target.pane_id, socket_path=target.socket_path)
        if current != target or select.select([descriptor], [], [], 0)[0]:
            raise RuntimeError('Original pane worker could not be validated alive.')
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


async def worker_exited(descriptor) -> None:
    loop = asyncio.get_running_loop()
    exited = loop.create_future()

    def observed():
        if not exited.done():
            exited.set_result(None)

    loop.add_reader(descriptor, observed)
    try:
        await exited
    finally:
        loop.remove_reader(descriptor)


async def resume_exit_observation(session) -> int:
    # A transient tmux error must not end ownership or lose a later actual SDK exit result.
    await asyncio.sleep(1)
    return await session.terminal.wait()


def runtime():
    try:
        from agent_shell.models.agent import AgentType as agent_type
        from agent_shell.models.resources import SessionResources as session_resources
        from agent_shell.shell import AgentShell as agent_shell
        from agent_shell.tmux import TmuxExecutionHost as tmux_execution_host
        from agent_shell.tmux import TmuxPlacement as tmux_placement
    except ImportError as error:
        raise RuntimeError('Select --agentshell-python pointing to an installed interpreter '
                           'with AgentShell 0.5 SessionResources and interactive tmux support: '
                           f'{error}') from error
    if not callable(getattr(agent_shell, 'open_interactive', None)):
        raise RuntimeError('AgentShell lacks open_interactive. Select --agentshell-python '
                           'pointing to an already installed compatible interpreter.')
    return agent_type, session_resources, agent_shell, tmux_execution_host, tmux_placement


@dataclass
class SessionState:
    session: object | None = None
    worker: int | None = None
    worker_error: str | None = None
    cleanup_known: bool = True


def validate_launch_config(config) -> None:
    deadline_names = {
        'controller_ready', 'controller_send', 'controller_close', 'parent_ready',
        'owner_watcher_start', 'owner_watcher_stop', 'owner_ready',
        'owner_controller_close', 'owner_pre_adoption_cleanup',
    }
    deadlines = config.get('deadlines') if isinstance(config, dict) else None
    if (not isinstance(config, dict)
            or any(not isinstance(config.get(key), str)
                   for key in ('cwd', 'model', 'effort', 'session_name'))
            or not isinstance(config.get('resources'), dict)
            or not isinstance(config.get('prompt'), (str, type(None)))
            or not isinstance(deadlines, dict) or set(deadlines) != deadline_names
            or any(type(value) not in (int, float) or not math.isfinite(value) or value <= 0
                   for value in deadlines.values())):
        raise ValueError('Invalid Foreman launch configuration.')


def build_shell(config):
    agent_type, session_resources, agent_shell, execution_host, placement = runtime()
    shell = agent_shell(agent_type=agent_type.PI, execution_host=execution_host(
        placement.new_session(config['session_name'])))
    return shell, session_resources


async def open_session(state, shell, resources_type, config, reply, opened) -> None:
    try:
        async with asyncio.timeout(config['deadlines']['controller_ready']):
            resources = resources_type(**config['resources'])
            state.session = await shell.open_interactive(
                config['cwd'], model=config['model'], effort=config['effort'],
                resources=resources, prompt=config['prompt'],
            )
            if config.get('report_target'):
                await capture_worker(state, reply)
            opened.set()
    except TimeoutError as error:
        raise RuntimeError('AgentShell launch timed out after '
                           f'{config["deadlines"]["controller_ready"]:g} seconds; '
                           'check Pi and tmux installations.') from error


async def capture_worker(state, reply) -> None:
    try:
        state.worker = await pin_worker(state.session.terminal.target)
    except Exception as error:
        state.worker_error = ('Native worker lifetime unavailable; exit remains '
                              f'uncertain: {str(error) or type(error).__name__}')
        print(state.worker_error, file=sys.stderr, flush=True)
    reply({'kind': 'launched', 'target': asdict(state.session.terminal.target)})


def replace_failed_exit_task(state, exit_task, session, config, reply, failed):
    error = exit_task.exception()
    if error is None:
        if config.get('report_target'):
            reply({'kind': 'exited', 'code': exit_task.result()})
        raise RuntimeError(f'Pi exited with status {exit_task.result()}; watcher stopped.')
    state.cleanup_known = False
    if not config.get('report_target'):
        raise error
    if not failed:
        suffix = f'. {state.worker_error}' if state.worker_error else ''
        reply({'kind': 'uncertain', 'message':
               'Foreman exit observation failed; terminal state uncertain: '
               f'{error}{suffix}'})
    return asyncio.create_task(resume_exit_observation(session)), True


async def cancel_tasks(tasks) -> None:
    for task in tasks:
        task.cancel()
    for task in tasks:
        with contextlib.suppress(asyncio.CancelledError, Exception):
            await task


async def supervise_session(state, reader, config, reply) -> None:
    session = state.session
    tasks = []
    try:
        conversation = asyncio.create_task(interact(
            session, reader, reply, config['session_name'], config['deadlines'],
            persistent=config.get('report_target', False),
            startup_warning=state.worker_error))
        tasks.append(conversation)
        exit_task = asyncio.create_task(session.terminal.wait())
        tasks.append(exit_task)
        identity_task = None
        if config.get('report_target'):
            identity_task = asyncio.create_task(retain_identity(session, reply))
            tasks.append(identity_task)
        lost_worker = None
        if state.worker is not None:
            lost_worker = asyncio.create_task(worker_exited(state.worker))
            tasks.append(lost_worker)
        pending = set(tasks)
        exit_failed = False
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            if exit_task in done:
                tasks.remove(exit_task)
                exit_task, exit_failed = replace_failed_exit_task(
                    state, exit_task, session, config, reply, exit_failed)
                tasks.append(exit_task)
                pending.add(exit_task)
            if lost_worker in done:
                lost_worker.result()
                state.cleanup_known = False
                reply({'kind': 'uncertain', 'message':
                       'Original pane worker exited; SDK Pi exit remains unconfirmed.'})
                break  # Original worker exit permits release, never a confirmed Pi stop.
            if identity_task in done:
                state.cleanup_known = False
                identity_task.result()  # Mismatch is fatal; unavailable stays uncertain.
                if state.worker_error:
                    reply({'kind': 'uncertain', 'message': state.worker_error})
            if conversation in done:
                conversation.result()
                break
    finally:
        await cancel_tasks(tasks)


async def close_session(state, config, reply) -> None:
    if state.worker is not None:
        os.close(state.worker)
    if state.session is None:
        return
    try:
        async with asyncio.timeout(config['deadlines']['controller_close']):
            await state.session.close()
        if config.get('report_target') and state.cleanup_known:
            reply({'kind': 'stopped'})
    except Exception as error:
        raise RuntimeError('Pi cleanup failed or timed out; '
                           f'check session {config["session_name"]}: '
                           f'{str(error) or type(error).__name__}') from error


async def serve(reader, config, reply, opened) -> None:
    validate_launch_config(config)
    shell, resources_type = build_shell(config)
    state = SessionState()
    try:
        await open_session(state, shell, resources_type, config, reply, opened)
        await supervise_session(state, reader, config, reply)
    finally:
        await close_session(state, config, reply)


async def control(reply) -> None:
    reader = asyncio.StreamReader()
    disconnected = asyncio.Event()

    class InputProtocol(asyncio.StreamReaderProtocol):
        def eof_received(self):
            result = super().eof_received()
            disconnected.set()
            return result

    protocol = InputProtocol(reader)
    transport, _ = await asyncio.get_running_loop().connect_read_pipe(lambda: protocol, sys.stdin)
    tasks = []
    try:
        line = await reader.readline()
        if not line:
            return
        config = json.loads(line)
        opened = asyncio.Event()
        serving = asyncio.create_task(serve(reader, config, reply, opened))
        eof = asyncio.create_task(disconnected.wait())
        tasks = [serving, eof]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        if serving in done:
            await serving
        elif isinstance(config, dict) and config.get('report_target'):
            # EOF during native open is not proof that nothing launched. Give the bounded open
            # a chance to return its owned handle so cancellation can report confirmed cleanup.
            known_start = asyncio.create_task(opened.wait())
            tasks.append(known_start)
            finished, _ = await asyncio.wait(
                (serving, known_start), timeout=config['deadlines']['controller_close'],
                return_when=asyncio.FIRST_COMPLETED)
            if serving in finished:
                await serving
    finally:
        for task in tasks:
            task.cancel()
        for task in tasks:
            with contextlib.suppress(asyncio.CancelledError):
                await task
        transport.close()


async def main(reply) -> int:
    task = asyncio.create_task(control(reply))
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, task.cancel)
    try:
        await task
    except asyncio.CancelledError:
        reply({'kind': 'closed'})
        raise
    except Exception as error:
        reply({'kind': 'error', 'message': str(error) or type(error).__name__})
        return 1
    else:
        reply({'kind': 'closed'})
    finally:
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.remove_signal_handler(sig)
    return 0


if __name__ == '__main__':
    if sys.argv[1:] == ['--check']:
        try:
            runtime()
        except Exception as error:
            print(str(error), file=sys.stderr)
            sys.exit(1)
        print('Factory AgentShell ready')
        sys.exit(0)
    # Redirect the actual stdout descriptor too: library/native prints cannot corrupt JSON lines.
    with os.fdopen(os.dup(sys.stdout.fileno()), 'w', buffering=1) as output:
        os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
        sys.stdout = sys.stderr

        def reply(value):
            with contextlib.suppress(BrokenPipeError):
                output.write(json.dumps(value) + '\n')

        try:
            status = asyncio.run(main(reply))
        except asyncio.CancelledError:
            # Process boundary: signal-driven cancellation already completed owned cleanup.
            status = 0
        sys.exit(status)
