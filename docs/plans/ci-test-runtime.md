# CI test runtime

Status: safe changes implemented and locally validated; hosted CI remains unverified. Scott
approved the planning-test boundary change, then limited this work to simple improvements.
Clock redesign, broader test restructuring and new dependencies are outside this pass.
No commit or push is authorized by this work record.

Back to [implementation plan](../plan.md) and [development checks](../adrs/development-checks.md).

## Baseline

Source: `0013a3704419751f630a78d8c4e6a8c9bc96d82b`.

- Latest hosted run: [40239921500][latest-ci]. Both Python jobs exceeded the 15-minute job limit.
  Python 3.12 completed 440 of 472 tests; Python 3.13 completed 423. Each included five skips.
  Completed cases were passing; this was not a reported assertion failure.
- The [preceding push][previous-ci] also exceeded the limit, before the Foreman guidance change.
- Fresh isolated local Python 3.12 run: 472 tests, no skips, PASS in 678.070 seconds.
  Runner wall time was 678.189 seconds. The five optional native SDK checks ran without inference.
- Thirteen deadline-focused methods used 232.549 seconds locally, including setup and cleanup.
- Three malformed planning-reply matrices covered 67 values and used 43.480 seconds locally,
  about 71 seconds in hosted Python 3.12. Each value restarted the full watcher.

Local timings and hosted timings are separate evidence. Module, fixture and case times overlap;
do not add those totals. New test IDs can include renames, not necessarily new behavior.
The older intermittent Python 3.13 shutdown failure remains unexplained and is not fixed here.

## Small slices

- [x] Measure the current suite and identify repeated setup and actual deadline waits.
- [x] Move the 67 malformed-reply variants to the real planning adapter's public operations.
  Retain full watcher checks for each distinct inventory/detail failure and safe recovery path.
  Record a case mapping and use deliberate regressions in a temporary copy to validate the tests.
- [x] Check for safe process-startup savings without changing production behavior or test seams.
  Precompile source with checked-hash caches in CI; retain isolated workspaces and all checks.
  A separate external-helper startup experiment showed no useful saving and was not adopted.
- [x] Add built-in unittest duration output to the existing CI command and local instructions.
  Keep verbose timestamped progress, which remains useful if CI stops before the final summary.
- [x] Run the affected checks, then complete suites on Python 3.12 and 3.13 without concurrent
  full-suite runs. Record test IDs, skips, durations and unchanged production behavior.
- [x] Obtain independent Claude Code review and resolve affected findings.
- [ ] After separate commit/push approval, verify hosted CI for the exact resulting commit.

## Tracking

Keep this record small: each completed slice gets its measured before/after time, retained
observations, validation evidence and any remaining limit. The CI log holds the total test count,
skips, total time and slowest 25 test durations. These durations include setup and cleanup.

Use the existing unittest runner and GitHub logs; add no dashboard, package or custom timing
framework for this pass. End-of-run durations do not survive a hard cancellation, so retain
verbose progress and GitHub's timestamps. Do not impose fragile per-case time assertions or
claim a hosted speed improvement from a local result. The 15-minute CI limit stays unchanged.

## Safety and scope

- No production timeout changes, shortened safety waits, skipped tests or weakened assertions.
- Keep real process, signal, ownership, Git and cleanup tests at their existing boundaries.
- The two watcher readiness timeouts are distinct: controller readiness after prompt launch,
  and the parent's outer deadline after slow launch. Neither is removed as a duplicate.
- Do not migrate DinoLand or edit existing workspaces, credentials or planning records.
- Protected `FACTORY.md`, root `AGENTS.md` and the plan's Design questions remain unchanged.

## Foreman `/forgetful plan`

Read-only source investigation is complete:

- The sibling Pi Forgetful extension registers `/forgetful plans`, plural, not `/forgetful plan`.
- Factory's default root definition selects only AgentShell and hide-tools extensions, and disables
  personal/project resource discovery. Native Forgetful CLI guidance does not register that command.
- The Pi extension has separate REST/account/project settings. Loading it would not establish that
  it points to the Factory's selected instance and project; it can also enable memory hooks.

