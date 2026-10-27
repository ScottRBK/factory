# CI test runtime

Status: the approved public-boundary and explicit-deadline follow-up is implemented. Final local
validation and independent review are complete; hosted CI remains unverified. Scott's later
approval supersedes the earlier simple-improvements restriction for the changes described below.
Production defaults, real safety evidence and dependencies are unchanged. No fake clocks, user
runtime overrides, new commit or push are authorized by this work record.

Back to [implementation plan](../plan.md) and [development checks](../adrs/development-checks.md).

## Earlier pass: baseline

The sections through the earlier Evidence record describe the completed first pass, not the
current follow-up. Their counts and scope limits remain historical evidence.

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

- No production-default timeout changes, skipped tests or weakened safety assertions.
  The earlier pass kept all real waits unchanged; the approved follow-up uses explicit short
  deadlines while retaining real expiry, signals, cleanup and process-identity evidence.
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

## Approved follow-up: explicit deadlines and public matrices

Baseline source: `688c92625cc866739a56530561adb8e934d6ee3c`.
Investigate durations strictly greater than 3.000 seconds; this is not a mandatory test limit.
The inventory contains 27 confirmed cases: 20 local and seven additional hosted cases. Another
16 hosted timestamp gaps are candidates, not exact test durations. The local 503-test baseline
passed without skips in 638.017 seconds on Python 3.12 and 619.997 seconds on Python 3.13.

Hosted run [40567916170][followup-ci] was completed/cancelled: Python 3.12 succeeded and 3.13 was
cancelled. Its logs report 503 tests in 819.849 and 879.308 seconds. The cancellation cause is not
established. This is not a green workflow, and local improvements do not establish hosted success.

### Implemented scope and retained coverage

- Frozen, finite-positive policies compose command, TERM-grace and AgentShell lifecycle deadlines
  through public `main(policy)`. Owned children receive lifecycle JSON and validate it before a
  session opens. Ordinary CLI values remain unchanged; no flag, environment override, saved value
  or global scaling is added. The detailed contract is in the development-checks ADR.
- Eleven Factory-controlled expiry cases use short real deadlines. The native AgentShell 0.5.0
  fixed-five-second timeout proof is unchanged. No private SDK patch or fabricated timeout is used.
  The installed pinned official source established that this SDK timeout has no public input;
  Context7 was unavailable. No dependency was installed or changed.
- Numbered input matrices retain every invalid answer and both valid endpoints at the public parser.
  All seven distinct worker prompts and both Foreman prompts retain real CLI rejection and exact
  no-mutation proofs; positive CLI model/effort wiring remains.
- All 25 invalid planning catalogs and both valid modes use the public connection adapter and a
  controlled real executable. HTTP policy cases use real loopback requests, with absent credentials,
  redirect refusal and retained CLI notice/access checks.
- Cleanup matrices use the public marker validator and real Git/filesystem verification. Watcher
  routes remain for absent/pending/invalid/removed markers, occupied paths and changed origin.
  Canonical mixed-case acceptance, stale/relocated registrations and no mutation/recreation remain.
- Saved diagnostic fixtures restore bytes, modes, symlinks, Git origin, environment, external state
  and logs between every case. Invalid skills retain all three failures and the corrected retry on
  the explicitly named partial review-skill case.
- Native reload starts from a failed manual setup and retains real SDK reload/session/edit checks.
  Its class is now named `NativeSetupReloadTests`; assisted owner gates have separate lifecycle
  coverage. This opt-in probe ran locally, not as a live-model or hosted-speed claim.
- Watcher alert tests use observable response gates, not race-avoidance sleeps. Later request
  entries prove completion of a later sequential cycle. Production watcher polling is unchanged.
  Clear the planning fault before waiting for the repaired source response: recovery can pause
  reads.
- Busy-owner first-setup repair and pane-loss replacement-refusal coverage remain unchanged.
  Proposed reductions of those distinct safety scenarios were rejected.

### Review fixes and validation

The first integrated suites passed 510 tests without skips in 417.197 seconds (3.12) and
406.561 seconds (3.13). Source/test hashes stayed unchanged during each run. These results precede
review fixes; they do not validate the final source.

Independent Claude review through AgentShell found one blocker: three short deadlines also bounded
uncontrolled startup. The tests now give watcher startup two seconds, real tmux/controller readiness
one second with a three-second owner deadline, and slow-launch parent/controller readiness one
second each. Real expiry and all path assertions remain. Reliability takes priority over three
seconds.

Recommended fixes also add command-startup margin, preserve a below-default TERM-grace watchdog,
acknowledge cleanup through a second FIFO, isolate catalog environment, and test malformed launch
maps plus policy types and immutability. Adapter defaults still duplicate policy literals.
CLI composition is tested, but separate changes to adapter defaults remain a maintenance risk.
No production-default change is claimed.

- Post-review focused selection: 16 passed, no skips, 22.832 seconds on Python 3.12.
- The next 511-test suites passed in 415.741 seconds (3.12) and 410.501 seconds (3.13), with
  no skips and unchanged source/test hashes. Those runs still predate the B2 coverage correction.
