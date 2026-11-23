"""tmux pane checks for the controller. Loaded by path beside controller.py, in AgentShell's
interpreter: only the standard library and agent_shell are importable there."""
import asyncio
import ctypes
import os
import select


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
