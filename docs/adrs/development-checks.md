# Development checks and dependency boundaries

Status: implemented locally; hosted validation status is tracked in the
[quality-checks plan](../plans/quality-checks.md).

Back to [architecture](../architecture.md).

## Context and decision

Preserve the hexagonal boundaries as providers and workflows grow. Check ordinary Python issues
and the import graph in CI without adding development tools to runtime installations.

## Lint and architecture contracts

The `dev` dependency group provides Ruff 0.17.0 and Import Linter 2.15, separate from runtime
package dependencies. `uv.lock` records exact resolved versions and artifact hashes for local
and CI installs. See [uv dependency management](uv-dependency-management.md) for the decision
and tool audit. Updates require another dependency audit.

Ruff checks `src/` and `tests/` for common Python errors, unused imports, import ordering, and
`E501` with a 100-column limit. Ruff infers Python 3.12 from `requires-python` rather than
repeating the setting. Formatting is not required or added.
Ruff's line-length rule has documented exceptions; it is not a strict Markdown-width validator.

Import Linter's three forbidden contracts in `pyproject.toml` enforce:

- Domain cannot depend on application, adapters, CLI, or the public configuration loader.
- Application cannot depend on adapters, CLI, or the public configuration loader.
- Adapters cannot depend on CLI.

These checks include submodules and indirect paths. Application may use domain contracts and its
own ports. Adapters may use application/domain types and shared adapter utilities. Bootstrap and
the public configuration loader are composition entry points and may construct adapters.
The rules are coarse layer checks, not an allowlist limiting adapters to application ports;
adapter-to-workflow imports and external integration imports are not separately restricted.
Dynamic imports and runtime operations such as built-in file access remain outside these checks.

`tests/test_architecture.py` invokes the real checker on temporary, importable fixture packages,
using the repository's actual contracts. It proves direct and indirect rejection for every listed
forbidden target, checks that disabling the target rule permits the violation, and verifies that
clean ports/shared utilities/composition pass. Assertions identify the exact forbidden area pair,
not merely a target appearing somewhere in a longer rejected path. Indirect helpers live outside
both endpoint areas. Rule isolation uses CLI contract selection, preserving all global settings.
No intentional violations are written into the actual source tree. These repeatable proofs guard
against later weakening of the configuration, rather than mocking an import-analysis library.

CI installs through `uv sync --locked` and runs Ruff, the real-source architecture check,
and the full unittest suite through `uv run --locked` on Python 3.12/3.13. CI also runs
`uv build` to validate wheel/sdist packaging rather than relying on editable installation.
Local commands are in the README. Validation and hosted-CI status are tracked in the
[quality-checks plan](../plans/quality-checks.md).

## Public testing boundaries

Use TDD at the public boundaries approved by Scott:

- **Initialization CLI:** exercise the real command with temporary Git repositories and files.
  Substitute only the external `gh` executable, covering configuration, label setup, safe reruns,
  and failures without touching live GitHub repositories.
- **Configuration loading:** read saved TOML through the public loading API, checking round-trips
  and rejection of invalid settings.

- **Watcher CLI:** temporary configuration and substitutes for external GitHub and AgentShell.
  Cover polling, startup choices, literal notifications, failures, cleanup, and exclusive ownership.
  Real Pi idle/busy validation is a separate isolated integration check, not a CI model call.

Do not add tests coupled to private helpers or internal mock calls. Use Python's `unittest`;
the architecture proof tests additionally invoke the development-only Import Linter command.
Independently validate the installed package through local `uvx`.
Live GitHub label validation in Dark Business requires separate confirmation of target repositories.

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
Movable tags can change after their release was checked. Hosted validation evidence is in the
[slice 1](../plans/slice-1.md), [slice 2](../plans/slice-2.md), and
[quality-checks](../plans/quality-checks.md) plans.
PR-event execution and cancellation have not yet been exercised on GitHub.

## Local static analysis

Local static analysis uses the existing SonarScanner CLI against `http://localhost:9001`, project
`forgetful-factory`. Ignored `.sonarqube/` metadata and a scan script identify this project and scan
`src/` plus `tests/`; the root ignored `.env` supplies the analysis token through environment
variables. This is a development check, not a factory runtime dependency. The selected server gate
is `Sonar way sans code coverage`; complexity rules come from the Python quality profile. Local
scanner setup does not follow Git worktrees and must be repeated where needed.

## Consequences

Import rules prevent known dependency directions, not all architectural mistakes. Keep the
repeatable violation proofs when changing contracts; reconsider rule isolation if contracts overlap.
Formatting, external-import allowlists, runtime sandboxing, and live model calls are not CI gates.
