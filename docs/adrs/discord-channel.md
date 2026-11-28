# Discord channel to the Foreman

## Status

Implemented on 2026-11-27 (slices 1 to 3), with fake Discord and fake AgentShell in tests. Scott
agreed the shape on 2026-11-27. The first live run on 2026-11-28 led to three changes: every text
block is posted, the bot reads only messages that mention it, and the Foreman sees who wrote. The
rest of the live check is still to do. The [work plan](../plans/discord-channel.md) holds the
slices, the audit and the validation.

## Context

Today a person reaches the Foreman only through its tmux terminal (`channels/ports.py`). On
2026-11-26 a plain `watch` run stopped while nobody was at the machine, and nothing told Scott.
A Discord channel lets a person read the Foreman's replies, see when the factory starts and stops,
and later answer the Foreman from a phone.

## Decisions

### 1. Plain watch first

The relay runs with plain `watch`, the "start it and leave it" way, where nobody is usually at
the terminal. Between GitHub polls, `watch` already waits on the controller's output
(`agents/adapters/agentshell/terminal.py`). The relay link is one more thing that wait listens to.

The persistent Foreman is not in scope. Its owner rejects unknown controller events, so the new
`reply` event is sent only when the launch asks for it. The persistent Foreman is unchanged. A
managed watcher with `[discord]` prints a warning that Discord works with plain watch only.

`ChatRelay` (`factory/services/chat_relay.py`) holds the rules. While watch waits, it checks the
chat at least once a second; during a GitHub poll, messages wait in the socket.

### 2. The relay is a separate child process

`watch` starts a Discord relay child and talks to it with JSON lines over a socket pair.

- The relay is the only process that holds the bot token and the only one that imports
  discord.py. `watch` sends the token over the socket in the first line, so the token is never in
  the relay's environment. The relay gets only what Python, TLS and proxies need.
- The relay runs in its own session, so Ctrl-C in the watch terminal does not stop it before it
  posts the stop reason. `watch` waits up to 10 seconds for it, then stops it.
- A Discord problem never stops `watch` or the Foreman. This covers a missing extra, a missing or
  bad token, no network and a relay crash, at startup or later. `watch` prints a warning and
  continues without Discord. The tmux terminal works as it does today.
- Only an invalid `factory.toml` stops `watch`, as for every other setting.
- If `watch` ends without saying goodbye (for example after an out-of-memory kill), the relay
  sees its socket close, posts "watch ended unexpectedly" and exits.

### 3. discord.py as an optional extra

The relay uses discord.py through an optional `discord` extra, pinned in `uv.lock`. A supply-chain
audit of discord.py and its dependencies comes before it is added. A factory without `[discord]`
installs and runs exactly as today. A factory with `[discord]` and without the extra runs without
Discord, and `watch` prints a warning that says how to install it.

An import rule, like `agentshell-in-agents`, allows only `channels/adapters/discord/` to import
`discord`.

### 4. One server, one channel per factory

The settings name one channel. One bot can serve all factories, or each factory can have its own
bot. Direct messages are not used.

### 5. Settings and secrets

Settings that are not secret go in `.factory/factory.toml`:

```toml
env_file = "~/.config/forgetful-factory/.env"   # optional; this is the default

[discord]
channel_id = "123456789012345678"
allowed_users = ["234567890123456789"]
token_variable = "DARK_BUSINESS_DISCORD_TOKEN"  # optional; default DISCORD_BOT_TOKEN
```

- `env_file` is a top-level setting because it is the factory's secrets file, not a Discord
  setting. A later secret can use the same file.
- `~` is expanded. A relative path is relative to the workspace folder.
- Factory reads the token by name: first the environment, then `env_file`. The environment wins,
  as in Forgetful (`app/config/settings.py`).
- The reader takes `KEY=value` lines. It ignores blank lines and `#` comments, accepts an
  `export ` prefix and removes one pair of matching quotes. It does not expand variables. It
  never copies values into `os.environ`.
- When the token is not found, the warning names the variable and both places that were checked.
  When the settings name an `env_file` that does not exist, the warning also says so. The file is
  read only when the environment does not have the token.
- `role_environment` removes the configured token variable from the Foreman's environment, as it
  removes `FORGETFUL_TOKEN` today. Pi and its agents never receive it.

Why not pydantic-settings, which Forgetful uses: it adds about seven packages for one secret.
Revisit when Factory has several secrets.

Older Factory builds refuse a `factory.toml` that has these keys, because unknown settings are an
error (`factory/model/configuration.py`).

### 6. What is posted

- 🟢 when the Foreman is ready. 🔴 when `watch` stops, with the reason that `watch` prints.
- Each text block that the Foreman writes, as it comes (AgentShell's `text` events). Tool calls
  and thinking are not posted. Turns that started from the terminal or from a watcher
  notification are posted too.
- Text between tool calls is posted too. In the first live run, the Foreman answered Discord
  messages in the middle of a busy turn. More tool calls followed, so posting only the text after
  the last tool call lost those answers.
- A turn that fails posts "⚠️" and the error, so a model or quota problem is not silent. If the
  controller cannot read AgentShell events, it posts "⚠️ Foreman replies stopped" once; sends
  continue.
- A text block over 2000 characters is split at line breaks. After five parts, the relay posts
  "Reply cut short; see the Foreman terminal."
- Posts never ping anyone: the client sets allowed mentions to none.
- A post or reaction that Discord refuses gives one warning in `watch`, with a hint to check
  `channel_id` and the bot's permissions.

### 7. What is accepted (slice 2)

- Only messages in the configured channel, from a user ID in `allowed_users`, that mention the
  bot. `@everyone`, `@here` and role mentions do not count. Messages from bots, edits, deletes
  and attachments are ignored.
- Each message reaches the Foreman as `[Discord] <display name>: <text>`, without the mention,
  through the controller's existing send. Messages that come while the Foreman starts wait until
  it is ready.
- Reactions show the result: ✅ sent, ⚠️ delivery uncertain, 💤 not sent because watch was
  stopping. A failed send still stops `watch`, as for an issue notification.
- The bot asks for no privileged intent. Discord gives the text of messages that mention the bot
  without the Message Content intent (discord.py `Intents.message_content`).
- Messages are never replayed later. This follows "reconcile, don't auto-replay". When the relay
  connects, it counts allowed people's messages to the bot after its last 🔴 post (in the last 100
  messages)
  and posts "📭 N messages came while watch was off. They were not sent to the Foreman."

## Security

- **Same power as the terminal:** a Discord message can do what typing in the Foreman terminal
  can do, and implementation workers run with `auto_approve=true`. Keep the allowlist short and
  use two-factor sign-in on the Discord accounts.
- **Stored by Discord:** Foreman replies can include code and issue details. Discord keeps them on
  its servers.
- **No privileged intent:** the bot reads only messages that mention it. Discord sends their text
  without the Message Content intent; other messages in the channel reach the bot without text.
- **Token files:** a token file inside the workspace is in the agents' working folder. Agents run
  as your user, so any file is readable to them if they look. Keep tokens outside the workspace.
- **Other factories' tokens:** Factory removes `DISCORD_BOT_TOKEN` and this factory's
  `token_variable` from the Foreman's environment. It does not know other factories' variable
  names, and the Foreman copies the rest of the environment. Keep bot tokens in the `env_file`,
  not exported in the shell profile.

## Later

- One thread per plan, and a Foreman tool to post into a plan's thread.
- A `/status` command that the relay answers itself, so it works when the Foreman is stuck.
- The persistent Foreman, as a second child of its owner.
