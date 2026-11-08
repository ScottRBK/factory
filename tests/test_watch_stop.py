"""One real stop signal at actual native-finalizer and ordinary-call timing boundaries."""
import json
import os
import signal
import socket
import struct
import subprocess

from test_watch import WatchFixture
from test_watch_status import read_status

TIMING_SHIM = '''
import json, os, socket, subprocess, sys
from pathlib import Path
if (sys.argv[:2] == ['-m', 'watch'] and os.getenv('WATCH_STOP_GATE')
        and not any(a in sys.argv for a in ('--status', '--start', '--stop'))):
    mode = os.environ['WATCH_STOP_MODE']
    code = subprocess.Popen.__del__.__code__ if mode == 'finalizer' else subprocess.run.__code__
    fired = False
    def checkpoint(frame, event, arg):
        global fired
        if fired or event != 'call' or frame.f_code is not code:
            return
        child = frame.f_locals.get('self')
        if mode == 'finalizer' and (child is None or child.returncode is None):
            return
        if (child is not None and os.getenv('WATCH_STOP_NATIVE') and
                Path(child.args[0]).name != os.environ['WATCH_STOP_NATIVE']):
            return
        log = Path(os.environ['WATCH_TERMINAL_LOG'])
        if (not os.getenv('WATCH_STOP_STARTUP') and
                (not log.exists() or '"kind": "ready"' not in log.read_text())):
            return
        fired = True
        with socket.socket(socket.AF_UNIX) as gate:
            gate.connect(os.environ['WATCH_STOP_GATE'])
            gate.sendall((json.dumps({'pid': os.getpid(), 'mode': mode,
                         'returncode': child.returncode if child is not None else None})
                          + '\\n').encode())
            gate.recv(1)
    sys.setprofile(checkpoint)
'''


class WatchStopTests(WatchFixture):
    def stop_at_native_boundary(self, mode, sig, native='git', startup=False):
        # Arrange: instrumentation changes timing only; Popen, handlers and signals are real.
        shim = self.workspace / 'timing-shim'
        shim.mkdir()
        (shim / 'sitecustomize.py').write_text(TIMING_SHIM)
        listener = socket.socket(socket.AF_UNIX)
        self.addCleanup(listener.close)
        path = str(self.workspace / 'stop-checkpoint.sock')
        listener.bind(path)
        listener.listen()
        listener.settimeout(12)
        self.env.update(WATCH_STOP_GATE=path, WATCH_STOP_MODE=mode, WATCH_STOP_NATIVE=native,
                        WATCH_STOP_STARTUP='1' if startup else '',
                        PYTHONPATH=str(shim) + os.pathsep + self.env['PYTHONPATH'])
        self.script({'team/app': [[[self.issue()]]]})
        process = self.start('--existing')
        with listener.accept()[0] as gate:
            gate.settimeout(5)
            pid, uid, _ = struct.unpack('3i', gate.getsockopt(socket.SOL_SOCKET,
                                                            socket.SO_PEERCRED, 12))
            self.assertEqual((pid, uid), (process.pid, os.getuid()))
            packet = json.loads(gate.makefile('rb').readline())
            self.assertEqual(packet['pid'], process.pid)
            if mode == 'finalizer':
                self.assertEqual(packet['returncode'], 0)
            before = read_status(self)
            self.assertEqual(before['observation'], 'live')
            self.assertEqual(before['foreman'], 'unknown' if startup else 'ready')
            # Act: exactly one stop signal to the owned watcher, no rescue signal.
            process.send_signal(sig)
            self.assertEqual(gate.recv(1), b'')
        try:
            stdout, stderr = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            self.fail('The single stop signal was lost at the native timing boundary')
        # Assert: no later issue delivery, owned Foreman closes, status remains historical.
        self.assertEqual(process.returncode, 130, stdout + stderr)
        self.assertEqual([e['kind'] for e in self.events()],
                         [] if startup else ['launch', 'ready', 'close'])
        after = read_status(self)
        self.assertEqual(after['observation'], 'saved')
        self.assertEqual(after['recorded_phase'], 'stopped')
        self.assertEqual(after['recorded_evidence'],
                         'exited_before_session' if startup else 'watcher_cleanup_finished')
        self.assertNotEqual(after['foreman'], 'ready')
        self.assertEqual(before['run_id'], after['run_id'])
        if mode == 'finalizer':
            self.assertIn('Exception ignored in:', stderr)  # CPython diagnostic is not suppressed.
        else:
            self.assertNotIn('Exception ignored in:', stderr)

    def test_one_sigint_at_completed_popen_finalizer_still_closes_owned_foreman(self):
        self.stop_at_native_boundary('finalizer', signal.SIGINT)

    def test_one_sigterm_at_completed_popen_finalizer_retains_exit_130_contract(self):
        self.stop_at_native_boundary('finalizer', signal.SIGTERM)

    def test_one_sigint_at_ordinary_native_call_retains_prompt_cancellation(self):
        self.stop_at_native_boundary('ordinary', signal.SIGINT)

    def test_one_sigterm_at_ordinary_native_call_retains_prompt_cancellation(self):
        self.stop_at_native_boundary('ordinary', signal.SIGTERM)

    def test_one_sigint_at_completed_forgetful_helper_finalizer_stops_before_later_work(self):
        self.stop_at_native_boundary('finalizer', signal.SIGINT, native='forgetful')

    def test_one_sigterm_at_completed_forgetful_helper_finalizer_stops_before_later_work(self):
        self.stop_at_native_boundary('finalizer', signal.SIGTERM, native='forgetful')

    def test_one_sigint_during_startup_finalizer_does_not_launch_a_foreman(self):
        self.stop_at_native_boundary('finalizer', signal.SIGINT, native='gh', startup=True)

    def test_one_sigterm_during_startup_finalizer_retains_cancellation_and_saved_status(self):
        self.stop_at_native_boundary('finalizer', signal.SIGTERM, native='gh', startup=True)
