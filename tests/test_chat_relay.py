"""ChatRelay: the rules between the Foreman terminal and a chat room, with fakes for both.

With a chat, a thread moves messages and replies all the time, also while watch polls.
"""
import threading
import time
import unittest
from unittest.mock import patch

from forgetful_factory.agents.model import ForemanReply
from forgetful_factory.channels.model import ChatMessage, Delivery
from forgetful_factory.factory.services import chat_relay
from forgetful_factory.factory.services.chat_relay import ChatRelay
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.watch_stop import check_watch_stop, watch_stop_scope


class Terminal:
    """Records calls and finds calls from two threads at the same time."""

    def __init__(self, replies=(), send_error=None, held=None):
        self.replies = list(replies)
        self.send_error = send_error
        # When set, each send waits here, as a slow Pi send does; `sending` says it began.
        self.held = held
        self.sending = threading.Event()
        self.attempts = 0
        self.waits = []
        self.sent = []
        self.active = 0
        self.overlaps = 0

    def _use(self):
        self.active += 1
        if self.active > 1:
            self.overlaps += 1
        time.sleep(0.001)
        self.active -= 1

    def wait(self, interval):
        check_watch_stop()  # as the AgentShell terminal does
        self._use()
        self.waits.append(interval)
        replies, self.replies = self.replies, []
        return replies

    def send(self, message):
        self._use()
        self.attempts += 1
        self.sending.set()
        if self.held is not None:
            self.held.wait(5)
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


def until(predicate, timeout=2):
    deadline = time.monotonic() + timeout
    while not predicate():
        if time.monotonic() > deadline:
            raise AssertionError('Timed out')
        time.sleep(0.005)


