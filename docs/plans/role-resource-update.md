# Role-resource update

Work record for [issue #4][issue]. The [ADR](../adrs/role-resource-update.md) records the design.

## Scope and decisions

- Add `forgetful-factory update` with `--dry-run`, `--delegated-work-stopped`, `--force` and
  `--install-role-runtime`. It updates only bundled files under `.factory/resources/`.
- Recognize earlier releases through the shipped hash history
  `resources/role-resources-history.json`, built from manifests `97f34b1`, `1e294fa`, `688c926`
  and `62231f7`: 55 paths, 62 hashes, 7 paths with more than one shipped version.
- Scott's decisions: an edited file needs `--force`, which keeps a backup; tests stay at the
  public CLI with the real bundle; removal of files that a bundle drops is deferred until a bundle
  first drops one.
- `ROLE-SOURCES.md` stays a build-time record. It is not in workspaces.
- First setup now reads the bundle through the same checked reader. The stale-file errors from
  Foreman/watch and first setup now name `update --dry-run` and `update --delegated-work-stopped`.

## Vertical slices

Each slice started with a failing CLI test in `tests/test_resource_update.py`.

1. A previous-release factory updates, agent files stay byte-identical, and Foreman starts.
   Real tmux, fake Pi.
2. An edited file stops the whole update and is named; no other file changes.
3. `--force` backs up the edited file, then updates every file.
4. `--dry-run` lists add/replace/edited per file and changes no file under `.factory`.
5. Refusal without `--delegated-work-stopped`, with a running Foreman (real tmux), and with a
   running plain watch (workspace lease).
6. A runtime whose sync receipt does not match the lock needs `--install-role-runtime`; the
   consented run performs one locked `uv sync`.
7. The Foreman stale-resource error names `update --dry-run`.

The refusal guards in slice 5 were written in slice 1, before their tests. Mutation checks
confirm that each test fails when its guard is removed. See validation below.

## Validation

Evidence is local to this host; hosted CI has not run for this branch.

- Focused run: 8 new tests and the resource-related suites (`test_owner_profiles`,
  `test_profiles`, `test_profile_recovery`, `test_foreman_memory_setup`,
  `test_normalized_lifecycle`, `test_setup_completion`): 105 tests passed, 3 platform skips.
- First full run (Python 3.12, serial unittest): 656 tests, 2 failures, 9 skips. Both failures
  were watch diagnostics that require the phrase `audited bundle`, which the new stale-file
  wording had dropped. The focused run missed them because it was chosen by resource paths, not by
  diagnostic text. The wording now keeps `audited bundle` and adds the `update` route; both tests
  pass. No suite gap: the existing full suite caught the regression.
- Second full run (before rebase): 656 tests, 1 failure, 9 skips, 698 seconds. All new and
  resource tests passed. The failure was the maximum-size discovery case in
  `test_watch_status_review.py`: the status-file race that `4488524` fixes. It passed in the
  first full run and is not caused by this change.
- Combined trial: this commit cherry-picked cleanly onto `test/parallel-runner` (`9336859`).
  Its parallel pytest runner, with native tmux and no fixture changes: 647 passed, 9 skipped,
  52 seconds. Ruff and import contracts also pass there.
- Mutation checks in a scratch copy: each change below made its test fail as expected.
  - remove the `--delegated-work-stopped` check;
  - remove the Foreman owner-state check;
  - remove the workspace lease;
  - accept edited files without `--force`;
  - drop the previous-release hash from the history;
  - drop the current hash from the history (integrity guard).
- Ruff, import contracts (3 kept), wheel build and `tests/check_package.py` pass. The wheel has
  the history file; the sdist has the `.ts` fixture. `update --help` runs from the built wheel
  through `uvx --offline --isolated`.
- Mycelium 0.4.5 map regenerated from the cached audited wheel without installs; a repeat export
  is byte-identical. 95 boxes; 13 unchanged external-base warnings.
- Host limit before rebase: tmux on this host comes from Nix, and lifecycle fixtures then
  searched only `/usr/bin:/bin`. Those runs used a scratch copy with only that search path
  changed. After the rebase onto `test/parallel-runner`, fixtures find tmux on `PATH`.

## First use: pi-forgetful refresh

Scott asked for upstream `pi-forgetful` at `45a0b79`, which includes the compaction fix
`b4630a8`. The source record, patch rebuild, conflicts and audit are in
[ROLE-SOURCES.md][refresh].

- 8 of 40 `pi-forgetful` files changed; no file was added or dropped, so the deferred
  removal was not needed. Other bundle members are byte-identical.
- Full parallel suite on the rebuilt bundle: 647 passed, 9 skipped. The previous-release
  fixture test still passes, because its hash stays in the history.
- One-off lifecycle check (not committed): a factory with the previous release's 40
  `pi-forgetful` files refused Foreman, `update` replaced 8 files with agent files unchanged,
  and Foreman then started.
- Read-only `update --dry-run` on DinoLand and dark-business: 8 to replace, 0 to add,
  0 edited.

## Not done

- Hosted CI for the exact commit.
- A live update of DinoLand or another real factory; Scott runs these.
- Removal of dropped files (deferred by decision).

[issue]: https://github.com/ScottRBK/factory/issues/4
[refresh]:
  ../../src/forgetful_factory/resources/ROLE-SOURCES.md#2026-11-22-pi-forgetful-refresh
