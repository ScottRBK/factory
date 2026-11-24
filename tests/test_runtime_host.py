"""The session host: the tmux adapter's promises, and the controller's host choice."""
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path

from contracts.runtime import SessionHostContract

from forgetful_factory.agents.adapters.agentshell.launch import CONTROLLER, TMUX_HOST
from forgetful_factory.agents.model import AgentShellLifecycleDeadlines
from forgetful_factory.runtime.adapters.tmux import TmuxHost


class TmuxHostContractTests(SessionHostContract, unittest.TestCase):
    target = {'socket_path': '/tmp/tmux-1000/default', 'pane_id': '%7', 'server_pid': 10,
              'server_started': 20, 'pane_pid': 30}

    def host(self):
        return TmuxHost()


class ControllerHostTests(unittest.TestCase):
    def frame(self, **changes):
        frame = {'cwd': '/', 'model': 'fixture/model', 'effort': 'high',
                 'session_name': 'host-check', 'resources': {}, 'prompt': None,
                 'deadlines': asdict(AgentShellLifecycleDeadlines()), 'host': {'kind': 'tmux'}}
        frame.update(changes)
        return {key: value for key, value in frame.items() if value is not ...}

    def reply(self, frame):
        # Act: keep stdin open until the controller replies, avoiding an EOF race.
        with subprocess.Popen([sys.executable, '-u', str(CONTROLLER)], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
            try:
                process.stdin.write(json.dumps(frame) + '\n')
                process.stdin.flush()
                self.assertTrue(select.select([process.stdout], [], [], 10)[0])
                reply = json.loads(process.stdout.readline())
                remaining, errors = process.communicate(timeout=10)
            finally:
                if process.poll() is None:
                    process.kill()
        self.assertEqual((process.returncode, remaining), (1, ''), errors)
        self.assertNotIn('Traceback', errors)
        return reply

    def test_an_unknown_host_kind_is_refused_before_a_session_opens(self):
        reply = self.reply(self.frame(host={'kind': 'herdr'}))
        self.assertEqual(reply, {'kind': 'error', 'message':
                                 "Unsupported Foreman host 'herdr'; AgentShell supports "
                                 'interactive sessions on tmux only.'})

    def test_a_launch_without_a_host_is_invalid(self):
        for host in (..., None, {}, {'kind': 7}):
            with self.subTest(host=host):
                reply = self.reply(self.frame(host=host))
                self.assertEqual(reply, {'kind': 'error',
                                         'message': 'Invalid Foreman launch configuration.'})


class ControllerPreflightTests(unittest.TestCase):
    """The preflight proves the controller and its host checks can load, as before the split."""

    def run_python(self, args, *, path=None):
        env = {key: value for key, value in os.environ.items()
               if key not in ('PYTHONDONTWRITEBYTECODE', 'PYTHONPATH')}
        if path is not None:
            env['PYTHONPATH'] = path
        return subprocess.run([sys.executable, *args], env=env, capture_output=True, text=True,
                              timeout=30)

    def test_preflight_fails_when_the_host_checks_cannot_load(self):
        # Arrange: an interpreter without ctypes, which the tmux pane checks need.
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, 'ctypes.py').write_text("raise ImportError('No ctypes here.')\n")
            # Act
            result = self.run_python(['-u', str(CONTROLLER), '--check'], path=temporary)
        # Assert
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertNotIn('Factory AgentShell ready', result.stdout)

    def test_launch_fails_at_start_when_the_host_checks_cannot_load(self):
        # Arrange: as preflight, but a plain launch (a watcher's terminal runs no preflight).
        with tempfile.TemporaryDirectory() as temporary:
            Path(temporary, 'ctypes.py').write_text("raise ImportError('No ctypes here.')\n")
            env = {key: value for key, value in os.environ.items() if key != 'PYTHONPATH'}
            # Act
            result = subprocess.run([sys.executable, '-u', str(CONTROLLER)],
                                    env=dict(env, PYTHONPATH=temporary), capture_output=True,
                                    text=True, timeout=30,
                                    input=json.dumps(ControllerHostTests.frame(self)) + '\n')
        # Assert: the old controller stopped on import, before any protocol reply.
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, '')
        self.assertIn('Traceback', result.stderr)

    def test_loading_the_host_checks_writes_no_bytecode_beside_them(self):
        # Arrange: a copy of the controller and its host file, as installed together.
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for name in (CONTROLLER.name, TMUX_HOST.name):
                shutil.copy(CONTROLLER.with_name(name), folder / name)
            # Act
            result = self.run_python(['-c', 'import runpy, sys; runpy.run_path(sys.argv[1], '
                                      "run_name='controller')['load_host']('tmux')",
                                      str(folder / CONTROLLER.name)])
            # Assert: the old controller ran as one script and left no cache files.
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(sorted(path.name for path in folder.iterdir()),
                             sorted((CONTROLLER.name, TMUX_HOST.name)))
