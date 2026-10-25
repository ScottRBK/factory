# Watcher problem alerts

Status: watcher follow-up implemented; later SQ refactors and final review are tracked separately.
The [SQ cleanup](sonarqube-remediation.md) records current combined validation and remaining gates.
[Decision and boundaries](../adrs/watcher-problems.md).

## Approved scope

Scott approved implementation after confirming that planning safety failures should pause affected
work and notify Foreman, not terminate the watcher. Foreman discusses reconciliation with the user.
Unrelated plans continue where isolation is safe. Shared failures pause affected factory operations.
Unknown outcomes never authorize repeated writes, replacement ownership or repeated terminal sends.

The later approval supersedes the review's initial recommendation to terminate on startup planning
failures. Native connection/lifecycle loss is separate from planning safety checks. DinoLand's
records remain untouched; the purpose is for Foreman to investigate through the alert path.

## Test boundaries and sequence

Agreed public boundaries: watch CLI sessions, captured Foreman submissions and temporary real Git
with external native Forgetful/GitHub command fixtures. No internal collaborator mocks, live model
calls, personal credentials or backend mutations are required. Follow test-first vertical slices.

1. Missing recorded worktree alerts while another plan continues; neither saved work nor records
   are repaired automatically.
2. Safe revalidation uses existing identities, including unchanged revisions, closed recovered
   issues, new-only startup, corrected cleanup and disappeared/replaced records.
3. Repeated errors are suppressed separately from successful submissions. Source read failures
   preserve first-success baseline behaviour and do not hide healthy sources.
4. Shared access/inventory failures pause rather than terminate. Known per-plan recovery failures
   are isolated. Unknown side effects remain pending without replay.
5. Failed alert delivery retains operator diagnostics and existing owned/borrowed lifecycle rules.
6. Foreman receives usable guidance without overwriting user edits. Guidance checks do not establish
   model compliance.
7. Run focused and full offline regression suites, architecture/lint/package checks and independent
   review. Regenerate the detailed map after the code settles.

## Evidence so far

Baseline: Factory `1e294fa619e64ff3b1e67429f59c384caf6b50c9`, clean before this change.
Source hashes and protected Design questions were captured before edits.

- Before implementation, five existing public regressions passed. They confirmed source retry,
  restart recovery and uncertainty protection, but the worktree test required whole-watcher exit.
  The missing isolation coverage was a test of the old policy, not a failed safety check.
- Starter Foreman guidance: the first test attempt incorrectly expected a relative resource path
  at runtime; correcting it to the public absolute launch path exposed six genuine missing-guidance
  assertions. The updated template then passed the watch CLI test and preserved a local edit.
- Context7 remained unavailable. AgentShell 0.5.0's official terminal examples were fetched to
  confirm submission, partial-send and no-replay semantics. No SDK changes or installs were made.
- Core implementation passed 74 broader watcher checks, then 24 alert checks after the final prefix
  alignment. The parent added plain-language cause/user-discussion coverage for preserved older
  skills: genuine red assertions preceded the controlled explanation mapping. All 26 alert/guidance
  checks then passed. A separate red/green check confirms unknown plan IDs are omitted.
- An independent preliminary review passed 76 existing watcher/guidance checks on Python 3.12,
  25 alert/guidance checks on 3.13 and seven real-SDK/private-tmux lifecycle checks. It nevertheless
  reproduced five defects: full-record identity validation, duplicate inventory rows, unknown
  nonempty statuses, filesystem parent conflicts and generic alert text. The final item was already
  fixed by the parent; the other four were then corrected test-first. Passing existing tests did
  not constitute acceptance.
- Coverage gaps: prior tests used integer identity changes and count mismatches, but not substituted
  full records, bool-as-int equality, duplicate rows with a matching count or unknown statuses.
  Git command errors did not cover parent-directory filesystem errors. Permanent public regressions
  now cover these paths instead of broadening exception catches around the watcher.
- Official Forgetful 0.5.5 source confirms plan statuses are `draft`, `active`, `completed` and
  `archived`; task cancellation is not a plan status. No dependency upgrade is needed.
