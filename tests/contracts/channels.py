"""Promises every Channel and ChatChannel adapter keeps.

A new channel (for example Slack) is done when a subclass of ChannelContract passes for it, and
a new chat room when a subclass of ChatChannelContract passes.
"""
import io
import time
from contextlib import redirect_stdout
from unittest.mock import patch

from forgetful_factory.channels.model import Delivery


class ChannelContract:
    """Mix into unittest.TestCase. The subclass supplies the channel and one launched target."""

    target: dict

    def channel(self):
        raise NotImplementedError

    def test_how_to_reach_names_the_session(self):
        self.assertIn('factory-foreman-0123456789ab',
                      self.channel().how_to_reach('factory-foreman-0123456789ab'))

    def test_open_without_a_terminal_only_prints_how_to_reach(self):
        with redirect_stdout(io.StringIO()) as output, patch('sys.stdin', io.StringIO()):
            self.channel().open(self.target)
        self.assertTrue(output.getvalue().strip())


class ChatChannelContract:
    """Mix into unittest.TestCase. The subclass supplies a working chat, a broken chat, what the
    room shows, and a way to say something in the room.

    chat(warnings) and broken_chat(warnings) return a ChatChannel that appends its warnings to
    the list. room() returns the texts posted so far. say(text) posts as an allowed person.
    """

    online_text: str

    def chat(self, warnings):
        raise NotImplementedError

    def broken_chat(self, warnings):
        raise NotImplementedError

    def room(self) -> list[str]:
        raise NotImplementedError

    def say(self, text: str) -> None:
        raise NotImplementedError

    def wait_for(self, predicate, timeout=10):
        deadline = time.monotonic() + timeout
        while not predicate():
            if time.monotonic() > deadline:
                self.fail('Timed out waiting for the chat room.')
            time.sleep(0.02)

    def test_status_and_posts_reach_the_room_in_order(self):
        # Arrange
        warnings = []
        chat = self.chat(warnings)
        # Act
        chat.start()
        chat.online()
        chat.post('first')
        chat.post('second')
        chat.close('test finished')
        # Assert
        room = self.room()
        self.assertEqual(room[:3], [self.online_text, 'first', 'second'])
        self.assertIn('test finished', room[3])
        self.assertEqual(warnings, [])

    def test_receive_never_waits(self):
        # Arrange
        chat = self.chat([])
        chat.start()
        # Act
        started = time.monotonic()
        messages = chat.receive()
        # Assert
        self.assertEqual(messages, [])
        self.assertLess(time.monotonic() - started, 1)
        chat.close('test finished')

    def test_messages_arrive_and_can_be_marked(self):
        # Arrange
        chat = self.chat([])
        chat.start()
        chat.online()
        self.say('status please')
        received = []
        # Act
        self.wait_for(lambda: received.extend(chat.receive()) or received)
        chat.mark(received[0].id, Delivery.SENT)
        chat.close('test finished')
        # Assert
        self.assertEqual([message.text for message in received], ['status please'])

    def test_a_broken_chat_warns_and_never_raises(self):
        # Arrange
        warnings = []
        chat = self.broken_chat(warnings)
        # Act
        chat.start()
        chat.online()
        chat.post('lost')
        self.assertEqual(chat.receive(), [])
        chat.mark('1', Delivery.SENT)
        chat.close('test finished')
        # Assert
        self.assertTrue(warnings)
