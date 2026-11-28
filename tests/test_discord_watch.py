"""Plain watch with Discord: fake AgentShell and fake discord.py, the real relay child.

The Foreman's replies and watch's status reach the channel, allowed people reach the Foreman,
and no Discord problem stops watch or the tmux terminal.
"""
import json
import os
import signal
import time

from fake_discord import BOT_ID
from test_discord_link import install_fake_discord, read_log
from test_watch import WatchFixture

from forgetful_factory.channels.adapters.discord import relay

CHANNEL = '123456789012345678'
USER = '234567890123456789'
TURN = [{'type': 'status', 'content': 'turn_started'},
        {'type': 'text', 'content': 'Let me read the issue.'},
        {'type': 'tool_use', 'content': 'bash'},
        {'type': 'text', 'content': 'The plan is ready.'},
        {'type': 'result', 'content': 'ok'}]


class DiscordWatchTests(WatchFixture):
    def setUp(self):
        super().setUp()
        self.external = self.workspace / 'external'
        self.discord_log = self.workspace / 'discord.jsonl'
        self.inbox = self.workspace / 'inbox.jsonl'
        self.fake_discord()
        for name in [name for name in self.env if 'DISCORD' in name]:
            del self.env[name]
        self.env['DISCORD_BOT_TOKEN'] = 'fixture-token'
        # Never the person's own default secrets file.
        self.add_discord(env_file='secrets/factory.env')

    def fake_discord(self, **settings):
        install_fake_discord(self.external, log=str(self.discord_log), inbox=str(self.inbox),
                             channel=CHANNEL, **settings)

    def add_discord(self, env_file, token_variable=None):
        path = self.workspace / '.factory/factory.toml'
        variable = f'token_variable = "{token_variable}"\n' if token_variable else ''
        path.write_text(f'env_file = "{env_file}"\n' + path.read_text() +
                        f'\n[discord]\nchannel_id = "{CHANNEL}"\nallowed_users = ["{USER}"]\n'
                        + variable)

    def discord(self, kind):
        return [call for call in read_log(self.discord_log) if call['kind'] == kind]

    def posts(self):
        return [call['text'] for call in self.discord('post')]

    def launch(self):
        return next(event for event in self.events() if event['kind'] == 'launch')

    def test_status_and_replies_reach_discord_and_the_token_stays_out_of_pi(self):
        # Arrange
        self.env['WATCH_PI_EVENTS'] = json.dumps(TURN)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: 'The plan is ready.' in self.posts())
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertEqual(self.posts(), [
            relay.ONLINE, 'Let me read the issue.', 'The plan is ready.',
            '🔴 Watch stopped: Watch was stopped with Ctrl-C or a stop signal.'])
        self.assertEqual([login['token'] for login in self.discord('login')], ['fixture-token'])
        self.assertEqual(self.launch()['discord_variables'], [])
        self.assertNotIn('Warning', stderr)

    def test_a_named_token_comes_from_the_env_file(self):
        # Arrange: DISCORD_BOT_TOKEN is still exported; only the named variable counts.
        self.configure()
        self.add_discord('secrets/factory.env', 'TEAM_DISCORD_TOKEN')
        (self.workspace / 'secrets').mkdir()
        (self.workspace / 'secrets/factory.env').write_text('TEAM_DISCORD_TOKEN="file-token"\n')
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: relay.ONLINE in self.posts())
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertEqual([login['token'] for login in self.discord('login')], ['file-token'])
        self.assertEqual(self.launch()['discord_variables'], [])

    def test_allowed_people_reach_the_foreman_and_see_its_answer(self):
        # Arrange
        self.env['WATCH_PI_ECHO'] = '1'
        self.inbox.write_text(json.dumps({'id': '42', 'author': USER, 'name': 'Scott',
                                          'content': f'<@{BOT_ID}> status please',
                                          'mentions': [BOT_ID]}) + '\n')
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: 'Echo: [Discord] Scott: status please' in self.posts())
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        sends = [event['text'] for event in self.events() if event['kind'] == 'send']
        self.assertEqual(sends, ['[Discord] Scott: status please'])
        self.assertEqual([(call['id'], call['emoji']) for call in self.discord('react')],
                         [('42', '✅')])

    def test_no_discord_problem_stops_watch_or_the_foreman(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        cases = {
            'bad token': ({'login': 'bad_token'}, 'refused the bot token in DISCORD_BOT_TOKEN'),
            'relay crash': ({'login': 'crash'}, 'relay failed: RuntimeError'),
            'relay exits later': ({'login': 'exit'}, 'ended unexpectedly'),
            'no network': ({'login': 'no_network'}, 'Cannot reach Discord'),
            'no token': ({}, 'DISCORD_BOT_TOKEN was not found in the environment or in'),
            'no discord.py': ({}, 'discord.py is not installed'),
        }
        for name, (settings, warning) in cases.items():
            with self.subTest(name):
                self.terminal_log.unlink(missing_ok=True)
                self.fake_discord(**settings)
                if name == 'no token':
                    del self.env['DISCORD_BOT_TOKEN']
                if name == 'no discord.py':
                    (self.external / 'discord/__init__.py').write_text(
                        "raise ImportError('No module named discord')\n")
                # Act
                process = self.start('--existing')
                self.wait_until(process, lambda: any(
                    event['kind'] == 'send' for event in self.events()), timeout=10)
                # Watch reads relay problems at least once a second while it waits.
                time.sleep(1.5)
                code, stdout, stderr = self.stop(process)
                self.env['DISCORD_BOT_TOKEN'] = 'fixture-token'
                # Assert
                self.assertEqual(code, 130, stderr)
                self.assertIn('Submitted github:team/app#1', stdout)
                self.assertIn(warning, stderr)
                self.assertNotIn('fixture-token', stderr)

    def test_a_killed_watch_is_reported_by_the_relay(self):
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: relay.ONLINE in self.posts())
        os.kill(process.pid, signal.SIGKILL)
        process.wait()
        deadline = time.monotonic() + 10
        while relay.LOST not in self.posts() and time.monotonic() < deadline:
            time.sleep(0.05)
        # Assert
        self.assertEqual(self.posts(), [relay.ONLINE, relay.LOST])

