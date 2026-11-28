"""A stand-in for the parts of discord.py 2.7.1 that the relay uses. It records each call.

Names and signatures follow discord.py 2.7.1 (client.py, channel.py, message.py, flags.py,
mentions.py, errors.py). In-process tests call reset(); a child process reads _fixture.json
beside this file, where tests write the settings and the log path.

Settings:
- login: None, 'bad_token', 'no_network', 'no_network_once', 'crash' or 'exit'.
- inbox: a file of JSON messages that the fake delivers to on_message, in order.
- history: messages newest first, for channel.history().
- send_fails: every send raises Forbidden.
- ungated: give message text without the Message Content intent. Discord does not; this lets a
  test prove the relay's own checks.

A message is {'author': id, 'content': text} with optional 'id', 'name' (display name),
'mentions' (user IDs), 'everyone', 'bot', 'channel', 'attachments' and 'age' (seconds).
Like Discord, the fake blanks the text of a message that neither mentions the bot nor comes from
it, unless the client has the Message Content intent.
"""
import asyncio
import datetime
import itertools
import json
import os
from pathlib import Path
from types import SimpleNamespace

FIXTURE = Path(__file__).with_name('_fixture.json')
BOT_ID = 555555555555555555
settings: dict = {}
calls: list[dict] = []
_ids = itertools.count(900000000000000001)
_attempts = itertools.count()


def reset(**values) -> None:
    global _attempts
    settings.clear()
    settings.update(values)
    calls.clear()
    _attempts = itertools.count()


if FIXTURE.exists():
    reset(**json.loads(FIXTURE.read_text()))


def record(kind: str, **fields) -> None:
    entry = {'kind': kind, **fields}
    calls.append(entry)
    if settings.get('log'):
        with open(settings['log'], 'a', encoding='utf-8') as log:
            log.write(json.dumps(entry) + '\n')


class DiscordException(Exception):
    pass


class ClientException(DiscordException):
    pass


class LoginFailure(ClientException):
    pass


class GatewayNotFound(DiscordException):
    pass


class HTTPException(DiscordException):
    def __init__(self, response, message):
        self.response = response
        self.status = getattr(response, 'status', 0)
        self.text = message
        super().__init__(f'{self.status} {message}')


class Forbidden(HTTPException):
    pass


class Intents:
    FLAGS = ('guilds', 'members', 'moderation', 'guild_messages', 'dm_messages',
             'message_content', 'presences')

    def __init__(self, **flags):
        for name in self.FLAGS:
            setattr(self, name, False)
        for name, value in flags.items():
            if name not in self.FLAGS:
                raise TypeError(f'{name!r} is not a valid flag name.')
            setattr(self, name, value)

    @classmethod
    def none(cls):
        return cls()


class AllowedMentions:
    def __init__(self, *, everyone=True, users=True, roles=True, replied_user=True):
        self.everyone, self.users = everyone, users
        self.roles, self.replied_user = roles, replied_user

    @classmethod
    def none(cls):
        return cls(everyone=False, users=False, roles=False, replied_user=False)


def _utcnow():
    return datetime.datetime.now(datetime.timezone.utc)


utils = SimpleNamespace(utcnow=_utcnow)


def _message(data: dict, channel_id: int, intents=None):
    created = _utcnow() - datetime.timedelta(seconds=data.get('age', 0))
    author = int(data['author'])
    mentions = [int(user) for user in data.get('mentions', [])]
    content = data.get('content', '')
    if (intents is not None and not intents.message_content and not settings.get('ungated')
            and author != BOT_ID and BOT_ID not in mentions):
        content = ''
    return SimpleNamespace(
        id=int(data.get('id', next(_ids))), content=content,
        author=SimpleNamespace(id=author, bot=data.get('bot', False),
                               display_name=data.get('name', f'Person {author}')),
        channel=SimpleNamespace(id=int(data.get('channel', channel_id))),
        mentions=[SimpleNamespace(id=user) for user in mentions],
        mention_everyone=data.get('everyone', False),
        attachments=[object()] * data.get('attachments', 0), created_at=created)


class PartialMessage:
    def __init__(self, *, channel, id):
        self.channel, self.id = channel, id

    async def add_reaction(self, emoji, /):
        record('react', id=str(self.id), emoji=emoji)


class PartialMessageable:
    def __init__(self, client, id):
        self.client, self.id = client, id

    async def send(self, content=None, *, allowed_mentions=None, **options):
        if settings.get('send_fails'):
            raise Forbidden(SimpleNamespace(status=403), 'Missing Access')
        mentions = allowed_mentions or self.client.allowed_mentions
        record('post', channel=str(self.id), text=content,
               mentions_none=mentions is not None and not any(
                   (mentions.everyone, mentions.users, mentions.roles, mentions.replied_user)))
        return _message({'author': BOT_ID, 'content': content}, self.id)

    def get_partial_message(self, message_id, /):
        return PartialMessage(channel=self, id=message_id)

    async def history(self, *, limit=100, before=None, after=None, around=None,
                      oldest_first=None):
        record('history', limit=limit)
        if settings.get('history_fails'):
            raise Forbidden(SimpleNamespace(status=403), 'Missing Access')
        for data in settings.get('history', [])[:limit]:
            yield _message(data, self.id, self.client.intents)


class Client:
    def __init__(self, *, intents, allowed_mentions=None, **options):
        self.intents = intents
        self.allowed_mentions = allowed_mentions
        self.user = SimpleNamespace(id=BOT_ID, bot=True)
        self._closed = False
        self._stop = asyncio.Event()
        self._ready = asyncio.Event()

    async def start(self, token, *, reconnect=True):
        attempt = next(_attempts)
        login = settings.get('login')
        record('login', token=token, message_content=self.intents.message_content,
               guild_messages=self.intents.guild_messages, guilds=self.intents.guilds,
               mentions_none=self.allowed_mentions is not None
               and not self.allowed_mentions.users and not self.allowed_mentions.everyone)
        if login == 'bad_token':
            raise LoginFailure('Improper token has been passed.')
        if login == 'no_network' or (login == 'no_network_once' and attempt == 0):
            raise OSError(101, 'Cannot connect to host discord.com:443')
        if login == 'crash':
            raise RuntimeError('relay fixture crash')
        self._ready.set()
        await self.on_ready()
        if login == 'exit':
            os._exit(3)
        inbox = settings.get('inbox')
        seen = 0
        while not self._stop.is_set():
            lines = Path(inbox).read_text().splitlines() if inbox and Path(inbox).exists() else []
            for line in lines[seen:]:
                seen += 1
                await self.on_message(_message(json.loads(line), int(settings['channel']),
                                               self.intents))
            try:
                await asyncio.wait_for(self._stop.wait(), 0.05)
            except TimeoutError:
                pass

    async def on_ready(self):
        pass

    async def on_message(self, message):
        pass

    async def close(self):
        record('close')
        self._closed = True
        self._stop.set()

    def is_closed(self):
        return self._closed

    def is_ready(self):
        return self._ready.is_set()

    async def wait_until_ready(self):
        await self._ready.wait()

    def get_partial_messageable(self, id, *, guild_id=None, type=None):
        return PartialMessageable(self, id)
