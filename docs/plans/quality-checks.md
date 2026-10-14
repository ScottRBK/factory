# Development checks before slice 3

Back to the [implementation plan](../plan.md).

Status: implemented, locally validated, and independently reviewed by Opus. The review blocker
was corrected and the recheck found no remaining actionable issues.
No commit, push, or hosted CI run is part of this request.

## Scope

- Ruff 0.17.0: basic Python errors, unused imports, import ordering, and `E501` at 100 columns.
- Import Linter 2.15: the three agreed forbidden contracts, including indirect imports.
- Both tools are development-only dependencies; the runtime remains AgentShell only.
- Declare tools in `pyproject.toml`'s `dev` dependency group and pin resolution in `uv.lock`.
  Use `uv sync --locked` and `uv run --locked` locally and in CI; audit dependency changes first.
- Run Ruff, the real-source architecture check, and unittest in each existing Python 3.12/3.13
  CI job. Preserve push/PR triggers, outdated-run cancellation, and read-only permissions.
- Keep formatting and additional external-import restrictions out of scope.

## Architecture test boundary

The agreed boundary is the real Import Linter CLI's exit status and reported dependency paths.
The three rules forbid domain-to-outer-layer, application-to-concrete-integration, and
adapter-to-CLI dependencies. Bootstrap and the public configuration loader remain composition.

Committed proof tests use temporary importable packages and the actual repository contracts.
For every forbidden target, verify both a direct dependency and an indirect path through a helper
outside the source/target areas. Confirm a clean baseline passes, the violation passes without the
target contract, that contract rejects it when enabled, and removing the mutation passes again.
Retain contract name and complete path evidence rather than full diagnostic snapshots.
Known-good fixtures also include ports, shared adapter utilities, and both composition entry points.

These are coarse import boundaries, not runtime isolation or an exhaustive import allowlist.
See the [development-checks ADR](../adrs/development-checks.md) for exact rules and limitations.

## Validation evidence

- The first domain proof failed because no checker configuration existed. After configuring an
  empty contract set, all four domain violations returned success and the rejection expectations
  failed. Adding the domain rule made those expectations pass.
- Application and adapter rejection checks each failed before their rule was added, then passed.
  These observed RED→GREEN cycles exercised the actual checker rather than mocked calls.
- Indirect-path checks pass through a neutral sibling helper and require the full reported path.
  Every direct/indirect proof also removes its target rule to confirm that another contract is
  not accidentally supplying the rejection.
- Ruff initially reported eight import-order findings and four overlong lines in the new tests.
  Import ordering and test line wrapping were corrected; no runtime behaviour was changed.
- Final suite after review fixes: all 61 tests passed on Python 3.12 in 132.7 seconds and
  Python 3.13 in 132.3 seconds.
  Seven new test methods cover 16 direct/indirect forbidden-path cases plus allowed composition.
- Ruff and the actual-source architecture check passed on both supported Python versions.
  Import Linter kept all three contracts on the 31-module source graph.
- Before the uv migration, fresh Python 3.13 installation using the dev extra and constraints
  passed. The offline wheel/sdist build passed, and wheel metadata kept the checkers dev-only.
  This packaging evidence predates the dependency-group migration recorded below.
- An ordinary rebuilt-wheel `uvx` environment installed only factory and AgentShell; neither
  `ruff` nor `importlinter` was importable. This verifies the dev-only separation in an actual
  isolated install, not just the manifest.
- Final SonarQube analysis `0075c041-bc77-4c72-a3f4-2bf93dc872bc`, main, 2026-10-13 23:58 UTC,
  passed the assigned `Sonar way sans code coverage` gate. Open findings and new violations were
  zero; new duplication was 0.0%. Coverage is not a gate condition. The scan covered uncommitted
  changes; its SCM revision metadata still identifies the previous commit.
- Opus found one blocker in the proof assertions: five deleted forbidden targets were hidden by
  rejection through another target in the same contract. The fixture intentionally contains real
  composition paths, so checking that a target appeared somewhere in output was insufficient.
  A reproduced deletion of application's configuration target passed the old proofs; the fixed
  assertions require the exact forbidden area pair and now reject that weakened configuration.
- All eight one-at-a-time forbidden-target deletion mutations fail with the corrected proofs,
  covering both direct and indirect cases. Narrow-terminal validation (`COLUMNS=30`) passes.
- Review advisories were addressed with normalized, fixed-width diagnostics, CLI contract
  selection that preserves global configuration, and an actionable missing-dev-tool message.
  Ruff now infers the Python minimum instead of repeating it; Grimp hash labels are consistent.
  Future overlapping contracts require reviewing fixture/rule isolation rather than silently
  dropping the additional rule.
- Full suites, Ruff, the architecture check, build, and SonarQube passed again after corrections.
  Opus independently confirmed all eight target deletions fail, narrow-terminal checks pass,
  and weakened indirect/descendant rules, bad contract types/IDs, and import exemptions are caught.
  The recheck found no remaining actionable issues.
- Hosted CI is unverified until the final changes are committed and pushed.

## uv dependency-management migration

Development dependencies now use `[dependency-groups].dev` in `pyproject.toml` and a generated
`uv.lock` to commit with these changes, replacing the dev extra and separate constraints file.
The migration preserves all nine checker-package versions and AgentShell 0.4.0; no factory runtime
dependency was upgraded.
CI installs audited uv 0.13.1, syncs the lock, builds wheel/sdist, and runs the checks.
The global uv was not changed.
See the [uv ADR](../adrs/uv-dependency-management.md) for the decision and pre-use tool audit.

Local validation after migration:

- Clean uv environments passed lint, all three real-source contracts, and all 61 tests on
  Python 3.12 (129.4 seconds) and Python 3.13 (128.9 seconds).
- `uv lock --check` passes. A changed manifest in a disposable copy is rejected by locked sync
  rather than silently updating the lockfile.
- Wheel and sdist builds pass. Wheel metadata declares only AgentShell and no dev extras.
  An isolated wheel install contained only factory and AgentShell; neither checker was importable.
  The packaged CLI help works and the sdist still includes the architecture proof tests.
- Local YAML parsing validates CI commands, retained push/PR events, read-only permissions,
  cancellation, and the Python matrix. Parsing caught an unquoted colon in the uv bootstrap
  command; a YAML block scalar fixes it. No new dependency was needed for this validation.
- SonarQube analysis `e5839575-dbba-4840-921a-48f1ecc08d7a` passed the assigned gate with
  zero open issues. The scan covers the uncommitted working tree; SCM revision metadata still
  identifies the previous commit.
- Hosted CI remains unverified until these changes are committed and pushed.

Migration review follow-up:

- Before the version guard, installed uv 0.8.0 accepted a locked-sync dry run. Adding
  `[tool.uv].required-version = ">=0.13.1"` makes that same command fail before sync;
  audited uv 0.13.1 still passes. The global installation remains unchanged.
- CI explicitly builds wheel/sdist and drops unnecessary `PYTHONPATH` overrides, matching
  the documented installed-project checks. uv's CI bootstrap remains version-pinned, not
  artifact-hash pinned; the ADR now states that limit and the lock's build-backend exclusion.
- Broken historical audit links now point to their recorded Git revision, without restoring
  the separately deleted local audit document.
- After these fixes, clean sync, build, lint, all contracts, and all 61 tests passed again on
  Python 3.12 (129.8 seconds) and Python 3.13 (129.6 seconds).
