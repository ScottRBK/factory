# Nix

This repository is built with Nix (flake-parts + uv2nix). The upstream Python
development loop (`uv sync --locked`, `ruff`, `lint-imports`, `unittest`) keeps
working unchanged; Nix adds a reproducible package, a locked dev shell, checks
that run the whole test suite, and non-flake entry points.

Decisions follow the house Nix practice matrix (`new-project-matrix`). Each axis
answer carries a one-line justification; deviations are called out explicitly.
Basis date: **2026-11-08**.

## Prerequisites

Nix with flakes enabled. Optionally `nix-direnv` (`.envrc` is not committed).

## Development

```bash
nix develop          # locked toolchain + git, gh, tmux, pre-commit hooks
uv sync --locked     # upstream loop still works; UV_NO_SYNC=1 stops uv racing Nix
python -m unittest discover -s tests -v --durations 25
```

The dev shell's `ruff` and `lint-imports` come from the **locked `dev` group**
(`.#dev`), not from nixpkgs, so the shell cannot drift from what CI runs.

## Build and run

```bash
nix build .#forgetful-factory   # the distribution (site-packages layout)
nix build .#env                 # interpreter with the locked runtime deps
nix build .#dev                 # + the locked dev group (ruff, import-linter)
nix run .#forgetful-factory -- --help
```

`#env` is what to install when something must actually run the CLI.
`python3.withPackages` will not pick up `#forgetful-factory`: uv2nix packages
carry no `pythonModule` marker.

## Checks

```bash
nix flake check
```

- `pre-commit` — git-hooks.nix default-stage hooks (nixfmt, statix, deadnix, ruff)
- `import-contracts` — the three import-linter contracts (hexagonal boundaries)
- `wheel-record` — builds the wheel offline and validates its RECORD against the
  packaging spec
- `tests` — the **entire** unittest suite: 550 tests, no module or test excluded

`wheel-record` sets `UV_PYTHON_DOWNLOADS=never` and an explicit `UV_PYTHON`;
without them `uv build` probes FHS paths (`/bin/sh`, `/usr/bin/env`) that the Nix
sandbox does not have.

`checks.tests` carries `git`, `gh`, `tmux` **and `nodejs`** in
`nativeBuildInputs`. Node is not optional: the product installs Pi with
`npm ci --ignore-scripts` (`host_dependencies.py`), and the installer tests drive
a real `npm`. The dev shell provides it for the same reason.

### Known red, deliberately not hidden

`nix flake check` is **not green** on the current upstream HEAD, and nothing is
deselected to hide it. One test fails consistently and two are intermittent:

- `test_assisted_lifecycle...changed_pane_is_preserved_and_cannot_receive_watcher_delivery`
  — **fails every run**, including under `nix develop` and a full dev-shell
  `discover` run. A real NixOS/host tmux-fixture failure, not a sandbox artifact.
- `test_watch_status...discovery_replacement_is_preserved_during_status_and_original_exit`
  — intermittent: 1 failure in 5 standalone dev-shell runs; passed the latest full
  check.
- `test_watcher_followup.RepositoryPreflightTests`
  `.test_origin_changed_after_startup_is_checked_again_before_next_plan`
  — errored in one sandbox run; passes standalone and in full dev-shell runs.
  Load/order sensitive, still being characterised; passed the latest full check.

Check liveness is not theoretical. `checks.tests` has failed on real runs with
exactly these failures, and `import-contracts` was proven to fail by injecting a
`domain -> cli` import in a throwaway clone: it named the violation chain and
errored.

## Test suite portability fixes made for Nix

The suite did not run under the Nix sandbox at all (7 of 47 modules passing). All
three causes were hardcoded FHS paths, fixed in the test-support layer so every
host benefits:

1. Fake-CLI stubs were written with `#!/usr/bin/env python3`; the sandbox has no
   `/usr/bin/env`. Stubs now name `sys.executable` (module-level `SHEBANG`).
2. Git fault-injection wrappers hardcoded `#!/usr/bin/python3` and
   `os.execv("/usr/bin/git", ...)`. Both are resolved at runtime now.
3. `lifecycle_support` built the isolated fixture PATH as
   `{bin}:{python}:/usr/bin:/bin`, so on NixOS the product correctly reported
   `git is missing` and every native lifecycle test failed. The git directory is
   resolved at runtime now.

Also: the tmux lookup no longer searches only `/usr/bin:/bin`, and three tests
that read `/etc/os-release` now **skip** when the host has no readable os-release
— mirroring what they already do on non-Ubuntu hosts — instead of erroring.

Correction on `node`: an earlier revision added a skip for the Pi-installer test
when `node` was missing. That masked an omission of our own — the check simply did
not declare `nodejs`. `node` is fully available on Linux/Nix, so the skip was
reverted and `pkgs.nodejs` was added to `checks.tests` and the dev shell instead.
The test now runs.

Probe progression (same harness, sandbox, `git` + `gh`, tmux from probe 6 on):

