# Issue polling and an owned Pi session

Status: Slice 2 lifecycle retained; Slice 4 adds planning, issue revisions and restart recovery.

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
requires tmux at runtime. Existing-session delivery is not integrated in Factory. AgentShell 0.5.0
now supplies `attach_interactive()` and `TmuxTarget`; [#25][attachment-issue] remains open.
A Pi session ID still reopens a conversation in a new process; it is not a terminal target.
The [main plan](../plan.md) proposes attachment integration with separate borrowed-session cleanup.
Attachment cannot change an existing process's resources or provide Pi session events; closing the
borrowed connection leaves its process running. The current watcher still owns every Pi it launches.
No custom notification queue. Validate idle and busy delivery; submission is not execution.

Watch first checks native Forgetful project/planning access. Browser sign-in or refresh may occur
for an attended watcher. The startup prompt then selects existing open matches or new matches only.
The command polls every 30 seconds by default; `--interval` overrides it.

Before each notification, `ScaffoldIssue` creates or reuses the plan, ownership task and ordinary
issue worktree. The extra `epic` label defers worktrees to the owner. Full recovery and metadata
rules are in [issue planning](issue-planning.md). The watcher never dispatches owners itself.

In-memory submitted revisions allow issue updates. Restart restores draft/active Factory plans,
including closed issues; new-only startup still sends replies to recovered work. Other initial
matches form a baseline. Retry failed GitHub reads on the next poll; stop on unresolved scaffold
or terminal failures. No work is deleted on failure. Notifications carry body/revision and saved
plan/task/worktree IDs as escaped external data; agents must reread current issue/comments.

The watcher owns the new Pi process and closes it when it stops; there is no detached operation.
A workspace lease prevents concurrent init/watch commands. The CLI acquires it before configuration
reads, readiness checks or setup mutations, and holds it until cleanup completes. The filesystem
adapter uses POSIX `flock` with no-follow directory opens: it locks the existing workspace, plus
`.factory` when present to remain compatible with older watchers. Fresh init need not create
`.factory` to acquire the lock. No PID or lock files are written. Different workspaces are not
globally coordinated. The application receives an already-guarded invocation and the CLI's
startup-choice callback. Rejected commands do not invalidate setup receipts, ask unused questions
or print commands for nonexistent targets.
If cleanup fails, inspect the printed session before retrying; the watcher never replaces it.

See the [slice 2 plan](../plans/slice-2.md) for tests, SonarQube analysis, and Opus review.
Profiles and role tools/skills were outside Slice 2 and are now covered by the
[agent-profiles ADR](agent-profiles.md). Slice 4 adds the planning/worktree ports; Slice 5 supplies
the Foreman's owner roster and native role instructions.

### Watcher integration

The package requires Python 3.12+ and now pins `agent-shell-py==0.5.0` as a runtime dependency
following the [shared-login audit](../plans/agentshell-0.5-audit.md); Slice 2 originally used 0.4.0.
`uvx` installs AgentShell into the factory's isolated environment; no source checkout or separate
AgentShell installation is needed. Pi, tmux, Git, and authenticated `gh` remain host prerequisites.
The default controller interpreter is the factory's Python. `--agentshell-python /path/to/python`
remains an optional override for an already installed compatible AgentShell environment.
The Python minimum follows AgentShell's requirement.
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
│   ├── watch_factory.py             # Polling, baseline, revisions, notifications
│   └── ports/
│       └── foreman_terminal.py      # Startup hint, launch, submit, wait, close
├── domain/
│   ├── models.py                    # Provider-independent Issue
│   └── services/work_tracking.py    # Adds matching-open-issue reads
└── adapters/
    ├── filesystem/watch_lease.py    # CLI-owned workspace and legacy factory-directory locks
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
Submitted revisions are not durable. Restart replays unfinished plans from Forgetful; it does not
claim exactly-once notification delivery or restore the previous agent process.

The [slice 2 plan](../plans/slice-2.md) records public-boundary tests, packaged-command checks,
real idle/busy Pi delivery, SonarQube, and independent review. It also records deferred event-log
growth and large-repository polling concerns. Routine tests substitute external commands and make
no live service or model calls. The
[current validation record](../plans/slices-4-5.md) separates those tests from native local
Forgetful and no-inference Pi checks.

[attachment-issue]: https://github.com/ScottRBK/agent-shell/issues/25

Upstream availability was rechecked against the [0.5.0 release][attachment-release] and installed
public API during Slice 3 close-out; no Factory attachment or live borrowed-Pi test ran.

[attachment-release]: https://github.com/ScottRBK/agent-shell/releases/tag/v0.5.0
