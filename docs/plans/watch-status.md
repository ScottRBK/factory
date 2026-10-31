# Watch status lifecycle correction

Final implementation: all nine approved findings implemented and validated with recorded limits.
Source remains frozen on `caec97...`; focused tests and fresh actual parent SQ pass. Broader tests
retain the baseline phrase failure, OS skips and one unreproduced intermittent 3.13 shutdown.
Parent verified the final source manifest and SQ result before the authorized commit and push.
No policy holds, full-suite GREEN, deployment or coverage claim. Earlier results remain historical.

## Scope and constraints

Scott approved lifecycle-only status for both plain and managed watch, through public CLI tests
and external-command/AgentShell boundary doubles. Preserve owned versus borrowed cleanup,
managed-only stop and delivery/replacement safeguards. Health stays explicitly unverified.
No live DinoLand interaction, dependency installation, commit, push or reviewer dispatch is part
of this implementation. The parent owns the authorized actual SQ scans; this implementation agent
does not scan or change scanner settings. `FACTORY.md` and the separate `plans/slice-7.md` work
are preserved.

Design: [watcher lifecycle observation](../adrs/watch-status.md).

## TDD evidence

Commands use `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests` and
`/tmp/factory-placeholder-venv/bin/python -m unittest`.

1. The implementation sandbox rejected the existing fixture's Unix socket bind. This was an
   environment failure, not defect RED: `/tmp/factory-status-red-1.log`.
2. Parent ran the new public concurrent plain-watch status regression before production changes.
   Actual RED: `watcher` was `stopped`, expected `running`; 1 test, 0.440 seconds.
   Evidence: `/tmp/factory-status-parent-red-1.log`.
3. First observer slice: parent confirmed the original regression GREEN. A second startup/exit
   regression reached the intended fallback failure after shutdown (`source` missing because the
   previous managed record was selected); 2 tests, 1.171 seconds.
   Evidence: `/tmp/factory-status-parent-cycle-2.log`.
4. Parent cycle 3 confirmed the discovery-replacement exit race: the original invocation overwrote
   replacement data during exit. The other 37 tests passed; 38 tests, 28.114 seconds.
   Evidence: `/tmp/factory-status-parent-cycle-3.log`. Exit publication now preserves changed,
   missing or unreadable discovery while the normal workspace lease still excludes another run.
5. Parent cycle 4 passed 41 tests, including the replacement fix and new startup-interruption,
   cleanup-in-progress and live-plain/broken-owner cases. The only failure was missing saved
   cleanup-uncertainty evidence; 42 tests, 29.494 seconds.
   Evidence: `/tmp/factory-status-parent-cycle-4.log`.
6. The final slice retains `recorded_evidence: cleanup_uncertain` when terminal close fails.
   Parent then confirmed all 42 focused tests pass in 28.933 seconds, without skips:
   `/tmp/factory-status-parent-green.log`. The deep-nesting case passed cycle 4; a public CLI probe
   also returned bounded unknown status for shallower payloads. Review later reproduced failures
   with larger within-limit payloads; finding 3 below supersedes that limited negative finding.

## Local candidate checks

- Full Ruff 0.17.0: passes (`/tmp/factory-status-lint.log`).
- All 114 Python files compile in memory without bytecode writes
  (`/tmp/factory-status-compile.log`).
- Import Linter: 59 files and 127 dependencies analyzed; all three existing source contracts kept,
  none broken (`/tmp/factory-status-import-boundaries.log`). The existing launcher resolves to
  Python 3.14, but its packages are installed for 3.12. The cached 3.12 interpreter with the
  existing `.venv/lib/python3.12/site-packages` runs the unchanged CLI successfully; no installation
  or launcher modification was needed.
- Wheel and sdist build through cached `uv_build==0.13.5`; 76 wheel checksums verified
  (`/tmp/factory-status-package-build.log`, `/tmp/factory-status-package-check.log`).
  All 59 source modules are present in the wheel, the observer bytes match current source, and
  the new public regression module is in the sdist (`/tmp/factory-status-package-coverage.log`).
- Cached Mycelium 0.4.5 analyzes and exports the current tree with tests excluded; 80 boxes,
  one nonempty class diagram, full signatures and twelve existing external-base warnings.
  Repeat export of the same map is byte-identical. Source relationships remain heuristic;
  the overview/ADRs were checked against source. Mermaid was checked as text, not rendered.
