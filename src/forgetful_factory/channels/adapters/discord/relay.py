"""The Discord relay: a child process of watch. It is the only process that holds the bot token
and the only module that imports discord.py.

It talks to watch with JSON lines over one inherited socket. The first line from watch is
`start` (token, token variable, channel ID and allowed users). Then watch sends `online`,
`post`, `mark` and `stopped`; the relay sends `ready`, `problem` and `message`. A problem never
stops watch: it prints a warning. When the socket closes, the relay posts its last messages
and exits.

Only messages that mention the bot reach watch. Discord gives the text of those messages
without the privileged Message Content intent, so the bot asks for none.
"""
import asyncio
import contextlib
import json
import re
import socket
import sys
from functools import partial

LIMIT = 2000  # Discord's limit for one message, in characters.
PARTS = 5
CUT_SHORT = 'Reply cut short; see the Foreman terminal.'
ONLINE = '🟢 Foreman is ready. Watch is running.'
LOST = ('🔴 Watch ended without a stop message; it may have been killed. '
        'Check the Factory machine.')
MISSED = '📭 {count} came while watch was off. They were not sent to the Foreman.'
MARKS = {'sent': '✅', 'uncertain': '⚠️', 'not_ready': '💤'}
INSTALL_HINT = ('Discord is off: discord.py is not installed. Install Factory with its discord '
                'extra; see "Discord" in docs/configuration.md. Watch continues without '
                'Discord.')
FIRST_RETRY = 5.0  # seconds; doubles up to LAST_RETRY while Discord cannot be reached
LAST_RETRY = 300.0
DRAIN = 8.0  # seconds to post the last messages after watch ends
HISTORY = 100  # messages searched for the last stop post


def split_reply(text: str) -> list[str]:
    """Split at line breaks into parts Discord accepts. After five parts, say where the rest is."""
    parts = []
    while text:
        if len(text) <= LIMIT:
            parts.append(text)
            break
        cut = text.rfind('\n', 0, LIMIT + 1)
        if cut <= 0:
            cut = LIMIT
        parts.append(text[:cut])
        text = text[cut:].removeprefix('\n')
    if len(parts) > PARTS:
        parts = parts[:PARTS] + [CUT_SHORT]
    return parts


def intents(discord):
    """Server and message events only; no privileged intent."""
    value = discord.Intents.none()
    value.guilds = True
    value.guild_messages = True
    return value


def client_type(discord):
    class RelayClient(discord.Client):
        def __init__(self, relay, **options):
            super().__init__(**options)
            self.relay = relay

        async def on_ready(self):
            await self.relay.connected(self)

        async def on_message(self, message):
            await self.relay.received(message)

    return RelayClient


