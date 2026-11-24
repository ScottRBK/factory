# Development checks and dependency boundaries

Push and pull-request CI build the package, verify the wheel, lint Python, check import boundaries
and run the test suite. See [current hosted results](../plan.md#current-status).

Back to [architecture](../architecture.md).

## Context and decision

Preserve the hexagonal boundaries as providers and workflows grow. Check ordinary Python issues
and the import graph in CI without adding development tools to runtime installations.

## Lint and architecture contracts

The `dev` dependency group provides Ruff 0.17.0, Import Linter 2.15, pytest 9.2.0 and
pytest-xdist 3.8.0, separate from runtime package dependencies. `uv.lock` records exact resolved
versions and artifact hashes for local and CI installs. See
[uv dependency management](uv-dependency-management.md) for the decision and tool audit.
Updates require another dependency audit.

Ruff checks `src/` and `tests/` for common Python errors, unused imports, import ordering, and
`E501` with a 100-column limit. `TID251` bans `pytest` imports, which keeps tests in `unittest`
style (see [test runner](#test-runner)). Ruff infers Python 3.12 from `requires-python` rather than
repeating the setting. Formatting is not required or added.
Ruff's line-length rule has documented exceptions; it is not a strict Markdown-width validator.

Import Linter's six contracts in `pyproject.toml` enforce:

- `top-level`: imports go down only: `__main__`, then `cli` and the `configuration.py` facade,
  then `factory`, then the contexts (`agents`, `channels`, `forge`, `planning`, `runtime`,
  `ticketing`, `workspace`), then `shared`. Siblings on one line may import each other (`:`):
  the CLI uses the facade, and contexts use each other's ports and models. It is exhaustive, so a
  new top-level module fails until it is classified. Every area may import `shared`.
- `inside-each-area`: inside `factory/` and each context, imports go down only: adapters,
  services, ports, model. It is exhaustive, so a module outside those layers fails.
- `adapters-from-composition`: shared, services, ports and models do not import any adapters.
  Only CLI composition and the configuration facade do.
- `adapters-independent`: adapter packages (`factory/adapters/` and each context's) do not import
  each other. Composition gives the agent team what it needs from planning: the role environment
  and the missing-tools check are functions passed in by `cli/bootstrap.py`.
- `core-no-processes`: services, ports and models do not import `subprocess` or `socket`, directly
  or through another module. Process and socket work stays in adapters and `shared/`.
- `agentshell-in-agents`: only `agents.adapters` imports `agent_shell` directly. It needs
  `include_external_packages = true`. It sets `allow_indirect_imports`, because composition reaches
  AgentShell through the agents adapter; its indirect proof rows must pass.

These checks include submodules and indirect paths. Bootstrap and the public configuration loader
are composition entry points and may construct adapters. The rules are coarse layer checks, not an
allowlist limiting adapters to ports; adapter-to-service imports and external integration imports
are not separately restricted. Dynamic imports and runtime operations such as built-in file access
remain outside these checks. `tests/test_architecture.py` invokes the real checker on temporary,
importable fixture packages, using the repository's actual contracts. Two tables drive it. `ALLOWED`
lists the permitted imports; together they form the known-good fixture, which must pass every rule.
`REJECTED` lists (rule, area, target) rows; the area is a package (the probe is a new module) or a
module (the probe line is added to it). Each configured rule gets its own test, which fails if the
rule has no rows. Only the row's own rule may reject it, so `cli` rows target `cli.prompts`, which
imports nothing. Where that cannot hold, the row names the other rules that must also reject it, and
step 1 turns those off too; for example, any import from `forge` to `ticketing.adapters` is also an
indirect `forge.adapters` to `ticketing.adapters` import. The checker's report must name the rule's
own units, worked out for forbidden, layers and independence rules. Each row proves direct and
indirect rejection, checks that disabling the target rule permits the violation, and checks that
removing it passes again. Assertions identify the exact forbidden area pair, not merely a target
appearing somewhere in a longer rejected path. Indirect helpers live outside both endpoint areas.
Rule isolation uses CLI contract selection, preserving all global settings. No intentional
violations are written into the actual source tree. These repeatable proofs guard against later
weakening of the configuration, rather than mocking an import-analysis library. Coverage checks in
the same file guard what the checker cannot see by itself:
- Every source folder with Python files has `__init__.py`; a missing marker hides modules.
- Every internal name in a rule matches a real module. Import Linter skips a wildcard that
  matches nothing, which turns a rule off silently. The check fails on a contract type it does
  not yet read, so a new type extends it.
- The `top-level` rule lists every top-level module and is exhaustive; a proof shows an
  unclassified top-level module and an unclassified module in `factory/` or a context fail. The
  fixture lets only the top-level rule ignore its `boundary_probe` package.
- `core-no-processes` uses wildcards for services, ports and models, so a new context is covered
  without an edit, and it does not allow indirect imports.
- Every `ports.py`, `model.py`, `model/` and `factory/` file names no provider or host
  (`github`, `gitlab`, `codeberg`, `linear`, `tmux`, `herdr`, `agent_shell`). Import rules cannot
  see a hard-coded name or URL. One known exception is recorded in the test: init's failure text
  after label writes says "check GitHub" (`factory/services/initialise_factory.py`). It is kept
  because the refactor must not change behaviour; changing it needs Scott's approval.
- No test writes a source file path (`src/forgetful_factory/.../*.py`); tests use the launch
  constants instead.
- Only `shared/resources.py`, `agents/adapters/agentshell/launch.py` and the controller use
  `__file__`. Files started by path (`controller.py`, `model_catalog.py`) and the owner module name
  are constants in `launch.py`, and a test checks that each resolves in the source tree. The
  controller runs in AgentShell's interpreter, where Factory cannot be imported, so it loads its
  host checks (`tmux_host.py`) from beside itself; `launch.TMUX_HOST` and a test check that file
  is there.

`tests/contracts/` holds one `unittest` mixin per port. `TicketingContract` states what every
`Ticketing` adapter promises: label matching ignoring case, `*`, epics, text keys that pass
`is_key`, content-only revisions, source checks (including another provider's source) and labels.
`ForgeContract` states that every accepted remote form names one repository, unsupported remotes
fail, and change-request URLs belong to their repository. `PlanStoreContract` states that a created
plan is in the store's project and found by reference, another project's plan is not owned, plans
and tasks update, and the backend identity is stable text; it runs against `ForgetfulPlanStore` with
the stateful native planning program. `PlanningSetupContract` states that a created project is
listed, the check confirms access to a selected project and refuses none, prepare can repeat, and
the browser-login need is yes or no; it runs against `ForgetfulSetup` with the profile command
double. `AgentTeamContract` states that declined home consent saves nothing, accepted consent is
kept once saved, setup is incomplete until recorded, and no memory notice exists before a launch is
selected. `ToolInstallerContract` states that a bare host misses the tool, an installed tool is not
missing, and other tools are neither described nor installed; it runs against each installer (Pi,
tmux, Forgetful, AgentShell runtime). `SessionHostContract` states that the host's launch data is
plain data with a kind, its attach text names the session, and entry without a terminal only prints
how to enter; it runs against `TmuxHost`. `ChannelContract` states that the way to reach a session
names it and that opening without a terminal only prints how; it runs against `TerminalChannel` on
`TmuxHost`. `PersistentForemanContract` states that without an owner there is no record, report or
status, an unreadable record is reported unknown with a warning, and a silent owner is history,
never a live observation; it runs against `AgentShellOwner` without live owners.
`AgreementStoreContract` states that an empty workspace has no agreement, a written agreement reads
back, and writing again never replaces it; it runs against `MarkdownAgreement`.
`tests/test_runtime_host.py` also sends launch frames to the real controller: an unknown host kind
is refused before a session opens, and a frame without a host is invalid. The ticketing and forge
mixins run against the GitHub adapter (with a stateful `gh` stub for ticketing) and a non-GitHub
fake: `FakeTicketing` (`tracker`, keys such as `ENG-123`, state in a JSON file) and `FakeForge`
(`forge.example`, `/changes/N`). A new adapter is done when it passes its mixin.

`tests/test_second_provider.py` runs the public watch CLI with `FakeTicketing` composed in on a
GitHub remote: intake, restart recovery with a GitHub PR cleanup marker, then completed-plan
cleanup. It failed when the marker was checked against the ticket source, and when cleanup scope
accepted only `github:` references. This is the leak check for GitHub strings, patterns and
numeric keys in the core.

`tests/test_saved_data.py` pins the bytes Factory stores or sends to agents: plan record and
context, ownership task, issue notification, watcher alert, cleanup receipts, init's
`factory.toml` and cleanup-marker decisions. It runs the public `watch` CLI with fake `gh` and
`forgetful` programs and compares against `tests/fixtures/saved_data/`. Only host paths and the
default branch name are normalized. Each stored JSON value must also re-serialize to its exact
bytes. A deliberate change is recorded with `UPDATE_SAVED_DATA=1` and reviewed as a fixture diff.

CI installs through `uv sync --locked` and runs Ruff, the real-source architecture check,
and the full test suite through `uv run --locked` on Python 3.12/3.13. CI also runs
`uv build` followed by `uv run --locked python tests/check_package.py dist/*.whl` to verify
wheel RECORD membership, sizes and standard Base64 digests, instead of relying on editable installs.
CI rebuilds the repository's Python source caches once before testing, using checked-hash
bytecode. The force option also replaces valid timestamp-based caches. Repeated CLI children can
reuse compiled source; Python checks its content hash before using a cache. This changes no
production behavior, assertion or deadline. The test-runner environment keeps bytecode writing
disabled; lifecycle fixtures manage their own child environments. No cache is restored from another
CI job.
The runner reports the slowest 25 cases, including setup and cleanup. Local commands are in
the README. The [quality-checks plan](../plans/quality-checks.md) records the original CI checks.

## Test runner

Tests are `unittest.TestCase` classes. pytest with pytest-xdist is the runner only. It runs the
same 648 test IDs as `python -m unittest discover`, in parallel worker processes:

```bash
uv run --locked pytest -n auto --dist worksteal -v --durations=25
```

- pytest 9 reports each failing `subTest`. It does not support the `load_tests` protocol; do not
  add it. Fixtures, `parametrize` and marks do not work in `TestCase` classes.
- Ruff `TID251` bans `pytest` imports. A bare `def test_x(): assert ...` function is not caught;
  review must reject it. Changing to pytest-style tests needs Scott's agreement.
- `--dist worksteal` balances test times from 0.01 s to about 12 s. `-n auto` uses one worker per
  CPU. The suite is CPU-bound (process creation), so more workers than CPUs gain nothing and make
  short harness timeouts more likely to expire.
- `[tool.pytest] faulthandler_timeout = 120` prints all thread stacks for a test that runs longer
  than 120 s. xdist prints a test name only when it finishes, so this is how a hang is found.
- Each test needs its own temporary workspace, tmux socket, HOME and port 0. Tests may change
  `os.environ` in-process only because each worker is a separate process.
- `python -m unittest discover -s tests` still works, but CI no longer guards it.

## Public testing boundaries

Use TDD at the public boundaries approved by Scott:

- **Initialization CLI:** exercise the real command with temporary Git repositories and files.
  Control external GitHub, Pi, Forgetful and installer commands. Cover consent, project/model
  selection, native schema responses, provisioning, safe reruns and failures without live accounts.
- **Configuration loading:** read saved TOML through the public loading API, checking round-trips
  and rejection of invalid settings.

- **Watcher CLI:** temporary configuration and controlled external commands, using real Git for
  worktree safety. Cover plan/task creation, uncertain outcomes, revisions, restart, notification,
  cleanup and exclusive workspace ownership. Run the real AgentShell lifecycle with Pi/tmux doubles.
- **Planning adapter reads:** approved for the CI runtime follow-up. Exercise the real
  `ForgetfulPlanStore.plans()`, `get_plan()` and `tasks()` operations with a controlled external
  Forgetful executable and real temporary files. Check complete malformed-input matrices here;
  retain watcher CLI proofs for each distinct inventory/detail pause, alert and recovery path.
  No private validation helpers or mocked internal calls replace either boundary.
- **Numbered choices:** use public `parse_numbered_selection()` for every malformed answer and
  both valid endpoints. Retain a real CLI rejection at each distinct prompt, positive model/effort
  wiring, and no configuration, receipt or label mutation.
- **Planning access catalogs:** call `AgentForgetfulConnection.check()` through a controlled real
  executable and JSON. Retain every permission/reference-field case and CLI access/completion
  proofs.
- **Login metadata:** call `uses_browser_login()` against real loopback HTTP for the policy matrix.
  Retain CLI notice/access routing, absent credentials and redirect refusal.
- **Persisted cleanup:** use public `validate_cleanup_marker()` for malformed and canonical markers.
  Use `GitWorktrees.verify_removed()` with real Git/files for occupied paths, stale/relocated
  registrations and changed origins. Retain absent/pending/invalid/removed watcher routes,
  occupied-path/changed-origin routing, no mutation and no recreation.
- **Package artifacts:** build the real wheel/sdist and inspect their public contents. The wheel
  checksum gate catches invalid RECORD encoding without importing or installing package code.
- **Native integration:** opt-in isolated Pi SDK/lifecycle and local Forgetful checks. Use temporary
  HOME/config/database paths and no-inference probes. No real login or provider requests. These
  validate native wiring and contracts, not an autonomous agent's planning quality.

Do not add tests coupled to private helpers or internal mock calls. Write `unittest.TestCase`
tests (see [test runner](#test-runner)); the architecture proof tests additionally invoke the
development-only Import Linter command.
Independently validate the installed package through local `uvx`.
Live GitHub label validation in Dark Business requires separate confirmation of target repositories.

Lifecycle tests need installed tmux on the runner's PATH (for example apt or Nix). They run real
AgentShell with fake Pi in a private tmux server and isolated homes, without service or model
calls. To include optional native SDK probes:

```bash
NATIVE_PI_SDK=/absolute/pi-coding-agent/dist/index.js \
  uv run --locked pytest -n auto --dist worksteal -v --durations=25
```

Use an isolated SDK environment, never a personal Pi profile. These probes test native loading
without inference; they do not prove provider access, OAuth refresh or autonomous planning.

## Explicit deadline composition

`cli/deadlines.py` provides frozen `DeadlinePolicy` and `AgentShellLifecycleDeadlines` values. Each
value must be finite and positive. Public `cli.main.main(policy)` and bootstrap composition pass
command deadlines, owned-process TERM grace, and lifecycle deadlines to the relevant adapters.
Owned owner/controller startup transports the lifecycle values as JSON; the controller validates
all fields before opening a session. Factory services retain their existing port contracts.

Ordinary CLI execution uses the original production values. There is no timeout flag, environment
variable, saved setting, global multiplier or fake clock. Existing installer/access deadlines and
unrelated transport waits are not globally scaled. The native AgentShell SDK's fixed five-second
command timeout remains unchanged and has its own real timeout/cleanup test.

Tests may supply short real expiry through this public composition. They must still observe the
actual process or session failure, signal handling, ownership, cleanup and uncertain outcomes.
The three-second threshold identifies cases to investigate; it is not a required test limit.
Repeated setup may be reused only with complete restoration of files, environment, Git origin,
external state and logs. Replace race-avoidance sleeps with observable external synchronization,
not shorter sleeps or production polling changes. Wait for the state an assertion depends on,
not an earlier signal: for example every expected alert, or the watcher's own published
readiness (`WatchFixture.wait_for_published_ready`) rather than the fake Pi `ready` record.
Preserve distinct busy-owner and pane-loss tests.

Implementation and measured evidence are in the [runtime plan](../plans/ci-test-runtime.md).

## Continuous integration

The GitHub Actions workflow `.github/workflows/ci.yml` runs the same test suite on every push,
without branch, tag, or path filters, and on pull-request opening, reopening, and updates.
New runs cancel older runs for the same workflow and ref. Push and PR refs remain separate, so
an open PR's branch push also produces a PR run. Separate `ubuntu-latest` jobs use Python 3.12
and 3.13. Each installs the package and locked development dependencies, runs Ruff and the
architecture check, then runs tests including the contract proofs. No project secrets are required;
tests substitute external GitHub and AgentShell, with no live model calls.
At Scott's request, official checkout and Python setup actions use movable `v7` tags to receive
compatible updates. Permissions remain read-only and checkout credentials are not persisted.
Movable tags can change after their release was checked. Historical hosted results are in the
[slice 1](../plans/slice-1.md), [slice 2](../plans/slice-2.md), and
[quality-checks](../plans/quality-checks.md) plans.
The job limit is 15 minutes. The test step prints a `::warning::` annotation when tests take
more than 450 s (half the limit), on pass or fail, so suite growth shows before a cancellation.
Record hosted test seconds for each slice in the [runtime record](../plans/ci-test-runtime.md),
which also keeps earlier job-limit failures, timings and changes to the test suite. Production
deadlines and process and Git safety checks still apply.

## Local static analysis

Local static analysis uses the existing SonarScanner CLI against `http://localhost:9001`, project
`forgetful-factory`. Ignored `.sonarqube/project.properties` identifies this project; scans include
`src/` plus `tests/`. The local `.sonarqube/start-scan.sh` passes the shared vault aliases
explicitly:

```bash
envault run --env SONAR_TOKEN=sonar-token --env SONAR_HOST_URL=sonar-host-url -- \
  sonar-scanner -Dproject.settings=.sonarqube/project.properties
```

These mappings need no per-repository `envault.toml`. Use explicit mappings for result queries too;
never put token values in arguments or source `.env`. This development check is not a factory
runtime dependency. The expected server gate is `Sonar way sans code coverage`; complexity rules
come from the Python quality profile. Local scanner setup does not follow Git worktrees and must
be repeated where needed. The [SonarQube record](../plans/sonarqube-remediation.md) identifies
the source covered by those scans. [CLI onboarding](../plans/cli-onboarding.md) records earlier
credential-permission limits.

## Consequences

Import rules prevent known dependency directions, not all architectural mistakes. Keep the
repeatable violation proofs when changing contracts; reconsider rule isolation if contracts overlap.
Formatting, external-import allowlists, runtime sandboxing, and live model calls are not CI gates.