- The final overview has 449 lines; local Markdown links and new 100-column widths pass checks.
  Existing unchanged width exceptions are retained (`/tmp/factory-status-final-doc-checks.log`).

## Final parent tests on the scanned source

Final source manifest digest:
`4d777095b8ed3a1a351a18487ca5ab2b66e22e1f577118d6476d5033b6e584d0`.

- Python 3.12.16: focused watch/status/architecture tests, 48 passed in 32.842 seconds.
  Log: `/tmp/factory-status-final-focused-312.log`.
- Python 3.13.18: the same 48 tests passed in 33.073 seconds.
  Log: `/tmp/factory-status-final-focused-313.log`.
- Python 3.12.16: broader 480-test run, 476 passed, 3 OS skips and 1 failure in 294.218 seconds.
  Log: `/tmp/factory-status-final-312.log`.
- Python 3.13.18: corrected broader run, 480 tests with the same 476 passes, 3 OS skips and
  1 failure in 301.364 seconds. Log: `/tmp/factory-status-final-313-corrected.log`.

The focused runs use the actual cached 3.12 Import Linter launcher; no harness source override
was needed. Broader selection uses `/tmp/factory-pi-alignment-YYrJLb/run-tests.py` and explicitly
lists 48 excluded `LifecycleFixture` cases: they hardcode tmux discovery under `/usr/bin:/bin`,
where tmux is absent on this Nix host. These include the modified native saved-stop assertion in
`test_assisted_lifecycle.py`; that path has not run natively here. New managed status tests with
external AgentShell doubles do pass. Isolated no-inference probes use the actual installed Pi SDK
1.4.0 with `NATIVE_PI_SDK` enabled. No live factory or inference validation is claimed.

The remaining broader failure is `GeneratedGuidanceTests` method
`test_owner_guidance_uses_explicit_permission_and_its_own_selected_definition`: it expects
`auto_approve false`, while the unchanged resource says `auto_approve=false`. Parent
reproduced it on unchanged HEAD in `/tmp/factory-status-baseline`: 0.384 seconds on 3.12 and
0.389 seconds on 3.13. Logs: `/tmp/factory-status-baseline-guidance.log` and
`/tmp/factory-status-baseline-guidance-313.log`. It is not fixed by this scope. No full-suite GREEN
is claimed.

Earlier evidence is retained: `/tmp/factory-status-full-tests.log` reports 528 tests in
291.090 seconds, with 56 failures and 9 skips: 48 host-dependent lifecycle cases, 7 missing-launcher
architecture cases and the same baseline phrase failure. The earlier 3.13 run in
`/tmp/factory-status-final-313.log` had 235 failures and 9 errors because its stale cached `.pth`
omitted AgentShell. The corrected isolated `/tmp/factory-status-python313` reuses existing 3.12
site packages without installation; the corrected result above supersedes that environment failure.

## Actual SQ analyses and refactor

The first actual repository scan used source manifest digest
`cc8ecdcd7095e3104023c87a8c7480c595a4b6bcb2b241f0c0efe847eab35591`.
Analysis `c0ed80b4-11c9-488e-a9c3-d056486c9a6b` processed successfully under CE task
`5e8db8c0-0fbe-4c2c-bae6-20758e6a8404`; its gate failed with two new issues:
`python:S7498` at `watch_status.py:77` and `python:S5899` at `test_watch_status.py:45`.
Results remain in `/tmp/factory-status-sq-results-1.json`.

Those findings supplied static RED for a behavior-preserving refactor. `unknown_status` uses a
dictionary literal; the unnecessary intermediate fixture was removed and its genuinely used
helper became module-level `read_status(fixture)`. No suppressions, fake test renames or assertion
changes were introduced. The AST preservation check is in
`/tmp/factory-status-refactor-preservation.log`. Ruff, all three import contracts and packaging
passed again; see `/tmp/factory-status-refactor-lint.log`,
`/tmp/factory-status-refactor-import-boundaries.log`,
`/tmp/factory-status-refactor-package-build.log` and
`/tmp/factory-status-refactor-package-check.log`.
The refreshed map has 80 boxes and a
byte-identical repeat export; test filtering removes 3,820 calls and 58 type relationships.

The parent completed and inspected the final actual scan before any reviewer dispatch:

