"""Chat channels: messages from a chat room, delivery marks and the Discord settings."""
import re
from dataclasses import dataclass
from enum import Enum

from forgetful_factory.shared.errors import FactoryError

DEFAULT_TOKEN_VARIABLE = 'DISCORD_BOT_TOKEN'
_ID = re.compile(r'\d{17,20}', re.ASCII)
_VARIABLE = re.compile(r'[A-Za-z_]\w*', re.ASCII)


class Delivery(Enum):
    """What happened to a chat message sent to the Foreman."""

    SENT = 'sent'
    UNCERTAIN = 'uncertain'
    NOT_READY = 'not_ready'


@dataclass(frozen=True)
class ChatMessage:
    id: str
    author: str  # the name people see in the chat, for the Foreman
    text: str


@dataclass(frozen=True)
class DiscordSettings:
    """One channel per factory. The token is read by name; it is never a setting."""

    channel_id: str
    allowed_users: tuple[str, ...]
    token_variable: str = DEFAULT_TOKEN_VARIABLE


def discord_from_mapping(data: object) -> DiscordSettings:
    if not isinstance(data, dict):
        raise FactoryError('discord must be a table: put the settings under [discord].')
    unknown = sorted(set(data) - {'channel_id', 'allowed_users', 'token_variable'})
    if unknown:
        raise FactoryError(f'Unknown [discord] settings: {", ".join(unknown)}. Allowed: '
                           'channel_id, allowed_users and token_variable. Keep the bot token '
                           'in the environment or the env_file.')
    channel = data.get('channel_id')
    if not isinstance(channel, str) or not _ID.fullmatch(channel):
        raise FactoryError('discord.channel_id must be a Discord channel ID in quotes, '
                           'for example "123456789012345678".')
    users = data.get('allowed_users')
    if (not isinstance(users, list) or not users
            or any(not isinstance(user, str) or not _ID.fullmatch(user) for user in users)):
        raise FactoryError('discord.allowed_users must list at least one Discord user ID in '
                           'quotes, for example ["234567890123456789"].')
    variable = data.get('token_variable', DEFAULT_TOKEN_VARIABLE)
    if not isinstance(variable, str) or not _VARIABLE.fullmatch(variable):
        raise FactoryError('discord.token_variable must be an environment variable name: '
                           'letters, digits and _, not starting with a digit.')
    return DiscordSettings(channel, tuple(dict.fromkeys(users)), variable)


def secret_names(settings: DiscordSettings | None) -> tuple[str, ...]:
    """Environment variables that hold chat secrets; agents must never receive them."""
    names = [DEFAULT_TOKEN_VARIABLE]
    if settings is not None and settings.token_variable not in names:
        names.append(settings.token_variable)
    return tuple(names)
