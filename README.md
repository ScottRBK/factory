# Forgetful Factory

A software factory for one repository or a group of repositories, coordinating work tracking,
Forgetful planning, and Pi agents. [FACTORY.md](FACTORY.md) is Scott's intent document; its older
agent configuration fields have not been updated. Current source uses the
[normalized agent definition contract](docs/adrs/agent-definitions.md).

`init` configures the factory and creates missing GitHub labels. `watch` reads matching issues
and saves a Forgetful plan, ownership task and ordinary-issue worktree before notifying the Foreman.
The Foreman launches a feature-owner for clarification, research and task planning. With execution
enabled through `execution_enabled`, the owner also coordinates implementation, independent PR
review and merge.
Deployment and end-to-end verification remain a later slice; live delivery validation is pending.

## Current source and release boundary

Factory source uses one `agent.json` per agent. The approved
[watcher fixes](docs/plans/watcher-problems.md) are implemented. The
[full SonarQube cleanup](docs/plans/sonarqube-remediation.md) has zero outstanding findings and
passes its assigned gate. Combined validation passes 471 tests on each supported Python without
skips. An earlier shutdown timeout remains unexplained after bounded investigation; diagnostics are
improved, but no timeout fix is claimed. Claude Code accepted the code with this limitation.
Changes are integrated locally. Native probes use isolated homes and fake children, without
inference. Recovery still requires user-approved Foreman repair.
Audited uv/build-backend 0.13.5 fixes the earlier checksum defect. Explicit runtime repair still
awaits Scott's decision.

Extension 1.5.0 is published from `5acb6aabfaae7c4d889600f6a5fffbb1c412dc6b`, with exact-commit
hosted CI passing. Factory now includes its independently audited published runtime. Archive
signatures, provenance and source bytes were verified; hide-tools and the SDK lock are unchanged.
The commands below describe the implemented CLI; they do not establish installation readiness.
There is no automatic migration for existing factories, including DinoLand.

## Run locally

Requires Python 3.12+, `uv`, Git, and authenticated GitHub CLI on Linux/WSL. Foreman setup also
needs Pi and tmux. Forgetful access uses its native CLI only. Persistent Foreman sessions need Linux
5.3+ process handles (`pidfd`); Python builds without `os.pidfd_open` also need glibc 2.36+. `uvx`
installs the AgentShell dependency automatically.

The package is not published yet. After the release gates above are complete, the local build and
invocation pattern is:

```bash
uv build
wheel="$(realpath dist/forgetful_factory-0.1.0-py3-none-any.whl)"

# In the same shell, move to your repository or group of repositories
cd /absolute/path/to/workspace
uvx --refresh --from "$wheel" forgetful-factory init
uvx --refresh --from "$wheel" forgetful-factory watch
```

First init provisions the full configured starter team once: Foreman, feature-owner and research,
plus implementation and review when execution is selected. This applies to manual and assisted
setup; `--planning-only` omits the workers. Starter names are templates, not required runtime names.
Factory settings live in `.factory/factory.toml`; each agent owns its choices in `agent.json`.

After configuration is saved, ordinary repeated init preserves all file bytes. It makes no backend
or model-catalog calls, asks no setup questions, performs no synchronization or reconciliation,
and does not consume an optional launch answer. `init --assisted` does not reopen saved setup.
Use explicit `init --finalize` to complete or revalidate incomplete first setup.

Assisted setup opens a dedicated Foreman that stays alive after init exits; its watcher starts
separately. Stopping that watcher leaves Foreman open. Plain `watch` starts and owns a fresh Foreman
and closes it when stopped; it refuses to duplicate an existing or uncertain owner.

Planning safety problems pause affected work and alert Foreman for discussion with the user.
A missing recorded worktree does not terminate the watcher or stop unrelated plans. Safe read-only
rechecks can observe repaired records without an issue edit. Shared failures pause planning;
uncertain writes require reconciliation and are never automatically repeated. Actual connection
loss or uncertain message delivery still stops delivery without replacing Foreman. See the
[problem-handling contract](docs/adrs/watcher-problems.md).

After successful first manual setup, init prints the start command and asks `Launch factory now?
[y/N]:` when run in a terminal. Enter means No. Yes starts ordinary watch, which asks whether to
include existing issues before launching Foreman. Piped input never triggers this launch offer.
Assisted setup and finalization have no extra CLI launch prompt: Foreman starts its watcher from the
same conversation after validation, explicit `/reload` and confirmation of which issues to include.