- Project `forgetful-factory`, main; date `2026-10-30T21:11:36+0000`.
- Analysis `35b504b6-7e57-4511-81d9-09d5df907f74`;
  CE `8ba2be5a-d5a6-41f1-abde-b0fabdea1e24`, `SUCCESS`.
- Gate `Sonar way sans code coverage`: `OK`; new violations 0, new duplication 0.0 percent.
- Zero unresolved issues, bugs, vulnerabilities, code smells, violations and hotspots;
  overall duplication 0.0 percent, 5,432 non-comment lines of code.
- No coverage was imported; `caycStatus: non-compliant` remains separate from the passing gate.
- Results: `/tmp/factory-status-sq-results-final.json`;
  scanner log: `/tmp/factory-status-sq-scan-2.log`.

The reported revision `afff583d0b67c861061cbddd49bd987d13bceee3` is the base HEAD, not a commit
containing these changes. The dirty snapshot is bound by build string
`watch-status-4d777095b8ed3a1a351a18487ca5ab2b66e22e1f577118d6476d5033b6e584d0`.
All 130 src/tests hashes matched before and after scanning; the five changed Python files matched
server source apart from terminal-newline normalization. Hash evidence:
`/tmp/factory-status-final-source-check.log`. Encoding and missing-blame warnings remain recorded
in the scan output; no source/configuration workaround was applied.

Parent used unchanged `.sonarqube/start-scan.sh` with official portable CLI 8.3.0.16463 in `/tmp`.
Provenance, checksum, tag, 15 Maven-component OSV checks and public GitHub advisory inspection are
recorded in `/tmp/factory-status-scanner-audit.md`. Archive SHA-256:
`565c5040aa77d35da4e1d64c48184174f3e7444ad6a99f23335a39223587bb56`.
Credentials used envault names only. No project dependencies, scanner configuration, gate,
exclusions, rules or source settings changed; normal server analyzers were cached under `/tmp`.
Both first-scan issues were resolved through the source refactor.

## Handoff

At the pre-review handoff, source was frozen at `/tmp/factory-status-before-opus.sha256`;
initial metadata is in
`/tmp/factory-status-candidate.json`, and the final reviewer briefing is
`/tmp/factory-status-review-handoff.md`. Earlier metadata/manifest remain in
`/tmp/factory-status-candidate-scan-1.json` and `/tmp/factory-status-source-scan-1.sha256`.
No reviewer was launched, and no commit, hosted CI, live adoption or autonomous-agent behavior
is claimed. Final evidence updates change documentation only.

The observer is Linux-specific and local to the watcher process. Its independent thread can answer
while the main loop is blocked; this is intentionally not health or progress monitoring. Plain
status does not capture a native target. Missing discovery cannot retrospectively instrument old
watchers. Same-user writes bypassing the lease remain outside transactional publication guarantees.

## Documentation and tool basis

Required factory/architecture/plan/ADR and Python, TDD, Mycelium/companion, Context7 and dependency
boundary guidance was read. No detailed map was loaded in full. The cached Mycelium 0.4.5 CLI and
uv build backend are available without installation. Context7 had no matching ScottRBK package;
the already fetched pinned official examples supplied the ownership/target contract.

## Independent review corrections in progress

Parent supplied independent Claude Opus review session `54b0290a-722d-4113-8091-c10af12ad9df` and
its public-boundary probes under `/tmp/claude-review`. Scott approved concrete findings 1, 2, 3,
5, 6, 8 and 9 for correction. Policy choices 4 (single-source saved-stop reporting) and 7
(observation-startup failure policy) remain on hold; neither is decided by this implementation.
No final SQ scan or reviewer dispatch is authorized for this correction stage.

The earlier passing SQ analysis and test results above describe the historical `4d777...` source,
not approval of the corrections. Its 130-file manifest and source contents were verified and copied
to `/tmp/factory-status-before-opus.sha256`, `/tmp/factory-status-before-opus.json` and
`/tmp/factory-status-before-opus-src-tests.tar` before edits. External FACTORY.md and Slice 7
changes are preserved independently.

