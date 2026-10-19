# Role resources, shared Pi login and Forgetful CLI

Status: shared Pi setup, coordinator roles and optional worker setup implemented and locally tested.
See [CLI onboarding](../plans/cli-onboarding.md) for the earlier setup checks and
[Slice 4/5 validation](../plans/slices-4-5.md) for the current role integration.

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
subsequent environment changes must not silently select another login store.

This shares the whole native Pi profile, not one provider credential. Native provider environment
credentials remain inherited after consent. Native settings, models, `APPEND_SYSTEM.md`, and
ordinary instruction files can participate. Foreman launch now excludes personal `SYSTEM.md`,
correcting the mismatch Scott found during onboarding. This is not complete instruction isolation.
Login/logout, OAuth refresh, trust decisions and native session storage remain Pi-owned.
The selected upstream extensions also use native home state: hide-tools preferences and
AgentShell extension configuration are shared. AgentShell writes resource-selection records in
its normal state directory. Resource selection is not a host sandbox or an account boundary.

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

Each role has a directory under `.factory/agents/`: `foreman`, `feature-owner` and `research`.
These are working directories, not Pi login directories. Native `AGENTS.md` supplies role
instructions because Pi starts in that directory. Repository/ancestor and personal instruction
files can still apply. Agents read the relevant repository instructions before working there.

- `resources.json` selects existing local skills/extensions, relative to the role or absolute.
  Repository resources require explicit selection; remote packages are not allowed.
- `AGENTS.md` introduces the role and points to its skill. Foreman also reads its preserved,
  editable `APPEND_SYSTEM.md`. That file is not automatically a native append-system file.
- The owner's unchanged grill-me skill is selected by `grill_me_skill`. Its explicit read is
  required because the skill disables automatic model advertisement.
- `roster.json` describes children: Foreman selects feature-owner; owner selects research.
  Research has an explicit disabled roster and currently accepts no extensions. Omission would
  allow fallback to a personal roster, so every selected Pi role has a roster file. Browser tools
  are not provisioned for research in this slice; its guidance reports unavailable tools.

The roster entry fixes the child's Pi model, effort, cwd and resources. Owner defaults to Foreman's
model/effort; init accepts separate owner choices. Research defaults to the owner or uses its own
explicit Pi model/harness/effort settings. Roster and resource selections are checked against
configuration and recorded with setup completion. Init registers readable role-local skill files
and records its automatic additions for bounded removal/rename and interrupted-write recovery.
Native harnesses validate skill contents; Factory does not parse YAML or resolve skill names.
Conflicting manually edited selections require explicit reconciliation, not silent replacement.
Foreman's dispatch and factory-maintenance skills and AgentShell extension are mandatory;
hide-tools is optional.
The [maintenance skill and onboarding ADR](agent-onboarding.md) explains setup advice, preserved
selections, stopped-session requirements and the still-pending Foreman-first setup flow.

For these Pi coordinator/research roles, both automatic inheritance flags are false,
packages/plugins are empty, native MCP is disabled,
and ordinary instruction files remain enabled. `include_home_system_prompt=False` excludes
personal `SYSTEM.md` while retaining Pi's built-in prompt. `APPEND_SYSTEM.md` remains independent.
AgentShell 0.5 rejects the interactive combination if the Foreman's launch directory contains
`.pi/SYSTEM.md`; init/watch stop and preserve that file. Ordinary tools are still available;
resource selection is not a sandbox or a prohibition on ad-hoc delegation through Bash.

Watch starts Foreman without an opening model prompt. The native role instructions are present
when the first notification or user input starts a turn. Handling work can incur provider usage;
readiness alone still does not prove a model response.

The shared Pi setting `max_sub_agent_depth` must be at least 1 to allow owner research delegation.
Factory checks it without modifying personal preferences or resetting inherited ancestry. Launch
from inside a Pi subagent is rejected. No roster field can override the native depth policy.

Only selected upstream extensions are provisioned. There is no Factory status/auth extension,
replacement Pi executable, Forgetful wrapper, or remote-package auto-install.

## Optional implementation and review workers

Worker configuration is all-or-none: both harness/model/effort selections plus a local TDD skill.
Factories with no worker settings remain planning-only. New init asks explicitly; `--planning-only`
selects that mode without prompting. Optional implementation/review skills are existing local files.

Worker roster entries omit `cwd`: the owner must supply the assigned worktree on every launch.
That retains the worktree's native repository instructions. Both roles have local Factory skills;
the task prompt tells the worker to read those and its selected TDD/repository guidance. Pi also
receives explicit selected skills and a disabled child roster. Codex and Claude receive no Pi-only
resource options or child roster; their native instruction and tool settings still apply.

Exact model selectors come from the selected harness's catalog in each configured repository.
The supported effort vocabulary is checked per harness; catalogs do not establish model-specific
effort support, live access or tool permissions. Discovery results are reused only during one init,
not across sessions. Watch does not list models.

Readiness binds worker selections, executable paths and selected skill-file bytes. It does not
freeze native settings, every referenced document or executable contents. Editing selected skills
requires re-init. Existing role files remain create-only; configuration changes can require explicit
reconciliation. See [delivery](feature-delivery.md) for native permission and resume limitations.

## Provisioning and editable files

The top-level Factory dependency is pinned to AgentShell 0.5.0 following its
[supply-chain audit](../plans/agentshell-0.5-audit.md). Pass already-provisioned local resources;
do not use AgentShell's automatic remote-package installer. The bundled extension's independent
Python worker uses the audited 0.5.0 lock. Extension 1.4.1 accepts named child roster entries and
forwards their selected resources. Bundled bytes and the installed worker runtime must match the
reviewed inputs; an old 1.3.0 extension or 0.4.0 worker does not count as ready.

Role guidance and initial selections are create-only and reject symlink destinations. Registration
updates only the affected skill lists and uses a recovery receipt; it never rewrites skill contents
or entire rosters. Bundled upstream bytes are checked against their per-file hashes before copying
missing files. User edits are preserved. Obsolete
instructions must be reconciled explicitly, not silently overwritten or accepted as equivalent.
There is no migration framework for previous testing factories.

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
Remote URLs require HTTPS, except loopback
HTTP, and reject embedded credentials, query strings and fragments. Local access needs no server;
remote CLI commands use the server's MCP interface without requiring Pi's MCP extension.

Watcher, Foreman and owner use one native CLI configuration scope. The existing directory under
Foreman is retained so native login/refresh state need not be copied when child roles are added.
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

Every init checks the configured Forgetful connection, project access and planning support before
saving completion. The earlier server-only opt-in made an otherwise valid setup fail at the last
step; Scott chose automatic checks for both local and server mode. The legacy `--check-connection`
flag remains accepted for command compatibility but changes nothing. `--login` remains an optional
explicit native sign-in before the final check, not a requirement for using saved credentials.
Server checks can open browser sign-in. Failure or cancellation leaves configuration available for
retry, but no valid completion receipt; the watcher remains blocked. Credentials stay CLI-owned.

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
