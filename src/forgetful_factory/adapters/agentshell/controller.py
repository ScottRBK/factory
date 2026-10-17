"""Run by the selected AgentShell interpreter using this installed file's absolute path."""
import asyncio
import contextlib
import json
import os
import signal
import sys


async def ready(session) -> None:
    async with contextlib.aclosing(session.events()) as events:
        async for event in events:
            if event.type == 'system' and event.session_id:
                return
    raise RuntimeError('Pi exited before its session-ready event.')


async def interact(session, reader, reply, name) -> None:
    try:
        async with asyncio.timeout(30):
            await ready(session)
    except TimeoutError as error:
        raise RuntimeError(f'Pi did not become ready within 30 seconds ({name}). '
                           'Watcher is stopping. Check any cleanup errors before retrying. '
                           'Restart watch, then promptly use the new tmux attach-session '
                           'command shown at startup to resolve any trust dialog.') from error
    reply({'kind': 'ready'})
    while line := await reader.readline():
        request = json.loads(line)
        try:
            async with asyncio.timeout(10):
                await session.terminal.send_text(request['text'], submit=True)
        except TimeoutError as error:
            raise RuntimeError('Pi send timed out after 10 seconds; '
                               'submission is uncertain. Watcher stopped.') from error
        reply({'kind': 'sent'})


async def serve(reader, config, reply) -> None:
    try:
        from agent_shell.models.agent import AgentType
        from agent_shell.models.resources import SessionResources
        from agent_shell.shell import AgentShell
        from agent_shell.tmux import TmuxExecutionHost, TmuxPlacement
    except ImportError as error:
        raise RuntimeError('Select --agentshell-python pointing to an installed interpreter '
                           'with AgentShell 0.5 SessionResources and interactive tmux support: '
                           f'{error}') from error
    if not callable(getattr(AgentShell, 'open_interactive', None)):
        raise RuntimeError('AgentShell lacks open_interactive. Select --agentshell-python '
                           'pointing to an already installed compatible interpreter.')

    shell = AgentShell(agent_type=AgentType.PI, execution_host=TmuxExecutionHost(
        TmuxPlacement.new_session(config['session_name'])))
    session = None
    tasks = []
    try:
        try:
            async with asyncio.timeout(30):
                resources = SessionResources(
                    **config['resources'], mcp_servers=[],
                    inherit_personal_resources=False, inherit_project_resources=False,
                    include_instruction_files=True, include_home_system_prompt=False,
                )
                session = await shell.open_interactive(
                    config['cwd'], model=config['model'], effort=config['effort'],
                    resources=resources, prompt=config['prompt'],
                )
        except TimeoutError as error:
            raise RuntimeError('AgentShell launch timed out after 30 seconds; '
                               'check Pi and tmux installations.') from error
        conversation = asyncio.create_task(interact(session, reader, reply, config['session_name']))
        exit_task = asyncio.create_task(session.terminal.wait())
        tasks = [conversation, exit_task]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        if exit_task in done:
            raise RuntimeError(f'Pi exited with status {exit_task.result()}; watcher stopped.')
        await conversation
    finally:
        for task in tasks:
            task.cancel()
        for task in tasks:
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await task
        if session is not None:
            try:
                async with asyncio.timeout(8):
                    await session.close()
            except Exception as error:
                raise RuntimeError('Pi cleanup failed or timed out; '
                                   f'check session {config["session_name"]}: '
                                   f'{str(error) or type(error).__name__}') from error


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
        serving = asyncio.create_task(serve(reader, config, reply))
        eof = asyncio.create_task(disconnected.wait())
        tasks = [serving, eof]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        if serving in done:
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
