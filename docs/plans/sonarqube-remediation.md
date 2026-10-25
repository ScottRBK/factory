# Full SonarQube remediation

Status: SQ clear and diagnostics merged; baseline/coverage follow-ups and acceptance remain pending.

## Scope and baseline

This extends the watcher work to all 38 outstanding findings from analysis
`51ceacbb-2597-4877-8f42-0fce536f1bbc`: 37 maintainability findings and one bug-classified finding.
Twenty-four are in unchanged code; fourteen are in changed/new functions, not necessarily introduced
by the watcher changes. The [watcher work record](watcher-problems.md) retains that scan's evidence.

Scott clarified that the cleanup includes existing Factory code, including its AgentShell adapters.
These are Factory files, not the external AgentShell project or installed SDK. The earlier adapter
byte-freeze is lifted for these fixes; ownership, cancellation and lifecycle safety remain required.
The starting source passes 465 tests on each of Python 3.12.3 and 3.13.5 without skips. Those checks
are baseline evidence, not acceptance of the upcoming refactors.

## Delegation and integration

Each group uses Pi with `openai-codex/gpt-5.6-sol` in a separate branch/worktree. All use one
snapshot including the uncommitted watcher changes. Main remains untouched during implementation.

- Watcher supervision: four findings in the polling/recovery loop and alert formatting.
- Planning and Git: six findings in scaffolding, recovery and worktree validation.
- Lifecycle: twelve findings in Factory's AgentShell integration and owned-command cancellation.
- Resources: eight findings in definitions, profiles, selected skills and resource files.
- CLI and test helpers: eight findings in setup flow, typing and inherited test helpers.

Source ownership is disjoint. Shared documentation and map changes belong to integration. Agents
commit locally under Scott's identity, with no agent authorship trailers. No push is authorized.
Merge only completed handoffs after checking scope, evidence and source hashes. Keep the initial
working copy safe; do not remove branches/worktrees until their changes are durably integrated.

## Integration evidence

- Resources commit `819def8317ac680dae4bc78987415bdb5b59f6be` changes only its five assigned files.
  Parent verified its clean worktree, source/test hashes and 131 passing tests on each Python.
  No tests changed. Ruff and the three import contracts pass for that slice.
- The first integration scan confirms all eight resources findings cleared, with no new findings
  in those files. Thirty issues remain across the other groups, so the overall gate still fails.
  The eight existing scanner/engine/plugin JARs remained byte-identical; no install or upgrade.
- Planning/Git commit `6ae010d13c7e29b11ad0083c2f1e299f116dcafa` changes its two assigned files.
  Parent verified source hashes and 111 passing related tests on each Python. All six findings
  cleared in the next integration scan: 24 remain, with none in either merged group. Three parent
  startup/source/branch-conflict probes also pass on both Pythons against the combined source.
- Lifecycle commit `2befd8e4fb31c7fd4e5d2d2031b857ff08333f90` is provisionally merged after hash,
  scope and test verification. Its 43-test lifecycle and ten-test controller selections pass on
  both Pythons. All twelve original findings cleared, including the synchronous-open report.
  SonarQube found two new async-without-await findings, leaving fourteen outstanding overall.
  The agent is correcting those and preserving cleanup guards around partially started resources
  identified during parent inspection. That follow-up needs fresh tests and another scan.
- Lifecycle follow-up `0a009d392edb1326df96ff0c2eb6b52d65ca5103` restores caller ownership before
  fallible socket setup and guards all partially created supervision tasks. Parent verified its
  exact source hashes and sixteen fresh focused tests per Python. The fifth scan clears both new
  async findings; four original watcher findings remain, with none elsewhere. The prior 43-test
  lifecycle results describe the earlier commit, not this follow-up.
- CLI/helpers commit `24b517b8739f369ce1734d02c6772fda6011d00f` is provisionally merged. Its eight
  findings clear in the fourth scan; six findings remain overall. Parent verified final hashes and
  that test syntax differs only by the three private-helper names, preserving every assertion.
  Discovery still yields exactly the original 465 test IDs, with none removed or invented.
  The reported 135/70/36-test selections passed on both Pythons, but their manifests predate the
  final CLI source bytes. A final-source rerun and explanation are requested; those earlier runs
  are not being presented as validation of the exact delivered commit.
  The follow-up explains that the last CLI change was one explanatory comment; parent verified
  removing that exact line reproduces the earlier hash. Fresh 135-test public and 36-test native
  selections now pass on both Pythons. Their four 117-file manifests match one another and the
  delivered bytes. This closes that evidence gap without a source or assertion change.
- Watcher commit `38e7a60386196a17e83d0d1a4ce76cf2481de1c7` changes only watcher orchestration.
  Parent verified its source hashes and final 133-test selections on both Pythons. An earlier
  parallel 3.13 run timed out stopping a watcher; the individual test and full selection reran
  successfully without a code change. That result alone does not explain the earlier failure.
