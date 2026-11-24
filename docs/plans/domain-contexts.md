# Domain contexts: base architecture and taxonomy

**Status: Approved 2026-11-23; slices 0–6 implemented** (see [Progress](#progress)). Fable reviewed
the first draft on 2026-11-23; see the [review record](#review-record). The design parts still need
to move to `docs/adrs/domain-contexts.md`; `docs/architecture.md` links to this plan for now.

## Goal

Split the package by **domain concept**, not only by technical layer. Each concept gets its own
model, its own ports and its own adapters. Then adding GitLab, Linear, Slack or herdr means adding
one adapter in one folder. The factory core does not change.

This plan only creates the structure and moves current behaviour into it. It adds no new
provider. Behaviour, saved data and agent-facing messages stay the same, except one deliberate
change: ticket keys become text (decision 6).

## Problems in the current code

The code has a hexagonal layout (`domain/`, `application/`, `adapters/`, `cli/`), and import rules
enforce it. But concepts are mixed together inside those layers:

1. **Ticketing and forge are one thing.** `GitHubWorkTracking` implements both issue reads
   (`adapters/github/work_tracking.py:72`) and remote-URL parsing (line 23). Each repository has
   one `work_source` (`domain/models.py:15-18`). The worktree mapping `repository` is the ticket
   source (`application/scaffold_issue.py:73`), but the cleanup marker uses it as the forge
   repository (`application/cleanup_marker.py:23-24`).
2. **GitHub is in the core.** `application/cleanup_marker.py:24` accepts only
   `https://github.com/.../pull/N`. `application/cleanup_completed.py:194` and
   `application/scaffold_issue.py:307` match only `github:` references. `cli/bootstrap.py:36-46`
   refuses any provider except `github`.
3. **tmux is part of the agent adapter.** `adapters/agentshell/controller.py:165-169` always
   builds a tmux host. The pane checks (lines 56-98), the attach text
   (`adapters/agentshell/terminal.py:34-36`) and tmux installation
   (`adapters/host_dependencies.py:77,160`) are all tmux-only.
4. **No channel concept.** `ForemanTerminal` (`application/ports/foreman_terminal.py`) mixes three
   jobs: run the Foreman session (`start`/`close`), deliver watcher messages (`send`) and tell
   the human how to reach it (`startup_hint`).
5. **Forgetful details are in the core.** `ForgetfulConnection` is in
   `application/configuration.py:10-78`. The core reads `config.forgetful.project_id`
   (`application/scaffold_issue.py:186,211,267,300`, `application/cleanup_completed.py:189`) and
   builds the receipt `backend` string from it (`application/cleanup_completed.py:355-356`).
6. **`ForemanProfile` is a god port** (`application/ports/foreman_profile.py:8-42`, 17 methods).
   It mixes agent definitions, Pi home, model lists, Forgetful login/projects and tool install.
   It also takes `FactoryConfiguration`, so agent code depends on the whole factory config.
7. **Adapters depend on the application.** Seven adapters import `application.watch_stop`
   (for example `adapters/command.py` and `adapters/agentshell/terminal.py:10`).
   Cancellation is shared plumbing, not workflow.
8. **The CLI holds logic.** `cli/main.py:295-466` and `693-897`, `cli/resource_update.py:24-27`
   and `cli/definition_of_done.py:4` import adapters directly. `cli/main.py` decides watch status
   and Foreman start. `cli/bootstrap.py:71-85` builds the agent environment.
9. **`adapters/filesystem/` groups by technology.** It holds Git, agent definitions, profiles,
   TOML, leases and receipts together.
10. **Hidden path coupling.** Five files find the resource root with `parents[n]`
    (`adapters/filesystem/role_resources.py:15` and others). `controller.py` and
    `model_catalog.py` are launched by file path; the owner is launched by module string
    (`adapters/agentshell/owner_client.py:138`). Import rules cannot see these links.

**Why the tests did not catch this.** The import rules check layers only. A hard-coded GitHub URL
is a string, not an import, so no rule sees it. Also, every test uses GitHub-shaped data. A second
fake provider would have exposed items 1 and 2.

## Target taxonomy

Format: context — meaning. Port(s). Adapter now → adapters later.

- **`factory`** — the factory's own work: watch, scaffold, cleanup, setup, status. Uses the ports
  of the other contexts. Its own adapters store factory data (config, lease, receipts, status).
- **`ticketing`** — where work requests come from. `Ticketing`. GitHub Issues → ADO Boards,
  Linear.
- **`forge`** — where code is hosted, reviewed and merged. `Forge`. GitHub → GitLab, Codeberg,
  ADO Repos.
- **`planning`** — plans and tasks. `PlanStore`, `PlanningSetup`. Forgetful.
- **`workspace`** — local checkouts and worktrees. `LocalRepositories`, `Worktrees`. Git.
- **`agents`** — the agent team: definitions, harness, sessions. `AgentSession`, `AgentTeam`.
  AgentShell + Pi.
- **`runtime`** — where a session runs. `SessionHost`. tmux → herdr and others, once AgentShell
  supports them for interactive sessions.
- **`channels`** — how a human talks to the Foreman. `Channel`. Terminal → Slack, Discord.

`shared/` holds plumbing with no business rules. `cli/` parses commands and is the composition
root: the only place that chooses adapters. The public `configuration.py` facade stays a second,
documented composition entry (`docs/adrs/initialization.md:202`).

### Folder layout

```text
src/forgetful_factory/
├── __main__.py
├── configuration.py   public load_configuration facade (composition entry)
├── shared/      errors, cancellation, command runners, safe file writes, resource root
├── factory/
│   ├── model.py      FactoryConfiguration (factory-level), records rules, problems
│   ├── ports.py      ConfigurationStore, WatchLease, CleanupReceipts, ToolInstaller
│   ├── services/     watch, scaffold, cleanup, initialise, watch status, start foreman, DoD
│   └── adapters/     TOML config, watch lease, cleanup receipts, watch status, DoD file
├── ticketing/   model.py · ports.py · adapters/github.py
├── forge/       model.py · ports.py · adapters/github.py
├── planning/    model.py · ports.py · adapters/forgetful/
├── workspace/   ports.py · adapters/git/
├── agents/      model.py · ports.py · adapters/agentshell/ · adapters/pi/
├── runtime/     model.py · ports.py · adapters/tmux.py
├── channels/    ports.py · adapters/terminal.py
├── cli/         commands, composition (adapter registry), DeadlinePolicy
└── resources/   unchanged
```

Every area has the same order: `adapters` → `services` → `ports` → `model`. Only `ports` is
required. A new adapter is one file or folder under `<context>/adapters/`, plus one registry line.

### Where every current module goes

- **`shared/`**: `FactoryError`, `application/watch_stop.py`, `adapters/command.py`,
  `adapters/sensitive_command.py`, `adapters/filesystem/resource_files.py`, the uv check from
  `host_dependencies.py`, and one new resource-root function that replaces the five `parents[n]`.
- **`factory/`**: `application/configuration.py` (without Forgetful), `factory_records.py`,
  `watcher_problems.py`, `cleanup_marker.py` (without the URL check), `watch_factory.py`,
  `scaffold_issue.py`, `cleanup_completed.py`, `initialise_factory.py`; ports for configuration,
  lease and receipts; `adapters/filesystem/{toml_configuration,watch_lease,cleanup_receipts}.py`;
  `adapters/watch_status.py`; logic from `cli/main.py:312-421` and `cli/definition_of_done.py`.
- **`ticketing/`**: `Issue`, `Label`, `WorkSource`; `WorkTrackingService`; the issue half of
  `adapters/github/work_tracking.py`.
- **`forge/`**: `application/ports/work_source_resolver.py` (becomes `Forge.repository`); the
  remote half of the GitHub adapter; the PR-URL check from `cleanup_marker.py`.
- **`planning/`**: `ForgetfulConnection` (model); `application/ports/planning.py`;
  `adapters/forgetful/*`; the Forgetful half of `ForemanProfile`; the Forgetful Python install.
- **`workspace/`**: ports `local_repositories.py`, `worktrees.py`;
  `adapters/filesystem/git_{repositories,worktrees}.py`. Remote branch deletion stays here: it is
  plain Git (`git_worktrees.py:340`).
- **`agents/`**: `initial_agent_choices.py` and `AgentShellLifecycleDeadlines` (model);
  `adapters/agentshell/*`, `adapters/filesystem/foreman_runtime.py`; agent definitions, profiles,
  role resources and selected skills (into `adapters/pi/`); the Pi and AgentShell-runtime installs.
- **`runtime/`**: tmux install, attach text and `enter_terminal` (`owner_client.py:176`).
- **`channels/`**: the terminal channel (attach text and entry, through the runtime adapter).
- **`cli/`**: commands and prompts, `bootstrap.py` (becomes the composition module with the
  adapter registry), `numbered_selection.py`, `DeadlinePolicy` from `deadlines.py`.

### Runtime: host and isolation

AgentShell 0.5 separates two things:

- **Host:** where the session lives. AgentShell has native, tmux, herdr and terminal-window
  hosts. Only tmux supports interactive sessions (`agent_shell/tmux.py:496,502`; `shell.py:114`
  rejects the others). The Foreman needs an interactive session, so **tmux is the only usable
  host today**.
- **Isolation:** what limits the agent. AgentShell has `NoIsolation` and
  `LinuxPidNamespaceIsolation`. The tmux, herdr and terminal-window hosts all accept
  `NoIsolation` only.

Docker and bubblewrap are isolation, not hosts. The two axes are recorded here as the agreed
direction. The port does **not** take an isolation value yet: there is only one usable value.
herdr, Docker and bubblewrap need AgentShell work first.

**Process boundary.** `controller.py` runs in AgentShell's own interpreter. It is launched by file
path and imports only the standard library and `agent_shell` (`terminal.py:90`). It cannot import
a Factory port. So:

- The host choice travels as **plain data** in the launch JSON: `{"host": {"kind": "tmux", ...}}`.
  The launched target comes back as an opaque `dict`.
- The controller maps `kind` to an AgentShell host. It knows only `tmux`, and it refuses any
  other kind with a clear error.
- The tmux pane checks that run inside the controller (`controller.py:55-98`) move to a sibling
  file beside it (`agents/adapters/agentshell/tmux_host.py`), loaded the same way. They are
  tmux-specific, but they must live where the controller runs.
- The Factory-side tmux parts (install, attach text, terminal entry) live in
  `runtime/adapters/tmux.py`.

### Channel versus session

- **Session** (`agents`): the running Foreman. The watcher sends system messages into it.
- **Channel** (`channels`): how a human talks to the Foreman. Today the human attaches to the tmux
  pane. A Slack channel would relay human messages into the session, and relay Foreman replies
  (from AgentShell session events) out to Slack.
- The terminal channel gets the runtime adapter from composition. It does not import it.

## Port contracts (minimum, from current use only)

Ports contain only what the code uses today. Each port speaks its own context's types, not
`FactoryConfiguration`.

- **`Ticketing`**: `check_ready()` (today's `gh api --slurp` check), `validate_source(source)`
  (today's `bootstrap.py:41-46` check), `is_key(text)` (replaces the numeric pattern at
  `cleanup_completed.py:194`), `check_access(source)`, `list_labels(source)`,
  `create_label(source, label)`, `list_open(source, labels)`. Model: `TicketSource`, `Ticket`,
  `Label`. `Ticket.key` is a `str` ("42", "ENG-123"; see decision 6). `Ticket.id` is
  `provider:source#key`, so a GitHub id keeps today's bytes. Branch names use the key with every
  character outside `[A-Za-z0-9._-]` replaced by `-`; GitHub branch names keep today's bytes.
- **`Forge`**: `repository(remote) -> RepositoryRef` and
  `is_change_request(repository, url) -> bool`. The forge comes from the remote host
  (`github.com` → GitHub). The marker check derives the forge repository from the configured
  `remote`, not from the mapping `repository`.
- **`PlanStore`**: today's `Planning` methods. It adds the project itself on create, and adds
  `owns(plan) -> bool` and `backend_identity() -> str`. So the core stops reading Forgetful
  settings. Plans stay `dict`s.
- **`PlanningSetup`**: the Forgetful half of `ForemanProfile`: `projects`, `create_project`,
  `prepare`, `uses_browser_login`, `login`, `check`.
- **`AgentSession`**: `start()`, `send(text)`, `wait(interval)`, `close()`.
- **`AgentTeam`**: the agent-definition half of `ForemanProfile`. It takes `AgentChoices` (today's
  `InitialAgentChoices`), the root agent file path and the execution flag, not
  `FactoryConfiguration`.
- **`ToolInstaller`**: `absent()`, `unready()`, `describe(name)`, `install(name)`. One installer
  per tool, in the context that owns the tool. Two lists instead of one `missing()` keep today's
  prompt order: init offers every absent tool first, then every tool whose managed copy is not
  ready (slice 4b). Python protocols are structural, so an implementer does not import `factory`.
- **`SessionHost`**: `spec() -> dict` (the plain-data host for the launch JSON),
  `how_to_attach(target) -> str`, `enter(target)`.
- **`Channel`**: `how_to_reach(target) -> str` and `open(target)`.

**Config:** the `factory.toml` shape does not change. `provider`/`source` keep their meaning as the
ticket source. The forge comes from `remote`. The "remote matches source" check
(`factory_records.py:35-45`, `initialise_factory.py:104-112`) runs only when the ticketing
provider and the forge are the same service. Init keeps today's default: when they are the same
service, it proposes the forge repository as the ticket source (`initialise_factory.py:85-92`).

## Saved data

These bytes are stored or sent to agents today.

**Changed once, on purpose, in slice 1** (decision 6):

- Plan context `issue` snapshot (`scaffold_issue.py:179-188`; read back at
  `factory_records.py:51-53`): the int field `number` becomes the string field `key`.
- Notification JSON (`watch_factory.py:510-514`): `"number": 42` becomes `"key": "42"`.
- Plan placeholder text (`scaffold_issue.py:182`) and Foreman guidance
  (`resources/foreman/skills/foreman/SKILL.md:261`) say `#key` instead of `#number`. The role
  resource bundle and its shipped-hash history are rebuilt for this.
- Plans saved by an older build become unreadable (`plan_recovery_invalid`). There is no reader
  for the old shape: factories are early in their life, and the README already says existing
  factories are not migrated. Upgrading needs a fresh factory and Forgetful project.

**Must not change.** Every slice must keep these identical:

1. Plan `external_ref`: `provider:source#key` (`Issue.id`). For GitHub this is today's string.
2. Notification JSON apart from the `key` field, including `repository`.
3. Watcher alert JSON (`watcher_problems.py:209`).
4. Ownership task description (`kind: factory-ownership`, `scaffold_issue.py:150`).
5. Worktree mappings: keys, `repository` value, branch `factory/<owner-repo>-<key>`, path
   `.factory/worktrees/<name>` (`scaffold_issue.py:71-76`), and cleanup markers.
6. Cleanup receipts: `CleanupSet` fields and the `backend` string (`cleanup_completed.py:355-356`).
7. `factory.toml` shape.

Slice 1 starts with **characterization tests**: golden fixtures captured from the current code
for items 1–6. The same commit records the deliberate `number` → `key` change in the fixtures.
Every later slice must read those fixtures and write identical bytes.

## Architecture tests

Four kinds of test protect the structure. The existing proof harness in
`tests/test_architecture.py` is the starting point. It already copies the real `pyproject.toml`
into a throwaway package, and it shows that each rule fails on a real violation.

### A. Dependency rules (final state)

Checked by import-linter 2.15 (`lint-imports --no-cache`, already required in CI at
`.github/workflows/ci.yml:48`). Lists below are shortened with `...`; the real config lists every
area.

```toml
[tool.importlinter]
root_package = "forgetful_factory"
include_external_packages = true      # needed to forbid subprocess, socket, agent_shell
exclude_type_checking_imports = false

[[tool.importlinter.contracts]]       # rules 1, 3, 4: who may import whom, top level
id = "top-level"
type = "layers"
containers = ["forgetful_factory"]
exhaustive = true                     # a new top-level package fails until it is classified
layers = [
    "__main__",
    "cli : configuration",
    "factory",
    "agents : channels : forge : planning : runtime : ticketing : workspace",
    "shared",
]

[[tool.importlinter.contracts]]       # rule 2: the same order inside every area
id = "inside-each-area"
type = "layers"
containers = ["forgetful_factory.factory", "forgetful_factory.agents", "..."]
exhaustive = true                     # a stray module such as ticketing/helpers.py fails
layers = ["(adapters)", "(services)", "ports", "(model)"]

[[tool.importlinter.contracts]]       # rule 5: only composition imports adapters
id = "adapters-from-composition"
type = "forbidden"
source_modules = ["forgetful_factory.shared", "forgetful_factory.*.services",
                  "forgetful_factory.*.ports", "forgetful_factory.*.model"]
forbidden_modules = ["forgetful_factory.*.adapters"]

[[tool.importlinter.contracts]]       # rule 6: adapters do not import each other
id = "adapters-independent"
type = "independence"
modules = ["forgetful_factory.factory.adapters", "forgetful_factory.agents.adapters", "..."]

[[tool.importlinter.contracts]]       # rule 7: the core and its contracts start no processes
id = "core-no-processes"
type = "forbidden"
source_modules = ["forgetful_factory.*.services", "forgetful_factory.*.ports",
                  "forgetful_factory.*.model"]
forbidden_modules = ["subprocess", "socket"]

[[tool.importlinter.contracts]]       # rule 8: only the agents adapter uses AgentShell
id = "agentshell-in-agents"
type = "forbidden"
source_modules = ["forgetful_factory.shared", "forgetful_factory.cli",
                  "forgetful_factory.factory", "forgetful_factory.ticketing", "...",
                  "forgetful_factory.agents.ports", "forgetful_factory.agents.model"]
forbidden_modules = ["agent_shell"]
allow_indirect_imports = true         # cli reaches agent_shell through the agents adapter
```

In plain words:

1. `shared` imports nothing above it.
2. Inside an area, imports go downwards only: adapters → services → ports → model.
3. `factory` imports no `cli`.
4. A context imports no `factory` and no `cli`. Contexts may use each other's ports and models.
5. Only `cli` and `configuration.py` import adapters.
6. One adapter package never imports another.
7. Core code and ports/models start no processes and open no sockets.
8. Only `agents.adapters` imports AgentShell directly.

**Checked in slice 0 (2026-11-23).** A spike with import-linter 2.15 and a two-context fixture
showed (Context7 docs agree):

- Wildcard `forbidden` sources work: `*.services → beta.adapters` failed with the full path.
- `exhaustive` with optional layers works: a context without `services` passed; a stray
  `alpha/helpers.py` failed with "not listed as layers".
- `include_external_packages` works for `subprocess` (also inside a function) and `agent_shell`.
- A wildcard that matches nothing is **skipped silently**; a plain missing name fails with
  "does not exist". So the "rule names exist" check (part C) is required for wildcards.
- Rule 8 first had no `allow_indirect_imports`. Then `cli → agents.adapters → agent_shell`
  broke it, although that is the composition path. The option is now set; a direct import from
  `cli` still fails.

The proofs (part B) establish each rule when it arrives. Do not trust a green run alone.

### B. Proof tests (rules really reject violations)

Rework `tests/test_architecture.py` into two tables. The steps for each case stay the same as
today. Function-level imports count (the controller imports `agent_shell` inside functions).

- **Rejection table**: rows of (rule id, from-module, to-module). Every row runs **direct** and
  **indirect**. The indirect path goes through `boundary_probe.bridge`, which sits outside both
  areas. The fixture copy adds `boundary_probe` to `exhaustive_ignores` only. The steps are:
  1. With the target rule off and all others on, the violation passes.
  2. With the target rule on, the run exits 1. The message names the rule and the full path.
  3. With the violation removed, the run passes again.
- **Rows** (at least): `shared → factory`; `ticketing.model → factory.model`;
  `ticketing.adapters → cli`; `factory.services → cli`; `ticketing.model → ticketing.ports`;
  `ticketing.ports → ticketing.adapters`; `factory.services → forge.adapters`;
  `forge.ports → ticketing.adapters`; `channels.adapters → runtime.adapters`;
  `factory.services → subprocess`; `runtime.model → agent_shell`;
  `ticketing.adapters → agent_shell`; an unclassified top-level package; an unclassified module
  inside a context.
- **Allowed table** (must pass): `factory.services → ticketing.ports`,
  `factory.model → planning.model`, `agents.adapters → runtime.model`,
  `channels.adapters → runtime.ports`, `cli → every adapter`,
  `configuration → factory.adapters`, `__main__ → cli`, `anything → shared`,
  `agents.adapters → agent_shell`,
  `shared → subprocess`.
- The fixture is generated from the area list, so a new context joins every proof by one entry.

### C. Coverage checks (the checker sees everything)

- **Package markers**: every directory under `src/forgetful_factory/` that holds `.py` files has
  an `__init__.py`. A missing marker hides files from the checker. Today none is missing. This
  needs no new dependency. Using Grimp's API directly would need a supply-chain audit.
- **Rule names exist**: every internal module name or wildcard in the contracts matches at least
  one real module. import-linter skips a missing `forbidden` name silently, so a typo would turn
  a rule off.
- **Launch paths exist**: the files launched by path (`controller.py`, `model_catalog.py`,
  `tmux_host.py`) and the owner module string are exposed as constants. A test checks that each
  one resolves in the source tree. Each slice also builds the wheel and runs
  `tests/check_package.py` plus the installed-package tests.

### D. Port conformance tests (adapters keep the port's promises)

- One `unittest` mixin per port under `tests/contracts/`. The repo bans pytest APIs in tests.
- Each adapter has a subclass that runs the mixin: the fake, and the real adapter with stubbed
  `gh`/`git` (as tests do today).
- Workflow tests use only fakes that pass their port's mixin, so fakes cannot drift.
- `AgentSession` keeps the existing real-tmux, fake-agent lifecycle tests as its conformance test.
- A future adapter (GitLab, Linear) is done when it passes its port's mixin.

### E. Leak checks (what import rules cannot see)

- **Second fake provider**: a fake ticketing provider with a non-GitHub name, URLs and text keys
  (`ENG-123`), plus a fake forge with non-GitHub change-request URLs. They run through scaffold,
  watch and cleanup. This catches hard-coded GitHub strings, regexes and numeric-key assumptions.
- **Provider-name scan**: files in `factory/`, and every `ports.py` and `model.py`, must not
  contain `github`, `gitlab`, `codeberg`, `linear`, `tmux`, `herdr` or `agent_shell` (any case).
  This is a small text test that guards the problem that occurred.
- Import checks do not see dynamic imports, attribute access or file/network actions. Behaviour
  tests and review remain responsible for those.

### When each rule arrives

- **Slice 0**: rework the harness into tables; add parts C and the `shared` rule. The three
  current contracts stay until their areas are empty.
- **Slices 1–4**: each new context joins `inside-each-area`, `adapters-from-composition`,
  `adapters-independent` and a temporary contract "contexts import no `application`, `factory`,
  `cli` or legacy `adapters`". Its proof rows and conformance mixin arrive in the same slice,
  test first: the new proof row fails until the rule is added. `agentshell-in-agents` arrives in
  4a.
- **Slice 5**: the legacy and temporary contracts go. `top-level` (exhaustive) and
  `core-no-processes` replace them.

## Slices

Each slice is vertical. It keeps every test passing, and it updates the rules,
`docs/architecture.md`, the relevant ADR and the Mycelium map.

- **0. Shared kernel and test harness.** Errors, `watch_stop`, command runners, safe writes and a
  resource-root function move to `shared/`. Adapters stop importing `application.watch_stop`
  (they still import application ports until those move). The uv check moves with the
  `host_dependencies.py` split in 4b.
  Proof: table-driven harness; coverage checks; `shared` rule; full suite.
- **1. Characterization and ticketing.** First commit: golden fixtures for the saved data. Then
  models, tracking port and GitHub issue reads move to `ticketing/`, and `number: int` becomes
  `key: str` (see [Saved data](#saved-data)). The `github:` matches at
  `cleanup_completed.py:194` and `scaffold_issue.py:307` use the ticket id format and
  `Ticketing.is_key`. A registry and `Ticketing.validate_source` replace `bootstrap.py:36-46`.
  Foreman guidance is updated (the hashed bundle did not need it; see Progress).
  Proof: fixtures match (with the recorded key change); ticketing mixin with `ENG-123` keys;
  GitHub ids and branch names unchanged; clear error for an unknown provider; resource update
  test passes with the new bundle.
- **2. Forge.** `Forge.repository` replaces `WorkSourceResolver`. The marker check uses
  `Forge.is_change_request`, with the repository taken from the configured remote. The
  remote-equals-source check runs only when the providers match.
  Proof: forge mixin; marker accepts/rejects the same input as today; GitHub forge plus fake
  ticketing works end to end; fixtures unchanged.
- **3a. Planning.** `ForgetfulConnection` moves to `planning/model.py`. Forgetful adapters move.
  `PlanStore` owns the project id and the backend string.
  Proof: planning mixin; receipts and plan fixtures unchanged.
- **3b. Workspace.** Git adapters and ports move. Proof: full suite, including real-Git tests.
- **4a. Agents, move only.** AgentShell, owner, runtime directory, model catalog, profiles and
  definitions move. No interface changes. Path launches use the new constants.
  Before this is installed anywhere, stop the live owner (DinoLand).
  Proof: launch-path check; built wheel; real-tmux lifecycle tests.
- **4b. Split `ForemanProfile`.** It becomes `AgentTeam`, `PlanningSetup` and one `ToolInstaller`
  per context. `host_dependencies.py` splits by tool.
  Proof: init/setup suites; mixins for the new ports.
- **4c. Runtime.** The host travels as plain data in the launch JSON. In-controller tmux checks
  move to `tmux_host.py`. Install, attach text and entry move to `runtime/adapters/tmux.py`.
  Proof: an unknown host kind is refused clearly; lifecycle tests unchanged.
- **4d. Channels.** The attach text leaves `AgentSession`. The terminal channel provides it and
  `foreman --attach`.
  Proof: full suite; DinoLand smoke trial (see [Trial run](#trial-run-dinoland)): fresh setup
  through to the first issue notification reaching the Foreman.
- **5. Thin CLI and final rules.** Watch status, Foreman start and DoD logic move to
  `factory/services/`. The CLI keeps parsing, prompts and composition. `DeadlinePolicy` moves to
  `cli/`. The legacy folders are empty and removed.
  Proof: `top-level` and `core-no-processes` rules with proofs; full suite.

- **6. Final trial.** Full trial (on the throwaway repo, not DinoLand; see below).

### Progress

**Rule (Scott, 2026-11-23): the refactor must not change functional behaviour.** Reviewers
(Fable 5.2 and Astra in Codex, through AgentShell, after a SonarQube scan) must check this. Every
change of behaviour so far is listed here, including small ones. Scott accepted the list below;
any further change of behaviour needs his approval first.

- **Agreed (decision 6):** ticket keys are text. The notification and plan snapshot carry
  `"key": "42"` instead of `"number": 42`; plans saved by older builds need reconciliation. The
  Foreman and feature-owner skills say `provider:source#key`.
- **Message text, edge cases (accepted by Scott, 2026-11-23):**
  - Init preflight now runs `GitHubTicketing.validate_source` before the origin check. A saved
    GitHub source in a bad format (for example `team/app.git`) now reports "Invalid GitHub work
    source …" instead of "Origin/source changed …". An unsupported provider still reports
    "Unsupported work-tracking provider …", with slightly different wording.
  - The cleanup-marker diagnostic (operator stderr only) says "change request URL" instead of
    "GitHub PR URL".
- **Not reachable with GitHub only:** mixed ticketing providers are refused; the remote-matches-
  source check is skipped when forge and ticketing differ; cleanup scope accepts any provider's
  key format through `could_be_key` (for GitHub, `main`'s pattern `[1-9]\d*`), and recovery
  checks saved keys with `is_key` (for GitHub: ASCII digits, no leading zero, readable as an int).
- **Wire order only:** `create_plan` sends `project_id` last in the CLI JSON; stored records match.

**Next steps:** Scott's decisions (damaged saved contexts, the `json`/`_ctypes` order, the known
limits below); the branch is not pushed. Trials use
a throwaway private GitHub repo and a new Forgetful project (Scott, 2026-11-23), deleted
afterwards. The DinoLand baseline watcher and Foreman were stopped with Ctrl-C on 2026-11-23.

- **Reviews** (2026-11-24, through AgentShell `AgentShell.execute`, each in its own scratch
  worktree at `edb84a2`): Fable 5.2 (`claude-fable-5-2`, Claude Code) said "no blocker"; Astra
  (`gpt-6.2-astra`, Codex) said "block merge". Every claim was checked against `ff5bc18` before
  it was fixed. Each fix restores `main`'s behaviour, and its test failed first:
  - **Blocker (Astra): saved ticket keys.** Recovery accepted any non-empty saved key, so `0` or
    `1٢` (ASCII 1, Arabic-Indic 2) passed. With the SonarQube change to `\d`, a completed plan
    with `#1٢` was cleaned up; `main` raised `plan_recovery_invalid`. Recovery now asks the ticket
    provider (`FactoryRecords` takes the `Ticketing` port). Tests: `tests/test_ticketing.py`.
    Round 2 finished this (below).
  - **Controller preflight (both).** `main`'s controller imported `ctypes` and `select` at the
    start, so `--check` failed on an interpreter without them. Now `--check` loads every host
    file. Loading also wrote `__pycache__` beside the installed files; it no longer does.
    Tests: `tests/test_runtime_host.py`.
  - **Install probes (Astra).** If the Forgetful CLI appeared between the two lookups, init
    offered it twice; `main` had a guard. The guard is back, and the managed Pi probe reads the
    saved home twice again, as `main` did. Tests: `ProbeTimingTests`.
  - **Init with an origin ending `.git.git` (Astra).** `main` set up with the derived source
    `team/app.git`; the branch refused it. `validate_source` now names a fault only when the
    provider differs or the saved source no longer matches the origin (the accepted message
    change still applies there). Test: `tests/test_init_sources.py`, which also passes on
    `ff5bc18`.
  - **Watch check order (both).** `main` checked each repository in turn, provider then source;
    the branch checked all providers first. Order restored. Test in `tests/test_ticketing.py`.
  - **`--help` without `fcntl` (Astra).** Composition imported the lease at start. It is
    imported lazily again. Test: `test_help_works_without_the_lock_module`.
  - **Launch paths (Fable).** `main` started the owner's controller and the model catalog by
    the path as installed; the branch resolved symlinks. Restored; the AgentShell terminal
    resolves its own path, as before. Test: `test_launch_paths_keep_the_installed_spelling`.
  - **Packaging (Astra).** The sdist missed `tests/contracts/` and the JSON fixtures, so its
    tests could not be collected. Patterns added; a test checks every test file is covered.
    The rebuilt sdist collects every test (775 at the last commit).
  - **Rule gaps (Astra, Fable).** `__main__` could import an adapter directly: new rule
    `entry-through-cli` (direct imports only). An `agents.services` module could import
    AgentShell: `agentshell-in-agents` now takes every services, ports and model package. The
    provider scan now also matches `AgentShell`; the five uses in `agents/model.py` are recorded.
  - **Golden tests (Astra).** `target_branch` is replaced only when it is the fixture repo's real
    branch; the saved TOML must end in one newline.
  - Docs: the ADR now names which ports have contract mixins (ten) and which rely on other tests.
- **Reviews, round 2** (same reviewers, at `2b41d1c`). Fable: "no blocker remains". Astra: one
  blocker left. Both confirmed the earlier fixes and showed each new test fails on `edb84a2`.
  Fixed, again test-first, restoring `main`:
  - **Blocker (Astra): a saved key longer than Python reads (4,301 digits)** was cleaned up;
    `main` failed to read the saved number and refused the plan. GitHub `is_key` now also needs
    the key to read as an int.
  - **Damaged reference reported again (both).** `2b41d1c` skipped a completed plan with `#1٢`
    silently; `main` reported `plan_recovery_invalid`. The `Ticketing` port gains
    `could_be_key` (the rough shape; every key passes, a damaged one may too); cleanup finds
    references with it (for GitHub, `main`'s `[1-9]\d*`), and recovery then refuses the damaged
    key. Tests: `tests/test_cleanup_damaged_reference.py` polls cleanup with a recording
    worktree double: sound key cleaned up, `#1٢` reported, the long key never cleaned up.
  - **Controller without `ctypes` (both).** A plain launch (no preflight) now stops at start
    with a traceback and no reply, as `main` did; the host files load first, with a loader that
    writes no cache for them only (their own imports cache as before).
  - **Forgetful lookups (Astra).** The executable is looked up twice again, as on `main`.
  - **Rule gap through `__init__.py` (Astra)** and **CRLF / literal branch token in the saved
    TOML check (Astra)**: new guard test; the TOML is read as bytes.
- **Reviews, round 3** (at `9cf35d6`). Astra confirmed the round-2 fixes and found intake could
  still write a plan whose saved key is longer than Python reads (`main` refused it as bad
  context). `FactoryRecords.context` now fails such an all-digit key with `plan_context_invalid`,
  as `main` did, before any write; cleanup reports the same code as `main`. Also: the over-long
  key test sets Python's digit limit itself; the branch golden compares with the real branch;
  the `__init__` guard reads the AST. Fable's round-3 run failed to start (AgentShell exit 1),
  so it has no round-3 report. Still open for Scott: with both `_ctypes` and `json` missing, the
  controller names `json` first (`main` named `_ctypes`).
- **Reviews, round 4** (Fable at `045f2f4` on `2b41d1c..045f2f4`, re-run after its round-3 run
  failed; Astra at `045f2f4`). Fable: "no blocker", no new behaviour change against `ff5bc18`,
  every earlier finding resolved except three small items. Astra: the round-3 case is fixed, and
  it built more damaged records (below). Fixed, test-first:
  - A minus sign before an over-long saved number now fails when the context is read, as the old
    JSON integer did (both reviewers).
  - That check now applies only to keys the provider calls key-shaped (`could_be_key`, GitHub
    only today): another provider's long text keys are read as before (Astra).
  - A test now shows the host file's own imports still cache (a global switch failed it) (Fable).
  - Doc slips: the re-run record, the test count, a line citation (Fable).
- **Decision for Scott: damaged saved plan contexts.** Decision 6 turned the saved integer
  `number` into the text `key`. `main` refused some damaged records only because Python's JSON
  parser failed on the integer. The branch now matches that for the realistic damage (zero,
  leading zeros, non-ASCII digits, numbers longer than Python reads, with or without a sign).
  Astra found two hand-built records that still differ: a context that repeats the `key` field
  with an over-long value first and a sound one last (`main` refused it; the branch reads the
  sound last value and, for a completed plan, cleans up), and an archived context that holds both
  the old `number` and an over-long text `key` (`main` skipped it; the branch reports it). Factory
  never writes either; matching them would mean re-running integer parsing on every repeated
  field. Recommendation: accept them as part of decision 6 and stop here.

- **Known limits (not changed; behaviour-neutral, for Scott to decide).**
  - `AgentTeam` names Pi (`choose_pi_home`, `pi_home`, `harness='pi'`) and four methods take
    `ForgetfulConnection`; `FactoryConfiguration` has a `forgetful` section (saved TOML shape).
  - The owner client validates a tmux-shaped target (`%` pane id, socket path, process fields).
  - The CLI's init paths still call `owner_client` directly (`cli/main.py`), and
    `_launch_setup_foreman` repeats the launch dict that `StartForeman` builds.
  - `unknown_status` (a watch-status shape) sits in `agents/model.py` because the owner adapter
    needs it. `adapters-independent` works between contexts; inside `agents`, the Pi adapter uses
    the AgentShell launch constants. `core-no-processes` forbids `subprocess` and `socket` only.
  - The plan text still says `AgentSession` (the code has `ForemanTerminal` with
    `startup_hint`), lists `runtime/model.py` (none exists) and gives `how_to_attach(target)`
    (the code takes the session name).
  - `watch --status` builds the owner, storage and team before its first read, and `foreman
    --attach` builds a lease it does not use. The constructors only store fields, so nothing
    visible changes.
  - Golden gaps: the `discuss` agreement transcript drops stderr and the exit code (they depend
    on the host's tmux); full init stdout, the launch frame and a live plain watcher are not
    pinned; the Ubuntu 24.04 tmux recipe tests skip on this host.

- **SonarQube** (2026-11-24, local Community Build, gate "Sonar way sans code coverage"). The
  server cannot analyse branches, so the scan script's `SONAR_MAIN_BRANCH` override scanned each
  commit as the project's one branch: first current `main` (`ff5bc18`), then this branch.
  - `main`: 1 issue, `cli/resource_update.py:22` (S3516, "always returns the same value"); 0%
    duplication; no hotspots. The gate fails on it (new since the stored 15 Nov analysis).
  - Branch at `9867804`: 5 new issues, all fixed with no behaviour change: `watch_status.py`
    `report` cognitive complexity 16 > 15 (two helpers); argument-type warnings on the
    `agree_definition_of_done` calls (the port's `location` is now a property); `[0-9]` instead
    of `\d` in `GitHubTicketing._KEY` (first changed to `[1-9]\d*`, which Astra showed let a
    non-ASCII key through; now `[1-9]\d*` with `re.ASCII`); a test hook
    read as an unused helper (`# NOSONAR(S5899)`, the form the sonar-python docs give through
    Context7).
  - After the fixes: only the `main` issue remains (pre-existing, unchanged: fixing it would
    change code outside this refactor). 0% duplication, no hotspots, no bugs or vulnerabilities.
    Rescanned after each review round; the same result at `045f2f4` (6,943 lines of code).

- **Slice 5b: done** (2026-11-24), thin CLI. No behaviour change.
  - Tests first: `tests/test_operator_transcripts.py` pins, as raw text, what these paths print:
    the agreement prompts and output for every answer (first setup, finalize, existing file), the
    `foreman` refusals, and `watch --status` JSON with no records, a saved or live owner, an
    unreadable owner record, both saved sources and complete setup. Recorded at `8d715d2`
    (`tests/fixtures/transcripts.json`); the same fixture also passes at `cff2499`, before
    slice 5. Only the `discuss` answer drops stderr: setup then starts a Foreman, which depends on
    the host.
  - Moves: Foreman start is `StartForeman` (`factory/services/start_foreman.py`), watch status
    is `WatchStatus` (`factory/services/watch_status.py`), and the agreement steps are
    `factory/services/definition_of_done.py` (moved with `git mv`; `print`/`input` became the
    `say`/`ask` functions the CLI passes in, and the file became the `AgreementStore` port with
    the `MarkdownAgreement` adapter). The CLI functions are now a few lines each.
  - New port `PersistentForeman` (`agents/ports.py`: `saved`, `status`, `report`, `start`) with
    `AgentShellOwner` in `owner_client.py`. The owner report (live, saved or unknown, with its
    recovery text) moved there verbatim from the CLI: the text names the owner's own files, so it
    belongs to the adapter. `unknown_status` moved to `agents/model.py`, because the owner adapter
    needs it and `agents` may not import `factory`. The port was first called `ForemanOwner`; that
    is the owner process class in `owner.py`, so it was renamed.
  - Contracts: `PersistentForemanContract` (`AgentShellOwner`, no live owners) and
    `AgreementStoreContract` (`MarkdownAgreement`).
  - Mutations in a scratch copy, each caught: the agreement file replaced on a second write; a
    stopped owner given a recovery warning; changed refusal and prompt text; the memory notice
    dropped from `foreman` (`test_normalized_lifecycle.py`). Swapping two keys in the combined
    report is not a change: they already exist in the owner report, so their position is kept.
  - Still in the CLI: `watch --start/--stop` (argument checks, one owner request) and the plain
    watcher's composition (`_watch_locked`: signals, observer and the saved-owner refusal). They
    are composition, so they stay.
  - Docs: the class diagram marks ports with one-line `<<interface>> Name` statements (Mermaid
    docs, through Context7), which keeps the overview under 500 lines.
  - Checks: full suite 740 passed, 14 skipped; 6 contracts kept; Ruff clean.

- **Slice 5a: done** (2026-11-24), move and final rules. No behaviour change.
  - The legacy folders are gone. `factory/model/` holds `configuration.py`, `repositories.py`
    (`RepositoryReference`, was `domain/models.py`) and `watcher_problems.py`; `factory/ports.py`
    holds `ConfigurationStore`, `WatchLease`, `CleanupSet`/`CleanupReceipts` and `ToolInstaller`;
    `factory/services/` holds the workflows, `factory_records.py` and `cleanup_marker.py` (both
    call ports, so they are services, not model); `factory/adapters/` holds the TOML store, the
    lease, the receipts and watch status. `DeadlinePolicy` is in `cli/deadlines.py`. Files moved
    with `git mv`; only import lines changed (Ruff merged two port imports into one line).
  - Deviation from the layout sketch: `factory/model/` is a package, not one `model.py`, so each
    moved file keeps its history. The `top-level` layers put `cli` and `configuration` on one line
    with `:`, which (Context7, import-linter docs) lets siblings import each other; `|` would make
    them independent. The CLI imports the facade, so `:` is required.
  - Rules: 6 contracts. New `top-level` (exhaustive) and `core-no-processes` (no indirect
    allowance). `factory` joins `inside-each-area` and `adapters-independent`; `*.services` is back
    in `adapters-from-composition`. `domain-independent`, `application-contracts`,
    `adapters-no-cli`, `contexts-not-legacy` and `shared-independent` are gone; `top-level` covers
    them (shared is its lowest layer).
  - Tests first: the proof tables were rewritten for the final layout (red: 17 failures), then the
    move made them pass. The fixture lets only `top-level` ignore `boundary_probe`. Only one
    fixture adapter starts processes, so a core probe that targets another adapter breaks only the
    composition rule. Two rows also break `adapters-independent` (the factory adapter reaches the
    probed factory port or model) and name it. New checks: an unclassified top-level module and
    an unclassified module in `factory/` fail; `top-level` lists every top-level module;
    `core-no-processes` keeps its wildcards and no indirect allowance.
  - Mutations in a scratch copy, each caught: `top-level` not exhaustive; `factory` beside the
    contexts; `core-no-processes` with indirect imports allowed or without `*.services`;
    `adapters-from-composition` without `*.services`; `inside-each-area` without `factory`;
    `adapters-independent` without `factory.adapters`.
  - Provider-name scan now covers `factory/` and `model/` packages. One known leak is recorded in
    the test: init's failure text after label writes says "check GitHub and the config file"
    (`factory/services/initialise_factory.py`). It stays: changing it changes behaviour and needs
    Scott's approval.
  - Checks: full suite 721 passed, 14 skipped; 6 contracts kept; Ruff clean.

- **Slice 4d: done** (2026-11-23). No behaviour change.
  - New `channels` context: `Channel` port (`how_to_reach`, `open`) and
    `channels/adapters/terminal.py` with `TerminalChannel`, which gets the session host from
    composition (`cli/bootstrap.py`, `build_channel`) and does not import it.
  - The AgentShell terminal asks its channel for the attach text; the session no longer knows
    how a person reaches it. `foreman`, `foreman --attach` and `init --attach` open the channel.
  - Tests first: `ChannelContract` (runs against `TerminalChannel` on `TmuxHost`) and proof rows
    for `channels` in the five rules (`channels.adapters → runtime.adapters` is rejected; the
    port is allowed). The exact attach and entry lines pinned in 4c still pass.
  - Checks: full suite 721 passed, 14 skipped; 9 contracts kept; Ruff clean.
  - Flaky under load: `test_cleanup_performance.py::…three_distinct_attempts…` failed in 2 of 3
    full parallel runs while the machine's load average was about 33 (other sessions' test runs
    and builds). It passed 4 of 4 runs alone. It waits up to 15 s for two polls
    (`tests/test_cleanup_performance.py:187`); 4d does not touch cleanup.

- **Slice 4c: done** (2026-11-23). No behaviour change a user can see.
  - New `runtime` context: `SessionHost` port (`spec`, `how_to_attach`, `enter`) and
    `runtime/adapters/tmux.py` with `TmuxHost` (launch data, attach text, terminal entry) and
    `TmuxInstall` (moved from 4b). `enter_terminal` left `owner_client.py`; the attach text left
    `terminal.py`. Composition (`cli/bootstrap.py`, `build_host`) gives the host to the AgentShell
    terminal and to `start_owner`.
  - The launch JSON carries `"host": {"kind": "tmux"}` from both launch paths (watch-owned
    terminal and persistent owner). The controller loads `tmux_host.py` (pane identity and worker
    pinning, moved verbatim) from beside itself for kind `tmux`, and refuses any other kind:
    "Unsupported Foreman host 'herdr'; AgentShell supports interactive sessions on tmux only." A
    frame without a host is "Invalid Foreman launch configuration." Factory sends only `tmux`, so
    users cannot meet the new refusal; it is the agreed guard for a future host.
  - Tests first: the attach and entry lines were pinned exactly on the old code
    (`test_watch.py`, `test_normalized_lifecycle.py`, `test_assisted_lifecycle.py`), then the
    move. `SessionHostContract` runs against `TmuxHost`; `tests/test_runtime_host.py` sends frames
    to the real controller. The Ubuntu 24.04 tmux recipe tests skip on this host, so the moved
    recipe was compared with the old `HostDependencies` (from `aed82f8`) on a faked Ubuntu 24.04:
    same question text and the same `apt-get` commands, root and non-root.
  - Rules: `runtime` joins `shared-independent`, `inside-each-area`, `adapters-independent`,
    `contexts-not-legacy` and `agentshell-in-agents`, with proof rows (the port-to-adapter row
    also breaks `adapters-from-composition` and `adapters-independent`; isolated). The controller
    may use `__file__` (it cannot import Factory); `launch.TMUX_HOST` must sit beside it.
  - Docs: the issue-watcher ADR tree was stale since 4a (old `adapters/agentshell/` paths) and the
    initialization ADR still named `WorkTrackingService` in the present tense since slice 1; both
    fixed.
  - Still tmux-aware in the agents adapter: the saved-target check in `owner_client.py` (`_reply`),
    the controller's AgentShell tmux classes, and error texts that mention the tmux attach command.
    Slice 4d moves the attach text out of the session.
  - Checks: full suite 719 passed, 14 skipped (the same environment skips); 9 contracts kept;
    Ruff clean; wheel (114 checksums) passes `tests/check_package.py`; the installed controller
    loads `tmux_host.py` from site-packages and refuses `herdr`. `dist/` was not rebuilt.

- **Slice 4b: done** (2026-11-23). No behaviour change.
  - `ForemanProfile` split. `PiAgentTeam` (`agents/adapters/pi/agent_team.py`) keeps the role
    files, native home, model catalog and completion; it takes the choices, the agent file, the
    execution flag and the repository directories instead of `FactoryConfiguration`.
    `ForgetfulSetup` (`planning/adapters/forgetful/setup.py`) keeps projects, sign-in, check and
    the local database folder. Ports: `AgentTeam` (`agents/ports.py`), `PlanningSetup`
    (`planning/ports.py`), `ToolInstaller` (`application/ports/tool_installer.py` until slice 5).
  - `host_dependencies.py` split by tool: `PiInstall` and `TmuxInstall`/`AgentShellRuntimeInstall`
    in `agents/adapters/`, `ForgetfulInstall` in `planning/adapters/forgetful/install.py`, and the
    uv check, lock extraction and install runner in `shared/installation.py`. tmux moves to
    `runtime` in 4c.
  - The agent team gets the planning role environment and the missing-tools check as functions
    from `cli/bootstrap.py`, so no agents module imports planning adapters or `application`.
  - Order kept: the old check listed tools absent from PATH (Pi, tmux, Forgetful), then managed
    copies not ready (Pi, Forgetful, AgentShell runtime). One `missing()` per tool would offer a
    stale managed Pi before a missing tmux. So the port has `absent()` and `unready()`, and
    `missing_tools` joins all absent names, then all unready names. A recipe is found by name in
    the same tool order, as the old name dispatch did. Probes run in the same order.
  - Rules: the three `ignore_imports` are gone; `agents` joins `contexts-not-legacy`. New proof
    rows: `agents.adapters → application.workflow`, `agents.model → deadlines` and
    `agents.adapters → adapters.shared` (also rejected by `adapters-independent`).
  - Tests first: a characterization test (`tests/test_pi_runtime_install.py`) showed on the old
    code that a missing tmux is offered before a stale managed Pi, and that Pi comes next; the
    existing `test_managed_forgetful_partial_install_cannot_be_accepted_on_retry` already pins
    Forgetful before the AgentShell runtime. Mutations in a copy: one `missing()` pass per tool
    fails the first; AgentShell runtime before Forgetful fails the second.
  - Contracts: `AgentTeamContract` (Pi team), `PlanningSetupContract` (Forgetful with the
    profile command double), `ToolInstallerContract` (all four installers).
  - Checks: full suite 714 passed, 14 skipped (`-n auto --dist worksteal`); 9 import contracts
    kept, no ignores; Ruff clean; wheel built to the scratchpad (110 checksums) passes
    `tests/check_package.py`, holds the new modules and none of the removed ones; an installed
    copy resolves the launch paths and builds the team. `dist/` was not rebuilt.

- **Slice 4a: done** (2026-11-23), move only.
  - `agents/adapters/agentshell/` holds the AgentShell adapter, owner, controller, model catalog,
    launch constants and runtime directory; `agents/adapters/pi/` holds definitions, profiles,
    role resources and selected skills. `agents/model.py` holds `InitialAgentChoices` and
    `AgentShellLifecycleDeadlines`; `agents/ports.py` holds `ForemanTerminal`. `DeadlinePolicy`
    stays in `deadlines.py` until slice 5; the duration check moved to `shared/validation.py`.
  - `OWNER_MODULE` and the path constants follow the files; the launch test, the built wheel
    (104 checksums) and the installed copy all resolve them. `dist/` was not rebuilt.
  - Rules: `agents` joins `shared`, layers and independence. One more temporary ignore
    (`foreman_profile → host_dependencies`). `agents` cannot join `contexts-not-legacy` until 4b:
    its profiles still take `FactoryConfiguration`. New rule `agentshell-in-agents` with
    `include_external_packages`; the harness takes external targets, and an indirect row for an
    `allow_indirect_imports` rule must pass (the composition path).
  - Before a 4a build is installed for DinoLand, stop its live owner (watcher and Foreman from
    the baseline trial are still running from the earlier wheel).
  - Finding: `tests/test_init.py:75` wrote the controller path as text, so 18 cases failed after
    the move. It now uses `CONTROLLER`, and a new coverage test refuses any `src/.../*.py` path
    written in a test. The `__file__` guard covers only `src/`, which is why it missed this.
  - Checks: full suite 692 passed, 14 skipped; 9 rules kept (3 ignores); Mycelium 0.4.5: 101
    boxes, 13 warnings, repeat export identical.
- **Slice 3b: done** (2026-11-23). `workspace/ports.py` holds `LocalRepositories`, `Worktrees`,
  `WorktreeProblem` and `WorktreeReadError`; the Git adapters moved to
  `workspace/adapters/git/{repositories,worktrees}.py`. No legacy adapter imported them, so no
  ignore was needed. `workspace` joins the context rules with proof rows. The real-Git tests
  pass unchanged.
- **Slice 3a: done** (2026-11-23).
  - `planning/model.py` holds `ForgetfulConnection`, `loopback_host` and
    `connection_from_mapping`; `planning/ports.py` holds `PlanStore` and `PlanningReadError`;
    the Forgetful adapters moved to `planning/adapters/forgetful/` (`ForgetfulPlanStore`).
  - `PlanStore.create_plan` adds the project; `owns(plan)` and `backend_identity()` replace the
    core's reads of `config.forgetful` in scaffold and cleanup. Init's setup reads stay until 4b
    splits `ForemanProfile`. The plan and receipt fixtures are unchanged.
  - The new rules found a hidden link: the Forgetful connection adapter imported
    `executable_path` from legacy `host_dependencies.py`. It moved to `shared/executables.py`;
    `nonblank` moved to `shared/validation.py`.
  - `adapters-independent` has two exact `ignore_imports` for legacy `foreman_profile.py` until
    4b. The proof fixture holds the same edges, so the ignores stay matched.
  - `PlanStoreContract` passes for `ForgetfulPlanStore` with the stateful native planning
    program; an `owns` that accepts every plan fails it.
  - Checks: full suite 690 passed, 14 skipped; 8 rules kept; Mycelium 0.4.5: 102 boxes, 13
    warnings, repeat export identical.
- **Slice 2: done** (2026-11-23).
  - `forge/` holds `RepositoryRef`, the `Forge` port and `GitHubForge`. `WorkSourceResolver` and
    `adapters/github/` are gone. `FactoryRecords.check_source` returns the remote's repository,
    and compares it with the ticket source only when the forge and ticketing provider are the
    same service. Init proposes the forge repository as the ticket source, as before.
  - The marker check takes the forge and the remote's repository
    (`validate_cleanup_marker(mapping, forge, repository)`). The saved marker fixture is
    unchanged. Its error text now says "change request URL" (operator text, not saved data).
  - Init's "Unsupported work-tracking provider" check moved into
    `GitHubTicketing.validate_source`, which refuses another provider's source; init adds its
    guidance. The ticketing contract now requires this.
  - `ForgeContract` (`tests/contracts/forge.py`) passes for `GitHubForge` and `FakeForge`.
    `tests/test_second_provider.py` runs watch with the `tracker` fake on a GitHub remote:
    intake, recovery with a GitHub PR marker, and cleanup. It failed under both old GitHub
    assumptions (marker against the ticket source; `github:`-only cleanup scope).
    `WatchFixture.entrypoint` lets a test compose a provider into the real CLI.
  - `forge` joins the four context rules and the `shared` rule. Rows may now name other rules
    that must also reject them (the skill's isolation): any `forge` to `ticketing.adapters`
    import is also an indirect adapter-to-adapter import. With that, the `*.ports` wildcard row
    `forge.ports → ticketing.adapters` is proven; it fails when the wildcard is removed.
  - A fake forge run through the whole watcher needs a host-based forge registry. That waits
    until a second real forge exists.
  - Checks: full suite 686 passed, 14 skipped; 8 rules kept; Mycelium 0.4.5: 99 boxes, 13
    warnings, repeat export identical.
- **Slice 1: done** (2026-11-23).
  - Golden fixtures (`tests/test_saved_data.py`, `tests/fixtures/saved_data/`) were recorded
    from the code before the change. The key change then shows as a two-line fixture diff:
    `"number": 1` became `"key": "1"` in the notification and in the plan snapshot.
  - `ticketing/` holds `Ticket`, `TicketSource`, `Label`, the `Ticketing` port and
    `GitHubTicketing`. `RepositoryReference` keeps its `work_source` field name, because the
    notification's `repositories` list serializes it. Remote parsing moved to
    `adapters/github/source_resolver.py` until slice 2.
  - Composition: a `TICKETING` registry and `select_ticketing` (`cli/bootstrap.py`). The core
    receives one `Ticketing`, so mixed providers in one factory are refused clearly.
  - The bundle did **not** need rebuilding: role skills are starter templates outside the hashed
    bundle, and no bundled extension reads the notification or `external_ref`. Only the Foreman
    and feature-owner skill texts changed.
  - Rules: `inside-each-area`, `adapters-from-composition`, `adapters-independent` and
    `contexts-not-legacy`. `*.services` is left out until a `services` package exists; the new
    rule-name check failed on it, as designed. Composition rule sources include legacy
    `application` and `domain` until they move. The harness now works out report names for
    layers and independence rules too.
  - `TicketingContract` (`tests/contracts/ticketing.py`) passes for GitHub (stateful `gh` stub)
    and `FakeTicketing` (`ENG-123` keys). Provider-name scan for every `ports.py`/`model.py`.
    The second fake provider's run through scaffold, watch and cleanup moves to slice 2, where
    the fake forge exists.
  - Proof: each new rule, weakened in a scratch copy, failed its test; integer keys from the
    GitHub adapter failed the contract; "GitHub" in `ticketing/model.py` failed the scan.
    Full suite 677 passed, 14 skipped; 8 rules kept. Mycelium 0.4.5: 98 boxes, 13 warnings.
- **Slice 0: done** (2026-11-23, branch `refactor/domain-contexts`).
  - `shared/` holds `FactoryError` (`errors.py`), `watch_stop.py`, `command.py`,
    `sensitive_command.py`, `resource_files.py` and `resources.py` (`resource_root()`, which
    replaces the five `parents[n]`). Adapters no longer import `application.watch_stop`.
  - `adapters/agentshell/launch.py` holds the launch constants (`CONTROLLER`, `MODEL_CATALOG`,
    `OWNER_MODULE`). Slice 4a moves them with the files; no `tmux_host.py` exists yet.
  - New rule `shared-independent`. The harness now uses `ALLOWED`/`REJECTED` tables, with one
    test per configured rule. Coverage checks: package markers, rule names, the `shared` rule
    covers every top-level module, `__file__` only in two files, launch targets and resources
    resolve.
  - Proof: in a scratch copy, each guard failed on its own mutation: weakened rule, rule
    without rows, row naming an unknown rule, rule rejecting composition, folder without
    `__init__.py`, wildcard matching nothing, unread contract type, new top-level module,
    `__file__` elsewhere, renamed controller, moved owner module.
  - Checks: Ruff; `lint-imports` 4 kept; compileall; full suite 640 passed, 14 skipped (was 635).
    Wheel built outside `dist/`: 89 checksums verified; resources and launch targets resolve
    in the installed wheel. Mycelium 0.4.5 from the cached archive (no install): 96 boxes,
    the same 13 warnings, repeat export identical. Doc line citations remapped with difflib.

Order reason: slices 0–2 are pure Python and low risk, and they fix the GitHub coupling first.
Slice 4 touches the live Foreman lifecycle, so it comes after the structure is proven.
Test churn: 10 test files import `adapters`/`application`/`domain` directly, and about 20 lines
import `deadlines`. `configuration.py` stays, so its imports do not change.

## Trial run (DinoLand)

Unit and integration tests use fake agents. Only a live run shows that a real user can set up a
factory and get an issue processed end to end. DinoLand
(`/home/scott/development/DinoLand`, `git@github.com:ScottRBK/DinoLand.git`) is the trial
workspace. Scott authorized removing its existing factory setup for this.

**When:**

- **Baseline:** on current `main`, before slice 0. This shows which failures already exist, so a
  later failure is not blamed on the refactor. Its results go in this file.
- **Smoke:** after slice 4d: fresh setup through to the first notification reaching the Foreman.
- **Final:** after slice 5, the full run below.

**Rule: act only as a user could.** The agent running the trial may only:

- build the wheel and run the README commands (`init`, `watch`, `foreman`, `update`), and answer
  their prompts;
- stop a watcher with Ctrl-C (or SIGINT to that watcher only), as a user would;
- use ordinary Git, `gh` and file commands to remove the old setup;
- create, label and comment on GitHub issues, and review or approve PRs, as Scott would;
- type into the Foreman's terminal, the user's channel (tmux `send-keys` to the Foreman pane only).

It must not:

- edit `.factory/` files by hand, unless the README or Foreman tells the user to do so;
- write Forgetful records directly, or edit plans, tasks or worktree mappings;
- type into worker panes, kill agent processes, or patch the installed package;
- change role guidance mid-run except through the documented `update` flow.

If a step needs anything outside these rules, **the trial fails at that step**. Record the
finding, fix it in code with a regression test, rebuild, and restart the trial from setup.

**Steps:**

1. **Stop the old factory.** Ctrl-C any running DinoLand watcher, which closes the Foreman it
   owns. Check by working directory: other factories (such as `dark-business`) run from the same
   wheel and must not be touched. On 2026-11-23 nothing ran for DinoLand; its last watch run
   (`81de0938…`) stopped on 2026-11-17 with `cleanup_uncertain`, and no DinoLand Pi was left.
2. **Remove the old setup, reversibly.** Move `DinoLand/.factory` to a dated backup outside the
   repo, then run `git worktree prune`. Old local `factory/*` branches may be deleted with
   `git branch -D`. Leave Forgetful project 13 and remote branches untouched.
3. **Install.** Build with `uv build --out-dir <scratch folder>`, then use the README
   `uvx --refresh --from "$wheel"` form with that wheel. Record the commit and wheel SHA256.
   **Never rebuild this repo's `dist/`:** other factories (such as `dark-business`) restart from
   that wheel path.
4. **Set up.** Run `init` in DinoLand: share the Pi profile, choose models, reuse Forgetful
   project 13 (Scott, 2026-11-23: "its just easier"), keep execution enabled, choose a Definition
   of Done preset, then launch the factory with `--new-only`. For the smoke and final trials,
   project 13 holds plans saved with integer issue numbers. Decision 6 has no reader for them,
   so those trials use a new project unless Scott decides otherwise.
5. **Raise an issue.** Create a small, clearly testable DinoLand issue with the `factory` label.
6. **Follow it to the end.** Answer clarification questions on the issue or in the Foreman
   terminal. Check each stage: watcher plan and worktree → Foreman notification → feature-owner
   plan → implementation PR → passing CI for the exact commit → independent review →
   merge → DoD checks → plan completed → cleanup removes the worktree and both branches.
7. **Record evidence** here: commit, wheel SHA256, issue and PR URLs, Forgetful plan id, stage
   times, CI run ids, and any step that failed or needed help.

**Pass:** every stage in step 6 completes with no action outside the rules.

### Baseline results (passed with findings)

- Build: commit `ff5bc18`, wheel SHA256
  `9acc02c5cd13663d4075b235340e82563d4e6c481cc75735d72b0e767658c6b1`. The wheel was built in
  `dist/` before the no-rebuild rule; dark-business runs from its uv cache copy of the same
  commit, so it was not changed.
- Setup: `init` with Pi profile `~/.pi/forgetful-agent`, server `http://localhost:8022/mcp`,
  project 13, label `factory`, DoD "After merge", execution enabled. Old setup backed up to
  `/home/scott/development/DinoLand.factory-backup-2026-11-23`.
- Issue [#22](https://github.com/ScottRBK/DinoLand/issues/22) created 20:40:06 UTC.
- Watcher restarted with `watch --existing` (see F1). Intake submitted 20:53:40; worktree
  `factory/scottrbk-dinoland-22`; Forgetful plan 14, ownership task 213.
- [PR #23](https://github.com/ScottRBK/DinoLand/pull/23) opened 21:02:17, head `c147c0bc`.
  Unit tests passed. Browser suites on the self-hosted runner: push run 45265461575 cancelled at
  20 minutes; PR run 45265515883 attempt 1 failed (`#app:not([inert])` 30 s timeout), attempt 2
  cancelled at 20 minutes, attempt 3 passed at about 22:00. The feature-owner ran the reruns.
- Review (plan task 215) posted 22:07:43 as COMMENTED, no blocking findings (see F4).
  PR merged 22:08:58; issue closed.
- Merge commit `bf7d8b0` (22:08:29 UTC). The Foreman checked the DoD ("After merge": review,
  checks on the exact final commit, confirmed merge) and checked `GET /healthz` on the server
  itself. It completed plan 14 with tasks 213–216 done.
- 22:31:59: the watcher confirmed cleanup for plan 14. The worktree, local branch and remote
  branch `factory/scottrbk-dinoland-22` are gone.
- Result: every stage passed with no action outside the rules. The F1 workaround (Ctrl-C, then
  `watch --existing`) is a normal user action. The watcher and Foreman were left running.

Findings:

- **F1. `--new-only` baseline is late.** The baseline is taken on the first successful read,
  after Foreman start, cleanup and recovery (`watch_factory.py:82-133`, `:280-295`). That was
  about 6 minutes after the user chose "n", so issue #22, created after launch, was treated as
  existing and skipped (`watch_factory.py:356-359`). Workaround inside the rules: Ctrl-C, then
  `watch --existing`. Fix test-first on `main`, outside this plan.
- **F2. Slow intake with a reused project.** Each cycle, cleanup and recovery read every plan in
  the project through the Forgetful CLI before intake (`cleanup_completed.py:46-95`). Intake
  began about 7.5 minutes after start.
- **F3. Start-later hint.** The `init` "start later" text prints a uv cache Python path, not the
  README `uvx --from "$wheel"` command.
- **F4. Reviewer cannot run tests.** The independent reviewer's sandbox blocked network and local
  servers (`listen EPERM`, `spawnSync git EPERM`), so its local `npm test` failed. It relied on
  the CI run for the exact head. The feature-owner posted the review for it. The review found no
  blocking issues.

### Smoke results (passed)

- Build: commit `32338e0` (slice 4d), wheel SHA256
  `47cb0397f1928ef0044186a31ba23a5ba8eb5b03aee373c93a0f6d9e5a1d41db`, built to the scratchpad
  (118 checksums verified). `dist/` was not rebuilt.
- Throwaway private repo `ScottRBK/factory-smoke-20261123` (Scott, 2026-11-23), cloned into the
  session scratchpad. `init` with the baseline's choices (Pi profile `~/.pi/forgetful-agent`,
  server `http://localhost:8022/mcp`, label `factory`, the same models, execution enabled, DoD
  "After merge"). Init offered the Forgetful CLI install, then the AgentShell runtime install
  (Pi and tmux were present), the order kept by slice 4b. It created Forgetful project 26
  (`factory-smoke-20261123`) and the `factory` label. F3 appeared unchanged.
- Launched from init with "e" (the repo had no issues, which avoids F1). The startup line was
  "Watcher owns Pi and closes it on stop. Attach during startup: tmux attach-session -t
  factory-foreman-8c8ccdc0124f", now made by the channel and the session host.
- Issue [#1](https://github.com/ScottRBK/factory-smoke-20261123/issues/1) created 00:03:46 UTC
  (2026-11-24). The watcher printed "Submitted github:scottrbk/factory-smoke-20261123#1 to Pi"
  and the Foreman's session log shows the notification by 00:04:44: `"id":
  "github:scottrbk/factory-smoke-20261123#1"`, `"key": "1"` (decision 6), plan 16, ownership
  task 225, worktree branch `factory/scottrbk-factory-smoke-20261123-1` (same format as before).
  The Foreman began dispatching a feature owner.
- Stopped with Ctrl-C at 00:05:09: "Error: Watch interrupted."; the Foreman session closed and
  no Pi process or pane was left. Plan 16 was a draft with task 225 still to do.
- Result: fresh setup to the first notification reaching the Foreman passed, with no action
  outside the rules. Intake took about one minute (new project, so F2 did not apply).
- Cleanup: Forgetful project 26 deleted (plan 16 went with it); the two Pi session folders the
  trial made in `~/.pi/forgetful-agent/sessions` removed; workspace, tmux session and local
  branch removed. The remote had only `main` and no PRs. Scott (2026-11-24): keep the private
  repo for now; later trials may reuse it. Deleting it needs the `delete_repo` token scope.

### Final trial results (passed)

- Build: commit `9867804` (slice 5b), wheel SHA256
  `f0b51ace56977a3d212287cd3115684ff0e6c102255bf29cbf9d44c68b3df2ad` (117 checksums), built to
  the scratchpad. `dist/` was not rebuilt.
- Repo: the kept `ScottRBK/factory-smoke-20261123`, cloned fresh. Before the run, a minimal CI
  workflow was added to its `main` (`f8850b1`, `actions/checkout` pinned to the `v4.2.2` SHA), so
  the "checks on the exact commit" stage is real. Open issue #1 ("Add hello.txt with a greeting").
- Setup (00:54–01:01 UTC, 2026-11-24): `init` with the smoke trial's choices. Init offered the
  Forgetful CLI install, then the AgentShell runtime install; it created Forgetful project 27 and
  reused the `factory` label; DoD "After merge". Launched from init with "e".
- 01:02: "Submitted github:scottrbk/factory-smoke-20261123#1 to Pi"; worktree
  `factory/scottrbk-factory-smoke-20261123-1`; plan 17, ownership task 226.
- 01:06: [PR #2](https://github.com/ScottRBK/factory-smoke-20261123/pull/2) (only `hello.txt`),
  head `f22c728`; CI run 45302435387 passed on that head.
- 01:10:44: independent review 6032104432 on `f22c728`, COMMENTED, no findings. The reviewer's
  sandbox could not reach GitHub, so the feature owner posted its pinned payload (as F4).
- 01:11:23: merged as `a90f1ad`; issue #1 closed; post-merge CI run 45303135941 passed.
- The Foreman checked the DoD itself (PR, merge commit, review, checks on the exact revisions)
  and completed plan 17 with tasks 226–230 done; evidence in `.factory/delivery/plan-17.md`.
- 01:22: the watcher removed the worktree, the local branch and the remote branch: "Cleanup
  confirmed for completed plan 17".
- Result: every stage of step 6 passed with no action outside the rules. Stopped with Ctrl-C
  ("Error: Watch interrupted."); the Foreman session closed and no Pi process was left.
- Cleanup: project 27 deleted (plan 17 went with it); the two Pi session folders removed; the
  workspace and tmux session removed. The repo is kept with its CI workflow; only `main` remains.
- The review fixes came after this build; see the re-run below.

### Final trial re-run (passed)

- Build: commit `2b41d1c` (first review fixes), wheel SHA256
  `310d85712e4e59fd15b3b993559262721c7d0b889e255681b5baba22094d13cd` (117 checksums), built to the
  scratchpad. Later commits (`9cf35d6`, `045f2f4`) change only edge cases on damaged saved data
  and controller start without `ctypes`; their tests cover them.
- Same repo, cloned fresh. Issue [#3](https://github.com/ScottRBK/factory-smoke-20261123/issues/3)
  ("Add goodbye.txt with a farewell") created by the user at 01:33 UTC before setup.
- Setup 01:34–01:39: same choices; Forgetful project 28 created; label reused; DoD "After
  merge"; launched from init with "e". 01:39: "Submitted github:scottrbk/factory-smoke-20261123#3
  to Pi"; plan 18, ownership task 231, worktree `factory/scottrbk-factory-smoke-20261123-3`.
- 01:45: [PR #4](https://github.com/ScottRBK/factory-smoke-20261123/pull/4) (only
  `goodbye.txt`), head `f05323a`; CI run 45307284863 passed.
- 01:48: the Foreman asked the user to decide: the review worker's sandbox had no network (F4),
  so it could not read the issue or post a review, and the Foreman would not let the owner post
  for it (in the first trial the owner did). The user (this trial's operator, through the
  Foreman's terminal) chose the owner's recommended option: a one-time `auto_approve` for that
  review dispatch only. This is a normal user answer inside the rules.
- 01:51: review 6032434549 on `f05323a`, COMMENTED, no blocking findings. 01:52:17: merged as
  `ad7be1c` (`--match-head-commit`); issue #3 closed; post-merge CI run 45308219094 passed.
- The Foreman verified the DoD and completed plan 18 (tasks 231–234 done). The watcher then
  confirmed cleanup for plan 18: worktree, local and remote branch removed.
- Later, while idle, two polls failed with "error connecting to api.github.com" and were retried
  as designed (a network problem on this host; GitHub answered again afterwards).
- Result: every stage passed; the only user action was the answer above. Stopped with Ctrl-C;
  the Foreman closed and no Pi was left. Cleanup: project 28 deleted; the two Pi session folders,
  the workspace and the agents' evidence folder `/tmp/fo-evidence-18` removed (its handoff was
  kept in the session scratchpad). The repo keeps `main` only.
- New observation for later (not the refactor): the reviewer's sandbox has no network, so every
  review needs a user decision or an owner workaround (F4 again).
- Smoke on the last code (`01b57f9`, wheel `86d0e609…`, 117 checksums), because later commits
  change how the controller starts: fresh setup with project 29, launched with "n": "Foreman
  session ready" and "Baseline scottrbk/factory-smoke-20261123: 0 matching issues". Stopped with
  Ctrl-C; project 29, its Pi session and the workspace removed.

## Decisions

Scott agreed these on 2026-11-23:

1. **Extra contexts.** `planning` (Forgetful), `agents` (AgentShell/Pi/definitions) and
   `workspace` (Git) are contexts, in addition to factory, forge, ticketing, channels and runtime.
2. **Layout.** Context-first folders (above). Rejected alternative: keep
   `domain/application/adapters` with context subfolders inside each, because a new provider
   would then touch three folders.
3. **Names.** `ticketing`/`Ticket` in code. Agent-facing text ("Factory issue notification")
   stays the same. The only exception is the `key` change in decision 6.
4. **Runtime axes.** Host and isolation are separate, as in AgentShell. Only tmux and no
   isolation are usable today (see [Runtime](#runtime-host-and-isolation)).
5. **FACTORY.md.** It names GitHub and tmux directly. Scott will update it to describe forge,
   ticketing, channels and runtime as separate work. This plan does not depend on that change.

6. **Ticket key type.** Text keys now (`Ticket.key: str`), with no reader for plans saved by older
   builds. Factories are early in their life; a fresh factory and Forgetful project are needed
   after upgrading. See [Saved data](#saved-data).
7. **Trial run.** Validate on DinoLand, acting only as a user could: baseline before slice 0,
   smoke after 4d, full run at the end. See [Trial run](#trial-run-dinoland).

## Review record

Fable reviewed the first draft on 2026-11-23 ("ready after changes"). Each finding was checked
against the source before it was accepted. All were accepted:

- Runtime port could not be a Python object across the controller process: now plain data.
- Only tmux supports interactive sessions: claim corrected; isolation removed from the port; the
  "native host plus terminal channel" rule and test removed.
- `Ticket.key: str` would break saved plan context and notifications: Scott then chose to make
  that change deliberately (decision 6), recorded in fixtures and guidance.
- Forge/ticketing still shared saved data and checks: marker uses the remote; same-provider check.
- More GitHub strings in the core; missing `validate_source`: added to problems and slice 1.
- `PlanStore` too thin: owns project id and backend string; `planning/model.py` added.
- Rules 2, 4 and 6 would fail at once: `factory/adapters`, optional layers, own-context port
  types, and the `configuration.py` composition entry added.
- Slice 4a too big; path coupling: split into 4a–4d; launch-path checks; resource-root function.
- Slice 3 split; `Forge.check_ready` cut; module homes listed; test-file counts corrected.

## Out of scope (follow-up work)

- **New adapters:** GitLab, Linear, Slack and others come after this plan.
- **Multi-repo ticket sources:** a Linear team or ADO project can cover many repositories. How a
  ticket maps to a repository needs its own design. This plan keeps one ticket source per
  repository entry.
- **Agent-side forge tooling:** role skills name `gh` directly. A GitLab forge needs
  forge-specific skill text. That needs its own design.
- **Other hosts and isolation:** herdr interactive sessions, Docker and bubblewrap need AgentShell
  work first.
- **Typed plans and tasks** in `planning`: wait until a second plan store or a real need.
