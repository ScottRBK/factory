# Issue polling and Foreman connection

Status: owned-Pi watching and managed watcher controls remain. Current Factory source reads
[normalized agent definitions](agent-definitions.md) through audited extension 1.5.0. Native SDK
probes and both full Python suites pass without inference. Runtime repair policy and final checks
remain open. Slice 4 planning/recovery and earlier lifecycle evidence remain historical; see
[current release limits](../../README.md#current-source-and-release-boundary).

Back to [architecture](../architecture.md). Scope and evidence: [slice 2](../plans/slice-2.md).

## Context and decision

Deliver matching GitHub issues to one Pi conversation without building a messaging framework.
AgentShell owns terminal operations; the factory owns the watcher lifecycle.

Poll configured GitHub work sources for matching issues and notify one Foreman through AgentShell.
Plain `watch` launches and owns a fresh Pi using the selected root `agent.json`. A persistent owner,
started by assisted first init or standalone `foreman`, retains Foreman independently and manages
a watcher that borrows its delivery channel. `foreman --attach` enters that existing terminal.
Neither standalone Foreman command starts a watcher. Reuse that
session; never silently replace or duplicate it. Keep polling behind `WorkTrackingService` and
terminal delivery behind an application port. GitHub and AgentShell adapters perform external I/O.

All notification delivery goes through AgentShell, not Factory-owned tmux input commands. Native
tmux client attach/switch only navigates the user's UI. The persistent owner's public captured
target, startup event and process wait identify its terminal and liveness. A Pi session ID alone is
not a running-terminal reference. AgentShell's guarded delivery still compares terminal identity; an
additional bounded identity probe detects a replaced pane even while idle. A live-pinned,
revalidated process handle observes original pane-worker exit even when tmux queries fail. Failed
queries alone preserve uncertain ownership; they do not authorize closing a still-running Pi.

This existing-Foreman integration connects to the persistent owner's held session, not directly to
an arbitrary pane. AgentShell 0.5.0 already supplies `attach_interactive()` and `TmuxTarget`
for that later expansion; [#25][attachment-issue] remains open. Connecting a watcher does not change
running resources or prove receipt. No custom notification queue is introduced.

After native launch prerequisites and the existing/new-only choice, watch connects Foreman before
checking Forgetful project/planning access. Access or incomplete inventory reads pause planning and
alert Foreman while read-only checks continue. Browser sign-in or refresh may occur for an attended
watcher. The command polls every 30 seconds by default; `--interval` overrides it.

For new intake, `ScaffoldIssue` creates or reuses the plan, ownership task and ordinary issue
worktree. Saved and blocked plans use a separate read-only recovery path; disappeared records never
fall back to creation. The extra `epic` label defers worktrees to the owner. Full recovery and
metadata rules are in [issue planning](issue-planning.md). The watcher never dispatches owners.

In-memory submitted revisions allow issue updates. Restart restores draft/active Factory plans,
including closed issues; new-only startup still sends replies to recovered work. Other initial
matches form a baseline. Known planning safety problems pause the affected plan and alert Foreman,
while unrelated work continues. Shared read failures pause planning for safe rechecks; an operation
that may have written latches a manual-reconciliation pause, without repeating it. Failed GitHub
reads alert once per episode and retry on the next poll while healthy sources continue.

Alert suppression, blocked records and issue revisions remain separate. A corrected record can
recover without an issue edit. No work is deleted on failure. Ordinary notifications carry
body/revision and saved plan/task/worktree IDs as escaped external data; agents must reread current
issue/comments. Problem alerts carry controlled explanations and recovery context, not raw external
diagnostics. See [watcher problems](watcher-problems.md) and its
[validation record](../plans/watcher-problems.md). Terminal failures retain their lifecycle rules.

Plain watch owns the new Pi process and closes it when stopped. For a persistent Foreman, `watch
--start` with `--existing` or `--new-only` asks its owner to start a watcher child; status/stop act
on that owner's actual process handle. Stopping the child leaves Foreman alive. Foreman exit or
owner loss stops delivery without replacement. Existing untrusted or missing ownership evidence
never authorizes a replacement or replay. Uncertain delivery blocks a new managed start; initial
finalization cannot clear it. A pending send can finish, but a transport failure has no later
acknowledgement; inspect the possible submission, then deliberately exit Foreman and relaunch before
watching again.

A workspace lease prevents concurrent setup mutation and watcher execution. The CLI acquires it
before configuration reads, readiness checks or setup mutations and holds it through cleanup.
Owner status, watcher stop and terminal entry do not take that lease. The filesystem
adapter uses POSIX `flock` with no-follow directory opens: it locks the existing workspace, plus
`.factory` when present to remain compatible with older watchers. Fresh init need not create
`.factory` to acquire the lock. The workspace lease writes no PID or lock files. The persistent
owner's private runtime directory has a separate lifetime lock and control metadata; saved PIDs
never authorize process signals. Different workspaces are not globally coordinated. The application
receives an already-guarded invocation and the CLI's startup-choice callback. Rejected commands do
not invalidate setup receipts, ask unused questions or print commands for nonexistent targets.
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
start event before submitting text, and calls `session.terminal.send_text(..., submit=True)`. For a
persistent Foreman, `ForemanOwner` retains that controller independently of init's terminal and
stdin lifetime. A bounded handover separates startup cancellation from later init exit. The managed
watcher uses `BorrowedForemanTerminal` over an inherited private socket pair; close cannot close
Foreman. Owner/control state remains under `.factory/runtime/foreman`. The root's canonical
`agent.json` is selected directly; no generated runtime roster is published during finalization.
Shared consent and the simple completion receipt live directly under `.factory`, separate from agent
names. See the [onboarding ADR](agent-onboarding.md). Startup and submission waits are bounded.
Native trust prompts remain enabled; the user may need to attach to the displayed session and answer
them. Closing the controller closes its owned session. The factory does not interpret terminal
screenshots or infer that a submitted issue was completed.

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
        ├── terminal.py              # Watcher-owned controller and acknowledgements
        ├── borrowed_terminal.py     # Managed watcher's private channel to its owner
        ├── owner.py                 # Persistent Foreman and watcher child lifetime
        ├── owner_client.py          # Local lifecycle commands and user terminal entry
        └── controller.py            # AgentShell-owned interactive session
```

GitHub fetches all pages of open issues and applies label matching locally: any configured label
matches, case-insensitively; `*` includes unlabelled issues. Pull requests are excluded. Multiple
local copies of a work source are polled once. Notifications use a fixed prose prefix and
JSON-escaped fields so issue titles cannot become terminal control sequences or slash commands.

Root model, effort, cwd and resources come from the selected JSON at launch. Omitted root cwd
inherits the CLI process cwd; starter coordinator definitions explicitly use `"."`. The extension's
roster selector does not change the running root's own settings. Root changes require restart;
child settings and actual parent membership require reload of affected snapshots. Changed canonical
child selections fail selected-session resume. Init is not a refresh operation.

## Consequences and validation

Submission acknowledgement means text reached the terminal, not that the agent executed it or
completed the issue. Session failure stops the watcher rather than silently replacing the agent.
Submitted revisions are not durable. Restart replays unfinished plans from Forgetful; it does not
claim exactly-once notification delivery or restore the previous agent process.

The [slice 2 plan](../plans/slice-2.md) records public-boundary tests, packaged-command checks, real
idle/busy Pi delivery, SonarQube, and independent review. It also records deferred event-log growth
and large-repository polling concerns. Routine tests substitute external commands and make no live
service or model calls. The [earlier Slice 4/5 validation record](../plans/slices-4-5.md) separates
those tests from native local Forgetful and no-inference Pi checks.

[attachment-issue]: https://github.com/ScottRBK/agent-shell/issues/25

The earlier onboarding availability check used the [0.5.0 release][attachment-release] and installed
public API. The [onboarding record](../plans/agent-onboarding.md) distinguishes isolated lifecycle
and reload tests from unperformed live autonomous-agent trials.

[attachment-release]: https://github.com/ScottRBK/agent-shell/releases/tag/v0.5.0

Native cancellation remains limited by [agent-shell#28][cancellation]. There is no workaround here;
uncertain cancellation or exit cannot authorize replacement or replay.

[cancellation]: https://github.com/ScottRBK/agent-shell/issues/28
