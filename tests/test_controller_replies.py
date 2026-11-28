"""The controller sends each text block the Foreman writes, only when the launch asks."""
import asyncio
import json
import unittest
from types import SimpleNamespace

from forgetful_factory.agents.adapters.agentshell import controller

DEADLINES = {'controller_ready': 5, 'controller_send': 5}


def event(kind, content='', error=None, session_id=None):
    return SimpleNamespace(type=kind, content=content, error=error, session_id=session_id)


TURN = [
    event('status', 'turn_started'),
    event('text', 'Let me look at the issue.'),
    event('tool_use', 'bash'),
    event('text', 'The plan is ready.'),
    event('text', 'Next I ask the owner.'),
    event('result', 'ok'),
]


class Session:
    """AgentShell keeps the read position between readers; only one reader at a time."""

    def __init__(self, events):
        self.queue = [event('system', session_id='pi-session'), *events]
        self.reading = False
        self.sent = []
        self.terminal = SimpleNamespace(send_text=self.send_text)

    async def send_text(self, text, *, submit=False):
        self.sent.append(text)

    async def events(self):
        if self.reading:
            raise RuntimeError('An interactive session permits only one event reader')
        self.reading = True
        try:
            while self.queue:
                yield self.queue.pop(0)
            await asyncio.Event().wait()
        finally:
            self.reading = False


async def converse(session, lines, *, replies):
    reader = asyncio.StreamReader()
    replied = []
    task = asyncio.create_task(controller.interact(
        session, reader, replied.append, 'factory-foreman-test', DEADLINES, replies=replies))
    for line in lines:
        reader.feed_data((json.dumps(line) + '\n').encode())
    await asyncio.sleep(0.05)
    reader.feed_eof()
    await asyncio.wait_for(task, 2)
    return replied


class ControllerReplyTests(unittest.TestCase):
    def test_each_text_block_is_sent_as_it_comes(self):
        # Act
        replied = asyncio.run(converse(Session(TURN), [], replies=True))
        # Assert: text between tool calls is sent too, so answers in the middle of a turn are
        # not lost.
        self.assertEqual(replied, [{'kind': 'ready'},
                                   {'kind': 'reply', 'text': 'Let me look at the issue.'},
                                   {'kind': 'reply', 'text': 'The plan is ready.'},
                                   {'kind': 'reply', 'text': 'Next I ask the owner.'}])

    def test_turn_without_text_posts_nothing_and_a_failed_turn_says_why(self):
        # Arrange
        events = [event('status', 'turn_started'), event('tool_use', 'bash'),
                  event('result', 'ok'), event('status', 'turn_started'),
                  event('result', 'error', error='model quota exceeded')]
        # Act
        replied = asyncio.run(converse(Session(events), [], replies=True))
        # Assert
        self.assertEqual(replied[1:], [{'kind': 'reply', 'text': '',
                                        'error': 'model quota exceeded'}])

    def test_sends_still_work_while_replies_are_read(self):
        # Arrange
        session = Session(TURN)
        # Act
        replied = asyncio.run(converse(session, [{'text': '[Discord] hello'}], replies=True))
        # Assert
        self.assertEqual(session.sent, ['[Discord] hello'])
        self.assertIn({'kind': 'sent'}, replied)
        self.assertEqual(sum(reply['kind'] == 'reply' for reply in replied), 3)

    def test_without_the_launch_flag_no_reply_is_sent(self):
        # The persistent Foreman's owner rejects unknown controller events.
        # Act
        replied = asyncio.run(converse(Session(TURN), [{'text': 'notice'}], replies=False))
        # Assert
        self.assertEqual(replied, [{'kind': 'ready'}, {'kind': 'sent'}])

    def test_a_failed_event_reader_is_reported_and_sends_continue(self):
        # Arrange
        session = Session([])

        async def broken():
            raise ValueError('Interactive event exceeds 8 MiB')
            yield  # pragma: no cover - makes this an async generator

        ready_events = session.events
        readers = iter((ready_events, broken))
        session.events = lambda: next(readers)()
        # Act
        replied = asyncio.run(converse(session, [{'text': 'notice'}], replies=True))
        # Assert
        problems = [reply for reply in replied if reply['kind'] == 'reply']
        self.assertEqual(len(problems), 1)
        self.assertIn('Interactive event exceeds 8 MiB', problems[0]['error'])
        self.assertIn({'kind': 'sent'}, replied)


if __name__ == '__main__':
    unittest.main()