Printed commands use the current Factory interpreter and an explicit workspace, with paths quoted
for copying. The start command also retains a chosen AgentShell interpreter. Under uvx, that Python
can live in uv's cache; if the cache is removed, use your original wheel/package invocation again.

Only one watcher may run per workspace. Init and watch also exclude each other before reading or
changing setup, so init cannot invalidate a running watcher's readiness. Use `watch --help` through
the same `uvx` command for options, including `--existing`, `--new-only`, and `--interval` (30
seconds). See [architecture](docs/architecture.md) for implemented behaviour and
[plan](docs/plan.md) for progress. Agent definition details and connection choices are below.

## Development

Use uv 0.13.5 or newer. It creates `.venv` and installs the locked runtime and dev dependencies:

```bash
uv sync --locked
uv run --locked ruff check src tests
uv run --locked lint-imports --no-cache
uv run --locked python -m unittest discover -s tests -v
```

Dependencies live in `pyproject.toml`; commit `uv.lock` after reviewed dependency changes.
Dev tools are not installed with the published package. CI runs all three checks on Python 3.12
and 3.13. Tests use external-command fixtures. Lifecycle tests also need installed tmux: they run
real AgentShell in a private tmux server with fake Pi, isolated homes and no service or model calls.
Optional SDK checks load Pi without inference.

## Foreman and Forgetful setup

`init` configures native Forgetful CLI access to a local database or an existing server. MCP
configuration is rejected with correction instructions. Setup provisions Foreman, feature-owner
and research roles. Select an existing Forgetful project or create one during setup. The backend
needs planning enabled and the `external_ref` capability supplied by Forgetful 0.5.5. A new CLI
installation does not upgrade an existing server.

Manual setup offers numbered owner and research model/effort choices; both currently use Pi.
Command-line setup defaults owner model/effort to Foreman's choices unless overridden with
`--feature-owner-model` and `--feature-owner-effort`. Research defaults to the owner; for a fresh
factory, supply `--research-harness pi`, `--research-model` and `--research-effort` to choose
independently. Existing configuration changes require explicit edits. Broader research apps remain
separate Factory integration work; AgentShell's capabilities are wider than this current menu.
`--grill-me-skill /absolute/path/SKILL.md` selects your existing, unchanged grill-me skill;
the default is `~/.agents/skills/grill-me/SKILL.md`. Factory does not download that skill.

### Implementation and review workers

Manual setup configures the implementation and independent review agents after owner and research.
Alternatively choose Foreman-assisted setup and discuss those choices in its terminal. Saved
factories without workers remain planning-only; updating Factory does not enable implementation. Use
`--planning-only` for explicit first-time planning-only setup. Interactive choices are numbered for
Foreman, owner and research model/effort, and worker app/model/effort. There are no skill-path
prompts. Enter the displayed number, not a provider/model name. Command-line options still take
exact native values. Models must be listed in every configured repository; matching catalogs are
reused during that init rather than repeatedly launched.

Execution requires a harness, exact native model selector and effort for both implementation and
review. The starter worker menu offers `pi`, `codex` and `claude_code`. They use their normal native
accounts and permissions; a Pi login does not sign you into Codex or Claude. Listing models does not
verify inference or a model's supported effort. Bundled implementation guidance still requires TDD;
you do not need to supply another skill file to complete setup.

**Check native permissions before using workers.** They need access to the assigned worktree and
its Git metadata, plus network/tool permission for push, CI and GitHub review. A linked worktree's
Git metadata lives in the original repository, outside the worker's cwd. AgentShell 0.5 starts
Codex with `workspace-write` when automatic approval is off; this may not permit the workflow.
Claude's noninteractive tool permissions can also block edits, shell commands or review submission.
Factory does not widen those permissions or enable bypass mode. The owner must report blocked work.
Browser/computer-use tools are not installed by Factory; only available native tools can be used.

For example, add these options to a fresh `init`, replacing the model placeholders:

```bash
--implementation-harness codex --implementation-model NATIVE_CODEX_MODEL \
--implementation-effort high \
--review-harness claude_code --review-model NATIVE_CLAUDE_MODEL --review-effort high
```

