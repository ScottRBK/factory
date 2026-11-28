# Discord channel work plan

## Status

Slices 1 to 3 implemented on 2026-11-27 and tested with fake Discord and fake AgentShell. The
live check on a real Discord server is still to do. The decisions and their reasons are in the
[Discord channel ADR](../adrs/discord-channel.md).

## Shape

```
watch (existing) ── JSON lines ── controller (existing) ── Pi Foreman in tmux
  │ socket pair, JSON lines
Discord relay (new child process) ── Discord
```

Link messages, one JSON object per line:

- `watch` to relay: `post` (text), `status` (`online` or `stopped`, with a reason), and in slice 2
  `mark` (message ID and delivery).
- Relay to `watch`: `ready`, `problem` (text; `fatal` when the relay stops), and in slice 2
  `message` (ID, author, text).
- The first line from `watch` is `start`: token, token variable, channel ID and allowed users.
- Controller to `watch`: `reply` (text and an optional error), only when the launch has
  `replies: true`.

## Files

New, under `src/forgetful_factory/`:

| File | Job |
|---|---|
| `channels/model.py` | `ChatMessage`; `Delivery`; `DiscordSettings` and their checks |
| `channels/adapters/discord/relay.py` | the relay child: gateway, filter, post, react |
| `channels/adapters/discord/link.py` | `watch`'s side: find token, start relay, JSON lines |
| `shared/env_file.py` | read one `KEY=value` file; never changes `os.environ` |
| `factory/services/chat_relay.py` | the rules: post replies, 🟢/🔴, forward and mark |

Changed:

| File | Change |
|---|---|
| `channels/ports.py` | add the `ChatChannel` port beside `Channel` |
| `agents/ports.py`, `agents/model.py` | `ForemanTerminal.wait` returns `ForemanReply` items |
| `agents/adapters/agentshell/controller.py` | after ready, read events; `reply` on `result` |
| `agents/adapters/agentshell/terminal.py` | read `reply` lines; wait on the chat link too |
| `agents/adapters/agentshell/borrowed_terminal.py` | new `wait` signature; no chat |
| `factory/services/watch_factory.py` | waits go through `ChatRelay`; 🟢 and 🔴 |
| `factory/model/configuration.py` | `env_file` and `[discord]`, validated |
| `factory/adapters/toml_configuration.py` | resolve `env_file`; save both settings |
| `planning/adapters/forgetful/connection.py` | remove the token variable from the Foreman |
| `cli/bootstrap.py` | build the link when `[discord]` is set, for plain watch only |
| `pyproject.toml`, `uv.lock` | `discord` extra and dev pin; import rule for `discord` |

Tests: `test_env_file.py`, `test_controller_replies.py`, `test_chat_relay.py`,
`test_discord_relay.py`, `test_discord_link.py` (with the `ChatChannel` contract in
`tests/contracts/channels.py`), `test_discord_api.py`, `test_discord_watch.py`, and the fake
`tests/fake_discord.py`.

## Checks before coding (results)

- **One events reader:** AgentShell 0.5 keeps the read position on the session and frees the
  reader in a `finally` block (`agent_shell/interactive.py`, `InteractiveSession.events`). A
  second `events()` call after `ready()` continues where it stopped, so replies use a second
  reader.
- **Event shapes:** confirmed in `agent_shell/adapters/pi_adapter.py`: `text` (full block, on
  `text_end`), `tool_use`, `status` `turn_started` (on `agent_start`) and `result` (on
  `agent_settled`, content `ok` or `error`, with `error` text).
- **Send and replies in one loop:** `forward_replies` runs as a second task beside the send loop
  in `interact` and is cancelled when the loop ends.
- **discord.py API:** checked in Context7 and in the audited 2.7.1 source:
  `Client.get_partial_messageable`, `PartialMessageable.history` (needs Read Message History),
  `get_partial_message(...).add_reaction`, `LoginFailure` for a bad token and
  `PrivilegedIntentsRequired` without the message intent. `test_discord_api.py` keeps the fake
  in step with the real library.

## Slices

### Slice 1: post only

Discord shows 🟢, 🔴 with the stop reason, and every Foreman reply. Nothing from Discord reaches
the Foreman.

1. Supply-chain audit of discord.py 2.7.1 and its dependencies: passed with notes; see the
   [audit](discord-py-audit.md). Scott approved the extra and the dev pin on 2026-11-27. The lock
   diff and every hash match the audited scratch lock.