class ChatRelayTests(unittest.TestCase):
    def running(self, terminal, chat, interval=0.01):
        """A relay whose chat thread runs until the test ends."""
        relay = ChatRelay(terminal, chat, interval=interval)
        relay.start()
        relay.online()
        self.addCleanup(relay.halt)
        return relay

    def test_without_a_chat_watch_waits_as_before(self):
        # Arrange
        terminal = Terminal()
        relay = ChatRelay(terminal, None)
        # Act
        relay.start()
        relay.online()
        relay.wait(30)
        relay.halt()
        relay.stop(KeyboardInterrupt())
        # Assert
        self.assertEqual(terminal.waits, [30])
        self.assertIsNone(relay.thread)

    def test_start_and_online_reach_the_chat(self):
        # Arrange
        chat = Chat()
        # Act
        self.running(Terminal(), chat)
        # Assert
        self.assertEqual(chat.calls, [('start',), ('online',)])

    def test_replies_are_posted_while_watch_is_busy(self):
        # Arrange
        terminal = Terminal([ForemanReply('The plan is ready.'),
                             ForemanReply('', 'model quota exceeded'),
                             ForemanReply('Partial answer', 'turn failed')])
        chat = Chat()
        # Act: watch never calls wait here, as during a long poll.
        self.running(terminal, chat)
        until(lambda: len(chat.calls) == 6)
        # Assert
        self.assertEqual(chat.calls[2:], [('post', 'The plan is ready.'),
                                          ('post', '⚠️ model quota exceeded'),
                                          ('post', 'Partial answer'), ('post', '⚠️ turn failed')])

    def test_chat_messages_reach_the_foreman_while_watch_is_busy(self):
        # Arrange
        terminal = Terminal()
        chat = Chat([ChatMessage('11', 'Scott', 'status please'),
                     ChatMessage('12', 'Dave', 'thanks')])
        # Act
        self.running(terminal, chat)
        until(lambda: len(chat.calls) == 4)
        # Assert
        self.assertEqual(terminal.sent, ['[Discord] Scott: status please',
                                         '[Discord] Dave: thanks'])
        self.assertEqual(chat.calls[2:], [('mark', '11', Delivery.SENT),
                                          ('mark', '12', Delivery.SENT)])

    def test_the_thread_holds_the_terminal_only_for_a_short_read(self):
        # Arrange: a long chat interval must not make watch's own sends wait.
        terminal = Terminal()
        relay = self.running(terminal, Chat(), interval=60)
        until(lambda: terminal.waits)
        # Act
        began = time.monotonic()
        relay.foreman.send('New issue: team/app#1')
        relay.halt()
        # Assert
        self.assertLess(time.monotonic() - began, 1)
        self.assertEqual(terminal.waits, [chat_relay.READ])
        self.assertEqual(terminal.sent, ['New issue: team/app#1'])

    def test_watch_and_the_chat_thread_never_use_the_terminal_at_once(self):
        # Arrange
        terminal = Terminal()
        chat = Chat([ChatMessage(str(number), 'Scott', 'hello') for number in range(20)])
        relay = self.running(terminal, chat, interval=0)
        # Act
        for number in range(20):
            relay.foreman.send(f'notice {number}')
        until(lambda: len(terminal.sent) == 40)
        # Assert
        self.assertEqual(terminal.overlaps, 0)

    def test_a_failed_send_is_marked_uncertain_and_stops_watch(self):
        # Arrange
        error = FactoryError('Pi send response timed out; submission is uncertain.')
        chat = Chat([ChatMessage('11', 'Scott', 'status please')])
        relay = self.running(Terminal(send_error=error), chat)
        # Act / Assert: watch stops at its next wait, not after the whole interval.
        began = time.monotonic()
        with self.assertRaises(FactoryError):
            relay.wait(30)
        self.assertLess(time.monotonic() - began, 5)
        self.assertEqual(chat.calls[2:], [('mark', '11', Delivery.UNCERTAIN)])
        # Watch sends nothing more to the Foreman after the failure.
        with self.assertRaises(FactoryError):
            relay.foreman.send('New issue: team/app#1')

    def test_a_watch_send_waiting_behind_a_failed_chat_send_is_not_made(self):
        # Arrange: the chat send holds the terminal, and watch's notice waits for it.
        held = threading.Event()
        error = FactoryError('Pi send response timed out; submission is uncertain.')
        terminal = Terminal(send_error=error, held=held)
        relay = self.running(terminal, Chat([ChatMessage('11', 'Scott', 'status please')]))
        self.assertTrue(terminal.sending.wait(2))
        outcome = []

        def notify():
            try:
                relay.foreman.send('New issue: team/app#1')
            except FactoryError as problem:
                outcome.append(problem)

        notice = threading.Thread(target=notify)
        notice.start()
        time.sleep(0.05)
        # Act
        held.set()
        notice.join(2)
        # Assert: only the chat send reached the terminal; the notice was refused.
        self.assertEqual(outcome, [error])
        self.assertEqual(terminal.attempts, 1)

    def test_after_a_failed_watch_send_the_chat_thread_sends_nothing(self):
        # Arrange
        error = FactoryError('AgentShell input closed; Pi delivery failed.')
        terminal = Terminal(send_error=error)
        chat = Chat()
        relay = self.running(terminal, chat)
        with self.assertRaises(FactoryError):
            relay.foreman.send('New issue: team/app#1')
        # Act
        chat.inbox.append(ChatMessage('11', 'Scott', 'status please'))
        time.sleep(0.1)
        relay.halt()
        # Assert: the message stays unmarked, so the relay marks it 💤 when watch stops.
        self.assertEqual(chat.calls, [('start',), ('online',)])
        self.assertEqual(terminal.attempts, 1)

    def test_halt_takes_no_new_message_and_waits_for_the_send_in_progress(self):
        # Arrange
        held = threading.Event()
        terminal = Terminal(held=held)
        chat = Chat([ChatMessage(str(number), 'Scott', 'hello') for number in range(3)])
        relay = self.running(terminal, chat)
        self.assertTrue(terminal.sending.wait(2))
        halting = threading.Thread(target=relay.halt)
        # Act
        halting.start()
        time.sleep(0.05)
        self.assertTrue(halting.is_alive())
        held.set()
        halting.join(2)
        # Assert: only the send in progress finished; nothing is used after halt.
        self.assertFalse(relay.thread.is_alive())
        self.assertEqual(len(terminal.sent), 1)
        self.assertEqual(chat.calls[2:], [('mark', '0', Delivery.SENT)])

    def test_a_very_long_watch_interval_still_stops_on_a_failure(self):
        # Arrange: threading waits refuse timeouts above threading.TIMEOUT_MAX.
        error = FactoryError('Pi send response timed out; submission is uncertain.')
        relay = self.running(Terminal(send_error=error),
                             Chat([ChatMessage('11', 'Scott', 'status please')]))
        # Act / Assert
        with self.assertRaises(FactoryError):
            relay.wait(1e12)

    def test_a_waiting_watch_send_goes_after_at_most_one_chat_send(self):
        # Arrange: a burst of chat messages, the first send held, and a notice waiting.
        held = threading.Event()
        terminal = Terminal(held=held)
        chat = Chat([ChatMessage(str(number), 'Scott', 'hello') for number in range(20)])
        relay = self.running(terminal, chat, interval=0)
        self.assertTrue(terminal.sending.wait(2))
        notice = threading.Thread(target=relay.foreman.send, args=('New issue: team/app#1',))
        notice.start()
        time.sleep(0.05)
        # Act
        held.set()
        notice.join(2)
        until(lambda: len(terminal.sent) == 21)
        # Assert
        self.assertEqual(terminal.sent.index('New issue: team/app#1'), 1)

    def test_a_failure_is_raised_even_when_the_wait_is_too_short_to_sleep(self):
        # Arrange
        error = FactoryError('Pi send response timed out; submission is uncertain.')
        relay = self.running(Terminal(send_error=error),
                             Chat([ChatMessage('11', 'Scott', 'status please')]))
        until(lambda: relay.failure is not None)
        # Act / Assert
        with self.assertRaises(FactoryError):
            relay.wait(0)

    def test_a_second_ctrl_c_does_not_cut_halt_short(self):
        # Arrange: the first join is interrupted, as by a second Ctrl-C.
        terminal = Terminal()
        relay = self.running(terminal, Chat())
        until(lambda: terminal.waits)
        join = relay.thread.join
        interrupted = []

        def interrupted_once(*arguments):
            if not interrupted:
                interrupted.append(True)
                raise KeyboardInterrupt
            return join(*arguments)

        relay.thread.join = interrupted_once
        # Act
        relay.halt()
        # Assert
        self.assertEqual(interrupted, [True])
        self.assertFalse(relay.thread.is_alive())

    def test_a_thread_that_cannot_start_does_not_hide_the_error(self):
        # Arrange
        relay = ChatRelay(Terminal(), Chat())
        refused = RuntimeError("can't start new thread")
        # Act / Assert
        with patch.object(threading.Thread, 'start', side_effect=refused):
            with self.assertRaises(RuntimeError) as raised:
                relay.online()
        relay.halt()
        self.assertIs(raised.exception, refused)

    def test_ctrl_c_also_stops_the_chat_thread(self):
        # Arrange
        terminal = Terminal()
        with watch_stop_scope() as stop:
            relay = self.running(terminal, Chat())
            until(lambda: terminal.waits)
            # Act: the signal handler sets this, then raises in the main thread only.
            stop.requested = True
            # Assert
            with self.assertRaises(KeyboardInterrupt):
                relay.wait(30)

    def test_halt_ends_the_thread_before_watch_closes_the_terminal(self):
        # Arrange
        terminal = Terminal()
        relay = self.running(terminal, Chat())
        until(lambda: terminal.waits)
        # Act
        relay.halt()
        calls = len(terminal.waits)
        time.sleep(0.05)
        # Assert
        self.assertFalse(relay.thread.is_alive())
        self.assertEqual(len(terminal.waits), calls)

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
                ChatRelay(Terminal(), chat).stop(error)
                # Assert
                self.assertEqual(chat.calls, [('close', reason)])


if __name__ == '__main__':
    unittest.main()