| Probe | Modules PASS | Modules FAIL |
| --- | --- | --- |
| 1 baseline | 7 | 40 |
| 2 after shebang fix | 35 | 12 |
| 5 after FHS git fix | 38 | 9 |
| 7 after fixture-PATH fix + skips | 45 | 2 |

Per-module `Ran N tests` sums to **550**, matching upstream exactly.

Latest full `nix flake check`: **550 tests in 577s, 1 failure, 9 skips**. The
remaining failure is the tmux-pane test above. Of the 9 skips, 3 are the
os-release guards and the rest are pre-existing Ubuntu-24.04-only recipe guards
that skip on any non-Ubuntu host.

## Practice matrix decisions

- **Channel — `nixos-unstable`.** Matches agent-shell and forgetful; the estate
  consumes inputs, not this runtime.
- **Release — none yet.** Package unpublished, 0 tags; revisit at the first tag.
- **Follows.** `flake-parts -> nixpkgs-lib`, `flake-compat`,
  `git-hooks -> {nixpkgs, flake-compat}`,
  `pyproject-nix`/`uv2nix`/`build-systems -> nixpkgs`: one nixpkgs and one
  flake-compat node in the closure.
- **Lock node count — 8** (`root`, `nixpkgs`, `flake-parts`, `flake-compat`,
  `git-hooks-nix`, `pyproject-nix`, `uv2nix`, `pyproject-build-systems`), with a
  single `nixpkgs` node. House target for an app is 7-13.
- **`nix-systems` — not declared.** Its default set includes `x86_64-darwin`
  (omitted as deprecated upstream) and nothing consumed it; `systems` is a
  literal list.
- **Hooks.** nixfmt, statix, deadnix and ruff at the default stage;
  **ruff-format is wired but `manual` only** because `ruff format --check` reports
  96 of 128 files would be reformatted — a default-stage or pre-push hook would
  rewrite most of the tree (agent-shell hit this with 73 files). Promotion is a
  tracked task.
- **Checks.** pre-commit + import-linter + wheel RECORD + full suite: a
  zero-check flake passes while proving nothing.
- **devShell — yes.** Locked toolchain including the dev group, plus git/gh/tmux.
- **Source filtering — none declared.** *Measured:* uv2nix builds the workspace
  from its own fileset, which already excludes `docs/`, `.github/` and root
  markdown — a docs-only commit leaves the package and env drv paths
  byte-identical. A `cleanSourceWith` filter here was provably dead code and was
  removed.
- **Binary cache — Cachix intended, not wired.** Separate PR, matching
  forgetful's current state.
- **CI — unchanged.** No Nix job demanded; the cache workflow lands with the
  cache PR.
- **Version identity.** See the caveat below.
- **Architectures.** `x86_64-linux` verified; `aarch64-linux` and
  `aarch64-darwin` are listed as **intent** — no builder exists, and
  `nix flake check` reports them as omitted incompatible systems.
  `x86_64-darwin` is omitted (deprecated upstream).
- **Non-flake entry point — included.** House default; `nix-build .` yields the
  identical store path to `nix build .#default`.
- **Secrets — none.** Factory keeps credentials in env vars and
  `forgetful-auth.json` `token_env`.

### Version identity caveat

The sibling projects use scm-stamp via `SETUPTOOLS_SCM_PRETEND_VERSION`.
**`uv_build` ignores that variable**, so copying the recipe verbatim would
silently do nothing. Instead the version is read from `pyproject.toml` at eval
time, with a `FACTORY_VERSION` override for release naming:

```bash
FACTORY_VERSION=$(git describe --tags --abbrev=0) nix build --impure
```

`--abbrev=0` matters: raw `git describe --tags` output is not a clean version.
`__intentionallyOverridingVersion = true` is set because the override renames the
derivation only — the built wheel's metadata still comes from `pyproject.toml`.
Revisit if the project adopts dynamic versioning or cuts its first tag.

## Non-flake usage

