# Configuration

How to change a factory's settings after first setup. The commands use `$wheel` from
[Run from source](../README.md#run-from-source). Run them from the workspace folder, or add
`--workspace /absolute/path/to/workspace`.

## Settings files

| File | What it holds |
|---|---|
| `.factory/factory.toml` | Factory settings: repositories, labels, Forgetful, Discord |
| `.factory/agents/<role>/agent.json` | One agent's settings |
| `.factory/definition_of_done.md` | The completion agreement |
| `.factory/agents/foreman/forgetful.json` | Foreman's memory extension settings |

Repeated `init` preserves saved files; it does not refresh settings or repeat setup.
Use `init --finalize` to complete or revalidate unfinished first setup. For later edits,
see the [reload rules](adrs/agent-onboarding.md#maintenance-and-selected-resources).
You can also ask Foreman for help with `/skill:factory-maintenance`.

## Update role resources

After you install a newer Factory, update the bundled role resources in `.factory/resources`.
Stop Foreman, watch and delegated work first. Preview the changes, then apply them:

```bash
uvx --refresh --from "$wheel" forgetful-factory update --dry-run \
  --workspace /absolute/path/to/workspace
uvx --refresh --from "$wheel" forgetful-factory update --workspace /absolute/path/to/workspace
```

The update replaces only unedited files and never changes `.factory/agents/` or `.factory/data/`.
An edited file stops the update; `--force` backs it up, then replaces it. When the new bundle
changes the AgentShell lock, the update installs the locked packages from PyPI;
`--no-install-role-runtime` skips that. See the [update ADR](adrs/role-resource-update.md).

## Foreman memory

Foreman's Forgetful extension reads its settings from `.factory/agents/foreman/forgetful.json`.
The file takes the extension's own settings and rules, for example:

```json
{"enabled": true, "capture_mode": "auto", "model": "provider/model-id",
 "context_limit_tokens": 262144, "logging": "debug"}
```

Factory sets the server, authentication, project and log folder, so the file must not set them.
Stop Foreman, edit the file, then start Foreman. After a Factory upgrade, run `update` first.
See [memory settings](adrs/foreman-memory.md#memory-settings).

## Discord

Plain watch can use one Discord channel for each factory. The channel shows:

- 🟢 when Foreman is ready, and 🔴 with the reason when watch stops;
- each text block that Foreman writes, as it comes (not tool calls or thinking);
- after a restart, how many messages came while watch was off.

People on the allowlist write to Foreman by mentioning the bot, for example `@YourBot status
please`. Foreman gets `[Discord] <display name>: status please`. Other messages are ignored. When
you type `@`, pick the bot, not a role with the same name. Each message gets 👀 when the bot has
it, then ✅ sent, ⚠️ delivery uncertain, or 💤 not sent because watch was stopping.

Messages and replies move while watch polls GitHub and Forgetful. Watch checks Discord every
second; to change this, use `watch --chat-interval <seconds>` (at most 60).

A Discord problem never stops watch. Watch prints a warning and continues without Discord, and
the Foreman terminal works as before. The persistent Foreman does not use Discord yet.

1. Run watch with the `discord` extra:

   ```bash
   uvx --refresh --from "forgetful-factory[discord] @ $wheel" forgetful-factory watch
   ```

2. In the [Discord Developer Portal](https://discord.com/developers/applications), make an
   application with a bot and copy its token. The bot needs no privileged intent. Invite it to
   your server with these permissions: View Channel, Send Messages, Read Message History and Add
   Reactions.

3. Put the token in the environment or in the secrets file. The default file is
   `~/.config/forgetful-factory/.env`; keep it outside the workspace and run `chmod 600` on it:

   ```bash
   DISCORD_BOT_TOKEN=your-bot-token
   ```

4. Add the settings to `.factory/factory.toml`. To copy IDs, switch on Developer Mode in
   Discord. `env_file` and `token_variable` are optional; `env_file` must come before the first
   `[table]`. A relative `env_file` is relative to the workspace.

   ```toml
   env_file = "~/.config/forgetful-factory/.env"

   [discord]
   channel_id = "123456789012345678"
   allowed_users = ["234567890123456789"]
   token_variable = "DISCORD_BOT_TOKEN"
   ```

The environment wins over the file. If each factory has its own bot, give each one its own
`token_variable`. Factory removes these variables from Foreman's environment, so Pi and its agents
never receive the token. Older Factory builds refuse a `factory.toml` with these settings.

**Security:** a message from an allowed person can do what typing in the Foreman terminal can do.
Keep the allowlist short and use two-factor sign-in on those Discord accounts. Discord stores the
Foreman replies. See the [Discord ADR](adrs/discord-channel.md).
