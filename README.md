# Forgetful Factory

A software factory for one repository or a group of repositories, coordinating work tracking,
Forgetful planning, and Pi agents. See [FACTORY.md](FACTORY.md) for the intended behaviour.

`init` configures the factory and creates missing GitHub labels. `watch` reads matching issues
and saves a Forgetful plan, ownership task and ordinary-issue worktree before notifying the Foreman.
The Foreman can launch a feature-owner for clarification, research and task planning.
Implementation,
review, merge and deployment execution remain later slices.

## Run locally

Requires Python 3.12+, `uv`, Git, and authenticated GitHub CLI on Linux/WSL.
Foreman setup also needs Pi and tmux. Forgetful access uses its native CLI only.
`uvx` installs the AgentShell dependency automatically.

The package is not published yet. Build it from this checkout:

```bash
uv build
wheel="$(realpath dist/forgetful_factory-0.1.0-py3-none-any.whl)"

# In the same shell, move to your repository or group of repositories
cd /absolute/path/to/workspace
uvx --refresh --from "$wheel" forgetful-factory init
uvx --refresh --from "$wheel" forgetful-factory watch
```

Follow the prompts. Settings are saved in `.factory/factory.toml`; edit it to change them.
The watcher prints how to view Pi. **Stopping the watcher closes its Pi session.** Only one
watcher may run per workspace. Use `watch --help` through the same `uvx` command for options,
including `--existing`, `--new-only`, and `--interval` (default: 30 seconds).
See [architecture](docs/architecture.md) for implemented behaviour and [plan](docs/plan.md)
for progress. Foreman profile details and connection choices are below.

## Development

Use uv 0.13.1 or newer. It creates `.venv` and installs the locked runtime and dev dependencies:

```bash
uv sync --locked
uv run --locked ruff check src tests
uv run --locked lint-imports --no-cache
uv run --locked python -m unittest discover -s tests -v
```

Dependencies live in `pyproject.toml`; commit `uv.lock` after reviewed dependency changes.
Dev tools are not installed with the published package. CI runs all three checks on Python 3.12
and 3.13. Tests use external-command fixtures, including the real AgentShell lifecycle with
Pi and tmux doubles; they make no live service or model calls.

## Foreman and Forgetful setup

`init` configures native Forgetful CLI access to a local database or an existing server. MCP
configuration is rejected with correction instructions. Setup provisions Foreman, feature-owner
and research roles. Select an existing Forgetful project or create one during setup. The backend
needs planning enabled and the `external_ref` capability supplied by Forgetful 0.5.5. A new CLI
installation does not upgrade an existing server.

Owner model/effort defaults to the Foreman's choices. Override with `--feature-owner-model` and
`--feature-owner-effort`. Both coordinators use Pi; research uses the owner's model/effort.
`--grill-me-skill /absolute/path/SKILL.md` selects your existing, unchanged grill-me skill;
the default is `~/.agents/skills/grill-me/SKILL.md`. Factory does not download that skill.

Owner research delegation needs `max_sub_agent_depth` at least 1 in the shared Pi home's
`extensions/agentshell.json`. Review that native preference yourself: it affects your other Pi
sessions too. Factory checks it but never changes it. Run Factory from a normal shell, not from
inside a Pi subagent.

Factory uses your **normal native Pi home**, defaulting to `PI_CODING_AGENT_DIR` or `~/.pi/agent`.
`--pi-agent-dir /absolute/path` chooses another normal home. Init explains and requests consent
before invoking Pi there. `--share-pi-profile` supplies that consent for noninteractive setup.
Declining stops setup. The chosen directory and consent are saved in the role's `pi-profile.json`;
watch uses that saved choice even if the environment later changes.

