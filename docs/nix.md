# Nix

This repository is built with Nix (flake-parts + uv2nix). The upstream Python
development loop (`uv sync --locked`, `ruff`, `lint-imports`, `unittest`) keeps
working unchanged; Nix adds a reproducible package, a locked dev shell, checks
that run the whole test suite, and non-flake entry points.

The decisions below follow a fixed checklist: nixpkgs channel, release strategy,
input follows, lock size, supported systems, hooks, checks, dev shell, source
filtering, binary cache, CI, version identity, architectures, non-flake entry
points and secrets. Each answer carries a one-line justification; deviations are
called out explicitly. Basis date: **2026-11-08**.

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

- `pre-commit` - git-hooks.nix default-stage hooks (nixfmt, statix, deadnix, ruff)
- `import-contracts` - the three import-linter contracts (hexagonal boundaries)
- `wheel-record` - builds the wheel offline and validates its RECORD against the
  packaging spec
- `tests` - the **entire** unittest suite: 656 tests, no module or test excluded

`wheel-record` sets `UV_PYTHON_DOWNLOADS=never` and an explicit `UV_PYTHON`;
without them `uv build` probes FHS paths (`/bin/sh`, `/usr/bin/env`) that the Nix
sandbox does not have.

`checks.tests` carries `git`, `gh`, `tmux` **and `nodejs`** in
`nativeBuildInputs`. Node is not optional: the product installs Pi with
`npm ci --ignore-scripts` (`host_dependencies.py`), and the installer tests drive
a real `npm`. The dev shell provides it for the same reason.

### Green in the sandbox, and what it took

`nix flake check` passes: 656 tests, 0 failures, 0 errors, 9 skips, exit 0. The 9
skips are 6 opt-in native-Pi probes plus the 3 os-release guards, all of which
skip on any host without those prerequisites.

Getting there needed three FHS assumptions removed from the support layer. The
fixture PATH ended at `/usr/bin:/bin`, so with no git there every native
lifecycle test reported `git is missing`. Stub scripts were written with
`#!/usr/bin/env python3`, which the sandbox cannot exec, so the failure surfaced
as `fatal: cannot exec ...: No such file or directory` from the git that tried to
run them. And two tmux fixtures opened and respawned a pane with `/bin/cat`; the
sandbox `/bin` holds only `sh`, so tmux accepted the command, the pane died, and
the server exited under the running test.

Check liveness is not theoretical. `checks.tests` failed on real runs with these
causes before they were fixed, and `import-contracts` was proven to fail by
injecting a `domain -> cli` import in a throwaway clone: it named the violation
chain and errored.

Two tests were historically intermittent (a `test_watch_status` discovery case and
a `test_watcher_followup` preflight case). Both pass in the current run; neither
is deselected.

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
- mirroring what they already do on non-Ubuntu hosts - instead of erroring.

Correction on `node`: an earlier revision added a skip for the Pi-installer test
when `node` was missing. That masked an omission of our own - the check simply did
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

Latest full `nix flake check`: **656 tests, 0 failures, 0 errors, 9 skips**.
Of the 9 skips, 6 are the opt-in native-Pi probes and 3 are the os-release
guards, which skip on any host without a readable `/etc/os-release`.

## Configuration decisions

- **Channel - `nixos-unstable`.** Anything consuming this flake takes its inputs,
  not this runtime, so tracking unstable moves this repo's build toolchain and
  leaves the host system alone.
- **Release - none yet.** Package unpublished, 0 tags; revisit at the first tag.
- **Follows.** `flake-parts -> nixpkgs-lib`, `flake-compat`,
  `git-hooks -> {nixpkgs, flake-compat}`,
  `pyproject-nix`/`uv2nix`/`build-systems -> nixpkgs`: one nixpkgs and one
  flake-compat node in the closure.
- **Lock node count - 8** (`root`, `nixpkgs`, `flake-parts`, `flake-compat`,
  `git-hooks-nix`, `pyproject-nix`, `uv2nix`, `pyproject-build-systems`), with a
  single `nixpkgs` node - one node per direct input, plus nixpkgs itself.
- **`nix-systems` - not declared.** Its default set includes `x86_64-darwin`
  (omitted as deprecated upstream) and nothing consumed it; `systems` is a
  literal list.
- **Hooks.** nixfmt, statix, deadnix and ruff at the default stage;
  **ruff-format is wired but `manual` only** because `ruff format --check` reports
  117 of 149 paths would be reformatted, so a default-stage or pre-push hook would
  rewrite most of the tree. The 149 is 136 Python plus 13 Markdown: ruff 0.17
  formats Markdown too, so promoting this hook rewrites prose as well as code. A
  pre-push stage is no safer - it still runs on every `git push`. Promotion needs a
  formatting-only commit first.
- **Checks.** pre-commit + import-linter + wheel RECORD + full suite: a
  zero-check flake passes while proving nothing.