The first vertical slice adds public CLI regressions in `tests/test_watch_status_review.py` for
nonlive plain/managed evidence coexistence: unreachable ready owner, saved stopped owner, malformed
owner record and a timed-out living plain endpoint beside a saved stopped owner. The tests require
current lifecycle fields to stay unknown while retaining managed metadata/recovery and nested
plain evidence. Parent established actual RED in `/tmp/factory-status-review-red-1.log`:
4 tests in 2.270 seconds, 3 failures and 1 error, all on lost managed metadata/plain evidence.
The merge is now implemented and documented in the ADR: only a live source wins outright;
nonlive sources retain managed top-level metadata and nested plain evidence with current lifecycle
fields unknown. Single-source policy choice 4 and fail-closed startup choice 7 remain unchanged.

The next slice added admission refusal and maximum-depth JSON regressions. Invalid interval,
unconfigured workspace and uncertain-owner refusal must not create or replace plain discovery.
Within-limit 16,384-byte deep discovery and 16,383-byte deep request frames must remain controlled
unknown input, without killing the observer thread or replacing cancellation status. Parent cycle 2
confirmed all 16 prior cases GREEN and all 7 new cases RED: 23 tests, 13.012 seconds, 7 failures
(`/tmp/factory-status-review-cycle-2.log`). Observer startup now follows admission, and the bounded
JSON reader converts excessive parser depth to ValueError. Parent cycle 3 confirmed these fixes
GREEN alongside the prior cases: 34 tests in 16.314 seconds, with only five publication failures
(`/tmp/factory-status-review-cycle-3.log`).
The earlier 1,500-depth probe only proved that shallower case safe; larger review reproductions
supersede its limited negative finding.

The next tests cover persisted readiness after abrupt loss, pre-session startup failure, mutable
same-identity history during queries, permission-denied publication preserving interruption/native
failure, and a listener advertising a different PID. Cycle 3 established actual RED for all five
publication cases: lost ready history, missing pre-session finalization, same-run update rejection
and two masked-result/diagnostic failures. The peer regression and five maintenance cases passed.

Corrections 5/6 now attempt one bounded-size history write per lifecycle transition, retaining
identity/replacement checks. Queries compare identity only across updates; pre-session exit is
finalized as stopped with `exited_before_session`. Runtime/final history write failures cannot
replace the watch command's primary result. Initial observer startup remains fail-closed and
single-source saved-stop reporting is unchanged while choices 4/7 are held.

The real peer-PID guard remains intact. The requested private copy is prepared at
`/tmp/factory-status-review-peer-mutant`: only the client PID/UID guard is removed there; all other
src/tests bytes match this candidate. Mutation metadata:
`/tmp/factory-status-review-peer-mutation.json`. Parent established mutant RED in that copy:
one test, 0.306 seconds, accepting `live` where the real guarded test requires `saved`
(`/tmp/factory-status-review-peer-mutant-red.log`). The real test passes on both interpreters.
Maintenance guidance now distinguishes live
managed owner identity from plain readiness, historical evidence and unchecked health (finding 9).
No new prompt-phrase assertions were added. Full Ruff passes.

Interim manifests `/tmp/factory-status-review-slice-1.sha256` and
`/tmp/factory-status-review-slice-2.sha256` retain correction progress. The interim candidate is
captured in `/tmp/factory-status-review-candidate.sha256`; the latest is also published
at `/tmp/factory-status-source.sha256`. Metadata marks work in progress, not a final frozen handoff.
Historical `4d777...` evidence remains separate. No final scan is authorized while 4/7 are held.

Current local candidate checks pass: full Ruff, all three existing import contracts (59 files,
127 dependencies), wheel/sdist build and 76 wheel checksums. Logs:
`/tmp/factory-status-review-candidate-lint.log`,
`/tmp/factory-status-review-candidate-imports.log`,
`/tmp/factory-status-review-candidate-build.log`,
`/tmp/factory-status-review-candidate-package.log`.
The cached Mycelium 0.4.5 full export was refreshed, retains 80 boxes and twelve external-base
warnings, and matches a repeat export byte-for-byte. Filtering removes 3,888 calls and 63 type
relationships. Source navigation/ADRs were checked against the correction; no final SQ or native
full-suite validation was run.

### Interim verification and remaining decisions

Status: READY FOR CONTINUATION, not complete. All approved concrete findings 1, 2, 3, 5, 6, 8 and 9
are covered on source manifest digest
`a69f76f763cffbbde469362e8a9e3f19489bda34e77e39c314d42dc25bb6cb78` (131 files).

