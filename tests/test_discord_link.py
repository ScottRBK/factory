"""watch's side of the Discord relay. The contract runs the real relay child with fake
discord.py; the other tests use small relay stand-ins to break it on purpose."""
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

from contracts.channels import ChatChannelContract
from fake_discord import BOT_ID

from forgetful_factory.channels.adapters.discord import relay
from forgetful_factory.channels.adapters.discord.link import DiscordLink
from forgetful_factory.channels.model import Delivery, DiscordSettings

ROOT = Path(__file__).resolve().parents[1]
CHANNEL = '123456789012345678'
USER = '234567890123456789'
SETTINGS = DiscordSettings(CHANNEL, (USER,))

STAND_IN = '''import json, os, socket, sys, time
record, behaviour = sys.argv[1], sys.argv[2]
connection = socket.socket(fileno=int(sys.argv[-1]))
reader = connection.makefile('rb')
start = json.loads(reader.readline())
with open(record, 'a') as file:
    file.write(json.dumps({'start': start, 'environment': dict(os.environ)}) + '\\n')
if behaviour == 'crash':
    sys.exit(3)
if behaviour in ('deaf', 'stuck'):
    time.sleep(30)
for line in reader:
    with open(record, 'a') as file:
        file.write(line.decode())
'''


def install_fake_discord(folder: Path, **settings) -> None:
    """Put fake discord.py where a relay child imports it, with its settings beside it."""
    package = folder / 'discord'
    package.mkdir(parents=True, exist_ok=True)
    shutil.copy(Path(__file__).with_name('fake_discord.py'), package / '__init__.py')
    (package / '_fixture.json').write_text(json.dumps(settings))


def read_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines()]


class Folder(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.env_file = self.folder / 'factory.env'


class DiscordLinkContractTests(Folder, ChatChannelContract):
    online_text = relay.ONLINE

    def setUp(self):
        super().setUp()
        self.log = self.folder / 'discord.jsonl'
        self.inbox = self.folder / 'inbox.jsonl'
        install_fake_discord(self.folder / 'external', log=str(self.log), inbox=str(self.inbox),
                             channel=CHANNEL)
        self.environment = {
            'PATH': os.environ['PATH'], 'DISCORD_BOT_TOKEN': 'fixture-token',
            'PYTHONPATH': os.pathsep.join((str(self.folder / 'external'), str(ROOT / 'src')))}

    def chat(self, warnings):
        return DiscordLink(SETTINGS, self.env_file, explicit_env_file=False, warn=warnings.append,
                           environment=self.environment)

    def broken_chat(self, warnings):
        install_fake_discord(self.folder / 'external', log=str(self.log), login='bad_token')
        return self.chat(warnings)

    def room(self):
        return [call['text'] for call in read_log(self.log) if call['kind'] == 'post']

    def say(self, text):
        with self.inbox.open('a') as inbox:
            inbox.write(json.dumps({'author': USER, 'content': f'<@{BOT_ID}> {text}',
                                    'mentions': [BOT_ID]}) + '\n')


class DiscordLinkTests(Folder):
    def stand_in(self, behaviour, warnings, **options):
        self.record = self.folder / 'relay.jsonl'
        script = self.folder / 'relay_stand_in.py'
        script.write_text(STAND_IN)
        return DiscordLink(SETTINGS, self.env_file, explicit_env_file=False,
                           warn=warnings.append,
                           command=[sys.executable, str(script), str(self.record), behaviour],
                           **options)

    def test_a_missing_token_names_the_places_checked_and_starts_nothing(self):
        # Arrange
        warnings = []
        link = self.stand_in('echo', warnings, environment={'PATH': os.environ['PATH']})
        # Act
        link.start()
        link.online()
        link.post('lost')
        self.assertEqual(link.receive(), [])
        link.close('done')
        # Assert
        self.assertEqual(len(warnings), 1)
        self.assertIn('DISCORD_BOT_TOKEN', warnings[0])
        self.assertIn(str(self.env_file), warnings[0])
        self.assertFalse(self.record.exists())

    def test_the_token_goes_over_the_socket_and_never_in_the_environment(self):
        # Arrange
        self.env_file.write_text('FACTORY_TOKEN=file-token\n')
        settings = DiscordSettings(CHANNEL, (USER,), 'FACTORY_TOKEN')
        warnings = []
        link = self.stand_in('echo', warnings, environment={
            'PATH': os.environ['PATH'], 'HOME': '/home/fixture', 'DISCORD_BOT_TOKEN': 'other',
            'FORGETFUL_TOKEN': 'unrelated', 'GH_TOKEN': 'unrelated'})
        link.settings = settings
        # Act
        link.start()
        link.post('hello')
        link.close('done')
        # Assert
        first, *lines = read_log(self.record)
        self.assertEqual(first['start'], {
            'kind': 'start', 'token': 'file-token', 'token_variable': 'FACTORY_TOKEN',
            'channel_id': CHANNEL, 'allowed_users': [USER]})
        self.assertEqual(set(first['environment']) - {'PWD', 'LC_CTYPE'}, {'PATH', 'HOME'})
        self.assertEqual(lines, [{'kind': 'post', 'text': 'hello'},
                                 {'kind': 'stopped', 'reason': 'done'}])
        self.assertEqual(warnings, [])

    def test_a_relay_that_crashes_gives_one_warning_and_watch_continues(self):
        # Arrange
        warnings = []
        link = self.stand_in('crash', warnings,
                             environment={'PATH': os.environ['PATH'], 'DISCORD_BOT_TOKEN': 't'})
        link.start()
        # Act
        deadline = time.monotonic() + 5
        while not warnings and time.monotonic() < deadline:
            link.receive()
            time.sleep(0.02)
        link.post('lost')
        link.mark('1', Delivery.SENT)
        link.close('done')
        # Assert
        self.assertEqual(len(warnings), 1)
        self.assertIn('ended unexpectedly', warnings[0])
        self.assertIn('3', warnings[0])

    def test_a_relay_that_stops_reading_is_dropped_without_blocking_watch(self):
        # Arrange
        warnings = []
        link = self.stand_in('deaf', warnings,
                             environment={'PATH': os.environ['PATH'], 'DISCORD_BOT_TOKEN': 't'})
        link.start()
        # Act
        started = time.monotonic()
        for _ in range(40):
            link.post('x' * 65536)
        link.close('done')
        # Assert
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(len(warnings), 1)
        self.assertIn('not keeping up', warnings[0])

    def test_a_relay_that_does_not_finish_is_stopped_after_the_close_wait(self):
        # Arrange
        warnings = []
        link = self.stand_in('stuck', warnings, close_wait=0.3,
                             environment={'PATH': os.environ['PATH'], 'DISCORD_BOT_TOKEN': 't'})
        link.start()
        # Act
        started = time.monotonic()
        link.close('done')
        # Assert
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(len(warnings), 1)
        self.assertIn('did not finish', warnings[0])


if __name__ == '__main__':
    unittest.main()