- Preliminary findings 1–4 are fixed with public red/green tests. Final focused checks passed 68
  tests, and seven managed SDK/tmux checks passed. Read boundaries now reject malformed/full-record
  identity substitutions and incomplete/duplicate inventories. Unknown statuses remain pending.
  A complete lookup can isolate an absent plan without calling its failing detail endpoint.
- An additional cross-source regression passed immediately. A scratch mutant removing the shared
  pause guard failed by creating a second plan. No production correction was needed for that case.
- Initial full native runs each collected 417 tests. Python 3.12 failed three assertions and three
  errors; 3.13 failed two assertions and three errors. Five cases retained old shutdown/startup
  expectations or inadequate launch fixtures. Their coverage was updated rather than removed.
  A separate 3.12 failure exposed a genuine Ctrl-C race in the native-command wrapper.
- That public failure showed a second `communicate()` call masking KeyboardInterrupt with missing
  Python pipe bookkeeping. A standalone library-only timing probe reproduced the mechanism on
  3.12.3 and 3.13.5; it is diagnostic evidence, not a new private Factory test seam. The wrapper now
  uses bounded process waiting with the same signals and grace period. Two new public CLI tests
  validate cooperative and stubborn native-check exits using transferred, live-validated pidfds.
  Those cancellation tests and seven cleanup regressions pass on both interpreters. They do not
  deterministically inject the rare library timing window or prove all detached descendants exit.
- All seven updated checks and 48 related checks passed on each interpreter. The pre-ready timeout
  test still exercises the original 30-second owner deadline through an external runtime fixture.
  Earlier launcher-shadowing and reduced-environment failures are retained separately as harness
  failures; the authoritative isolated native-environment runs pass without weakened assertions.
- The next full run passed 421 tests on 3.12; 3.13 exposed a fixture read during file truncation.
  Fake GitHub state publication is now atomic, with serialized fixture writers. Native planning
  fixture state uses the same protections so concurrent read observations cannot erase records.
  The two existing slow-poll fault injections were updated and assert their insertion point exists.
  This was a fixture race, not a product error or a reason to relax malformed-reply validation.
- Pre-Opus full native-enabled suites passed 421 tests each: Python 3.12.3 in 616.740 seconds and
  Python 3.13.5 in 611.616 seconds, with no skips. Source/test hashes were unchanged during both
  runs. Five SDK probes use the installed real Pi SDK, isolated homes and fake children, without
  inference. These runs do not establish live delivery or fresh-host installation.
- Ruff, all three import contracts and whitespace checks pass. Mycelium 0.4.5 regenerated the final
  source map: 64 boxes, 2,557 filtered calls and 47 filtered type relationships. Repeated export
  matches byte-for-byte; ten external-base warnings remain. Mermaid was checked as text, not
  rendered.
- Offline uv 0.13.5 builds pass: 72 wheel checksums, safe/unique archive members, all 69 source and
  resource files match, and all 46 test files match the source archive. Five extracted-wheel CLI
  help checks pass. No dependency was installed or upgraded; this is not a fresh-host install test.
- Opus reviewed all 147 frozen files and requested changes. Its before/after hashes match. It
  confirmed three defects through public CLI scenarios on both Python versions: pre-ownership
  recovery had no supported completion path, an interrupted first-success baseline could admit old
  issues, and pure reads could latch an uncertain-write pause. Duplicate-plan reporting and changed
  local diagnostics also need correction. Its scenario tests print observed failures; their `OK`
  results are not proof of the intended behaviour. The 42 existing alert tests still passed.
- Coverage gap: recovery tests usually seeded complete ownership; they did not validate interrupted
  first-time setup through to an approved completion. Baseline tests did not interrupt the first
  successful issue loop. New assertion-based public regressions must cover both gaps.