At the end, init lists the starter agents' skill folders. Add files as `<skill-name>/SKILL.md`
inside a directory already selected by `agent.resources.skills`, or edit that list to select an
external file or directory. Stop delegated work before reloading affected parent rosters. Restart
Foreman when changing its own launch settings. Init does not register or synchronize skills.
Native harnesses validate skill contents; selecting a path does not prove a model read it.

Explicit `--tdd-skill`, `--implementation-skill` and `--review-skill` options remain available for
first setup; none is required. Implementation/review options are repeatable. Their selections go
into the worker's `agent.json`, not TOML. Factory does not download skills or overwrite repository
instructions. Partial first-time worker app/model/effort choices are an error.

For a later execution change, edit `execution_enabled` in TOML and the relevant agent definitions
and child references. Reconcile preserved guidance that still prohibits implementation or assigns
PR creation to the owner. Stop delegated work, then reload affected parent rosters or restart as
needed. Repeated init does not activate workers, regenerate files or renew a completion fingerprint.
Older formats require explicit reconciliation; there is no automatic migration.

The owner makes a feature-specific plan with actual changes, acceptance criteria and tests. Once
requirements are clear it can proceed; only repository-required approvals or unresolved decisions
need another user response. Workers use the assigned worktree, not the coordinator's role directory.
Implementation owns commits, pushes, opening or reusing the PR, and CI corrections. It can open the
PR before checks that need a PR, but required CI must pass before implementation is complete. The
owner verifies the returned PR and exact-commit evidence, arranges independent review and merges
only when repository gates pass. Draft status follows repository rules and owner guidance; Factory
does not require it. Native tool permissions are not bypassed. Agent review using the author's
account cannot supply a required approval from another GitHub user.

The owner preserves uncertain or unfinished work, and reports merged revisions to the Foreman.
It records worktree removal so watcher restart can distinguish cleanup from missing active work.
Deployment/E2E tasks and the plan stay open. The [delivery ADR](docs/adrs/feature-delivery.md) and
[Slice 6 validation](docs/plans/slice-6.md) describe the implementation boundary and test limits.

### Factory setup and maintenance help

The starter Foreman has a selected `factory-maintenance` skill for configuration, local skills and
setup failures. Ask it for help or use `/skill:factory-maintenance`. It preserves plans, worktrees,
native accounts and user edits; it does not bypass setup validation or widen native permissions.

The root definition must select Foreman's dispatch and maintenance skills and the audited
AgentShell entrypoint under `.factory/resources`. Preserve those selections when editing JSON.
Existing skill contents and `AGENTS.md` files stay editable. Pi or the selected native harness owns
YAML, metadata and duplicate-name validation; successful setup does not prove model advertisement.

Stop the watcher and confirm child agents stopped before changing selections. Add local skills
under a selected directory, or edit `agent.resources.skills` in that agent's definition. Child
settings and parent membership are snapshots: reload every affected parent before new launches.
Changed canonical child selections cannot be used to resume an older selected session. Resource
file contents and directory membership are not frozen by a model/resource fingerprint.

Factory reads the root Foreman's own settings at launch. A change to its model, effort, cwd,
resource selections or launch environment requires a deliberate restart. The extension's roster
selector only selects children; `/reload` does not apply new root launch settings. Init is not a
settings refresh. A plain watcher owns its Foreman; perform restart work from another session.
A persistent Foreman can stop its managed watcher and help edit definitions in the same
conversation.

### Foreman-assisted setup and watcher control

Choose Foreman-assisted in the wizard, or add `--assisted` to first init. It provisions the full
configured starter team and launches Foreman without recording completion or starting issue
processing. Factory sends no opening prompt; ask Foreman to review the team and finish setup.
It selects the canonical root `agent.json`; there is no empty generated runtime roster. Setup
instructions prohibit delivery while incomplete, and Python blocks watching. These instructions
and roster selections are not a security sandbox.

Standalone Foreman commands use the same ownership protections and do not start a watcher:

```bash
forgetful-factory foreman --workspace /absolute/path/to/workspace
forgetful-factory foreman --attach --workspace /absolute/path/to/workspace
```

The first command starts Foreman after completed setup; `--attach` enters its existing terminal.
An existing or uncertain owner blocks a duplicate. Missing or untrusted evidence about an existing
owner never authorizes replacement or replay.

Init enters the new tmux session when possible; otherwise it prints the attach command. Closing
init's original terminal after handover does not close Foreman. Return later with:

```bash
forgetful-factory foreman --attach --workspace /absolute/path/to/workspace
```