- **devShell - yes.** Locked toolchain including the dev group, plus git/gh/tmux.
- **Source filtering - none declared.** uv2nix builds from the workspace root
  unfiltered, so every tracked file, `docs/` included, is derivation input.
  Measured 2026-11-08: a docs-only edit changed the `drvPath` of the package and
  of both environments. The shipped modules are unchanged; only the 59 `.pyc`
  files, which embed the source store path, and `nix-support/setup-hook` differ
  in the output tree. A filter would cut those rebuilds.
- **Binary cache - Cachix intended, not wired.** Lands in a separate PR together
  with the push workflow.
- **CI - `nix-check.yml` added.** `nix flake check` now runs on push and pull
  request; without it the flake checks execute only on a contributor's machine. The
  cache workflow lands with the
  cache PR.
- **Version identity.** See the caveat below.
- **Architectures.** `x86_64-linux` verified; `aarch64-linux` and
  `aarch64-darwin` are listed as **intent** - no builder exists. `nix flake
  check` does not build them and warns that it omitted them as incompatible
  systems, so the warning is expected output rather than a failure. Verified
  2026-11-23: `all checks passed!` alongside `warning: The check omitted these
  incompatible systems: aarch64-darwin, aarch64-linux`. `x86_64-darwin` is
  omitted entirely because nixpkgs deprecates it upstream, so it is not
  reported.
- **Non-flake entry point - included.** Supplied through `flake-compat`;
  `nix-build .` yields the identical store path to `nix build .#default`.
- **Secrets - none.** Factory keeps credentials in env vars and
  `forgetful-auth.json` `token_env`.

### Version identity caveat

The usual recipe stamps the version from git through
`SETUPTOOLS_SCM_PRETEND_VERSION`. **`uv_build` ignores that variable**, so copying
the recipe verbatim would silently do nothing. Instead the version is read from
`pyproject.toml` at eval time, with a `FACTORY_VERSION` override for release
naming:

```bash
FACTORY_VERSION=$(git describe --tags --abbrev=0) nix build --impure
```

`--abbrev=0` matters: raw `git describe --tags` output is not a clean version.
`__intentionallyOverridingVersion = true` is set because the override renames the
derivation only - the built wheel's metadata still comes from `pyproject.toml`.
Revisit if the project adopts dynamic versioning or cuts its first tag.

## Non-flake usage

`default.nix` and `shell.nix` are provided via
[flake-compat](https://github.com/NixOS/flake-compat), so the project also works
under stable Nix without `experimental-features = nix-command flakes`:

```bash
nix-build .      # same store path as `nix build .#default`
nix-shell .      # delegates to the flake's own dev shell
```

## Build backend: the wheel matches the pin

`pyproject.toml` pins `requires = ["uv_build==0.13.5"]`, and the wheel this flake
builds reports exactly that. Measured on 2026-11-08:

```console
$ P=$(nix build .#forgetful-factory --no-link --print-out-paths)
$ cat $P/lib/python3.12/site-packages/forgetful_factory-0.1.0.dist-info/WHEEL
Wheel-Version: 1.0
Generator: uv 0.13.5
Root-Is-Purelib: true
Tag: py3-none-any
```

Two backend versions exist in this build, and only one produces the wheel:

- **The frontend is `uv` 0.13.5**, taken from nixpkgs through
  `pyproject-build-systems`. Its hook runs `uv build --no-build-isolation`.
- **`pyproject-build-systems` also puts `uv-build-0.13.6` on `PATH`**, because it
  resolves build systems from its own lock and `uv.lock` carries no backend
  entry. That is where the 0.13.6 store-path name comes from.
- Because the pin is exactly `uv_build==0.13.5`, `uv build` logs
  `Using bundled uv_build backend` and calls the backend compiled into itself.
  The 0.13.6 package on `PATH` never executes.

So the 0.13.6 label is cosmetic: a derivation listing shows an
`uv-build-0.13.6` input, while the artifact's `Generator` line comes from the
backend that actually ran. A wheel diff against CI shows no backend difference.

Two changes would move the `Generator` line, and both are worth watching:

- Pinning `uv_build` to anything other than the frontend's bundled version. With
  `uv_build==0.13.6` the log says
  `Not using uv_build direct build ... is not a known compatible range` and the
  `uv_build` package is called instead, producing `Generator: uv 0.13.6`. The pin
  selects the backend; it is not decoration.
- A nixpkgs bump moves the `uv` frontend, and with it the bundled backend used for
  the `==0.13.5` fast path.

Only the `Generator` line was compared with the CI wheel; byte-for-byte equality
was not tested.

## Deferred

- Cachix wiring (`nixConfig` + push workflow) - separate PR.
- Dependabot for `nix` and `github-actions` - separate PR.
- Promoting `ruff-format` to the default stage - needs a formatting-only commit
  first, since 117 files would change.

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

Totals: **550 tests**, 2 failing at probe time. Neither was caused by Nix; both
are fixed now, and the current suite runs 656 tests with no failures. See the
sandbox-green note for what each one was.
