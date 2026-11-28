"""ChatRelay: the rules between the Foreman terminal and a chat room, with fakes for both."""
import unittest

from forgetful_factory.agents.model import ForemanReply
from forgetful_factory.channels.model import ChatMessage, Delivery
from forgetful_factory.factory.services.chat_relay import ChatRelay
from forgetful_factory.shared.errors import FactoryError


class Clock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


class Terminal:
    def __init__(self, clock, replies=(), send_error=None):
        self.clock = clock
        self.replies = list(replies)
        self.send_error = send_error
        self.waits = []
        self.sent = []

    def wait(self, interval):
        self.waits.append(interval)
        self.clock.now += interval
        replies, self.replies = self.replies, []
        return replies

    def send(self, message):
        if self.send_error is not None:
            raise self.send_error
        self.sent.append(message)


class Chat:
    name = 'Discord'

    def __init__(self, inbox=()):
        self.inbox = list(inbox)
        self.calls = []

    def start(self):
        self.calls.append(('start',))

    def online(self):
        self.calls.append(('online',))

    def post(self, text):
        self.calls.append(('post', text))

    def receive(self):
        messages, self.inbox = self.inbox, []
        return messages

    def mark(self, message_id, delivery):
        self.calls.append(('mark', message_id, delivery))

    def close(self, reason):
        self.calls.append(('close', reason))


class ChatRelayTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()

    def test_without_a_chat_watch_waits_as_before(self):
        # Arrange
        terminal = Terminal(self.clock)
        relay = ChatRelay(terminal, None, clock=self.clock)
        # Act
        relay.start()
        relay.online()
        relay.wait(30)
        relay.stop(KeyboardInterrupt())
        # Assert
        self.assertEqual(terminal.waits, [30])

    def test_start_and_online_reach_the_chat(self):
        # Arrange
        chat = Chat()
        relay = ChatRelay(Terminal(self.clock), chat, clock=self.clock)
        # Act
        relay.start()
        relay.online()
        # Assert
        self.assertEqual(chat.calls, [('start',), ('online',)])

    def test_wait_checks_the_chat_every_tick_and_posts_foreman_replies(self):
        # Arrange
        terminal = Terminal(self.clock, [ForemanReply('The plan is ready.'),
                                         ForemanReply('', 'model quota exceeded'),
                                         ForemanReply('Partial answer', 'turn failed')])
        chat = Chat()
        relay = ChatRelay(terminal, chat, tick=1.0, clock=self.clock)
        # Act
        relay.wait(2.5)
        # Assert
        self.assertEqual(terminal.waits, [1.0, 1.0, 0.5])
        self.assertEqual(chat.calls, [('post', 'The plan is ready.'),
                                      ('post', '⚠️ model quota exceeded'),
                                      ('post', 'Partial answer'), ('post', '⚠️ turn failed')])

    def test_chat_messages_reach_the_foreman_and_are_marked_sent(self):
        # Arrange
        terminal = Terminal(self.clock)
        chat = Chat([ChatMessage('11', 'Scott', 'status please'),
                     ChatMessage('12', 'Dave', 'thanks')])
        relay = ChatRelay(terminal, chat, clock=self.clock)
        # Act
        relay.wait(1)
        # Assert
        self.assertEqual(terminal.sent, ['[Discord] Scott: status please',
                                         '[Discord] Dave: thanks'])
        self.assertEqual(chat.calls, [('mark', '11', Delivery.SENT),
                                      ('mark', '12', Delivery.SENT)])

    def test_a_failed_send_is_marked_uncertain_and_still_stops_watch(self):
        # Arrange
        error = FactoryError('Pi send response timed out; submission is uncertain.')
        chat = Chat([ChatMessage('11', '22', 'status please')])
        relay = ChatRelay(Terminal(self.clock, send_error=error), chat, clock=self.clock)
        # Act / Assert
        with self.assertRaises(FactoryError):
            relay.wait(1)
        self.assertEqual(chat.calls, [('mark', '11', Delivery.UNCERTAIN)])

    def test_stop_gives_the_reason_that_watch_prints(self):
        # Arrange
        cases = [
            (KeyboardInterrupt(), 'Watch was stopped with Ctrl-C or a stop signal.'),
            (FactoryError('AgentShell: Pi exited with status 7; watcher stopped.'),
             'AgentShell: Pi exited with status 7; watcher stopped.'),
            (RuntimeError('boom'), 'Watch stopped after an unexpected error: RuntimeError: boom'),
            (None, 'Watch stopped.'),
        ]
        for error, reason in cases:
            with self.subTest(reason=reason):
                chat = Chat()
                # Act
                ChatRelay(Terminal(self.clock), chat, clock=self.clock).stop(error)
                # Assert
                self.assertEqual(chat.calls, [('close', reason)])


if __name__ == '__main__':
    unittest.main()