`init --attach` remains a compatibility route. With watching and delegated work stopped, complete
or revalidate first setup explicitly:

```bash
forgetful-factory init --finalize --delegated-work-stopped --workspace /absolute/path/to/workspace
```

Foreman uses the exact Factory invocation passed in `FACTORY_COMMAND` and the workspace in
`FACTORY_WORKSPACE`, rather than an unrelated installed version or its role folder as the workspace.
Finalization preserves configuration comments, edited role files and the existing Foreman. Failed
first-setup checks leave watching blocked. It never clears lost-send or ownership uncertainty. Older
testing instructions may need reconciliation; no automatic migration or
instruction overwrite is provided.

After successful finalization, use Pi **`/reload` while idle** in the same Foreman. This loads the
current child definitions and parent membership without replacing the conversation. Reload also
stops extension jobs, so confirm all delegated runs have stopped first. Additional top-level Foreman
resource paths or environment changes still require a deliberate restart; `/reload` does not adopt
new launch arguments.

Then you or Foreman can control its watcher:

```bash
forgetful-factory watch --start --new-only --workspace /absolute/path/to/workspace
forgetful-factory watch --status --workspace /absolute/path/to/workspace
forgetful-factory watch --stop --workspace /absolute/path/to/workspace
```

Use `--existing` instead of `--new-only` to forward existing matches. Status/stop do not need the
watcher's exclusive lease. A duplicate start is refused. Foreman exit stops its watcher; uncertain
owner or terminal state does not start a replacement. A forced watcher stop reports delivery or
external-work uncertainty. It never uses a saved PID to kill an unrelated process.

If terminal submission fails, Foreman stays open but the message may already have arrived. Inspect
its pane, then deliberately exit Foreman and relaunch before starting another watcher. Rerunning
finalization does not clear a failed delivery; Factory does not automatically resend it.

Closing the original pane ends its owner, but without Pi's exit result the saved state remains
`unknown`. `watch --status` explains recovery: independently confirm the original Foreman and owner
have exited before archiving only `owner.json` and `control.sock` in `.factory/runtime/foreman`.
A normal Pi exit allows relaunch without that reconciliation. Failed process-handle capture instead
preserves Foreman and blocks watching; fix the reported host/capture problem before retrying. A
transient terminal-check failure also blocks watching until a deliberate exit and relaunch.
Factory does not infer exit from a failed tmux query or signal PIDs read from saved state.

The managed watcher connects to the persistent owner's existing AgentShell delivery channel. It
checks saved setup, readiness and liveness, not live model/effort/resources. General attachment to
arbitrary running terminals is deferred. The worker menu remains Pi, Codex and Claude Code;
AgentShell already supports wider skill/plugin and effort mechanisms, but broader Factory app
integration is separate. See [agent onboarding](docs/adrs/agent-onboarding.md) for contracts and
validation limits.

### Shared Pi profile

Owner research delegation needs `max_sub_agent_depth` at least 1 in the shared Pi home's
`extensions/agentshell.json`. Review that native preference yourself: it affects your other Pi
sessions too. Factory checks it but never changes it. Run Factory from a normal shell, not from
inside a Pi subagent.

Factory uses your **normal native Pi home**, defaulting to `PI_CODING_AGENT_DIR` or `~/.pi/agent`.
`--pi-agent-dir /absolute/path` chooses another normal home. Init explains and requests consent
before invoking Pi there. `--share-pi-profile` supplies that consent for noninteractive setup.
Declining stops setup. The chosen directory and consent are saved in `.factory/pi-profile.json`;
watch uses that saved choice even if the environment later changes.

This shares the **whole Pi profile**, including native login, settings, trust and session state. The
starter Foreman definition excludes your personal `SYSTEM.md`. `AGENTS.md`, `APPEND_SYSTEM.md`, and
other native instructions may still load. This is not full instruction isolation. AgentShell
extension configuration and the hide-tools preference also use that shared home; native user toggles
can change shared preferences. Nothing copies or links credentials. Model listing follows native Pi
resource behavior: it can still read personal `SYSTEM.md` and execute resources from that profile or
repository. The exclusion applies to Foreman launch, not model listing during setup; this is not
auth-only isolation.

