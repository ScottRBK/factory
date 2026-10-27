"""Observable rendezvous for a controlled GitHub response, without timed race windows."""
import select
import socket


class PollGate:
    def __init__(self, fixture, name):
        self.fixture = fixture
        self.path = fixture.workspace / f'{name}.sock'
        self.listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        fixture.addCleanup(self.listener.close)
        self.listener.bind(str(self.path))
        self.listener.listen(1)

    def reply(self, value):
        return {'gate': str(self.path), 'result': value}

    def wait(self, process):
        self.fixture.wait_until(process, lambda: select.select([self.listener], [], [], 0)[0])
        self.connection, _ = self.listener.accept()
        self.fixture.addCleanup(self.connection.close)

    def release(self):
        self.connection.sendall(b'1')
        self.connection.close()