- Python 3.12: all 34 focused tests pass in 16.467 seconds.
  `/tmp/factory-status-review-green-312.log`.
- Python 3.13: all 34 focused tests pass in 16.935 seconds.
  `/tmp/factory-status-review-green-313.log`.
- Peer guard: real GREEN on both; guard-disabled private copy RED as recorded above (finding 8).
- Adjacent selections each run 44 tests: 41 pass, 3 fail before behavior because the native fixture
  cannot find Nix-host tmux under `/usr/bin:/bin`. Times: 28.426 seconds on 3.12 and 29.102 on 3.13.
  `/tmp/factory-status-review-adjacent-312.log` and
  `/tmp/factory-status-review-adjacent-313.log`. These are host-blocked, not behavioral passes.

Held decision 4 concerns single-source saved stopped Foreman reporting: the current implementation
retains top-level `foreman: stopped` with saved observation. Choosing always-unknown current state
with stopped only in recorded evidence requires explicit approval. No change was made to that path.
Held decision 7 concerns initial observation failure: private-directory, `/proc` identity or socket
registration failure currently refuses watch startup. Allowing watch without observation also
requires explicit approval. Runtime history failures remain best effort under approved finding 6.

No final validation, final SQ, further review or full-suite acceptance is claimed or authorized
while these decisions are held. Earlier SQ success binds historical `4d777...` source only.
Continuation briefing: `/tmp/factory-status-review-corrections-handoff.md`. The original
`/tmp/factory-status-review-handoff.md` remains historical and unchanged. Source hash checks before
and after this evidence-only update confirm all 131 files unchanged; external edits are preserved.

### Policies 4/7 explicitly approved; next TDD slice

Scott has now explicitly approved both remaining recommendations. The earlier held-policy record
describes the interim `a69f...` snapshot; it is no longer the current decision state. That source,
manifest and metadata are preserved under `/tmp/factory-status-before-policy-4-7` before new tests.

New public CLI tests cover clean saved-stop reporting without invented recovery and optional
observer fallback for real nonprivate-directory/initial-publication failures. The post-bind failure
checks only the original fixture process's `/proc/PID/fd` socket descriptors for listener cleanup.
Further tests preserve native preflight failure and prior discovery during fallback. No private
method calls, syscall monkeypatches, production test hooks or prompt-phrase assertions were added;
warning checks verify severity/scope, not generated agent prose. Direct `/proc`-identity and bind
fault injection is not introduced under this seam; real filesystem refusal and partial startup
are covered. Existing admission/ownership protections remain exercised by prior regressions.

Affected public/native saved-stop assertions now require current unknown plus recorded stopped.
Canonical native-host constraints remain; parent can later run the unchanged assertions in an
isolated copy with only the fixture's tmux search adapted to the known host path. No portability
patch belongs in product/test source. Full Ruff passes. Relevant production behavior is unchanged
until actual parent RED for the new tests. Final validation and actual parent SQ will follow the
completed source correction; no current gate/full-suite success is claimed.

Parent confirmed actual RED in `/tmp/factory-status-policy-red.log`: 5 tests in 1.578 seconds,
all 5 failed. Production now keeps clean managed stop only in recorded history, with current
Foreman unknown and no invented recovery. The optional observation context includes constructor
`/proc` reads and startup, ending before actual watcher composition/execution. Startup failures
warn through the CLI's safe diagnostic path and yield no observer. Partial listener/thread state
is closed; any published failure history is identity checked. Cleanup/publication warnings cannot
replace cancellation or actual watcher diagnostics. Existing admission/lease/owner checks are
unchanged. Parent policy GREEN and final full/native validation are pending.

Two fresh private full-test copies are prepared at `/tmp/factory-status-policy-full-312` and
`/tmp/factory-status-policy-full-313`. Each changes exactly one fixture line: the native tmux search
path points to the existing Nix store executable. All assertions and other src/tests bytes match
the repository. Each `.venv` is a symlink to its already cached interpreter environment, exposing
a valid `lint-imports` launcher without installation or source override. Both launchers use the
existing 3.12 graph checker; the 3.13 test process and AgentShell imports use 3.13. No host or
repository portability change was made. Exact replacement/digests:
`/tmp/factory-status-policy-private-copies.json`.