An explicitly chosen home must already exist. Factory does not create a missing Pi home. If your
default home is absent, consented executable installation can finish, but setup stays incomplete:
initialize your normal native Pi home and `/login` in another terminal. Before configuration is
saved, retry the original init arguments. After it is saved, use explicit `init --finalize`.
Correct mistyped paths before proceeding. If consent names the wrong home, review only
`.factory/pi-profile.json` and explicitly approve the corrected home through that setup path;
never delete native login state.

First init uses AgentShell's public model list and shows numbered choices grouped by provider.
Supply `--foreman-model` with an exact listed `provider/model` string to select noninteractively.
Listing only establishes that a model is selectable; access remains unverified and no model request
is made. A supplied model is validated before labels or factory configuration are written. If setup
stops before configuration is saved, repeat your original init arguments when retrying. If there are
no models, open Pi in the displayed home in another terminal, use `/login`, then choose recheck or
rerun init. Factory does not perform model login or refresh credentials itself.

```bash
forgetful-factory init --repo /path/to/repo --label factory \
  --foreman-model provider/model --foreman-effort high --share-pi-profile --planning-only \
  --forgetful-instance local --forgetful-project 12 --install-role-runtime \
  --grill-me-skill /path/to/grill-me/SKILL.md

# Remote Forgetful checks can start the server's OAuth flow
forgetful-factory init --repo /path/to/repo --label factory \
  --foreman-model provider/model --foreman-effort high --share-pi-profile --planning-only \
  --forgetful-instance server --forgetful-server https://memory.example/mcp \
  --forgetful-project 12 --install-role-runtime \
  --grill-me-skill /path/to/grill-me/SKILL.md
```

Replace `12` with an existing project ID visible to your native Forgetful login. Without
`--forgetful-project`, init lists existing projects and offers `c` to create a new one. If the list
is empty, it offers creation directly. Enter a name or accept the suggested workspace name, then
confirm. Factory creates a development project with a short default description and saves its ID.
One project can cover the whole Factory workspace, including multiple repositories. There is no
skip option because Forgetful plans require a project.

Declining creation leaves setup incomplete without creating a project. If creation fails or you
interrupt it, the project may already exist: rerun init and check the list before creating another.
Factory never retries creation automatically. A created project is retained if a later setup step
fails. Watch checks project access and planning tool permissions before starting Pi. Forgetful 0.5.5
has no stable user ID in its response; Factory verifies access under the shared CLI scope instead.

Local mode uses the absolute `.factory/data/forgetful.db` SQLite path. Override it with
`--forgetful-database /absolute/path/memory.db`; no HTTP service is needed. `[forgetful]` in
`.factory/factory.toml` records the target, executable and project ID. Local planning is enabled
by Factory; a remote server must enable it independently. Remote servers require HTTPS except on
loopback/localhost. URLs with credentials, query strings, or fragments are rejected.
`--forgetful-executable` accepts an existing native executable, including paths with spaces.

### Agent files and shared state

`factory.toml` contains repository, watcher and Forgetful settings, `execution_enabled`, and
`foreman_agent_file`. It contains no duplicate agent models, efforts, harnesses or skill lists.
The Foreman path is relative to the TOML directory or absolute. A starter reference is:

```toml
foreman_agent_file = "agents/foreman/agent.json"
execution_enabled = false
```

Each agent file has exactly two sections. `agent` requires `name`, `description`, `agent_type`,
`model` and `effort`; `cwd` and `resources` are optional. `roster` contains `enabled` and a `roles`
list of references. For example, a parent can select an owner with:

```json
"roster": {
  "enabled": true,
  "roles": [{"agent_file": "../feature-owner/agent.json"}]
}
```

This is a section of an agent document, not a complete file. Each child owns its name and settings;
parents supply no aliases or overrides. Paths resolve lexically from the containing agent file,
using relative or absolute local paths. Loading follows one hop at a time. The root must select Pi.
Pi children use their own file as their child-roster source; non-Pi leaves require a disabled, empty
roster.

Starter coordinator definitions set `cwd` to `"."`, so native `AGENTS.md` loads from their agent
folders. An omitted root cwd inherits the Factory CLI process cwd, not the agent file's directory
or `--workspace`. Worker definitions omit cwd to preserve the owner's assigned worktree. Resource
paths are relative to their agent file even when cwd differs. A definition can move independently
of its resources and working directory if its references remain correct.