- Scott explicitly chose option 2 for incomplete first-time setup: Foreman completes it only with
  the user's approval; watcher recovery remains read-only. The reviewer's proposed automatic
  continuation when no task/marker exists is not approved. Alerts must explain the required repair,
  and revalidation must distinguish no established ownership identity from a lost pinned identity.
  Uncertain-write markers and manual pauses cannot authorize replay.
- Baseline/reporting fixes (F2, F4 and F5) passed genuine public red/green checks, followed by 129
  related tests and eight managed/native checks on each Python. Five new assertions cover complete
  first-success batches, duplicate-plan context and changing local diagnostics. Creation policy,
  parent fixtures and cancellation safeguards were unchanged during that round.
- An independent assertion-based probe against the frozen pre-Opus source exposed another F1
  boundary: a pre-existing incomplete plan discovered after startup was automatically completed.
  The approved policy also covers that case; fresh intake must not bypass Foreman-led repair just
  because startup inventory did not see the plan. Evidence: `parent/late-incomplete-plan-red.log`.
- F1 option 2 and F3 passed 20 focused checks, 160 related checks and nine managed/native checks
  on each Python. These selections overlap and are not additive. Proven reads retry safely; only
  uninterrupted fresh intake may create. Existing incomplete plans require approved native repair,
  including plans discovered after startup. The independent late-discovery probe now passes too.
- New regressions caught lost ownership IDs after Git read failure, lost acknowledged identities
  after an issue edit, post-task-write readback self-clearing, and duplicate setup alerts after
  losing known path context. The fixes retain IDs and reporting paths without granting repair
  authority. A marker-clearing negative control proves no automatic completion or latch clearing.
- Parent tightened self-contained repair alerts after two genuine public failures: native creation
  requires evidence no owner was previously established, and must never replace a previously
  established task. Both full setup/guidance modules then passed 20 checks on each Python.
- Before the second Opus review, full suites passed 446 tests with no skips: Python 3.12.3 in
  644.795 seconds and Python 3.13.5 in 639.978 seconds. Source/test hashes stayed unchanged during
  both runs. Real SDK/private tmux and five no-inference Pi SDK probes were included; no live
  backend/model behavior is claimed.
- Pre-second-review Ruff and all three import contracts passed. The map has 65 boxes; filtering
  removed 3,073 calls and 48 type relationships. Repeat exports match. Ten external-base warnings
  and text-only Mermaid validation limits remain.
- Pre-second-review offline builds passed 72 wheel digests, safe/unique members, matching 69 source
  and resource files and 47 test files, and five extracted-wheel help checks. No install or upgrade
  was needed. These checks belong to the second review's snapshot, not the later follow-up.
- The second Opus review requested changes after all 148 snapshot hashes stayed unchanged. The
  earlier five findings are fixed or superseded by Scott's option 2. The reviewer found no replay
  of uncertain writes and no automatic completion of saved incomplete plans. It independently ran
  93 related checks per Python, two managed SDK/private-tmux checks on Python 3.12, lint and import
  contracts; those passed. It did not rerun the full suites, packaging or map.
- Three new public assertions failed on both Python versions: a stale pending lookup creates work
  after its issue closes; duplicate ownership candidates become permanent pins; and Git checks
  occur after plan creation, multiplying user-approved repairs for a known repository problem.
  The last is a deliberate ordering choice in the earlier tests, not a hidden test failure.
- Scott approved dropping stale unsaved work, Foreman-led duplicate reconciliation with user
  approval, and repository/mapping checks at startup plus before each new plan. The
  [approved contract](../adrs/watcher-problems.md) distinguishes these requirements from current
  implementation. Do not delete duplicate history/work, replace an established owner, or modify
  Git/configuration automatically. Existing incomplete plans remain read-only for the watcher.
- Coverage gaps: pending lookup tests restored access while the issue remained eligible; identity
  tests pinned single owners rather than resolving initial duplicates; pre-add error tests assumed
  a plan was already saved. New regressions must cover those missing sequences. Preserve genuine
  interrupted-setup tests by arranging an existing plan or a fault after creation, rather than
  weakening the approved repair boundary when pre-write checks move earlier.
