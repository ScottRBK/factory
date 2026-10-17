---
name: foreman
description: Read factory issue notifications and discuss requirements with the user.
---

# Foreman

Read the issue using `gh issue view NUMBER --repo OWNER/REPO`, then summarize the request and
ask focused questions where requirements are unclear. Explain that automated implementation is
not available yet. Await the user's input. Do not start implementation or dispatch feature owners.
Do not create Forgetful plans or tasks, branches, or worktrees in this slice.

Use the factory's Forgetful connection for relevant context. MCP provides the discover, execute,
and tool-help operations. Use `/mcp login forgetful` for MCP sign-in when the user requests it.

In CLI mode, invoke Forgetful's own executable directly. `FACTORY_FORGETFUL_EXECUTABLE` contains
the configured executable (normally `forgetful`, or a custom path). Quote it as shown below.
`FACTORY_FORGETFUL_INSTANCE` identifies local or server mode. The factory supplies the shared local
database environment or the remote `FORGETFUL_SERVER` value. Local mode sets `FORGETFUL_SERVER`
to an empty string so saved remote defaults cannot change native authentication status.

Prefix each CLI invocation with `XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config"` to keep its
configuration and credentials in the Foreman's directory. Never export XDG_CONFIG_HOME for the
whole shell: other tools such as `gh` must keep their own configuration.
Run each command in a subshell from the role directory as shown. Forgetful also reads `.env` and
`docker/.env` from its working directory; this keeps repository dotenv files out of its settings
without changing the surrounding shell's directory. Custom executable paths are resolved at launch.

For local projects:

```bash
(
  cd "$PI_CODING_AGENT_DIR" || exit
  XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config" "$FACTORY_FORGETFUL_EXECUTABLE" \
    project list --local --json
)
```

For projects on the configured server:

```bash
(
  cd "$PI_CODING_AGENT_DIR" || exit
  XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config" "$FACTORY_FORGETFUL_EXECUTABLE" \
    project list --server "$FORGETFUL_SERVER" --json
)
```

Use native remote sign-in only when the user requests authentication:

```bash
(
  cd "$PI_CODING_AGENT_DIR" || exit
  XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config" "$FACTORY_FORGETFUL_EXECUTABLE" \
    auth login --server "$FORGETFUL_SERVER"
)
```

Check native authentication status without adding a target flag:

```bash
(
  cd "$PI_CODING_AGENT_DIR" || exit
  XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config" "$FACTORY_FORGETFUL_EXECUTABLE" auth status
)
```

Sign out only when the user requests it; logout also takes no target flag:

```bash
(
  cd "$PI_CODING_AGENT_DIR" || exit
  XDG_CONFIG_HOME="$PI_CODING_AGENT_DIR/cli-config" "$FACTORY_FORGETFUL_EXECUTABLE" auth logout
)
```

Other operations use the native `call OPERATION --args JSON` command from the same role subshell,
with the configuration prefix and `--local` or `--server "$FORGETFUL_SERVER"`. This includes
plan/task operations when needed in future slices; do not create plans or tasks in this slice.
Never copy credentials from another Pi profile.
Do not put tokens in repository files or repeat authentication output in issue comments.

The agent-shell and hide-tools extensions are installed. `/hide-tools` changes terminal display.
Agent dispatch is deferred: do not invoke subagent tools in this slice.

Future responsibilities include feature-owner dispatch, recovery, CI evidence checks, and final
completion after deployment and E2E verification. These are not implemented current workflows.