The starter Foreman selects feature-owner; owner selects research and any configured workers.
Names may be changed or added later. Dispatch still follows Foreman -> owner -> worker, with full
role, task, worktree and review context. There is no Python worker controller. The owner reads the
selected worker definition and supplies absolute selected skill references with read-before-work
instructions. For normalized Codex/Claude children, extension 1.5 source also supplies deterministic
skill references and strips only outbound native `skills`; the saved canonical selection remains
complete. This is prompt guidance, not native skill registration or proof of model compliance.
Pi and OpenCode retain native selected-skill support; other resource options retain native checks.
This extension behavior remains subject to the release gates above.

Foreman's instructions ask it to read its preserved `APPEND_SYSTEM.md`; it is not sent as an opening
prompt. Watch sends no opening model prompt. The first notification or user input can incur usage.

The root JSON owns resource policy. Starter Pi definitions disable automatic personal/project
resources, native MCP and home `SYSTEM.md`, while keeping native instructions enabled. Omitted
flags use native defaults. Personal append/context files and native settings can still apply.
AgentShell 0.5 rejects interactive launch with home-system exclusion when cwd contains
`.pi/SYSTEM.md`; Factory preserves it and reports the conflict. No remote package auto-install or
custom Factory launcher is used.

Shared state is separate from agent names: `.factory/pi-profile.json` records consent and the Pi
home; `.factory/setup-complete.json` records only `{"complete": true}`; `.factory/resources/` holds
audited shared resources. The receipt is not a model/resource fingerprint. There is no generated
runtime roster copy or skill-registration sidecar. Owner/control state remains under
`.factory/runtime/foreman`. Native credentials and settings are preserved.

Existing edited instructions, old profile files and credentials are not deleted or migrated.
Known obsolete guidance and altered audited runtime bytes need explicit reconciliation. Old
`resources.json`, `roster.json` and `model-selection.json` belong to the superseded design; do not
regenerate them or treat them as current settings. Existing/DinoLand factories are not automatically
converted. Changing a completed factory's definitions does not require init. If first setup was
saved but incomplete, use `init --finalize` after correcting it; if configuration was never saved,
retry the original init arguments.

Watcher, Foreman and owner share native Forgetful CLI state under
`.factory/cli-config`. `FACTORY_FORGETFUL_DIR` selects `.factory` as command cwd, with
`XDG_CONFIG_HOME="$FACTORY_FORGETFUL_CONFIG_DIR"` for that command only. The inherited
`FACTORY_ROLE_DIR` compatibility variable does not identify a child role.
`PI_CODING_AGENT_DIR` always identifies the shared Pi home; it is never the Forgetful auth path.
The surrounding shell and `gh` configuration remain unchanged. Local mode supplies an explicit
empty `FORGETFUL_SERVER`; remote mode supplies the chosen URL. `FORGETFUL_TOKEN` is removed from
the launch environment. There is no wrapper, alias, custom tool, or command forwarding layer.
Arbitrary agent commands must follow the skill to retain these configuration boundaries.

First setup and explicit `init --finalize` check Forgetful connectivity, project access and planning
support before recording completion, for both local databases and servers. Ordinary repeated init
makes no backend calls. Server checks reuse native saved credentials and may open browser sign-in.
Failed or cancelled first-setup checks keep saved work, with watching blocked until finalization.
The old `--check-connection` flag is accepted but no longer needed.
The check uses two CLI calls: selected project and the permitted tool catalog.
Project access also verifies the connection and native login; preflight needs no user-profile
request or separate process per planning tool. Agents may request user context separately.

The browser notice appears only when the server's public `/api/v1/auth/info` reports OAuth.
Other modes or unavailable metadata do not show it. Metadata only controls this notice; the native
CLI still owns authentication and the access check always runs.

`--login` during first init or `init --finalize` explicitly runs native
`forgetful auth login --server` before the final access check.
It signs in to Forgetful, not Pi, and saves login state in the Factory's CLI scope above. It is
optional; normal setup already checks access. Native `auth status` and `auth logout` keep their
own syntax, without a target flag. Restart the Foreman after changing connection settings.

Watch checks saved consent, completion, selected resources and runtime metadata before polling.
It then checks Forgetful planning access through the native CLI. This can refresh credentials or
open browser login in an attended run. Ctrl-C cancels; timeouts/failures preserve saved work.
Watch does not list models or test model-provider access. Session readiness does not establish a
successful model response; terminal submission does not prove an agent acted on an issue.