- The sixth scan of all integrated groups reports zero outstanding issues and assigned gate OK.
  It used unchanged cached analyzers, with no exclusions, issue suppression or gate changes.
- Full combined Python 3.12.3 passes 465 tests without skips in 641.935 seconds. The subsequent,
  sequential Python 3.13.5 run executed 465 tests in 676.205 seconds with one shutdown timeout in
  `test_relocated_definition_keeps_selected_guidance_and_explicit_launch_directory`.
  Source/test hashes stayed unchanged. This failed run is retained, not counted as acceptance.
- A new Pi investigation worktree starts from the complete integrated source. It must capture the
  public shutdown failure and distinguish a live watcher from an exited watcher whose child holds
  a pipe. No assumed load diagnosis, timeout increase, weakened assertion or historical-PID cleanup.
  Any actual bug fix needs a public failing regression; lack of reproduction remains uncertainty.
- No shutdown cause was reproduced: 500 repetitions of the failing test with diagnostic
  instrumentation passed, as did 100 uninstrumented pre-SQ baseline repetitions. These do not prove
  the timeout absent. Parent verified and merged the diagnostic series ending at `1d0e29f`:
  authenticated original pidfds, bounded socket reads and preserved 15-second pipe-drain checks.
  Both final-byte 134-test selections pass. Wrong-payload and non-pidfd controls reject safely;
  a stalled peer now fails at the five-second socket deadline rather than its ten-second watchdog.
  These are fixture controls, not product defects. The seventh scan stays at zero findings and gate
  OK with all eight analyzer JARs unchanged. Product code is unchanged by this investigation;
  the original failed runs remain visible.
- Parent found a separate remaining first-success baseline gap, with real public assertion failures
  on both Pythons against combined and pre-SQ source. A shared planning read failure in source A
  can skip source B's first-success baseline even though B was successfully fetched. A new B issue
  arriving before planning recovers is then incorrectly treated as old. Earlier coverage handled
  the interrupted source's own whole batch, not another source's first success in the same poll.
  A separate Pi worktree is adding the public regression and completing the approved F2 correction.
- Actual Claude Code/Opus review has started against an immutable 150-file snapshot of the combined
  production changes. It is not final acceptance: the two follow-ups and renewed aggregate evidence
  must be reviewed afterward. The first review completed without a capacity failure and found no
  blocking SQ regression. Its 150-file snapshot remained unchanged. R1 corrects stale adapter
  wording; R2 records the benign startup-error reporting difference. Parent selected tests of the
  owner process for R3's moved defensive checks. R4's conservative saved `starting` state is
  pre-existing and remains outside this work. R5 leaves the shutdown timeout unexplained; a bounded
  stack-capture investigation will test it without changing production or fixture deadlines.
  The separately discovered cross-source baseline fix also needs final review.
  Parent self-review is permitted only if Claude exhausts capacity.
- Candidate offline packages verify 72 wheel checksums, 69 source/resource files, 48 test files,
  README/TOML equality and five extracted-wheel help commands. No installation occurred. The uv
  executable matches its previously audited wheel contents; these candidate artifacts must be
  refreshed after the remaining source/test/documentation changes.
- Ruff and all three import contracts pass. The refreshed Mycelium map has 72 boxes, identical
  repeat exports and eleven external-base warnings. Tests filter 3,407 calls and 52 relationships;
  diagram validation is text-only. Package checks and final review await settled source.
- Temporary branches/worktrees remain until the complete reviewed result is integrated into main.

## Safety and validation

Use the approved public CLI, external-command, real Git and native SDK/private-tmux test seams.
Existing failing SonarQube findings provide the static-analysis baseline. Preserve behavior with
focused public baselines and small refactors; any behavioral bug needs an actual failing public
regression before its fix. Do not weaken assertions, turn helpers into fake tests, suppress rules,
exclude code or change the quality gate/new-code baseline to manufacture a pass. Investigate proven
false positives honestly, with their call-site/type-resolution evidence.

Preserve read-only saved-plan recovery, user-approved Foreman completion, established ownership
identity, scoped repository pauses and uncertain-write latches. Terminal loss and uncertain delivery
remain fatal. Keep lifecycle deadlines, owned handles, safe cancellation and private socket/lock
boundaries. A blocking call must not merely move into a helper to evade an async rule.

No dependency install/upgrade, SDK workaround, live product inference/backend test, DinoLand repair
or unrelated cleanup. Keep `FACTORY.md`, `AGENTS.md`, Design questions, dependency/lock/CI files and
audited bundles unchanged. Context7 remains unavailable; use pinned official documentation.

After integration, repeat both full native-enabled suites, lint/import/scope checks, a fresh
SonarQube scan, Mycelium repeat export and offline package checks. Report the assigned gate apart
from `caycStatus`, with actual findings rather than assumed fixes. Claude Code reviews the immutable
combined source and validation evidence; parent self-review is allowed only if Claude runs out of
capacity. Address review findings and revalidate changed source before final acceptance and cleanup.