Discovery only (not execution) finds 550 cases: canonical broad selection 502 with 48 native
exclusions, or all 550 in each private copy. IDs are in
`/tmp/factory-status-policy-canonical-ids.json`, `/tmp/factory-status-policy-private-312-ids.json`
and `/tmp/factory-status-policy-private-313-ids.json`. Parent runner
`/tmp/factory-status-policy-test-runner.py` supports all/canonical-broad/native selections and logs
exclusions. It can save actual failure/error/skip IDs with `--result`. Actual full runs must reuse
the validated `NATIVE_PI_SDK` value; it was unset during discovery only. No test execution,
private full-suite GREEN or new baseline outcome is claimed at this stage.

### Current policy candidate: actual validation and source freeze

All nine findings are implemented on source manifest digest
`caec97d7630235d4fdc9a9c6aaf305960a4efffacc955f338a06bb9a1faf68cb` (131 files).
Manifest: `/tmp/factory-status-final-source.sha256`; base HEAD remains
`afff583d0b67c861061cbddd49bd987d13bceee3`. All src/tests hashes match the exact parent-tested
source before and after local checks. No code changed for the unexpected failure described below.
No policy holds remain. Fresh actual parent SQ and the follow-up results are recorded below.

Parent actual runs use installed Pi SDK 1.4.0, enabled without inference probes or installation:

| Selection | Python | Cases | Passed | OS skips | Failures | Seconds |
| --- | --- | --- | --- | --- | --- | --- |
| Focused status/review/maintenance | 3.12 | 39 | 39 | 0 | 0 | 18.706 |
| Same focused selection | 3.13 | 39 | 39 | 0 | 0 | 19.251 |
| Canonical broad, 48 native excluded | 3.12 | 502 | 498 | 3 | 1 | 309.235 |
| Same canonical selection | 3.13 | 502 | 498 | 3 | 1 | 315.654 |
| Private full, one tmux fixture adaptation | 3.12 | 550 | 546 | 3 | 1 | 371.771 |
| Same private full selection | 3.13 | 550 | 545 | 3 | 2 | 390.853 |
| Sequential private full rerun | 3.13 | 550 | 546 | 3 | 1 | 373.641 |

Focused logs: `/tmp/factory-status-policy-green-{312,313}.log`.
Canonical logs/results: `/tmp/factory-status-policy-canonical-{312,313}.log` and corresponding
`-result.json`. Private logs/results: `/tmp/factory-status-policy-private-{312,313}.log` and
corresponding `-result.json`. All 48 native lifecycle cases pass on each Python in private copies,
including changed saved-stop assertions. Private assertions are unchanged; only the tmux fixture
search path differs. Cached environment symlinks provide the existing Import Linter launcher.
The three skips are the Ubuntu 24.04-only tmux recipe cases; exact IDs/reasons are in each JSON.

The guidance phrase failure remains the independently reproduced unchanged-HEAD baseline described
above. The additional private 3.13 failure is
`WatcherAlertTests.test_archived_plan_is_finished_for_closed_recovery_and_ordinary_intake`:
the fixture's single SIGINT did not end watch within 15 seconds. Its diagnostic records the root
still running, launch/ready events without close, and `KeyboardInterrupt` reported as ignored
inside Python 3.13 `Popen.__del__`/`_internal_poll`. This is consistent with interruption in a
destructor being swallowed. The observer is absent from that stack and does not catch runtime
KeyboardInterrupt; extra observer work could still affect scheduling. Neither causality nor a
pre-existing baseline defect is established. No production fix is made without coordination.
All five targeted repeats pass in 1.166, 1.175, 1.171, 1.541 and 1.448 seconds:
`/tmp/factory-status-policy-timeout-repeat-{1..5}.log`. The sequential full 3.13 rerun passes
546 of 550 with three OS skips, only the known baseline phrase failure and zero errors; all 48
native cases pass. Log/result: `/tmp/factory-status-policy-private-313-sequential.log` and
`/tmp/factory-status-policy-private-313-sequential-result.json`. The original parallel failure
remains retained as intermittent evidence, with cause unproved and no out-of-scope code fix.
Assessment: `/tmp/factory-status-policy-timeout-assessment.txt`. No additional functional issue
in the approved status scope is known; inability to reproduce is not proof of resolution.