- Independent startup probes against the frozen second-review snapshot fail on both Pythons:
  without any incoming issue, neither a changed actual origin nor a mismatched source with matching
  saved/actual remote URLs raises an alert. The final failures are explicit missing-alert assertions
  with no planning writes and clean intentional watcher stops. Earlier probe import/fixture errors
  are retained separately and are not product evidence. See `parent/runs/startup-product-assert-*`.
- A separate real-Git probe against that snapshot shows an existing unregistered feature branch
  also leaves an incomplete plan. It fails the explicit no-plan assertion on both Pythons while
  preserving the branch. Pre-create inspection must cover branch conflicts, not only origin and
  target-directory checks. Evidence: `parent/runs/branch-conflict-red-*`.
- Implementation evidence is under `followup-fixes`; full validation, map/package refresh and a
  third Opus review remain parent-owned gates. No current completion or acceptance is claimed.
- Scott requested a fresh SonarQube scan before the next review. The results below apply to the
  current source; historical scans of other snapshots do not satisfy this check.
- N1–N3 implementation passes 186 related checks, 23 focused checks and ten managed/native checks
  on each Python. These selections overlap. Fourteen delivered source/test hashes match, including
  retained protected bytes and meaningful older safety assertions. The three independent parent
  startup/branch probes now pass on both Pythons. See `followup-fixes/handoff.md` for red/green
  evidence and the precise old fixture arrangements adapted for the approved earlier checks.
- Fresh full native-enabled suites pass 465 tests each without skips: Python 3.12.3 in 634.338
  seconds and Python 3.13.5 in 630.866 seconds. Both runs and the SonarQube scan pin the same 117
  source/test files, with unchanged hashes. Ruff and all three import contracts pass. The new
  Mycelium map has 68 boxes; test filtering removed 3,407 calls and 52 type relationships. Repeat
  exports match; ten external-base warnings remain and Mermaid validation is text-only.
- SonarQube analysis `51ceacbb-2597-4877-8f42-0fce536f1bbc` completed successfully, but the assigned
  gate failed on 38 new violations: 37 maintainability findings and one bug-classified finding.
  It reports zero vulnerabilities, security hotspots and duplication; these are scanner results,
  not proof that none exist. The separate `caycStatus` is non-compliant. The server's new-code
  period starts at the previous version on 2026-10-09, not this working diff.
- Scope triage finds 23 findings in unchanged files and one in an unchanged function within a
  changed file; 14 are in changed/new functions, which does not prove all 14 were introduced here.
  The bug-classified finding concerns synchronous `os.open` in protected `agentshell/owner.py:283`;
  that file is byte-identical to HEAD. It is not a reproduced runtime failure. Three test-helper
  findings need triage, not renaming helpers into fake tests. No findings were suppressed.
  No gate/profile/baseline was changed, and protected lifecycle code remains untouched.
- Scanner 8.1.0.6389 used local server 26.8.0.126808, `src` and `tests`, and vault aliases only.
  The eight cached engine/plugin jars stayed byte-identical; JRE auto-provisioning was disabled
  using the existing bundled JRE, and dependency resolution was disabled. No install or upgrade.
  Missing blame warnings for uncommitted files limit SCM features; source hashes identify the
  actual scanned bytes rather than claiming HEAD alone describes the scan. No coverage report was
  imported. Evidence is in `sonar-followup`, including gate/issue results and scope triage.
- Current offline packages pass 72 wheel digests, exact matching of 69 source/resource files and
  48 test files, safe/unique archive checks and five extracted-wheel help commands. No installation.
- SonarQube remediation and renewed review acceptance remain gates. Scott subsequently approved
  [fixing all outstanding findings](sonarqube-remediation.md), including the previously protected
  Factory integration code, with separate Pi worktrees and Claude Code review. Behavioral safety
  remains required; the source-byte freeze no longer prevents those approved refactors.

Transient logs and review material live under `/tmp/factory-watcher-alerts-hpVnTr`, not in the repo.
Only durable architecture and progress records belong here. No commit or push is part of this task.