- Closure review found B2: the acknowledged cleanup checked owner lifetime but not cancelled init
  lifetime. The test now checks both before acknowledgement and keeps the default readiness limit,
  so cancellation cannot be confused with a short readiness timeout. Optional cleanup upper bounds
  were increased; production values remain unchanged. Three focused cases pass in 8.510 seconds.
- Independent Claude review through AgentShell closes B2 with APPROVE and no remaining code-review
  blocker. Its final evidence note confirms both full passes and current source/test hash equality.
  The reviewer read the parent's logs and did not rerun tests. Hosted CI remains unverified.
  Code approval is separate. The 0.3-second delay gives less time to detect an early-exit mutant
  than the old 15-second wait. Review accepts this limit; correct-code ordering is gated.
- Ruff and all three import contracts pass after B2. Final offline wheel/sdist verification passes:
  75 wheel RECORD checksums, 72 source/resource files, 54 sdist test files and four extracted-wheel
  help commands. No artifact is installed or copied into the delivery directory.
- Mycelium 0.4.5: 77 boxes, 3,682 test calls and 56 type relationships filtered, no missing in-scope
  call endpoints; repeated export is byte-identical. Twelve external-base warnings remain.
  Mermaid is checked as text, not rendered.

### Final local results

Both final-source suites pass the same 511 tests, without skips or source/test hash changes:

| Python | Baseline: 503 tests | Final: 511 tests | Reduction |
| --- | ---: | ---: | ---: |
| 3.12 | 638.017 s | 413.314 s | 224.703 s (35.2%) |
| 3.13 | 619.997 s | 413.763 s | 206.234 s (33.3%) |

The 20 baseline local slow cases total 280.741/279.015 seconds. Their mapped final cases total
39.930/40.209 seconds. Mapping includes moved public checks, so attribution is approximate.
These are individual local full runs, not statistical speed estimates or hosted measurements.
All 27 confirmed cases and 16 hosted-gap candidates have per-case comparisons in
`/tmp/factory-fast-tests-lbh9u1xh/final-comparison-3.json`. Hosted gaps remain candidates, not
measured test durations. Rounded case times need not sum to full-suite elapsed time.

Seven cases remain strictly above three seconds on both interpreters:

| Case | 3.12 | 3.13 | Why retained |
| --- | ---: | ---: | --- |
| Native send timeout | 7.409 s | 7.503 s | SDK's fixed-five-second timeout proof |
| Watcher prerequisite timeout | 4.135 s | 4.094 s | Real startup and frozen-watcher cleanup |
| Readiness timeout with retry | 3.552 s | 3.591 s | Real tmux/controller startup and cleanup |
| Approved busy-owner repair | 3.111 s | 3.085 s | Protected distinct ownership scenario |
| Native named workers | 3.087 s | 3.108 s | Both harnesses, real tools and session contracts |
| Native coordinator resources | 3.077 s | 3.246 s | Three independent native role loads |
| Changed-pane preservation | 3.036 s | 3.011 s | Protected replacement-refusal scenario |

The native worker and coordinator tests crossed the threshold in these final runs. Inspection of
`tests/test_native_workers.py:131-169` shows public setup, real Git worktrees and native tool calls
for both harnesses. `tests/test_native_roles.py:193-236` checks three roles through separate native
loaders. Both files are unchanged. Their distinct cases are retained; no delay was added or removed,
and the small timing change has not been attributed to a specific cause. No test is split or
weakened to meet the investigation threshold.

### Evidence accounting

The final suite has eight more tests than the 503-test baseline. Five old IDs are replaced by
thirteen IDs: four cleanup watcher cases move into two retained CLI routes and five public-boundary
checks; native reload is renamed; three deadline checks and two numbered-parser checks are added.
This is a coverage mapping, not a claim that the old and new test inventories are identical.
Both supported interpreters ran the same final inventory without skips.

Worker measurements are focused snapshot evidence, not final full-suite measurements. The deadline
worker's 14-test selection included 12 expiry cases and two policy checks. Both policy durations
rounded to 0.000 seconds; thus both the 14 displayed durations and the 12 expiry durations sum to
21.492 seconds. This resolves the apparent count mismatch; it does not imply fourteen expiry cases.
That selection predates the added startup margins. The 12-case local baseline was 229.329 seconds.

The parent restored all seven worker CLI prompts after merging, so the worker's four-representative-
CLI timing total is not the final coverage or timing. The early poll-pair measurement fell from
8.269 to 3.824 seconds before worker integration; do not substitute it for final integrated timings.
The first repaired-response gate run failed because it waited before clearing the planning fault;
that failure and the corrected ordering are retained in the evidence.

Current local evidence: `/tmp/factory-fast-tests-lbh9u1xh/`; inventory and hosted logs:
`/tmp/factory-slow-tests-BOKbOz/`. Worker handoffs and earlier attempts remain available.
No live account, model, watcher, memory enablement, dependency operation, commit or push occurred.
The previously unexplained Python 3.13 shutdown remains a limitation, not a fixed issue.

[followup-ci]: https://github.com/ScottRBK/factory/actions/runs/40567916170
