"""The real discord.py has what the relay uses, in the shape the fake copies. A lock update that
changes this API fails here, not in a live run. Nothing here connects to Discord."""
import datetime
import inspect
import unittest

import discord
import fake_discord

from forgetful_factory.channels.adapters.discord import relay

# (real, fake, the parameters the relay passes)
CALLS = [
    (discord.Client.start, fake_discord.Client.start, ('token',)),
    (discord.Client.get_partial_messageable, fake_discord.Client.get_partial_messageable, ('id',)),
    (discord.PartialMessageable.send, fake_discord.PartialMessageable.send, ('content',)),
    (discord.PartialMessageable.history, fake_discord.PartialMessageable.history, ('limit',)),
    (discord.PartialMessageable.get_partial_message,
     fake_discord.PartialMessageable.get_partial_message, ('message_id',)),
    (discord.PartialMessage.add_reaction, fake_discord.PartialMessage.add_reaction, ('emoji',)),
]


class DiscordApiTests(unittest.TestCase):
    def test_the_audited_version_is_installed(self):
        self.assertEqual(discord.__version__, '2.7.1')

    def test_the_fake_takes_the_relays_arguments_as_the_real_library_does(self):
        for real, fake, used in CALLS:
            with self.subTest(call=real.__qualname__):
                real_parameters = inspect.signature(real).parameters
                fake_parameters = inspect.signature(fake).parameters
                for name in used:
                    self.assertEqual(real_parameters[name].kind, fake_parameters[name].kind)
                self.assertEqual(inspect.iscoroutinefunction(real) or inspect.isasyncgenfunction(
                    real), inspect.iscoroutinefunction(fake) or inspect.isasyncgenfunction(fake))

    def test_errors_the_relay_tells_apart(self):
        # The relay handles LoginFailure before network errors.
        for name in ('LoginFailure', 'HTTPException', 'Forbidden', 'GatewayNotFound'):
            with self.subTest(name):
                self.assertTrue(issubclass(getattr(discord, name), Exception))
        self.assertFalse(issubclass(discord.LoginFailure, discord.HTTPException))
        self.assertTrue(issubclass(discord.Forbidden, discord.HTTPException))

    def test_messages_have_what_the_relay_reads(self):
        for name in ('id', 'content', 'author', 'channel', 'mentions', 'mention_everyone',
                     'created_at'):
            with self.subTest(name):
                self.assertTrue(hasattr(discord.Message, name))
        for kind in (discord.User, discord.Member, discord.ClientUser):
            with self.subTest(kind.__name__):
                self.assertTrue(hasattr(kind, 'display_name'))
                self.assertTrue(hasattr(kind, 'bot'))

    def test_the_relay_client_builds_on_the_real_client(self):
        # Act
        client = relay.client_type(discord)(object(), intents=relay.intents(discord),
                                            allowed_mentions=discord.AllowedMentions.none())
        # Assert: server message events, and no privileged intent.
        self.assertTrue(client.intents.guilds and client.intents.guild_messages)
        self.assertFalse(any((client.intents.message_content, client.intents.members,
                              client.intents.presences)))
        mentions = client.allowed_mentions
        self.assertFalse(any((mentions.everyone, mentions.users, mentions.roles,
                              mentions.replied_user)))
        self.assertEqual(discord.utils.utcnow().tzinfo, datetime.timezone.utc)


if __name__ == '__main__':
    unittest.main()
