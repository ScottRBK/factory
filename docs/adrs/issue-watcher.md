# Issue polling and an owned Pi session

Status: accepted and implemented (slice 2).

Back to [architecture](../architecture.md). Scope and evidence: [slice 2](../plans/slice-2.md).

## Context and decision

Deliver matching GitHub issues to one Pi conversation without building a messaging framework.
AgentShell owns terminal operations; the factory owns the watcher lifecycle.

Poll configured GitHub work sources for issues matching the watched labels, then
forward notifications to one newly launched Pi session through AgentShell's tmux runner, using the
configured Foreman model and effort. Reuse that session; do not silently replace or duplicate it.
Keep polling behind `WorkTrackingService` and terminal delivery behind an application port.
The application coordinates polling; GitHub and AgentShell adapters perform external operations.
All terminal interaction goes through AgentShell, not factory-owned tmux calls. The host still
requires tmux at runtime. Existing-session delivery is deferred pending
[AgentShell #25](https://github.com/ScottRBK/agent-shell/issues/25); a Pi session ID reopens a
conversation in a new process, not a connection to the already-running terminal.
No custom notification queue. Validate idle and busy delivery; submission is not execution.

Prompt at startup whether to forward existing matching open issues or watch for new matches only.
For new matches only, the initial results form a baseline without notifications. Slice 2 forwards
new matches, not edits to already-seen issues; restarts use the same startup prompt. Consider update
notifications and durable restart tracking in slice 3 alongside Foreman setup.

The agreed `forgetful-factory watch` command launches Pi and starts polling every 30 seconds
by default, with `--interval` overriding it. Keep notified issue IDs in memory, recording successful
submissions; seed the seen set with initial results when the user chooses new matches only.
Notifications contain repository, issue number, title, and URL, not the issue body. Retry failed
GitHub reads next poll; stop with a clear error on terminal delivery failure. For new-only startup,
each work source is baselined on its first successful read, even if its initial read failed.
The watcher owns the new Pi process and closes it when it stops; there is no detached operation.
A workspace lease prevents a second concurrent watcher from launching another Pi. It is an advisory
lock on the existing `.factory` directory, held until shutdown cleanup completes; no PID or lock
files are written. The filesystem adapter uses POSIX `flock` with a no-follow directory open, and
the application depends on the `WatchLease` port. Different workspaces are not globally coordinated.
The CLI supplies the startup-choice callback; the application acquires the lease before invoking it
or reporting the terminal adapter's startup hint. Rejected second watchers therefore do not ask
unused questions or print commands for nonexistent targets.
If cleanup fails, inspect the printed session before retrying; the watcher never replaces it.

See the [slice 2 plan](../plans/slice-2.md) for tests, SonarQube analysis, and Opus review.
Profiles, role tools/skills, plans, worktrees, and owner dispatch remain out of scope.

### Watcher integration

The package requires Python 3.12+ and declares `agent-shell-py==0.4.0` as a runtime dependency.
`uvx` installs AgentShell into the factory's isolated environment; no source checkout or separate
AgentShell installation is needed. Pi, tmux, Git, and authenticated `gh` remain host prerequisites.
The default controller interpreter is the factory's Python. `--agentshell-python /path/to/python`
remains an optional override for an already installed compatible AgentShell environment.
The Python minimum follows AgentShell 0.4.0's requirement.
Dependency changes require a pre-install audit.

`AgentShellTerminal` starts one small controller using the selected interpreter and the installed
controller file's absolute path. Its private line-based protocol carries launch settings,
notification text, and submission acknowledgements. Library output goes to stderr, separate from
that protocol. The controller owns the interactive session lifetime; keeping it in a subprocess
also supports the optional interpreter override without mixing Python environments.
It is an adapter detail, not a domain service or a general messaging framework.

The controller uses `AgentShell.open_interactive` with `TmuxExecutionHost`, waits for Pi's session
start event before submitting text, and calls `session.terminal.send_text(..., submit=True)`.
Startup and submission waits are bounded. Native trust prompts remain enabled; the user may need
to attach to the displayed session and answer them. Closing the controller closes its owned session.
The factory does not interpret terminal screenshots or infer that a submitted issue was completed.

```text
src/forgetful_factory/
├── application/
│   ├── watch_factory.py             # Polling, baseline, seen IDs, notifications
│   └── ports/
│       ├── foreman_terminal.py      # Startup hint, launch, submit, wait, close
│       └── watch_lease.py           # Exclusive workspace ownership contract
├── domain/
│   ├── models.py                    # Provider-independent Issue
│   └── services/work_tracking.py    # Adds matching-open-issue reads
└── adapters/
    ├── filesystem/watch_lease.py    # Advisory lock on the factory directory
    ├── github/work_tracking.py      # Paginated issue reads and label matching
    └── agentshell/
        ├── terminal.py              # Controller process and acknowledgements
        └── controller.py            # AgentShell-owned interactive session
```

GitHub fetches all pages of open issues and applies label matching locally: any configured label
matches, case-insensitively; `*` includes unlabelled issues. Pull requests are excluded. Multiple
local copies of a work source are polled once. Notifications use a fixed prose prefix and
JSON-escaped fields so issue titles cannot become terminal control sequences or slash commands.

## Consequences and validation

Submission acknowledgement means text reached the terminal, not that the agent executed it or
completed the issue. Session failure stops the watcher rather than silently replacing the agent.
Seen IDs are not durable; a restart requires a new startup choice.

The [slice 2 plan](../plans/slice-2.md) records public-boundary tests, packaged-command checks,
real idle/busy Pi delivery, SonarQube, and independent review. It also records deferred event-log
growth and large-repository polling concerns. Routine tests substitute external GitHub and
AgentShell and make no live service or model calls.