2. `env_file` and `[discord]` settings, and the env file reader.
3. Remove the token variable from the Foreman's environment.
4. Controller `reply` events, only when the launch asks for them.
5. Relay child, link and `ChatRelay`; `watch` posts 🟢, 🔴 and replies.
6. Import rule, "Discord" section (now in [configuration](../configuration.md#discord)),
   architecture and Mycelium map.

### Slice 2: talk to the Foreman

Allowed users' messages reach the Foreman as `[Discord] <text>`, with ✅, ⚠️ or 💤 reactions.
Needs the `MESSAGE_CONTENT` intent.

### Slice 3: missed messages

When `watch` starts, the relay counts allowed messages after the last 🔴 post and posts
"N messages came while watch was off; they were not sent."

## Validation

Write each test first and see it fail (TDD).

- **Env file reader:** comments, quotes, `export`, environment wins, `os.environ` unchanged.
  A set-but-missing file and a token that is not found give warnings that name the places
  checked, and `watch` continues.
- **Settings:** a valid `[discord]` and `env_file` load. A bad channel ID, empty `allowed_users`
  and unknown keys are refused. Existing `factory.toml` files load unchanged.
- **Token isolation:** the Foreman environment has neither the default nor a named token
  variable, even when both are exported.
- **Controller:** with fake AgentShell events, `reply` holds the text after the last tool call,
  and a turn with no text posts nothing. Without the launch flag, no `reply` is sent, so the owner
  keeps working.
- **Relay rules (`ChatRelay`):** with a fake chat and a fake Foreman:
  - 🟢 after start;
  - 🔴 with the reason after an error, after Ctrl-C and after a Foreman exit;
  - a chat failure gives a warning and `watch` continues.
- **Link:** with a fake relay child and no network, JSON lines both ways. A child that crashes
  gives a warning. A parent that closes its socket makes the child post and exit.
- **Relay:** with faked discord.py objects, the 2000-character split, the five-part cut, mentions
  set to none and, in slice 2, the channel and user filter.
- **Packaging:** the wheel without the extra runs as today. `[discord]` without the extra warns
  with the install hint and runs without Discord. The import rule's proof test fails when another
  module imports `discord`.
- **Never blocks:** for each Discord problem (no extra, no token, bad token, no network, relay
  crash), `watch` starts or keeps running, and Foreman notifications still arrive in tmux.
- **Live check:** a private test server and a test factory. Record the evidence here, not in the
  ADR.

## Validation record (2026-11-27)

Tests were written first and seen to fail, then the code was added.

| File | Tests | What they prove |
|---|---|---|
| `test_env_file.py` | 8 | reader rules; environment wins; warnings name the places checked |
| `test_configuration.py` | 5 new | settings load, refuse bad values, save and load again |
| `test_controller_replies.py` | 5 | reply text after the last tool call; errors; no reply unasked |
| `test_chat_relay.py` | 6 | ticks, replies, marks, a failed send, stop reasons |
| `test_discord_relay.py` | 14 | split, order, no pings, token, network, intent, filter, 💤, 📭 |
| `test_discord_link.py` | 9 | contract on the real relay; token on the socket; bad relays |
| `test_discord_api.py` | 4 | the real discord.py 2.7.1 takes the relay's calls as the fake does |
| `test_discord_watch.py` | 5 | end to end, six "never blocks" cases, a killed watch |

- The architecture test proves the new `discord-in-its-adapter` rule with six rejected rows,
  direct and indirect. A new check keeps `services/` and `ports.py` free of chat provider names.
- `test_discord_api.py` failed when the fake's `add_reaction` signature was changed on purpose,
  then passed again with the fake restored.
- The end-to-end tests found one fault: a relay that stopped after its last problem lost that
  problem when `watch` first failed to send. The link now reads first.
- Full suite on Python 3.12.16 and on 3.13.18 (scratch environment from the same lock): 819
  passed, 14 skipped each. Ruff clean, `lint-imports` 8 rules kept, `compileall` clean.
  `tests/check_package.py`: 123 wheel checksums verified. The Discord tests passed five runs in
  a row.
- The guide's command `uvx --refresh --from "forgetful-factory[discord] @ $wheel"` ran with a wheel
  built in a scratch folder; the tool environment held exactly the audited versions.
- Not covered by tests: a real Discord gateway, rate limits and reconnects. The live check covers
  these.

## First live run (2026-11-28)

Clyewyre Discord server, the dark-business factory, token in `CW_FACTORY_DISCORD` in the default
`env_file`, two allowed users.

- 🟢 was posted. Both allowed users got ✅, and the Foreman received `[Discord] Pmsl` and two more
  messages. The text at the end of the turn reached Discord.
- The first message waited about 2 minutes. Watch's first poll with existing issues took that
  long, and messages wait in the socket during a poll. A later poll took about 8 seconds.
- The Foreman answered two messages in the middle of a busy turn. Tool calls followed each
  answer, so only the last text was posted, and the two answers did not reach Discord.

Changes after the run (Scott's choices), test first:

- The controller sends each text block as it comes, not only the text after the last tool call.
- The relay accepts only messages that mention the bot and takes the mention out. It asks for no
  privileged intent: Discord gives the text of messages that mention the bot without the Message
  Content intent (discord.py `Intents.message_content`, checked in Context7). The intent fallback
  is removed. 📭 counts only messages to the bot. `@everyone` does not count as a mention
  (`ClientUser.mentioned_in` would count it, so the relay checks `message.mentions`).
- The Foreman gets `[Discord] <display name>: <text>`.
- The fake blanks text as Discord does without the intent. Its `ungated` setting proves the
  relay's own checks. `test_discord_api.py` checks `mentions`, `mention_everyone` and
  `display_name` on the real classes, and that the relay asks for no privileged intent.
- Full suite: 819 passed, 14 skipped. Ruff clean, 8 import rules kept. Map regenerated.

### Live check steps

1. Make a test bot (no privileged intent), invite it to a server and channel.
2. Add `[discord]` to a factory and run plain `watch` with the `discord` extra.
3. Check 🟢, Foreman text, an @mention from an allowed account (👀 at once, then ✅, the name
   and the answer), a message without a mention and one from another account (both ignored),
   Ctrl-C (🔴 with the reason), and a restart after an @mention (📭 count). Then stop the network
   for a minute and check that watch keeps running.
4. Send an @mention while watch polls (for example just after start with `--existing`). The
   answer must come without waiting for the poll.

## Chat thread (2026-11-28)

Scott chose a chat thread (option A) and the 👀 reaction (option B), and asked for the chat check
time as a flag like `--interval`. The decision is in ADR decision 8.

- `ChatRelay` starts a thread at `online` when a chat is set. Watch's own sends go through
  `ChatRelay.foreman`, which shares one lock with the thread. The thread holds it for a 0.05
  second read and for each chat send. `WatchFactory` ends the thread before it closes the
  terminal.
- `watch --chat-interval` (default 1 second, at most 60) is checked like `--interval`. With
  `--start`, `--stop` or `--status` it is an error.
- The relay reacts 👀 when it has a message, before watch sends it on.
- Tests, written first:
  - `test_chat_relay.py`: replies and messages move while watch is busy; a 60 second interval
    does not delay a watch send; watch and the thread never use the terminal at the same time
    (this test fails with the lock removed); a thread failure stops watch at its next wait and
    blocks later sends, also a send already waiting for the lock; after a failed watch send the
    thread sends nothing; `halt` takes no new message and waits for the send in progress;
    Ctrl-C reaches the thread; a 1e12 second wait still stops on a failure; a waiting watch send
    goes after at most one chat send; a failure is raised from a zero wait; a second Ctrl-C
    does not cut `halt` short; a thread that cannot start keeps its own error.
  - `test_discord_watch.py`: the first GitHub read waits at a gate; an @mention written after
    the read reached the gate is answered within 4 seconds, and Ctrl-C during the held read
    still stops watch, Pi and the relay. On the old code this test fails. `--chat-interval 0`,
    `61` and `--start --chat-interval` are refused.
  - `test_discord_relay.py` and `test_discord_watch.py`: 👀 then ✅; 👀 then 💤 at a stop.
- Codex review (gpt-6.2-astra) of the change, all fixed test first:
  - a watch send that waited behind a failed chat send could still reach Pi: a failed terminal
    use is now kept under the lock, and the other thread checks it under the same lock;
  - `halt` could return while the thread still sent messages: the thread checks the stop under
    the lock before each use, and `halt` waits for it to end;
  - a very long chat interval hid a Pi exit: at most 60 seconds;
  - `Event.wait` refuses timeouts above `threading.TIMEOUT_MAX`: watch waits in steps of at most
    a minute;
  - the end-to-end test now sends the message while the poll is held, not before start.
- The same change clears the SonarQube findings in the Discord commit: cognitive complexity in
  `controller.interact` (split into `become_ready` and `send_line`), two `async` functions with
  no `await` in the relay, and `[0-9]`/`[A-Za-z0-9_]` written as `\d`/`\w` with `re.ASCII`.
  New tests prove that other digits and letters are still refused.
- A second Codex pass, all fixed test first:
  - a burst of chat messages kept a waiting watch notice behind 20 sends (a lock is not fair):
    watch now holds a `turn` lock while it waits, and the test fails without it;
  - a second Ctrl-C cut `halt` short, so the terminal could close during a send: `halt` waits on;
  - a thread that cannot start hid its error behind `halt`: `thread` is set only after start;
  - a very short `--interval` skipped the failure check: `wait` always checks;
  - source-navigation line numbers in the overview, some already 2 lines out.
- The thread catches `Exception` and `KeyboardInterrupt` by name (SonarQube S5754), not
  `BaseException`.
- Validation on top of the cleanup commit: full suite 844 passed, 14 skipped; ruff clean; 8 import
  rules kept; map regenerated and stable (22 warnings). SonarQube: no bugs, vulnerabilities or
  hotspots; the only open issue is the older S3516 in `cli/resource_update.py`.