The running Foreman's workspace and command menu were not inspected. If `/forgetful` is available,
the singular name may explain the problem. If it is absent, the default resource selection explains
why. The existing native CLI remains the configured planning route. No plugin installation,
personal-resource enablement, credential migration or running-session change was made.
The full source references and remaining checks are in the temporary diagnosis below.

## Focused results

The exact 67 malformed cases are retained at the approved public adapter boundary. Five valid-input
checks also reject an always-failing adapter. Existing full watcher checks remain for plan/task
inventories and full records, including pause, alert deduplication, preservation and safe repair.
The replaced three matrices took 43.480 seconds locally. The new adapter module plus one additional
full watcher proof took 2.943 seconds (3.027 seconds with runner overhead). These are different
method selections, not a claim that the full suite is now that fast.

The 17-test affected selection passes on Python 3.12 and 3.13 without skips. Temporary-copy controls
prove the tests fail when type, association, count or row-ID guards are removed. Claude Code
approved the source and independently checked the 67-case mapping, 479-test inventory and 18 focused
tests on each Python. Its initial count-equality coverage concern was corrected: an unchanged
watcher test rejects that deliberate regression. Four documentation-width issues are fixed.
Complete-suite results are below. Hosted CI remains unverified.

An unchanged nine-test CLI selection had median times of 2.794 seconds without precompiled source
and 2.565 seconds with it, across three paired runs. One checked-hash run took 2.637 seconds.
Compilation took about 0.06 seconds. This is a small selected-workload saving, not a projected
whole-suite saving. A same-size, same-mtime source edit correctly invalidated the hash cache.
Skipping Python site setup in fake external programs showed only noise-level differences, so no
fixture interpreter or shebang changes were made.

## Complete validation

Both full suites ran sequentially against immutable reviewed source:

- Python 3.12.3: 479 tests, no skips, PASS in 625.295 seconds; runner wall time 625.444 seconds.
- Python 3.13.5: 479 tests, no skips, PASS in 617.344 seconds; runner wall time 617.496 seconds.
- All 479 IDs are unique and match the intended inventory. The only removed methods are the three
  mapped matrices; nine adapter methods and one watcher proof were added. Source hashes match.
- The Python 3.12 full-run replacement selection took 2.663 seconds: 1.300 for the adapter tests
  and 1.363 for the added watcher proof, versus the old matrices' 43.480 seconds.
- The observed Python 3.12 suite reduction is 52.775 seconds (7.78%). Separate-run variation means
  the full difference cannot be attributed solely to this change. There is no matched fresh 3.13
  baseline. Hosted runner times must be measured separately after an approved push.
- Real deadline-focused tests still take about 232 seconds per suite. The complete suite remains
  integration-heavy and takes about ten minutes locally; this pass does not meet a seconds target.

Validation exposed one cache detail: `compileall --invalidation-mode checked-hash` can preserve an
already-valid timestamp cache. The final CI command adds `-f` to rebuild those caches too. A public
CLI probe on both Pythons demonstrated stale same-size/same-mtime content without force and correct
source loading with force. All 55 source caches then had checked-hash headers on each interpreter.
The unchanged source/tests passed 11 affected checks per Python with the final forced-precompile
command. The full runs above used the earlier non-forced precompile; no test/source bytes changed.

Ruff and all three import contracts pass. An offline wheel/sdist build and the existing 72-checksum
wheel gate pass. The Mycelium map was regenerated and a repeat export matched; it remains a static
heuristic map, not a rendered-diagram proof. No runtime package was installed or delivered.

The four initial documentation-width findings are fixed. The count-equality review correction and
final cache-command adjustment are included in review closure. No production Python, timeout,
credential, bundle, dependency, workspace or saved plan changed. No commit or push was made.

## Evidence

Baseline audit: `/tmp/factory-ci-timing-pOYx3v/REPORT.md` and `timing-audit/full-312/` below it.
Current implementation/review evidence: `/tmp/factory-test-runtime-r1K5G2/`.

[latest-ci]: https://github.com/ScottRBK/factory/actions/runs/40239921500
[previous-ci]: https://github.com/ScottRBK/factory/actions/runs/40225651777