This shares the **whole Pi profile**, including native login, settings, trust and session state.
The Foreman excludes your personal `SYSTEM.md`. `AGENTS.md`, `APPEND_SYSTEM.md`, and other native
instructions may still load. This is not full instruction isolation.
AgentShell extension configuration and the hide-tools preference also use that shared home;
native user toggles can change shared preferences. Nothing copies or links credentials. Model
listing follows native Pi resource behavior: it can still read personal `SYSTEM.md` and execute
resources from that profile or repository. The exclusion applies to Foreman launch, not model
listing during setup; this is not auth-only isolation.

An explicitly chosen home must already exist. Factory does not create a missing Pi home. If your
default home is absent, consented executable installation can finish, but setup stays incomplete:
initialize your normal native Pi home and `/login` in another terminal, then rerun init. Correct
mistyped paths before proceeding. If consent was saved for the wrong path, review or remove only
`.factory/agents/foreman/pi-profile.json`, then rerun init to approve the corrected home.

Init uses AgentShell's public model list and shows numbered choices grouped by provider. Supply
`--foreman-model` with an exact listed `provider/model` string to select noninteractively. Listing
only establishes that a model is selectable; access remains unverified and no model request is
made. A supplied model is validated before labels or factory configuration are written. If setup
stops before configuration is saved, repeat your original init arguments when retrying.
If there are no models, open Pi in the displayed home in another terminal, use `/login`, then
choose recheck or rerun init. Factory does not perform model login or refresh credentials itself.

