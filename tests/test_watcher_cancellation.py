"""Cancel native checks through watch CLI, retaining only live-validated fixture handles."""
import array
import json
import os
import selectors
import signal
import socket
import struct
import sys

from lifecycle_support import pidfd_send_signal
from test_watch import ROOT, WatchFixture


class WatcherCancellationTests(WatchFixture):
    def assert_cancelled_check_exits(self, *, stubborn):
        # Arrange: the external check transfers its own live pidfd before cancelling its caller.
        address = self.workspace / 'check.sock'
        listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.addCleanup(listener.close)
        listener.bind(str(address))
        listener.listen(1)
        listener.settimeout(5)
        term_log = self.workspace / 'term.txt'
        program = self.bin / 'forgetful'
        program.write_text(
            f'#!{sys.executable}\n'
            'import array, json, os, signal, socket, sys\n'
            'from pathlib import Path\n'
            f'sys.path.insert(0, {str(ROOT / "tests")!r})\n'
            'from lifecycle_support import pidfd_open, pidfd_send_signal\n'
            'parent = pidfd_open(os.getppid())\n'
            'descriptor = pidfd_open(os.getpid())\n'
            'def terminate(signum, frame):\n'
            f'    Path({str(term_log)!r}).write_text("TERM received")\n'
            f'    if not {stubborn!r}: sys.exit(0)\n'
            'signal.signal(signal.SIGTERM, terminate)\n'
            'with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:\n'
            f'    channel.connect({str(address)!r})\n'
            '    channel.sendmsg([json.dumps({"pid": os.getpid()}).encode()],\n'
            '                    [(socket.SOL_SOCKET, socket.SCM_RIGHTS,\n'
            '                      array.array("i", [descriptor]))])\n'
            '    assert channel.recv(1) == b"K"\n'
            'os.close(descriptor)\n'
            'pidfd_send_signal(parent, signal.SIGINT)\n'
            'os.close(parent)\n'
            'while True: signal.pause()\n')
        process = self.start('--new-only')
        connection, _ = listener.accept()
        with connection:
            connection.settimeout(5)
            credentials = connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12)
            peer_pid, peer_uid, _ = struct.unpack('3i', credentials)
            data, controls, flags, _ = connection.recvmsg(1024, socket.CMSG_SPACE(4))
            self.assertFalse(flags & socket.MSG_CTRUNC)
            descriptors = array.array('i')
            for level, kind, payload in controls:
                if level == socket.SOL_SOCKET and kind == socket.SCM_RIGHTS:
                    descriptors.frombytes(payload)
            self.assertEqual(len(descriptors), 1)
            descriptor = descriptors[0]
            try:
                self.assertEqual(peer_uid, os.getuid())
                self.assertEqual(peer_pid, json.loads(data)['pid'])
                with open(f'/proc/self/fdinfo/{descriptor}') as stream:
                    identity = dict(line.split(':', 1) for line in stream if ':' in line)
                self.assertEqual(int(identity['Pid']), peer_pid)
                self.assertEqual(os.readlink(f'/proc/self/fd/{descriptor}'), 'anon_inode:[pidfd]')
            except BaseException:
                os.close(descriptor)
                raise
            self.addCleanup(self.close_owned_check, descriptor)
            # Act: release only this verified check to interrupt its original watcher parent.
            connection.sendall(b'K')
        output, errors = process.communicate(timeout=12)
        code = process.returncode
        # Assert: cancellation closes the owned Foreman and reaps this exact native check.
        self.assertEqual(code, 130, errors)
        self.assertNotIn('Traceback', errors)
        self.assertNotIn('Submitted', output)
        self.assertEqual([event['kind'] for event in self.events()], ['launch', 'ready', 'close'])
        self.assertEqual(term_log.read_text(), 'TERM received')
        with selectors.DefaultSelector() as selector:
            selector.register(descriptor, selectors.EVENT_READ)
            self.assertTrue(selector.select(1), 'Native check survived watcher cancellation')
        self.assertFalse((self.workspace / '.factory/fixture-plans.json').exists())

    @staticmethod
    def close_owned_check(descriptor):
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(descriptor, selectors.EVENT_READ)
                if not selector.select(0):
                    pidfd_send_signal(descriptor, signal.SIGKILL)
                    if not selector.select(5):
                        raise AssertionError('Owned native fixture survived cleanup')
        finally:
            os.close(descriptor)

    def test_cancelled_native_check_exits_without_losing_keyboard_interrupt(self):
        self.assert_cancelled_check_exits(stubborn=False)

    def test_cancelled_native_check_keeps_bounded_escalation_for_stubborn_process(self):
        self.assert_cancelled_check_exits(stubborn=True)