class Relay:
    def __init__(self, discord, reader, writer, start: dict):
        self.discord = discord
        self.reader, self.writer = reader, writer
        self.token = start['token']
        self.variable = start['token_variable']
        self.channel_id = int(start['channel_id'])
        self.allowed = {int(user) for user in start['allowed_users']}
        self.client = None
        self.channel = None
        self.ready = asyncio.Event()
        self.ready_at = None
        self.outbox: asyncio.Queue = asyncio.Queue()
        self.stopped = False
        self.unmarked: set[int] = set()
        self.reported: set[str] = set()

    def tell(self, value: dict) -> None:
        if not self.writer.is_closing():
            self.writer.write((json.dumps(value) + '\n').encode())

    def problem(self, text: str, *, key: str | None = None, fatal: bool = False) -> None:
        """Tell watch once for each kind of problem."""
        key = key or text
        if key not in self.reported or fatal:
            self.reported.add(key)
            self.tell({'kind': 'problem', 'text': text, **({'fatal': True} if fatal else {})})

    async def run(self) -> int:
        connecting = asyncio.create_task(self.connect())
        listening = asyncio.create_task(self.listen())
        posting = asyncio.create_task(self.post())
        try:
            done, _ = await asyncio.wait((connecting, listening),
                                         return_when=asyncio.FIRST_COMPLETED)
            if connecting in done:
                return 1  # Only a final problem ends the connection loop.
            if not self.stopped:
                self.outbox.put_nowait(partial(self.send, LOST))
                self.stop()
            if self.ready.is_set():
                with contextlib.suppress(TimeoutError):
                    await asyncio.wait_for(self.outbox.join(), DRAIN)
            return 0
        finally:
            for task in (connecting, listening, posting):
                task.cancel()
            if self.client is not None:
                with contextlib.suppress(Exception):
                    await self.client.close()
            await asyncio.gather(connecting, listening, posting, return_exceptions=True)

    async def connect(self) -> None:
        discord = self.discord
        delay = FIRST_RETRY
        while True:
            self.client = client_type(discord)(
                self, intents=intents(discord), allowed_mentions=discord.AllowedMentions.none())
            try:
                await self.client.start(self.token)
                return
            except discord.LoginFailure:
                self.problem(f'Discord refused the bot token in {self.variable}. Discord is off; '
                             'watch continues.', fatal=True)
                return
            except (OSError, TimeoutError, discord.HTTPException,
                    discord.GatewayNotFound) as error:
                self.problem(f'Cannot reach Discord ({error}); the relay keeps trying. '
                             'Watch continues.', key='network')
                await asyncio.sleep(delay)
                delay = min(delay * 2, LAST_RETRY)
            except Exception as error:
                self.problem(f'Discord relay failed: {type(error).__name__}: {error}. Discord '
                             'is off; watch continues.', fatal=True)
                return
            finally:
                with contextlib.suppress(Exception):
                    await self.client.close()

    async def connected(self, client) -> None:
        self.channel = client.get_partial_messageable(self.channel_id)
        if not self.ready.is_set():
            self.ready_at = self.discord.utils.utcnow()
            self.tell({'kind': 'ready'})
            self.ready.set()

    async def listen(self) -> None:
        while line := await self.reader.readline():
            try:
                value = json.loads(line)
                kind = value['kind']
                if kind == 'online':
                    self.outbox.put_nowait(partial(self.send, ONLINE))
                elif kind == 'post':
                    self.outbox.put_nowait(partial(self.send, value['text']))
                elif kind == 'stopped':
                    self.outbox.put_nowait(partial(
                        self.send, f'🔴 Watch stopped: {value["reason"]}'))
                    self.stop()
                elif kind == 'mark':
                    message_id = int(value['id'])
                    self.unmarked.discard(message_id)
                    self.outbox.put_nowait(partial(
                        self.react, message_id, MARKS[value['delivery']]))
            except (ValueError, KeyError, TypeError) as error:
                self.problem(f'Discord relay ignored an invalid request: {error}.', key='request')

    def stop(self) -> None:
        """Watch sends nothing more to the Foreman: open messages were not sent."""
        self.stopped = True
        for message_id in sorted(self.unmarked):
            self.outbox.put_nowait(partial(self.react, message_id, MARKS['not_ready']))
        self.unmarked.clear()

    def addressed(self, message) -> bool:
        """An allowed person mentions the bot. @everyone does not count."""
        return (not message.author.bot and message.author.id in self.allowed
                and any(user.id == self.client.user.id for user in message.mentions))

    async def received(self, message) -> None:
        if message.channel.id != self.channel_id or not self.addressed(message):
            return
        text = re.sub(rf'\s*<@!?{self.client.user.id}>\s*', ' ', message.content).strip()
        if not text:
            return
        if self.stopped:
            self.outbox.put_nowait(partial(self.react, message.id, MARKS['not_ready']))
            return
        self.unmarked.add(message.id)
        self.tell({'kind': 'message', 'id': str(message.id),
                   'author': message.author.display_name, 'text': text})

    async def post(self) -> None:
        await self.ready.wait()
        await self.count_missed()
        while True:
            action = await self.outbox.get()
            try:
                await action()
            except self.discord.HTTPException as error:
                self.problem(f'Discord did not accept a post or reaction: {error}. Check '
                             "discord.channel_id and the bot's permissions in that channel.",
                             key='post')
            except Exception as error:
                self.problem(f'Discord post failed: {type(error).__name__}: {error}.',
                             key='post')
            finally:
                self.outbox.task_done()

    async def send(self, text: str) -> None:
        for part in split_reply(text):
            await self.channel.send(part)

    async def react(self, message_id: int, emoji: str) -> None:
        await self.channel.get_partial_message(message_id).add_reaction(emoji)

    async def count_missed(self) -> None:
        """Count messages to the bot after its last stop post: watch did not see them."""
        count = 0
        try:
            async for message in self.channel.history(limit=HISTORY):
                if message.created_at >= self.ready_at:
                    continue
                if message.author.id == self.client.user.id:
                    if message.content.startswith('🔴'):
                        break
                elif self.addressed(message):
                    count += 1
            else:
                return  # No stop post to count from.
        except self.discord.HTTPException as error:
            self.problem(f'Cannot read the Discord channel history ({error}); missed messages '
                         'are not counted.', key='history')
            return
        if count:
            await self.send(MISSED.format(count=f'{count} message{"s" * (count != 1)}'))


async def serve(connection: socket.socket) -> int:
    reader, writer = await asyncio.open_connection(sock=connection)
    try:
        start = json.loads(await reader.readline())
        try:
            import discord
        except ImportError:
            writer.write((json.dumps({'kind': 'problem', 'text': INSTALL_HINT, 'fatal': True})
                          + '\n').encode())
            return 1
        return await Relay(discord, reader, writer, start).run()
    finally:
        writer.close()
        with contextlib.suppress(Exception):
            await writer.wait_closed()


def main(argv: list[str]) -> int:
    return asyncio.run(serve(socket.socket(fileno=int(argv[0]))))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
