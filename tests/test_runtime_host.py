"""The session host: the tmux adapter's promises, and the controller's host choice."""
import json
import select
import subprocess
import sys
import unittest
from dataclasses import asdict

from contracts.runtime import SessionHostContract

from forgetful_factory.agents.adapters.agentshell.launch import CONTROLLER
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