`default.nix` and `shell.nix` are provided via
[flake-compat](https://github.com/NixOS/flake-compat), so the project also works
under stable Nix without `experimental-features = nix-command flakes`:

```bash
nix-build .      # same store path as `nix build .#default`
nix-shell .      # delegates to the flake's own dev shell
```

## Known build-backend divergence (documented, not fixed)

`pyproject.toml` pins `requires = ["uv_build==0.13.5"]`, but the wheel this flake
builds reports `Generator: uv 0.13.6`. Cause: `uv.lock` carries no build-backend
entry, and the shared `pyproject-build-systems` input resolves build systems from
**its own** lock, which pins `uv-build` 0.13.6. Our pin is therefore ignored by the
Nix build.

Impact and status:

- Deterministic: the version is frozen in `flake.lock`, so builds do not drift
  between runs. It is simply frozen to a version we did not choose.
- The Nix-built wheel is **not byte-comparable** with the CI wheel, which resolves
  the backend from PyPI and does honour `==0.13.5`.
- A bump of the `pyproject-build-systems` input silently changes our build backend.
- Not an estate-vs-unstable difference: reproduced identically on both channels, and
  on `nixos-26.05` via `follows`.
- `agent-shell` and `forgetful` use the same overlay but declare unversioned
  `requires = ["hatchling", "hatch-vcs"]`, so nothing conflicts there; this repo is
  the first to pin a backend.

A proper fix would be a project-local build-systems lock so the backend is 0.13.5
because this repo declared it. Accepted as-is for now; raising it so the divergence
is a known quantity rather than a surprise for whoever diffs a Nix wheel against a
CI wheel.

## Dependency updates

`.github/dependabot.yml` covers two ecosystems, weekly, mirroring the `forgetful`
setup: `nix` (flake inputs, grouped into one PR per week) and `github-actions`.

Python is deliberately excluded from *version* updates. Every requirement in
`pyproject.toml` is exactly pinned and CI installs with `uv sync --locked`, so
scheduled bumps would break the lock and undo the audit trail behind those pins.
Python still receives Dependabot **security** updates, which only fire on versions
with a known advisory.

Known trap: a PR opened with a `GITHUB_TOKEN` does not trigger workflows. Automated
bump PRs therefore arrive with no checks unless the repo is wired to a GitHub App or
a Dependabot PAT, so a green-looking bump PR means nothing on its own — run
`nix flake check` locally before merging.

## Deferred

- Cachix wiring (`nixConfig` + push workflow) — separate PR.
- Promoting `ruff-format` to the default stage — needs a formatting-only commit
  first, since 96 files would change.
- The three known-red tests above — raise with the repo owner at PR time.

## Per-module sandbox results (probe 7)

Harness: Nix sandbox, `doCheck = true`, `HOME=$TMPDIR`,
`nativeBuildInputs = [dev-env, git, gh, tmux]`, per-module
`python -m unittest -q <module>`.

| Module | Result | Ran | Failed |
| --- | --- | --- | --- |
| `test_agent_definitions` | pass | 15 | 0 |
| `test_architecture` | pass | 7 | 0 |
| `test_assisted_lifecycle` | **fail** | 10 | 1 |
| `test_assisted_review_fixes` | pass | 16 | 0 |
| `test_assisted_setup` | pass | 9 | 0 |
| `test_auth_notice` | pass | 5 | 0 |
| `test_cleanup_boundaries` | pass | 5 | 0 |
| `test_cleanup_recovery` | pass | 5 | 0 |
| `test_configuration` | pass | 11 | 0 |
| `test_factory_maintenance` | pass | 5 | 0 |
| `test_foreman_issue_intake` | pass | 3 | 0 |
| `test_foreman_memory_setup` | pass | 15 | 0 |
| `test_foreman_setup_repair` | pass | 18 | 0 |
| `test_init` | pass | 31 | 0 |
| `test_init_launch` | pass | 8 | 0 |
| `test_installer_onboarding` | pass | 10 | 0 |
| `test_local_skills` | pass | 17 | 0 |
| `test_managed_watcher_alerts` | pass | 3 | 0 |
| `test_native_assisted_reload` | pass | 1 | 0 |
| `test_native_roles` | pass | 4 | 0 |
| `test_native_workers` | pass | 1 | 0 |
| `test_normalized_lifecycle` | pass | 10 | 0 |
| `test_owner_profiles` | pass | 9 | 0 |
| `test_owner_startup` | pass | 5 | 0 |
| `test_pi_runtime_install` | pass | 2 | 0 |
| `test_planning_adapter` | pass | 9 | 0 |
| `test_planning_setup` | pass | 9 | 0 |
| `test_planning_watch` | pass | 20 | 0 |
| `test_profile_recovery` | pass | 19 | 0 |
| `test_profiles` | pass | 25 | 0 |
| `test_project_onboarding` | pass | 9 | 0 |
| `test_research_configuration` | pass | 4 | 0 |
| `test_review_regressions` | pass | 28 | 0 |
| `test_setup_completion` | pass | 19 | 0 |
| `test_shared_pi` | pass | 15 | 0 |
| `test_watch` | pass | 29 | 0 |
| `test_watch_lock` | pass | 3 | 0 |
| `test_watch_status` | **fail** | 12 | 1 |
| `test_watch_status_review` | pass | 22 | 0 |
| `test_watcher_alerts` | pass | 46 | 0 |
| `test_watcher_cancellation` | pass | 2 | 0 |
| `test_watcher_followup` | pass | 17 | 0 |
| `test_watcher_guidance` | pass | 3 | 0 |
| `test_worker_configuration` | pass | 14 | 0 |
| `test_worker_profiles` | pass | 7 | 0 |
| `test_worker_setup` | pass | 11 | 0 |
| `test_worker_watch_permissions` | pass | 2 | 0 |

Totals: **550 tests**, 2 failing at probe time. Neither is caused by Nix: see
Known red above — `changed_pane_is_preserved...` fails consistently including in
`nix develop`, while the `test_watch_status` case is intermittent and passed in
the later full `nix flake check` run.