An ordinary issue gets a branch/worktree under `.factory/worktrees/`. Add the extra `epic` label
for work spanning repositories: the owner chooses the affected repositories and records their trees.
Existing valid plans/tasks/trees are reused. Incomplete first-time setup needs user-approved
Foreman completion; the watcher only observes the repair. Duplicate ownership or mismatched trees
block affected work and alert Foreman. Uncertain writes pause planning until reconciliation and a
deliberate restart. None of these safety conditions terminates supervision or permits work reset.

Issue edits produce notifications with the same saved IDs. Restart sends unfinished plans again,
including closed issues. `--new-only` still sends updates to recovered work while baselining other
open matches. Foreman must check ownership before dispatching; duplicate notifications are possible.
A missing job record or session ID does not prove the owner stopped. Unknown liveness leaves work
pending. See [planning and recovery](docs/adrs/issue-planning.md) for the exact limits.

AgentShell also writes a resource-selection digest under `$XDG_STATE_HOME/agent-shell/resources`
(default `~/.local/state/agent-shell/resources`). That local state record can remain after a
session ends; it records a digest rather than resource contents or credential values.

Init provisions pinned AgentShell and hide-tools extensions; `/hide-tools` changes terminal display.
The current bundle contains audited AgentShell extension 1.5.0; its independent worker uses
AgentShell 0.5.0. Normalized native loading is tested without inference. Its real
Python environment requires installation consent (`--install-role-runtime`), using
existing uv >=0.13.5 and Python. No background-memory or custom Factory Pi extension is installed.
Generated ignore rules protect runtime and credential paths without weakening existing exclusions.

Missing executables require consent. Pi 1.2.0 can be installed into `.factory/runtime/pi` using
existing Node 22.19+ and npm, with a reviewed npm lock and scripts disabled. Forgetful 0.5.5 can be
installed as the **Forgetful CLI** into `.factory/runtime/forgetful`, with frozen hashes and wheels
only. It does not start another server. The installer checks uv and selects an already installed
Python 3.12 before asking permission; Factory itself can run under Python 3.13 or later. Missing
prerequisites give retry guidance, without downloading Python or changing existing installations.
Ubuntu 24.04 amd64 supports a pinned tmux 3.4-1ubuntu0.1 APT installation, after a
simulation confirms no upgrades/removals; this requires system privileges. Other hosts/custom
executable paths require manual installation. Existing installations are never upgraded.
Bundled provenance and installation constraints are in
[role resources](src/forgetful_factory/resources/ROLE-SOURCES.md). The original Slice 3 installation
audit document is absent from this working copy. The separate
[AgentShell 0.5.0 audit](docs/plans/agentshell-0.5-audit.md) covers only the launcher upgrade.

Pi's fallback binary downloads and local Forgetful embedding-model downloads default to offline
mode. Provision reviewed models separately before local setup, and set `FASTEMBED_CACHE_DIR` to an
existing cache if needed. A cold cache produces an incomplete connection check, not a readiness
claim. These defaults do not block model-provider calls for conversations, but `PI_OFFLINE` also
stops automatic model-catalog/provider-list refresh, update checks, and telemetry. New or account-
specific models may therefore be absent. Refresh the shared native Pi catalog outside the watcher
with Pi's `update --models` command and `PI_OFFLINE` unset, or configure the shared home's
`models.json`. Setting `PI_OFFLINE=0` is not a reliable opt-out in Pi 1.2.0.

Most tests use controlled external commands and temporary Git repositories. Optional native tests
can load an isolated Pi SDK without inference. Normalized loading still needs the audited released
bundle and successful native checks; the earlier checks do not establish that result:

```bash
NATIVE_PI_SDK=/absolute/pi-coding-agent/dist/index.js \
  uv run --locked python -m unittest discover -s tests -v
```

The [Slice 4/5 record](docs/plans/slices-4-5.md) distinguishes command-fixture tests, actual local
Forgetful checks, and isolated Pi loading/lifecycle checks. These do not prove autonomous owner
planning, live OAuth refresh or model-provider access. The earlier
[CLI onboarding record](docs/plans/cli-onboarding.md) retains the Slice 3 smoke evidence.
Never point test probes at a personal Pi profile.

Native cancellation remains limited by [agent-shell#28][native-cancellation]. This change adds no
workaround and does not turn cancellation into proof that delegated work stopped.

[native-cancellation]: https://github.com/ScottRBK/agent-shell/issues/28
