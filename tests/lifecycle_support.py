"""Real AgentShell/tmux, isolated homes, and a fake interactive Pi with no inference."""
import array
import ctypes
import json
import os
import selectors
import shlex
import shutil
import signal
import socket
import subprocess
import sys

from profile_support import COMMAND
from test_init import GH, ROOT, InitFixture


def pidfd_open(pid):
    if hasattr(os, 'pidfd_open'):
        return os.pidfd_open(pid)
    function = ctypes.CDLL(None, use_errno=True).pidfd_open
    function.argtypes = [ctypes.c_int, ctypes.c_uint]
    function.restype = ctypes.c_int
    descriptor = function(pid, 0)
    if descriptor < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    return descriptor


def pidfd_send_signal(descriptor, sig):
    if hasattr(signal, 'pidfd_send_signal'):
        return signal.pidfd_send_signal(descriptor, sig)
    function = ctypes.CDLL(None, use_errno=True).pidfd_send_signal
    function.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_uint]
    function.restype = ctypes.c_int
    if function(descriptor, sig, None, 0) < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))


INTERACTIVE = r'''
elif name == 'pi' and '--extension' in args:
    import re
    observer = next(Path(args[i + 1]) for i, arg in enumerate(args)
                    if arg == '--extension' and args[i + 1].endswith('pi-events.mjs'))
    with Path(os.environ['FAKE_PI_LOG']).open('a') as log:
        log.write(json.dumps({'started': os.getpid(), 'cwd': os.getcwd(), 'args': args,
                             'command': os.environ.get('FACTORY_COMMAND'),
                             'workspace': os.environ.get('FACTORY_WORKSPACE'),
                             'roster': os.environ.get('PI_AGENTSHELL_ROSTER_FILE')}) + '\n')
    if os.environ.get('FAKE_PI_NOTIFY'):
        with open(os.environ['FAKE_PI_NOTIFY'], 'w') as notify:
            notify.write('started\n')
    if os.environ.get('FAKE_PI_NO_READY'):
        import signal
        signal.pause()
    observer.with_name('events.jsonl').write_text(
        json.dumps({'type': 'session_start', 'session_id': 'fixture-conversation'}) + '\n')
    print('FAKE_PI_READY', flush=True)
    for line in sys.stdin:
        with Path(os.environ['FAKE_PI_LOG']).open('a') as log:
            log.write(json.dumps({'input': line}) + '\n')
        if os.environ.get('FAKE_PI_INPUT_NOTIFY'):
            with open(os.environ['FAKE_PI_INPUT_NOTIFY'], 'w') as notify:
                notify.write('input\n')
        if 'EXIT_FAKE' in line:
            sys.exit(7)
'''

SEND = '''
import asyncio, json, sys
from agent_shell import TmuxExecutionHost, TmuxTarget
from agent_shell.shell import AgentShell
from agent_shell.models.agent import AgentType
from agent_shell.execution import NoIsolation
async def main():
    shell = AgentShell(AgentType.PI, execution_host=TmuxExecutionHost(),
                       isolation_policy=NoIsolation())
    async with await shell.attach_interactive(TmuxTarget(**json.loads(sys.argv[1]))) as c:
        await c.terminal.send_text(sys.argv[2], submit=True)
asyncio.run(main())
'''


