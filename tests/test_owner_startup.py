"""Owner startup defenses at the real module process boundary."""
import errno
import fcntl
import json
import os
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER_MODULE = 'forgetful_factory.adapters.agentshell.owner'


class OwnerStartupTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(
            prefix='owner-', dir=os.environ.get('TMPDIR'))
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.cwd = self.root / 'cwd'
        self.cwd.mkdir()
        self.home = self.root / 'home'
        self.home.mkdir()
        self.tmp = self.root / 'tmp'
        self.tmp.mkdir()
        self.controller_marker = self.root / 'controller-started'
        self.selected_python = self.root / 'selected-python'
        self.selected_python.write_text(
            f'#!{sys.executable}\n'
            'from pathlib import Path\n'
            f'Path({str(self.controller_marker)!r}).write_text("started\\n")\n'
            'raise SystemExit(97)\n')
        self.selected_python.chmod(0o700)
        self.environment = {
            'HOME': str(self.home),
            'LANG': 'C.UTF-8',
            'LC_ALL': 'C.UTF-8',
            'PATH': '/usr/bin:/bin',
            'PYTHONDONTWRITEBYTECODE': '1',
            'PYTHONPATH': str(ROOT / 'src'),
            'TMPDIR': str(self.tmp),
            'XDG_CACHE_HOME': str(self.root / 'cache'),
            'XDG_CONFIG_HOME': str(self.root / 'config'),
            'XDG_STATE_HOME': str(self.root / 'state'),
        }

    def _runtime(self, workspace):
        runtime = workspace / '.factory/runtime/foreman'
        runtime.mkdir(parents=True, mode=0o700)
        runtime.chmod(0o700)
        return runtime

    def _save_state(self, workspace, foreman):
        runtime = self._runtime(workspace)
        state = runtime / 'owner.json'
        state.write_text(json.dumps({
            'workspace': str(workspace),
            'run_id': 'previous-owner',
            'foreman': foreman,
            'watcher': 'stopped',
            'target': None,
        }) + '\n')
        state.chmod(0o600)
        return state

    def _receive_handover(self, channel):
        deadline = time.monotonic() + 10
        payload = bytearray()
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                self.fail('Owner handover did not close within ten seconds')
            channel.settimeout(remaining)
            chunk = channel.recv(4096)
            if not chunk:
                return bytes(payload)
            payload.extend(chunk)
            if len(payload) > 65536:
                self.fail('Owner handover exceeded one bounded frame')

    def _stop_process(self, process):
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3)

    def _run_owner(self, workspace):
        command = [
            sys.executable,
            '-s',
            '-m',
            OWNER_MODULE,
            str(workspace),
            str(self.selected_python),
        ]
        parent, child = socket.socketpair()
        with parent, child, tempfile.TemporaryFile() as log:
            process = subprocess.Popen(
                [*command, str(child.fileno())],
                pass_fds=(child.fileno(),),
                stdin=subprocess.DEVNULL,
                stdout=log,
                stderr=log,
                cwd=self.cwd,
                env=self.environment,
                start_new_session=True,
            )
            child.close()
            try:
                payload = self._receive_handover(parent)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.fail('Owner process did not exit within ten seconds')
                log.seek(0)
                output = log.read().decode(errors='replace')
                return process.returncode, payload, output
            finally:
                self._stop_process(process)

    def _assert_rejected(self, result, message):
        returncode, payload, output = result
        self.assertEqual(returncode, 0, output)
        self.assertEqual(len(payload.splitlines()), 1, payload)
        reply = json.loads(payload)
        self.assertEqual(set(reply), {'error'})
        self.assertIn(message, reply['error'])
        self.assertNotIn('Traceback', output)
        self.assertFalse(self.controller_marker.exists(), 'Controller unexpectedly launched')

    def _assert_lock_released(self, path):
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        try:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                self.fail('Owner lifetime lock remained held after process exit')
        finally:
            os.close(descriptor)

    def test_uncertain_previous_state_is_preserved_without_controller_launch(self):
        workspace = self.root / 'workspace'
        state = self._save_state(workspace, 'unknown')
        before = state.read_bytes()

        result = self._run_owner(workspace)

        self._assert_rejected(result, 'Previous Foreman state is uncertain')
        self.assertEqual(state.read_bytes(), before)
        self.assertFalse((state.parent / 'control.sock').exists())
        self._assert_lock_released(state.parent / 'owner.lock')

    def test_invalid_old_control_socket_is_preserved_without_controller_launch(self):
        workspace = self.root / 'workspace'
        state = self._save_state(workspace, 'stopped')
        state_before = state.read_bytes()
        endpoint = state.parent / 'control.sock'
        endpoint.write_bytes(b'preserve old endpoint\n')
        endpoint.chmod(0o600)
        identity = endpoint.stat().st_ino

        result = self._run_owner(workspace)

        self._assert_rejected(result, 'Invalid old Foreman socket; preserved for review')
        self.assertEqual(state.read_bytes(), state_before)
        self.assertEqual(endpoint.read_bytes(), b'preserve old endpoint\n')
        self.assertEqual(endpoint.stat().st_ino, identity)
        self._assert_lock_released(state.parent / 'owner.lock')

    def test_too_long_control_socket_path_is_rejected_without_replacement_authority(self):
        suffix = Path('.factory/runtime/foreman/control.sock')
        padding = max(1, 102 - len(os.fsencode(self.root / 'w' / suffix)))
        workspace = self.root / ('w' + 'x' * padding)
        runtime = self._runtime(workspace)
        preserved = runtime / 'preserve.txt'
        preserved.write_bytes(b'keep runtime evidence\n')
        endpoint = runtime / 'control.sock'
        self.assertGreater(len(os.fsencode(endpoint)), 100)

        result = self._run_owner(workspace)

        self._assert_rejected(result, 'Workspace path is too long')
        self.assertEqual(preserved.read_bytes(), b'keep runtime evidence\n')
        self.assertFalse((runtime / 'owner.json').exists())
        self.assertFalse(endpoint.exists())
        self._assert_lock_released(runtime / 'owner.lock')

    def test_nonregular_lock_descriptor_is_rejected_at_fstat_gate(self):
        workspace = self.root / 'workspace'
        runtime = self._runtime(workspace)
        lock = runtime / 'owner.lock'
        os.mkfifo(lock, 0o600)
        identity = lock.stat().st_ino
        keeper = os.open(lock, os.O_RDWR | os.O_NONBLOCK)
        try:
            result = self._run_owner(workspace)
        finally:
            os.close(keeper)

        self._assert_rejected(result, 'Foreman owner lock must be a regular file; preserved')
        try:
            unexpected_writer = os.open(lock, os.O_WRONLY | os.O_NONBLOCK)
        except OSError as error:
            self.assertEqual(error.errno, errno.ENXIO)
        else:
            os.close(unexpected_writer)
            self.fail('Owner retained the rejected FIFO lock descriptor')
        info = lock.stat()
        self.assertTrue(stat.S_ISFIFO(info.st_mode))
        self.assertEqual(info.st_ino, identity)
        self.assertFalse((runtime / 'owner.json').exists())
        self.assertFalse((runtime / 'control.sock').exists())

    def test_unsafe_runtime_directory_sends_controlled_handover_error(self):
        workspace = self.root / 'workspace'
        runtime = self._runtime(workspace)
        preserved = runtime / 'preserve.txt'
        preserved.write_bytes(b'keep private runtime evidence\n')
        runtime.chmod(0o755)

        result = self._run_owner(workspace)

        self._assert_rejected(result, 'Foreman runtime must be a private owned directory')
        self.assertEqual(stat.S_IMODE(runtime.stat().st_mode), 0o755)
        self.assertEqual(preserved.read_bytes(), b'keep private runtime evidence\n')
        self.assertFalse((runtime / 'owner.lock').exists())
        self.assertFalse((runtime / 'owner.json').exists())
        self.assertFalse((runtime / 'control.sock').exists())


if __name__ == '__main__':
    unittest.main()
