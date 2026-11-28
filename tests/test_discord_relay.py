"""The Discord relay child, run in-process with fake discord.py and a real socket pair."""
import asyncio
import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import fake_discord

from forgetful_factory.channels.adapters.discord import relay

CHANNEL = '123456789012345678'
USER = '234567890123456789'
OTHER = '345678901234567890'
BOT = str(fake_discord.BOT_ID)
START = {'kind': 'start', 'token': 'fixture-token', 'token_variable': 'DISCORD_BOT_TOKEN',
         'channel_id': CHANNEL, 'allowed_users': [USER]}


class Harness:
    """watch's end of the link."""

    def __init__(self, start=START):
        self.start = start

    async def __aenter__(self):
        parent, child = socket.socketpair()
        self.task = asyncio.create_task(relay.serve(child))
        self.reader, self.writer = await asyncio.open_connection(sock=parent)
        self.send(self.start)
        return self

    async def __aexit__(self, *exc):
        self.writer.close()
        await asyncio.wait_for(asyncio.shield(self.task), 5)

    def send(self, value):
        self.writer.write((json.dumps(value) + '\n').encode())

    async def read(self):
        line = await asyncio.wait_for(self.reader.readline(), 5)
        return json.loads(line) if line else None

    async def end(self):
        """Close watch's side and return the relay's exit status."""
        self.writer.write_eof()
        return await asyncio.wait_for(asyncio.shield(self.task), 5)


def to_bot(text, **fields):
    """A message from the allowed person that mentions the bot."""
    return {'author': USER, 'content': f'<@{BOT}> {text}', 'mentions': [BOT], **fields}


def posts():
    return [call['text'] for call in fake_discord.calls if call['kind'] == 'post']


async def until(predicate):
    for _ in range(200):
        if predicate():
            return
        await asyncio.sleep(0.01)
    raise AssertionError(f'Timed out; calls: {fake_discord.calls}')


class RelayTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.inbox = Path(temporary.name) / 'inbox.jsonl'
        fake_discord.reset(inbox=str(self.inbox), channel=CHANNEL)
        modules = patch.dict(sys.modules, {'discord': fake_discord})
        modules.start()
        self.addCleanup(modules.stop)

    def deliver(self, *messages):
        with self.inbox.open('a') as inbox:
            for message in messages:
                inbox.write(json.dumps(message) + '\n')

    def test_split_keeps_short_replies_and_splits_long_ones_at_line_breaks(self):
        # Arrange
        line = 'x' * 999
        # Act / Assert
        self.assertEqual(relay.split_reply('short'), ['short'])
        self.assertEqual(relay.split_reply('\n'.join([line] * 3)),
                         [line + '\n' + line, line])
        self.assertEqual(relay.split_reply('y' * 2001), ['y' * 2000, 'y'])

    def test_split_stops_after_five_parts(self):
        # Act
        parts = relay.split_reply('z' * 2000 * 7)
        # Assert
        self.assertEqual(parts, ['z' * 2000] * 5 + [relay.CUT_SHORT])
        self.assertTrue(all(len(part) <= 2000 for part in parts))

    def test_posts_wait_for_discord_keep_their_order_and_ping_nobody(self):
        async def scenario():
            async with Harness() as link:
                link.send({'kind': 'online'})
                link.send({'kind': 'post', 'text': '@everyone the plan is ready'})
                self.assertEqual(await link.read(), {'kind': 'ready'})
                await until(lambda: len(posts()) == 2)
                return await link.end()

        # Act
        status = asyncio.run(scenario())
        # Assert
        self.assertEqual(status, 0)
        login = fake_discord.calls[0]
        # No privileged intent: Discord gives the text of messages that mention the bot.
        self.assertEqual((login['token'], login['message_content'], login['guilds'],
                          login['guild_messages'], login['mentions_none']),
                         ('fixture-token', False, True, True, True))
        self.assertEqual(posts()[:2], [relay.ONLINE, '@everyone the plan is ready'])
        self.assertTrue(all(call['mentions_none'] for call in fake_discord.calls
                            if call['kind'] == 'post'))
        self.assertEqual(fake_discord.calls[-1]['kind'], 'close')

    def test_stop_reason_is_posted_before_the_relay_exits(self):
        async def scenario():
            async with Harness() as link:
                self.assertEqual(await link.read(), {'kind': 'ready'})
                link.send({'kind': 'stopped', 'reason': 'AgentShell: Pi exited with status 7.'})
                return await link.end()

        # Act
        status = asyncio.run(scenario())
        # Assert
        self.assertEqual(status, 0)
        self.assertEqual(posts(), ['🔴 Watch stopped: AgentShell: Pi exited with status 7.'])

    def test_a_link_that_ends_without_a_stop_reason_is_reported(self):
        async def scenario():
            async with Harness() as link:
                self.assertEqual(await link.read(), {'kind': 'ready'})
                return await link.end()

        # Act
        asyncio.run(scenario())
        # Assert
        self.assertEqual(posts(), [relay.LOST])

    def test_a_refused_token_is_a_final_problem_that_names_the_variable(self):
        # Arrange
        fake_discord.settings['login'] = 'bad_token'

        async def scenario():
            async with Harness() as link:
                problem = await link.read()
                return problem, await link.end()

        # Act
        problem, status = asyncio.run(scenario())
        # Assert
        self.assertEqual(status, 1)
        self.assertTrue(problem['fatal'])
        self.assertIn('DISCORD_BOT_TOKEN', problem['text'])
        self.assertNotIn('fixture-token', problem['text'])

    def test_no_network_is_reported_once_and_retried(self):
        # Arrange
        fake_discord.settings['login'] = 'no_network_once'

        async def scenario():
            with patch.object(relay, 'FIRST_RETRY', 0.01):
                async with Harness() as link:
                    problem = await link.read()
                    ready = await link.read()
                    await link.end()
                    return problem, ready

        # Act
        problem, ready = asyncio.run(scenario())
        # Assert
        self.assertIn('Cannot reach Discord', problem['text'])
        self.assertNotIn('fatal', problem)
        self.assertEqual(ready, {'kind': 'ready'})

    def test_without_discord_py_the_relay_gives_the_install_hint(self):
        async def scenario():
            with patch.dict(sys.modules, {'discord': None}):
                async with Harness() as link:
                    return await link.read(), await link.end()

        # Act
        problem, status = asyncio.run(scenario())
        # Assert
        self.assertEqual(status, 1)
        self.assertEqual(problem, {'kind': 'problem', 'text': relay.INSTALL_HINT, 'fatal': True})

    def test_only_allowed_people_who_mention_the_bot_reach_watch(self):
        # Ungated: the relay's own checks drop these, not only Discord's missing text.
        for ungated in (False, True):
            with self.subTest(ungated=ungated):
                # Arrange
                self.inbox.unlink(missing_ok=True)
                fake_discord.reset(inbox=str(self.inbox), channel=CHANNEL, ungated=ungated)
                self.deliver(
                    to_bot('not allowed', id='1', author=OTHER),
                    to_bot('a bot', id='2', bot=True),
                    to_bot('elsewhere', id='3', channel='999999999999999999'),
                    to_bot('  ', id='4', attachments=1),
                    {'id': '5', 'author': USER, 'content': 'no mention'},
                    {'id': '6', 'author': USER, 'content': '@everyone hi', 'everyone': True},
                    {'id': '7', 'author': USER, 'content': f'<@{OTHER}> hi', 'mentions': [OTHER]},
                    {'id': '8', 'author': USER, 'name': 'Scott', 'mentions': [BOT],
                     'content': f'status <@!{BOT}> please', 'attachments': 1},
                )

                async def scenario():
                    async with Harness() as link:
                        self.assertEqual(await link.read(), {'kind': 'ready'})
                        message = await link.read()
                        link.send({'kind': 'mark', 'id': message['id'], 'delivery': 'sent'})
                        await until(lambda: any(call['kind'] == 'react'
                                                for call in fake_discord.calls))
                        link.send({'kind': 'stopped', 'reason': 'Ctrl-C'})
                        await link.end()
                        return message

                # Act
                message = asyncio.run(scenario())
                # Assert: the mention is taken out and the display name goes with the text.
                self.assertEqual(message, {'kind': 'message', 'id': '8', 'author': 'Scott',
                                           'text': 'status please'})
                reactions = [(call['id'], call['emoji']) for call in fake_discord.calls
                             if call['kind'] == 'react']
                self.assertEqual(reactions, [('8', '✅')])

    def test_messages_that_watch_did_not_send_are_marked_not_ready(self):
        # Arrange
        self.deliver(to_bot('are you there?', id='7'))

        async def scenario():
            async with Harness() as link:
                self.assertEqual(await link.read(), {'kind': 'ready'})
                self.assertEqual((await link.read())['id'], '7')
                link.send({'kind': 'stopped', 'reason': 'Ctrl-C'})
                await asyncio.sleep(0.05)
                self.deliver(to_bot('hello?', id='8'))
                await until(lambda: sum(call['kind'] == 'react'
                                        for call in fake_discord.calls) == 2)
                await link.end()

        # Act
        asyncio.run(scenario())
        # Assert
        reactions = {(call['id'], call['emoji']) for call in fake_discord.calls
                     if call['kind'] == 'react'}
        self.assertEqual(reactions, {('7', '💤'), ('8', '💤')})

    def test_messages_since_the_last_stop_are_counted_once_connected(self):
        # Arrange: newest first, as Discord returns history.
        fake_discord.settings['history'] = [
            to_bot('anyone?', age=10),
            {'author': USER, 'content': 'not to the bot', 'age': 15},
            to_bot('not allowed', author=OTHER, age=20),
            to_bot('', attachments=1, age=30),
            {'author': fake_discord.BOT_ID, 'bot': True, 'content': '🔴 Watch stopped: x',
             'age': 40},
            to_bot('before the stop', age=50),
        ]

        async def scenario():
            async with Harness() as link:
                link.send({'kind': 'online'})
                await until(lambda: len(posts()) == 2)
                await link.end()

        # Act
        asyncio.run(scenario())
        # Assert
        self.assertEqual(posts()[:2], [
            '📭 2 messages came while watch was off. They were not sent to the Foreman.',
            relay.ONLINE])

    def test_no_count_without_an_earlier_stop_or_with_unreadable_history(self):
        for setting in ({'history': [{'author': USER, 'content': 'hi', 'age': 5}]},
                        {'history_fails': True}):
            with self.subTest(setting=setting):
                # Arrange
                fake_discord.reset(inbox=str(self.inbox), channel=CHANNEL, **setting)

                async def scenario():
                    async with Harness() as link:
                        self.assertEqual(await link.read(), {'kind': 'ready'})
                        link.send({'kind': 'online'})
                        await until(lambda: posts())
                        await link.end()

                # Act
                asyncio.run(scenario())
                # Assert
                self.assertEqual(posts()[0], relay.ONLINE)

    def test_failed_posts_are_reported_once_and_the_relay_continues(self):
        # Arrange
        fake_discord.settings['send_fails'] = True

        async def scenario():
            async with Harness() as link:
                self.assertEqual(await link.read(), {'kind': 'ready'})
                link.send({'kind': 'post', 'text': 'one'})
                link.send({'kind': 'post', 'text': 'two'})
                problem = await link.read()
                link.send({'kind': 'stopped', 'reason': 'Ctrl-C'})
                return problem, await link.end()

        # Act
        problem, status = asyncio.run(scenario())
        # Assert
        self.assertEqual(status, 0)
        self.assertIn('Discord did not accept a post', problem['text'])


if __name__ == '__main__':
    unittest.main()