The existing stop tests synchronize on startup/polling and then send one SIGINT; they do not force
delivery during Python object destruction. Passing focused/native runs therefore do not exclude
this timing window. No full-suite GREEN, live delivery or final acceptance is claimed.

Fresh local checks on the same source:

- Ruff passes; all three import contracts kept (59 files, 127 dependencies).
- All 115 Python files compile in memory without bytecode writes.
- Cached build produces wheel/sdist; 76 wheel checksums pass. All 59 source modules and maintenance
  guidance match wheel bytes; all test Python files match the sdist.
- Mycelium 0.4.5 exports one nonempty diagram with 80 boxes and twelve existing external-base
  warnings. Tests are excluded: 3,914 calls and 65 type relationships filtered. Repeat export is
  byte-identical; overview/ADRs are checked against source. Mermaid was checked as text.

Logs use `/tmp/factory-status-final-candidate-` with suffixes `lint.log`, `imports.log`,
`compile.log`, `build.log`, `package.log`, `package-coverage.log` and `map-check.log`.
Map analysis/export logs: `/tmp/factory-status-final-map-{analyze,export,repeat}.log`.
No dependency, scanner, gate, exclusion, rule or live configuration changed. Protected external
`FACTORY.md` and `plans/slice-7.md` remain untouched. Parent completed the fresh actual scan below;
historical `4d777...` gate success is not evidence for this candidate. Source remains frozen.
Correction mapping and exact source/test references:
`/tmp/factory-status-policy-final-handoff.md`.

Scratch evidence correction: the historical `/tmp/factory-status-final-source-check.log` was
accidentally overwritten during this handoff. Its original text is not retained at that path;
the historical source manifest/archive and scan JSON/logs remain intact. Current source verification
uses the distinct `/tmp/factory-status-policy-final-source-check.log`.

### Fresh actual parent SQ on the final source

Analysis `8aad91c4-ff23-48f2-9eca-c327fa5368cf`, dated `2026-10-31T00:15:49+0000`, completed under
CE task `bdc0dc9d-8fa9-440a-bcc9-17fd89ad4df0` with status `SUCCESS`. The assigned gate
`Sonar way sans code coverage` is `OK`: zero unresolved issues, bugs, vulnerabilities, code smells,
hotspots and new violations; duplication and new duplication are 0.0%. No coverage was imported:
Coverage/new coverage are 0.0. Separate `caycStatus` remains `non-compliant`; this is not a gate
failure.

The latest server analysis/build string is verified as
`watch-status-caec97d7630235d4fdc9a9c6aaf305960a4efffacc955f338a06bb9a1faf68cb`.
Revision is base HEAD `afff583d0b67c861061cbddd49bd987d13bceee3`; the manifest binds the dirty
source. All 131 hashes match before/after scan. Seven changed Python server sources match local
bytes apart from terminal-newline normalization. Actual results/inspection:
`/tmp/factory-status-policy-sq-results-final.json`,
`/tmp/factory-status-policy-sq-verification.log`; scanner log:
`/tmp/factory-status-policy-sq-scan-1.log`. Source checks:
`/tmp/factory-status-policy-prescan-hashes.log` and
`/tmp/factory-status-policy-postscan-hashes.log`.

Parent reused the audited official portable CLI 8.3.0.16463 under `/tmp`, rechecking archive hash
`565c5040aa77d35da4e1d64c48184174f3e7444ad6a99f23335a39223587bb56`.
The actual repository `.sonarqube/start-scan.sh` is unchanged. Metadata and working directory were
passed through `SONAR_SCANNER_OPTS`, with no global PATH, dependency, scanner config, gate,
exclusion or rule change. Parent read envault before credential commands and used secret names
`sonar-token` and `sonar-host-url` only. Persisted results redact host/token. This implementation
agent did not scan or access credentials. No new review, commit, push or live change was performed.

Optional-startup tests use real 0755 pre-listener directory refusal and 0500 post-bind publication
failure. No direct `/proc` identity, bind or thread-start fault was forced. The optional try covers
constructor/entry failures, but exhaustive OS-fault behavior is not claimed. No health monitoring
or additional fault-injection API was introduced. All nine findings are addressed. Parent verified
all 131 source hashes and the matching SQ analysis before the authorized commit and push; this is
not deployment. The handoff's documentation manifest, before this verification note, is
`/tmp/factory-status-evidence-final-docs.sha256`.