```bash
forgetful-factory init --repo /path/to/repo --label factory \
  --foreman-model provider/model --foreman-effort high --share-pi-profile \
  --forgetful-instance local --forgetful-project 12 --install-role-runtime \
  --grill-me-skill /path/to/grill-me/SKILL.md

# Remote Forgetful checks can start the server's OAuth flow
forgetful-factory init --repo /path/to/repo --label factory \
  --foreman-model provider/model --foreman-effort high --share-pi-profile \
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

Editable roles live under `.factory/agents/foreman`, `feature-owner` and `research`. Each Pi
starts in its role directory and loads native `AGENTS.md`. Its selected skill describes the
workflow.
Foreman's instructions also ask it to read the preserved `APPEND_SYSTEM.md`; that file is not a
native system-prompt append file. Watch supplies no opening model prompt. The first notification
or user input can start a chargeable turn; setup does not make a model request.

Each role's `resources.json` selects existing local skill/extension paths. Foreman's `roster.json`
selects feature-owner; the owner's selects research. Research has no child roster or AgentShell
extension selected. Model, effort, cwd and resource choices are passed through the native extension,
not copied into ad-hoc prompts. Review both resource and roster files when changing selections;
init rejects conflicts and preserves edits.

Automatic personal/project resource discovery and native MCP are disabled. Ordinary instructions
and built-in tools remain available. Personal `SYSTEM.md` is excluded at launch; Pi keeps its own
built-in prompt. AgentShell 0.5 rejects the interactive combination if the Foreman launch directory
has `.pi/SYSTEM.md`. Init/watch preserve that file and ask for reconciliation. No remote package
auto-install, Factory-owned extension, or custom launcher is used.

Re-running init preserves edited role files, including old `settings.json`, `mcp.json`, status
extensions, and wrappers. Those old settings are not used as the role's resource selection. Review
and refresh an old testing profile manually; no migration or hidden cleanup is performed. Known
obsolete commands in the Foreman skill or role prompt, such as using the Pi home for Forgetful CLI
state or requesting MCP sign-in, stop init and watch with manual reconciliation instructions.
Harmless edits remain supported. Old discussion-only guidance and stale/edited installed upstream
extension code are refused. Reconcile them against the current bundled templates without discarding
custom instructions or credentials. An old extension 1.3/worker 0.4 installation is not ready for
child rosters; there is no automatic migration or silent runtime upgrade. If an older config lacks
`forgetful.project_id`, add the existing numeric project ID under `[forgetful]` in `factory.toml`,
then rerun init. Init will not overwrite that existing file to save a prompted choice.

Changing the saved Pi home requires explicitly reviewing `pi-profile.json`; change the model or
Forgetful target in `factory.toml`, then rerun init. `model-selection.json` is generated completion
evidence, not an editable role resource. Init invalidates it before setup work and atomically
regenerates it only after all required checks succeed. It binds both models/efforts, Pi home,
Forgetful project/target, role selectors/rosters and the grill-me source hash. Failed or skipped
checks cannot reuse an older receipt. Both local metadata files
are git-ignored; no credential values are recorded.

Watcher, Foreman and owner share native Forgetful CLI state under
`.factory/agents/foreman/cli-config`. Their commands use `FACTORY_FORGETFUL_DIR` as cwd and
`XDG_CONFIG_HOME="$FACTORY_FORGETFUL_CONFIG_DIR"` for that command only. The inherited
`FACTORY_ROLE_DIR` compatibility variable does not identify a child role.
`PI_CODING_AGENT_DIR` always identifies the shared Pi home; it is never the Forgetful auth path.
The surrounding shell and `gh` configuration remain unchanged. Local mode supplies an explicit
empty `FORGETFUL_SERVER`; remote mode supplies the chosen URL. `FORGETFUL_TOKEN` is removed from
the launch environment. There is no wrapper, alias, custom tool, or command forwarding layer.
Arbitrary agent commands must follow the skill to retain these configuration boundaries.

Every `init` checks Forgetful connectivity, project access and planning support before marking
setup complete, for both local databases and servers. Server checks reuse native saved credentials
and may open browser sign-in if needed. Failed or cancelled checks leave setup incomplete and keep
saved work for retry. The old `--check-connection` flag is accepted but no longer needed.
The check uses two CLI calls: selected project and the permitted tool catalog.
Project access also verifies the connection and native login; no user-profile request is needed.
It does not start a new CLI process for each planning tool.

The browser notice appears only when the server's public `/api/v1/auth/info` reports OAuth.
Other modes or unavailable metadata do not show it. Metadata only controls this notice; the native
CLI still owns authentication and the access check always runs.

`init --login` explicitly runs native `forgetful auth login --server` before the final access check.
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
Existing matching plans/tasks/trees are reused. Uncertain task creation, duplicate ownership, or
missing/mismatched saved trees stop for reconciliation; Factory never resets or deletes work.

Issue edits produce notifications with the same saved IDs. Restart sends unfinished plans again,
including closed issues. `--new-only` still sends updates to recovered work while baselining other
open matches. Foreman must check ownership before dispatching; duplicate notifications are possible.
A missing job record or session ID does not prove the owner stopped. Unknown liveness leaves work
pending. See [planning and recovery](docs/adrs/issue-planning.md) for the exact limits.

AgentShell also writes a resource-selection digest under `$XDG_STATE_HOME/agent-shell/resources`
(default `~/.local/state/agent-shell/resources`). That local state record can remain after a
session ends; it records a digest rather than resource contents or credential values.

Init provisions pinned AgentShell and hide-tools extensions; `/hide-tools` changes terminal display.
The audited AgentShell extension is 1.4.1; its independent worker uses AgentShell 0.5.0. Its real
Python environment requires installation consent (`--install-role-runtime`), using
existing uv >=0.13.1 and Python. No background-memory or custom Factory Pi extension is installed.
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
load the installed Pi SDK and bundled extension without inference:

```bash
NATIVE_PI_SDK=/absolute/pi-coding-agent/dist/index.js \
  uv run --locked python -m unittest discover -s tests -v
```

The [Slice 4/5 record](docs/plans/slices-4-5.md) distinguishes command-fixture tests, actual local
Forgetful checks, and isolated Pi loading/lifecycle checks. These do not prove autonomous owner
planning, live OAuth refresh or model-provider access. The earlier
[CLI onboarding record](docs/plans/cli-onboarding.md) retains the Slice 3 smoke evidence.
Never point test probes at a personal Pi profile.
