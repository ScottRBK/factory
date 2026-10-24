# Role resources, shared Pi login and Forgetful CLI

Status: Factory uses [normalized agent definitions](agent-definitions.md) and audited extension
1.5.0. Native SDK loading and controlled worker probes pass without inference. Shared Pi consent,
resource checks and native Forgetful access remain; runtime repair policy and final checks are open.
See [current release limits](../../README.md#current-source-and-release-boundary).

[CLI onboarding](../plans/cli-onboarding.md), [Slice 4/5](../plans/slices-4-5.md) and
[Slice 6](../plans/slice-6.md) retain historical validation. They do not establish normalized native
loading or migration success.

Back to [architecture](../architecture.md).

## Context and responsibility

The watcher prepares plans and ordinary-issue worktrees, then notifies the Foreman. The Foreman
alone dispatches feature-owners. An owner conducts grill-me, may launch research agents, and
prepares the task plan. Slice 6 adds optional implementation/review workers; its validation is
recorded separately in [Slice 6](../plans/slice-6.md).

Initialization uses application ports. The profile adapter prepares editable resources, delegates
host provisioning and native Forgetful commands, and uses a process boundary for AgentShell model
discovery. CLI gathers consent and selections. Domain/application code remains independent of Pi,
AgentShell, concrete installers and token stores. See [issue planning](issue-planning.md) for
ownership and recovery rules.

## Why the approach changed

Separate role directories moved model-provider credentials away from the user's existing Pi login.
AgentShell 0.5.0 now selects local resources per session without changing the native Pi directory.
However, its Pi adapter excludes personal and project resources together and requires native MCP
to be disabled in that mode. Pi's CLI does not expose strict per-session MCP configuration while
retaining the normal authentication directory. [AgentShell #27][mcp-gap] was closed after that
feasibility review; an SDK wrapper was not adopted.

Scott chose native Forgetful CLI access for now. Docker is a separate future investigation, not
part of this implementation. The change supersedes Slice 3's MCP default and separate Pi login.
The existing `method` field remains but accepts only `cli`; old MCP configurations fail explicitly
rather than being silently converted. Local and existing-server instances remain supported.

## Shared Pi home and consent

Initialization asks before invoking Pi in its chosen normal agent directory. The default follows
`PI_CODING_AGENT_DIR`, otherwise `~/.pi/agent`; `--pi-agent-dir` selects it explicitly.
`--share-pi-profile` supplies noninteractive consent. Saved consent identifies that directory;
subsequent environment changes must not silently select another login store. Consent is saved in
`.factory/pi-profile.json`, independently of the root definition's name or location.

This shares the whole native Pi profile, not one provider credential. Native provider environment
credentials remain inherited after consent. Native settings, models, `APPEND_SYSTEM.md`, and
ordinary instruction files can participate. The starter root definition excludes personal
`SYSTEM.md`; its JSON owns that policy and omitted resource flags retain native defaults. This is
not complete instruction isolation. Login/logout, OAuth refresh, trust decisions and native session
storage remain Pi-owned. The selected upstream extensions also use native home state: hide-tools
preferences and AgentShell extension configuration are shared. AgentShell writes resource-selection
records in its normal state directory. Resource selection is not a host sandbox or an account
boundary.

No credentials are copied, symlinked, printed, or written into Factory configuration. Factory
never asks for a token value. Missing model login is handled through native interactive Pi
`/login` in the chosen home, followed by rechecking setup. This is distinct from Forgetful login.
The Factory does not invent a standalone `pi auth login` command.

Model discovery uses AgentShell's public `list_models` and preserves its exact selectors.
CLI groups Foreman models by provider and uses numbered model/effort choices. Implementation and
review also use numbered app/model/effort choices, preserving the exact returned selectors.
Listing follows Pi's native behavior and may load
personal resources or resolve configured keys; it does not use the launch resource filter.
It can still read home `SYSTEM.md` during setup: home-prompt exclusion applies only to Foreman
launch. The public listing API has no resource filter; do not claim complete instruction exclusion.
A selected or configured model is not proof of endpoint access, quota, OAuth refresh, or inference.
Setup does not make a test model request. Live provider validation requires separate consent.

## Role resources and launch

The first init creates the configured starter team under `.factory/agents/`: Foreman, feature-owner
and research, plus implementation/review when enabled. Manual, assisted and planning-only routes
use the same one-time provisioning. Starter names and locations are templates, not runtime limits.

Each `agent.json` owns `name`, `description`, `agent_type`, `model`, `effort`, optional `cwd` and
`resources`. Its `roster.roles` entries contain only `agent_file` references. Child settings and
names are never copied into parent entries. TOML contains Factory settings and `foreman_agent_file`,
not agent model/effort/harness/skill fields. Execution permission remains a separate Factory
setting.

References use lexical relative or absolute local paths from the containing agent file. Each file
loads one hop of children. Resource paths and cwd belong to the agent that declares them. An agent
file can move without moving resources or cwd if references are kept correct. Non-Pi agents are
leaves with disabled, empty rosters. The normalized extension selects a Pi child's own agent file
as its roster source. Selecting a root file through `PI_AGENTSHELL_ROSTER_FILE` selects its children
only; Factory reads the root's own settings before launch.

Starter coordinators set `cwd: "."` so native `AGENTS.md` supplies their role instructions. Those
folders are working directories, not login stores. An omitted root cwd inherits the CLI process
cwd, which can differ from `--workspace`. Worker cwd is omitted so the owner can assign a worktree.
Repository/ancestor and personal instructions can still apply. Agents read repository instructions
before working there. Foreman also reads its preserved `APPEND_SYSTEM.md`; this is not a native
append-system argument. The owner explicitly reads its selected, unchanged grill-me skill because
that skill disables automatic model advertisement.

The starter Foreman references feature-owner; owner references research and any configured workers.
Research and workers have disabled child rosters. Browser tools are not provisioned for research;
its guidance reports missing tools. Foreman's dispatch and maintenance skills and audited
`.factory/resources/agentshell/extensions/agentshell.ts` entrypoint remain required; hide-tools is
optional. Factory checks required paths and runtime integrity. Native harnesses own YAML, metadata
and skill-name validation.

Starter Pi resource policies disable automatic personal/project resource discovery, native MCP and
home `SYSTEM.md`, keep ordinary instructions enabled, and select no remote packages/plugins. The
JSON is authoritative; omitted flags use native defaults. `APPEND_SYSTEM.md` remains separate.
AgentShell 0.5 rejects interactive home-system exclusion when Foreman's cwd contains
`.pi/SYSTEM.md`; Factory preserves the file and reports the conflict. Resource selection is not a
sandbox or a prohibition on ad-hoc delegation through Bash.

Add skills under a selected directory or edit the owning definition's `agent.resources.skills`.
Parent membership and child settings are complete snapshots from extension load. Reload affected
parents for new launches; changed canonical selections fail selected-session resume. Root model,
effort, cwd, resource selection or environment changes require restart. Neither init nor the roster
selector updates a running root's launch settings. Skill contents and directory membership are not
frozen. There is no registration sidecar, generated runtime roster or model/resource fingerprint.
See [onboarding](agent-onboarding.md) for lifecycle and maintenance limits.

Watch starts Foreman without an opening model prompt. The native role instructions are present
when the first notification or user input starts a turn. Handling work can incur provider usage;
readiness alone still does not prove a model response.

The shared Pi setting `max_sub_agent_depth` must be at least 1 to allow owner research delegation.
Factory checks it without modifying personal preferences or resetting inherited ancestry. Launch
from inside a Pi subagent is rejected. No roster field can override the native depth policy.

Only selected upstream extensions are provisioned. There is no Factory status/auth extension,
replacement Pi executable, Forgetful wrapper, or remote-package auto-install.

## Optional implementation and review workers

First-time worker app/model/effort choices are all-or-none; `--planning-only` omits both workers.
The setup menu currently offers Pi, Codex and Claude Code for workers, with Pi coordinators and
research. This menu is narrower than AgentShell's native capabilities. Later names and definitions
are editable; execution still requires explicit `execution_enabled` permission and suitable agents.
Skill paths are not requested in the wizard. Explicit TDD/implementation/review paths remain
optional initial choices and are saved in each worker's `agent.resources.skills`. Bundled guidance
requires TDD even without an additional TDD file.

Workers omit cwd so the owner's call supplies the assigned worktree and its repository instructions.
The owner reads each selected definition and supplies the full role, task, worktree and review
briefing, plus absolute selected skill references and read-before-work instructions. Workers remain
agent-driven; Python does not launch or control them.

For normalized Codex/Claude children, extension 1.5 source additionally supplies deterministic skill
references, then removes only native `skills` from the outbound request. The canonical saved
selection stays intact; other resource options retain native validation and errors. This is prompt
skill delivery, not native registration or proof the model follows instructions. Pi and OpenCode
retain native selected-skill support. Factory's audited 1.5.0 bundle passes real SDK/fake-native
checks for these references and native resume, without claiming model compliance.

Exact initial selectors come from each chosen harness's catalog in the configured repositories.
Effort vocabulary is checked per harness; listing does not prove model-specific effort, live access
or tool permissions. Catalog results are reused only during first setup. Repeated init and watch
do not list models. Later edits do not renew a settings or skill-byte fingerprint. See
[delivery](feature-delivery.md) for permissions and selected-session resume limits.

### Superseded selection synchronization

Earlier slices saved `resources.json` and inline `roster.json` beside role instructions. Completion
bound settings and skill bytes; init registered local skills and used a recovery receipt for partial
updates. This kept duplicated parent/child selections consistent, but made ordinary edits depend
on rerunning setup. [Normalized definitions](agent-definitions.md) replace that design with
child-owned settings and reference-only parent entries. The earlier validation records describe
that previous design; they are not instructions to regenerate those files.

## Provisioning and editable files

The top-level Factory dependency is pinned to AgentShell 0.5.0 following its
[supply-chain audit](../plans/agentshell-0.5-audit.md). Pass already-provisioned local resources;
do not use AgentShell's automatic remote-package installer. The bundled extension's independent
Python worker uses the audited 0.5.0 lock. The current 1.5.0 bundle supports normalized references
and preserves inline/ad-hoc behavior. Its published bytes passed independent artifact audit before
adoption. Bundled bytes and the installed runtime must match reviewed inputs; a stale or edited
runtime does not count as ready.

Role guidance and initial definitions are create-only and reject symlink destinations. Ordinary
repeated init preserves all file bytes and does not scan, register or reconcile selections. Bundled
upstream bytes are checked against per-file hashes before copying missing files during provisioning.
User edits are preserved. Obsolete instructions require explicit reconciliation. Shared resources
live in `.factory/resources`, separate from agent names. There is no migration framework for
existing factories, including DinoLand.

Missing Pi, tmux, Forgetful and the extension worker require installation consent. Existing
executables are not upgraded. Supported recipes retain frozen dependency metadata, wheel-only
Python installation and the reviewed distro transaction. Worker setup uses a real virtual
environment and verified temporary uv project, not a Python-path stub. Setup requires existing
reviewed uv >=0.13.1 and never upgrades it implicitly. Forgetful's reviewed lock still targets
Python 3.12, but its installer selects a compatible existing interpreter independently of the Python
running Factory. Read-only prerequisite checks precede installation consent. Discovery and setup
forbid Python downloads; package hashes and binary-only installation remain enforced.

Managed installations require successful-sync evidence and bounded executable/import checks;
an existing directory alone is insufficient. Failed provisioning leaves setup incomplete.
Ignore rules exclude generated local state and credentials, never undo user exclusions, and
cannot protect arbitrary secrets placed in editable files or remove already tracked files.

## Forgetful CLI connection and credentials

The `[forgetful]` configuration identifies `method=cli`, `instance`, `executable`, and either an
absolute SQLite `database` path or a `server` endpoint, plus an existing numeric `project_id`.
Remote URLs require HTTPS, except loopback HTTP, and reject embedded credentials, query strings and
fragments. Local access needs no server; remote CLI commands use the server's MCP interface without
requiring Pi's MCP extension.

Watcher, Foreman and owner use `.factory` as the native CLI command cwd and `.factory/cli-config`
as its configuration scope. These paths are independent of agent names and working directories.
Native login/refresh state and credentials remain CLI-owned; older factories are not migrated.
`FACTORY_FORGETFUL_DIR` identifies the safe command cwd; `FACTORY_FORGETFUL_CONFIG_DIR` identifies
its CLI settings directory. `FACTORY_FORGETFUL_PROJECT_ID` carries the selected project.
`FACTORY_ROLE_DIR` remains a compatibility variable and does not identify a child role.

Launch supplies native `FORGETFUL_SERVER` and local database settings. Local mode explicitly sets
an empty server value so saved remote defaults cannot take precedence. Inherited `FORGETFUL_TOKEN`
is removed. Custom executable paths are resolved before changing working directory.

The skill invokes the actual Forgetful executable from `FACTORY_FORGETFUL_DIR` with a per-command
`XDG_CONFIG_HOME="$FACTORY_FORGETFUL_CONFIG_DIR"`. This scopes Forgetful settings and credentials
without redirecting `gh` or other tools. The cwd prevents repository `.env` or `docker/.env` files
from selecting another Forgetful target. Credential isolation is supported on Linux/WSL only.
`auth login` takes a server flag; `auth status` and `auth logout` retain their own native syntax.

Factory's checks use the same scoped environment and cwd. Arbitrary agent shell commands are not
intercepted: omitting these instructions can read personal/repository configuration. This remains
an explicit limit of direct CLI access, not an enforced credential boundary. Shared-target changes
require a Foreman restart because commands inherit launch-time settings.

## Readiness and delivery limits

First setup and explicit `init --finalize` check the configured Forgetful connection, project access
and planning support before saving `.factory/setup-complete.json` as `{"complete": true}`.
Consent/home and this simple initial-completion receipt are separate. Ordinary repeated init makes
no backend/catalog calls and consumes no setup or launch answers. The earlier server-only opt-in
made an otherwise valid setup fail at the last step; Scott chose automatic checks for both local and
server mode. The legacy `--check-connection` flag remains accepted for command compatibility but
changes nothing in those setup checks. `--login` remains an optional explicit native sign-in before
the final check, not a requirement for using saved credentials. Server checks can open browser
sign-in. Failure or cancellation leaves configuration available for explicit first-setup
finalization; incomplete first setup still blocks watching. Credentials stay CLI-owned.

Init shows the browser notice only for a public policy response with `authEnabled=true` and
`authMode=oauth`. The Forgetful adapter reads `/api/v1/auth/info` directly, without launching the
CLI or sending credentials. It retains an application prefix before `/mcp`; a custom endpoint
whose application prefix is unknown is not probed. The request uses verified HTTPS where configured,
a two-second socket timeout and an 8 KiB response cap. It follows no redirects or returned login URL
and does not read proxy settings. Disabled/JWT/introspection, unknown, malformed or unavailable
metadata suppress the notice. This is advisory only: native access checks still run and own auth.

Watch validates consent, setup completion, role selections, depth and runtime metadata before
starting Pi. It then checks the selected Forgetful project's planning access through the native
CLI. Scott accepts browser login/refresh from an attended watcher. Cancellation and timeouts
preserve saved plans/worktrees; Factory never reads credential values or treats cache presence as
proof of access. The exact permission/schema checks are described in [issue
planning](issue-planning.md).

Model listing and inference remain absent from watch preflight. AgentShell's session-ready event
proves startup, and terminal submission proves only delivery to the terminal. Neither proves that
a model authenticated or acted on a notification. Pending plans survive; a restart sends them again.

Pi management/catalog downloads default offline; local Forgetful models use cache-only operation.
This does not prohibit intentional inference, OAuth or extension commands. Live authentication,
concurrent refresh and autonomous owner planning require separate evidence.

[mcp-gap]: https://github.com/ScottRBK/agent-shell/issues/27

Native cancellation remains subject to [agent-shell#28][cancellation]. No workaround is added;
cancellation alone is not proof that delegated work stopped.

[cancellation]: https://github.com/ScottRBK/agent-shell/issues/28