class LifecycleFixture(InitFixture):
    def setUp(self):
        super().setUp()
        self.owner_descriptors = {}
        self.tmux = shutil.which('tmux', path='/usr/bin:/bin')
        self.assertIsNotNone(self.tmux, 'Native lifecycle tests need existing tmux')
        self.socket = self.workspace / 'tmux.sock'
        self.env = {key: value for key, value in self.env.items()
                    if key in ('PYTHONPATH', 'GH_STATE', 'PI_CODING_AGENT_DIR')}
        self.env.update(HOME=str(self.workspace), XDG_CONFIG_HOME=str(self.workspace / 'config'),
                        PATH=f'{self.bin}:{os.path.dirname(sys.executable)}:/usr/bin:/bin',
                        TMPDIR=str(self.workspace), PI_OFFLINE='1',
                        FAKE_PI_LOG=str(self.workspace / 'pi.jsonl'),
                        PLANNING_STATE=str(self.workspace / 'plans.json'))
        # The selected interpreter transfers a live parent pidfd before native open. Queued
        # descriptors retain that exact owner even if init is cancelled before public readiness.
        self.owner_handles = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        handle_path = self.workspace / 'owner-handles.sock'
        self.owner_handles.bind(str(handle_path))
        self.owner_handles.setblocking(False)
        self.addCleanup(self.owner_handles.close)
        self.interpreter = self.bin / 'tracked-python'
        self.interpreter.write_text(
            f'#!{sys.executable}\nimport array, os, socket, sys\n'
            f'sys.path.insert(0, {str(ROOT / "tests")!r})\n'
            'from lifecycle_support import pidfd_open\n'
            'if "--check" not in sys.argv:\n'
            '    descriptor = pidfd_open(os.getppid())\n'
            '    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as channel:\n'
            f'        channel.connect({str(handle_path)!r})\n'
            '        channel.sendmsg([str(os.getppid()).encode()],\n'
            '                        [(socket.SOL_SOCKET, socket.SCM_RIGHTS,\n'
            '                          array.array("i", [descriptor]))])\n'
            '    os.close(descriptor)\n'
            f'os.execv({sys.executable!r}, [{sys.executable!r}, *sys.argv[1:]])\n')
        self.interpreter.chmod(0o700)
        (self.bin / 'tmux').write_text(
            f'#!/bin/sh\nexec {shlex.quote(self.tmux)} -S {shlex.quote(str(self.socket))} "$@"\n')
        (self.bin / 'pi').write_text(COMMAND.replace(
            "elif name == 'pi' and args == ['mcp', 'list', '--json']:",
            INTERACTIVE + "\nelif name == 'pi' and args == ['mcp', 'list', '--json']:"))
        (self.bin / 'gh').write_text(GH.replace(
            "    if endpoint.endswith('/labels'):",
            "    if endpoint.endswith('/issues'):\n"
            "        if os.environ.get('GH_FREEZE_NOTIFY'):\n"
            "            os.kill(os.getppid(), signal.SIGSTOP)\n"
            "            with open(os.environ['GH_FREEZE_NOTIFY'], 'w') as notify:\n"
            "                notify.write('frozen\\n')\n"
            "        print(json.dumps([state.get('issues', [])]))\n        sys.exit(0)\n"
            "    if endpoint.endswith('/labels'):"))
        subprocess.run([str(self.bin / 'tmux'), 'new-session', '-d', '-s', 'fixture',
                        '/bin/cat'], env=self.env, check=True, capture_output=True)
        self.addCleanup(self.close_tmux)

    def close_tmux(self):
        self.collect_owner_handles()
        # Explicit fixture teardown owns these pinned processes, including intentionally uncertain
        # owners. Product behavior must not mistake loss of tmux queries for proof of native exit.
        for descriptor in self.owner_descriptors.values():
            try:
                pidfd_send_signal(descriptor, signal.SIGTERM)
            except ProcessLookupError:
                pass
        subprocess.run([self.tmux, '-S', str(self.socket), 'kill-server'],
                       env=self.env, capture_output=True, timeout=5)
        try:
            with selectors.DefaultSelector() as selector:
                for descriptor in self.owner_descriptors.values():
                    selector.register(descriptor, selectors.EVENT_READ)
                while selector.get_map():
                    ready = selector.select(30)
                    self.assertTrue(ready, 'Fixture owner survived private server cleanup')
                    for key, _ in ready:
                        selector.unregister(key.fd)
        finally:
            for descriptor in self.owner_descriptors.values():
                os.close(descriptor)

    def collect_owner_handles(self):
        while True:
            try:
                data, ancillary, _, _ = self.owner_handles.recvmsg(100, socket.CMSG_SPACE(4))
            except BlockingIOError:
                return
            for level, kind, payload in ancillary:
                self.assertEqual((level, kind), (socket.SOL_SOCKET, socket.SCM_RIGHTS))
                descriptors = array.array('i')
                descriptors.frombytes(payload)
                self.assertEqual(len(descriptors), 1)
                previous = self.owner_descriptors.get(int(data))
                if previous is not None:
                    os.close(previous)
                self.owner_descriptors[int(data)] = descriptors[0]

    def run_cli(self, cwd, *args, **kwargs):
        if '--agentshell-python' not in args:
            args = (*args, '--agentshell-python', str(self.interpreter))
        return super().run_cli(cwd, *args, **kwargs)

    def watch(self, repo, *args, timeout=15):
        return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'watch',
                               '--workspace', str(repo), *args], cwd=ROOT, env=self.env,
                              capture_output=True, text=True, timeout=timeout)

    def foreman(self, repo, *args, timeout=20):
        return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'foreman',
                               '--workspace', str(repo), '--agentshell-python',
                               str(self.interpreter), *args], cwd=ROOT, env=self.env,
                              capture_output=True, text=True, timeout=timeout)

    def status(self, repo):
        self.collect_owner_handles()
        result = self.watch(repo, '--status')
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        pid = value.get('owner_pid')
        if pid and pid not in self.owner_descriptors:
            self.owner_descriptors[pid] = pidfd_open(pid)
        return value

    def send(self, target, text):
        result = subprocess.run([sys.executable, '-c', SEND, json.dumps(target), text],
                                env=self.env, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)

    def send_and_wait_for_exit(self, repo, target):
        import select

        # Pin the PID returned by the live public status before asking the fake terminal to exit.
        # pidfd readiness reports process exit without polling or signaling a persisted PID.
        descriptor = pidfd_open(self.status(repo)['owner_pid'])
        try:
            self.send(target, 'EXIT_FAKE')
            self.assertTrue(select.select([descriptor], [], [], 15)[0],
                            'Owner did not finish cleanup')
        finally:
            os.close(descriptor)
