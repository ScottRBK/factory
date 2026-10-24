# Agent setup and factory maintenance

Status: one-time starter provisioning and standalone Foreman use
[normalized agent definitions](agent-definitions.md) and audited extension 1.5.0. Both supported
Python runs pass 373 tests, including native SDK probes, without inference or skips. Runtime repair
policy and final checks remain open. Earlier onboarding results below describe the preceding design.
See [release limits](../../README.md#current-source-and-release-boundary).

Back to [architecture](../architecture.md).

## Why change onboarding

The Foreman model prompt accepted a number, but implementation/review prompts required typing
native app/model names. The worker-versus-planning-only question also obscured which settings
would be saved. Scott wants two understandable routes after setting up Foreman: configure each
remaining agent manually, or finish the configuration with Foreman's help.

Scott also wants a skill for setting up and maintaining the factory. Users should be able to put
skills in a selected folder, or ask an agent to do that work, without maintaining duplicated
resource lists. Each normalized agent file now owns its own selections.

## Implemented changes

First init provisions the full configured starter team in manual, assisted and planning-only modes.
It sets up Foreman, feature-owner and research, plus implementation/review when enabled. Assisted
setup does not provision only Foreman. Starter names are templates; later definitions can use
arbitrary names. `execution_enabled` remains a separate Factory permission, independent of names.

Interactive model/effort choices and worker app choices use numbered menus. Each number maps to the
displayed native value; command-line flags take exact values. Owner/research choices default from
their parent unless explicitly supplied. The initial research menu supports Pi; workers offer Pi,
Codex and Claude Code. This menu is narrower than native AgentShell capabilities. Model listing
uses native accounts/settings and proves selectability, not inference or model-specific effort.
Catalog caching and shared-Pi-profile consent remain part of first setup.

The setup menu offers manual choices or Foreman's help. Neither route asks for skill paths. Initial
skill flags remain optional; selections are saved in `agent.resources.skills`. Bundled
implementation guidance retains TDD. Init lists the starter skill folders; add files beneath a
selected directory or edit the owning agent file directly. There is no automatic skill download or
registration pass. Native harnesses validate contents; selecting a path is not proof of model
advertisement.

Once configuration is saved, ordinary repeated init preserves every file byte. It makes no backend
or catalog calls, asks no setup questions, performs no synchronization/reconciliation, and consumes
no optional launch answer. `--assisted` does not reopen saved setup. Explicit `init --finalize`
completes or revalidates first setup; it preserves an existing Foreman and any delivery uncertainty.
Later settings changes use direct TOML/JSON edits and reload/restart, not init.

### Completion and manual launch

Successful first manual init prints the watch command and, when stdin is a terminal, asks
`Launch factory now? [y/N]:`. Only `y` or `yes` launches; other answers or EOF leave setup complete.
Ctrl-C at this optional prompt returns 130 without describing setup as incomplete. Noninteractive
init prints the command without consuming an answer or launching, even if piped input contains Yes.
Failed validation never reaches the offer. Ordinary repeated init returns before this offer,
without reading another answer.

The CLI releases the init workspace lease before this offer. On Yes it replaces its own process
with the existing public watch command using the same interpreter and environment. Watch acquires
its own lease, asks about existing versus new issues, validates readiness and owns normal cleanup.
No additional watcher process manager or new launch flag is introduced.

Commands use the running Factory Python, a shell-quoted absolute workspace and the selected
AgentShell interpreter when overridden. Relative interpreter paths are made absolute without
resolving the virtualenv executable symlink; bare executable names retain PATH lookup. The commands
work from another directory while that installation remains available. Under uvx the interpreter
may live in its cache; after clearing that cache, use the original package/wheel invocation.

Assisted init, explicit finalization and init with a live or uncertain setup owner never offer
CLI launch or suggest ordinary watch. Foreman's maintenance guidance assigns it the managed watcher
start after validation and the user's explicit `/reload`, with confirmed existing/new issue scope.
That reuses the existing conversation. No second Foreman is started. This is instructed agent
behavior, not proof that a real model follows the guidance. Custom guidance stays preserved.

### Maintenance and selected resources

New factories select Foreman's dispatch and `factory-maintenance` skills, plus the audited
AgentShell entrypoint under `.factory/resources`. The selected skills can live apart from the agent
file or cwd; moving JSON does not move resources. Keep required selections when editing. The
maintenance skill preserves accounts, plans, worktrees and custom instructions, and distinguishes
setup validation from inference. Native guidance points to it; Pi owns skill advertisement, YAML,
metadata and name-clash validation. Factory checks paths and audited runtime integrity.

Agent choices live only in `agent.json`; `factory.toml` retains Factory settings and
`foreman_agent_file`. Shared consent/home is `.factory/pi-profile.json`, and first-setup completion
is `.factory/setup-complete.json` containing `{"complete": true}`. Neither depends on an agent's
name. The receipt does not bind model or resource fingerprints. Owner/control files remain under
`.factory/runtime/foreman`; native credentials and settings stay preserved.

### Superseded registration design

Earlier onboarding scanned `<role>/skills/*/SKILL.md`, synchronized `resources.json` and inline
parent `roster.json` selections, and tracked automatic additions in
`.factory/agents/skill-registration.json`. Pending before/after lists allowed interrupted multi-file
writes to recover while preserving manual edits. Completion fingerprints prevented use of stale
copies. This addressed consistency between duplicated selections.

[Normalized definitions](agent-definitions.md) replace that design: child settings have one owner,
parents contain file references, and skill directories can be selected directly. The registration
sidecar, synchronization pass, generated runtime roster and model/resource fingerprint are no longer
used. Earlier tests and reviews of those mechanisms remain historical evidence, not current
instructions. The proposed YAML parser dependency was removed at Scott's request; native harnesses
continue to own content validation.

Init and watch acquire the workspace lease at the CLI boundary, before configuration validation
or mutation. The lock also covers bootstrap/readiness checks and remains held through cleanup.
The existing workspace directory is locked even before `.factory` exists, with the original factory
lock retained when present for compatibility with running older watchers. No PID files are added.
A rejected init preserves the active setup receipt; a rejected watch cannot inspect partial setup.

Maintenance requires confirmed-stopped delegated work before reload/restart. A plain watcher owns
its Foreman, so that Foreman cannot stop itself and continue maintenance. A persistent Foreman can
stop its managed watcher and help edit definitions in the same conversation. First-setup
finalization can also run there. The lease guards CLI setup/watch, not arbitrary agent file edits or
every native child process. Editing a definition does not update a running agent's selections.

## Assisted setup and persistent Foreman

Assisted first init saves the whole starter team and opens a dedicated tmux Foreman without a
completion receipt. Review and finalize the choices in that conversation. The watcher cannot poll,
restore issue work or dispatch while first setup is incomplete. Both setup routes validate the same
saved format; agents must not manufacture receipts or bypass readiness checks. No automatic
migration is provided for older testing factories or DinoLand.

### Setup Foreman and watcher attachment

`foreman` also starts a persistent Foreman after completed setup; `foreman --attach` enters the
existing session. Neither starts a watcher. The maintenance skill describes managed watcher
start/status/stop through public Factory commands. This reuses the owner's held connection;
arbitrary-terminal discovery remains outside this integration.

Keep one watcher per workspace. Before attachment, verify the intended Foreman's terminal identity
and readiness; monitor its liveness while watching. A saved Pi conversation ID alone does not
identify a running terminal. Terminal attachment and notification delivery use AgentShell.
Stopping an attached watcher leaves Foreman running. Foreman exit stops the watcher without
launching a replacement. Keep the existing watcher-owned launch option and its cleanup behavior.

Scott explicitly removed live model, effort and loaded-resource verification from attachment.
Configuration validation belongs to setup and maintenance. The watcher still requires completed
saved setup, but does not inspect the running Foreman's current selections. Native in-session
model/effort changes do not trigger live-settings inspection. Edits to root launch settings in JSON
still require restart. Recorded launch settings are not live-state proof.

The implementation design below supplies launcher and lifecycle support as well as instructions.
The plain watcher closes its owned session when its caller disconnects. Connecting another
watcher cannot alter Foreman's settings or prove that it processed a submitted notification.

### Lifecycle implementation design

The persistent-owner lifecycle was implemented and reviewed before normalization. Its earlier
corrections and suite evidence remain in the progress record. Normalized source and native SDK
validation now pass as stated above; final checks and runtime repair policy remain open.

Keep one small owner process for the persistent Foreman. It retains the actual AgentShell session
and observes startup and process exit. The watcher borrows that owner's delivery connection rather
than creating another AgentShell controller. Notification text still goes through AgentShell's
guarded `send_text`; the watcher never owns or closes Foreman. This is connection to an existing
Factory controller, not arbitrary-terminal discovery or a new call to `attach_interactive()`.

The public routes are:

- First `init --assisted` provisions the configured team and starts setup Foreman without a
  completion receipt. Ordinary repeated init, including `--assisted`, preserves saved setup.
- `foreman` launches after completed setup without watching. `foreman --attach` enters the known
  terminal. `init --attach` remains a compatibility route. Native tmux attach/switch only navigates
  the UI; noninteractive or other-server callers receive a command instead of a forced switch.
- `init --finalize --delegated-work-stopped` completes or revalidates first setup. This confirmation
  is not process-exit evidence; do not finalize when delegated-work exit is uncertain. Finalization
  also works without a live setup owner and does not clear lost-send uncertainty.
- `watch --start` starts the owner's watcher with `--existing` or `--new-only`; `watch --status` and
  `watch --stop` query or stop that child. Plain watch owns a fresh Foreman and its cleanup, but
  refuses a duplicate or uncertain owner. There is no public foreground `watch --attach`.

The persistent Foreman selects its canonical root `agent.json` at launch, including during assisted
setup. There is no empty generated roster and no publication to a runtime copy on finalization.
Python blocks watching until the simple first-setup completion receipt exists. Setup guidance
prohibits delivery while incomplete; a roster is not a sandbox. First-setup checks preserve custom
files, and finalization cannot erase runtime uncertainty or authorize replay.

The extension loads complete child definitions and actual parent membership as a snapshot. Changed
or missing child settings fail before launch until reload; a changed canonical selection cannot
silently retarget a resumed native session. Reload affected parents while idle after all delegated
work has stopped. Native Pi `/reload` also reloads resources and cancels extension jobs, so Factory
must not inject it during a setup tool call. Cancellation alone is not proof that children stopped.

Factory reads root model, effort, cwd, resources and environment at launch. Changes require a
deliberate restart. Selecting the root through `PI_AGENTSHELL_ROSTER_FILE` or `roster_file` only
selects children; it cannot change the running root's own settings. Omitted root cwd inherits the
CLI process cwd; starter coordinators explicitly use `"."`. Worker definitions omit cwd to keep
the assigned worktree. Paths resolve from the owning agent file, not from fixed role names.

The owner must survive loss of init's terminal as well as init exit: isolate its process session and
redirect its standard streams to private runtime files. A bounded startup handshake defines when
ownership transfers from init. Cancellation before transfer cleans up that launch; afterward init
exit leaves it running. Expose the exact Factory invocation used by init to the setup Foreman, so
maintenance from a uvx environment does not accidentally invoke another installed version.
`FACTORY_WORKSPACE` supplies the workspace explicitly; the role cwd is not the factory root.

Use the existing init/watch lease for finalization versus watcher exclusion, and a separate owner
lifetime lock. Status and stop cannot wait on the lease held by the watcher. The owner keeps its
actual child handle and reports starting versus ready honestly. Stops are bounded and may terminate
that known child after graceful cancellation fails, reporting uncertain delivery. Never signal a
PID taken from editable saved state. A free owner lock proves only owner exit, not that its old Pi
has stopped; stale or uncertain terminal identity must not authorize a replacement launch.

A persistent-session send failure stops the watcher and preserves Foreman, but delivery remains
uncertain. It cannot acquire a later acknowledgement once the send failed. Inspect the possible
submission, exit Foreman deliberately and relaunch before restarting watching; finalization does
not clear delivery uncertainty. A still-running send may instead finish and acknowledge normally.
No automatic replay or manual receipt fabrication is allowed.

The controller pins the original live pane worker with a Linux pidfd, then rechecks AgentShell's
public captured target before trusting that handle. It never opens a process handle from saved
state or signals through it. Worker exit allows the controller to release ownership without killing
an unrelated replacement, but does not establish Pi's exit result: saved state remains unknown.
Actual SDK exit or confirmed owned cleanup can record stopped. Offline status explains manual
reconciliation before replacement; normal stopped status does not demand that extra recovery.

A failed SDK wait alone is not proof of exit: closing its ownership channel can stop a live Pi.
Keep ownership and resume the public exit wait after a one-second pause, while the pinned worker
handle independently observes pane loss. This retries only exit observation, never delivery. A
transient query failure leaves watching blocked until deliberate exit/relaunch, even if queries
later recover. No current model, effort or resource inspection is involved.

This local Linux path needs kernel 5.3+ pidfd support. If Python omits `os.pidfd_open`, the typed
stdlib libc fallback needs glibc 2.36+. Unsupported hosts or invalid live capture retain an
uncertain Foreman and refuse watching. Without a validated handle, closing its pane can leave the
owner waiting; resolve the host/capture issue and independently establish process exit before
recovery. Neither a free lock nor failed terminal querying proves exit. No automatic replacement is
allowed.

Cancellation has nested bounds: up to eight seconds to obtain the opening session, then eight for
owned close; the owner permits twenty seconds before bounded escalation, and init waits forty-five
seconds for owner cleanup. Unknown outcomes remain unknown rather than authorizing a new launch.

Keep local control bounded to lifecycle and delivery. No notification queue, automatic replacement,
service-manager integration, native settings observer or new dependency is needed.

### Agent-local skills

Use a directory selected in the agent's `agent.resources.skills`, such as the starter
`.factory/agents/<name>/skills/`. Preserve bundled guidance and user edits. Add
`<skill-name>/SKILL.md` there or select an external file/directory in that same JSON. Init does not
register paths or copy selections into parents. There is no separate refresh command.

Reload affected parent snapshots before new child launches. Restart root Foreman for changes to
its own launch selections; edits beneath already-selected paths remain subject to native reload
behavior. Skill contents and directory membership are not frozen. The harness may reject contents
on load, and Factory must not claim otherwise.

### Downstream apps and skill delivery

The starter Foreman, owner and research agents use Pi; the worker menu offers Pi, Codex and Claude
Code. Later definitions are child-owned and named freely. Native app support, effort, permissions,
continuation and selected-resource support are distinct contracts. Do not infer unsupported native
behavior from the narrower starter menu or invent model selectors.

The owner reads the selected worker's `agent.json` and includes full role/task/worktree/review
context plus absolute skill references and read-before-work instructions. For normalized
Codex/Claude children, extension 1.5 source also supplies deterministic selected-skill references.
It strips only outbound native `skills`; canonical saved selections stay complete. All other
resource options retain their native validation and errors. There is no native registration or
model-compliance guarantee. Factory has not yet adopted a released normalized extension bundle.

Pi accepts native selected skills/extensions; OpenCode accepts native skills/plugins. Claude Code,
Copilot CLI and Cursor have native plugin-directory mechanisms. Codex and Grok reject nondefault
native explicit resource selections in AgentShell 0.5. Native formats differ; prompt-based skill
references do not establish native loading. No blanket all-non-Pi-unsupported rule applies.
OpenCode's individual `SKILL.md` loading still needs native validation, and some apps need optional
effort support beyond the current nonempty normalized field.

Personal native preferences, credentials, tool permissions, Forgetful project requirements and the
agent-driven Foreman -> owner -> worker responsibilities remain unchanged. Native cancellation is
still limited by [agent-shell#28][cancellation]; no workaround is added here.

## Historical pinned-contract findings

The earlier onboarding release check recorded AgentShell 0.5.0 and extension 1.4.2. This section
preserves that version-specific evidence, not a current release or normalized-loading claim.
Factory then bundled extension 1.4.1; those checks used Pi 1.3.0. Extension 1.4.2 treats null
resource/roster arguments as omitted; it does not change the required roster effort field. No
upgrade was made. These are version-specific contracts, not general claims about native apps.

- A launched Pi needs its owner process to remain alive. The long-lived Factory owner retains its
  controller; borrowed attachment cannot transfer ownership. Init exit alone no longer closes it.
- Attachment exposes terminal controls, not readiness or agent exit. The owner can observe actual
  exit through public `terminal.wait()`; attachment must use that owner and its startup evidence.
  It need not observe current model, effort or loaded resources. Their absence from the public
  attachment API is not a blocker, and no live-settings observer is required.
- Automatic user entry requires native tmux client attachment/switching, distinct from notification
  delivery. AgentShell 0.5 has no client-focus method for a new session. Factory uses native tmux
  client commands only for UI entry; message delivery continues through AgentShell.
- Effort support already exists. The narrower mismatch is the extension's mandatory nonempty
  roster effort field: OpenCode/Cursor have launch paths where separate effort must be omitted.
  Optional roster effort needs upstream work; never invent a sentinel value or silently ignore it.
- Selected skill/plugin mechanisms already exist as listed above. OpenCode's individual SKILL.md
  loading still needs native validation. All seven apps list models, but none exposes a public
  per-model effort catalog. That check added no app choices or native-delivery fallback.

Upstream changes require audited adoption. The earlier lifecycle findings do not remove the
normalized extension release and native-validation gates.

Official references used by that historical check:

- [AgentShell 0.5.0 resource contracts][resources]
- [Owned and borrowed terminal examples][terminals]
- [Extension 1.4.2 release][extension-release]
- [Extension roster requirements][rosters]

[resources]:
  https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/development/agent_parameter_comparison.md
[terminals]: https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/examples.md
[extension-release]: https://github.com/ScottRBK/pi-agentshell-extension/releases/tag/v1.4.2
[rosters]:
  https://github.com/ScottRBK/pi-agentshell-extension/blob/v1.4.2/docs/session-rosters.md

## Validation boundary

Earlier init/watch checks used temporary repositories and controlled commands for numbered choices,
provisioning, selections and edit preservation. The earlier isolated native Pi loader checked the
maintenance skill without inference. These results do not prove normalized native loading or that an
agent follows maintenance guidance. Historical evidence is in the [onboarding
record](../plans/agent-onboarding.md); normalized work is tracked in the [agent-definition
plan](../plans/agent-definitions.md). Current native-enabled results and remaining gates are
stated at the top of this ADR.

[cancellation]: https://github.com/ScottRBK/agent-shell/issues/28
