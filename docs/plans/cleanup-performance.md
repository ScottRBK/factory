# Factory-only completed cleanup performance

Status: implemented and locally validated after the sole independent Opus review. Final SQ has
zero findings; the isolated unchanged-CLI/backend trial passed. Wider tests retain one known
baseline wording failure. This work made no live DinoLand operation, Forgetful code edit,
dependency graph/version change, commit or push.
See the [decision](../adrs/completed-plan-cleanup.md) and [architecture](../architecture.md).

## Approved scope and implementation

The public watcher CLI is the approved test seam. Tests use actual disposable repositories,
registered worktrees and local bare remotes through the existing disposable SSH bridge. GitHub and
Forgetful CLI replies are controlled externally. There are no private workflow tests or API backend
changes. Native completed status remains the sole disposal permission; all existing exact mapping,
Git identity, cross-plan claim, target/default, receipt and cancellation checks remain in place.

`CleanupCompleted.poll` retains the full plans and complete task snapshots only for that cleanup
cycle. Candidate ownership validation and claim indexing share those tasks. The ordinary planning
adapter stays unchanged. `FactoryRecords.ownership_records` extracts the existing validation so the
cleanup workflow can supply its complete discovery records; `ownership` still reads fresh tasks.
Each disposal calls that fresh path for the selected plan and rereads its plan record, including
siblings in the same batch. Foreign ownership claims stay at the discovery snapshot across the
batch. Repository remote defaults are read on first use each cycle and shared across its sets.
Fresh selected owner/tasks/plan checks do not imply refreshing those foreign claims or defaults.
Incomplete or failed discovery blocks all disposal. Unknown fresh ownership/status stops the rest
of the batch; safe intake still has its turn. No snapshots cross polls or enter generic recovery.

A fixed three-set bound replaces one attempt per poll. The sorted rotation starts after the cursor,
wraps once, and selects at most three distinct pending sets. Advance the cursor before each attempt,
including failures. Ordinary per-set Git failures permit siblings; failed fresh reads and failed
receipt persistence stop the remaining batch. Earlier durable receipts remain terminal across
polls/restarts. Receipt-backed sets are excluded before claims/Git work and cannot regain authority
through new human resources using the same names.

Parallel CLI reads were investigated and not adopted. Existing `run_owned` cancellation owns one
process group on the main thread. Python signal handling and the watch ContextVar do not propagate
that cancellation automatically to worker threads. Safely coordinating/reaping several groups would
expand lifecycle machinery. This change preserves serial reads and the existing Forgetful CLI as
sole transport. No HTTP/MCP transport, `include_descriptions`, new configuration or dependency
exists.
Cached Context7 returned official CPython signal/subprocess documentation; no CLI upgrade ran.

For one selected completed plan, public CLI observations reduce discovery plus pre-disposal task
inventories from three to two, while retaining the fresh full read. With 36 tasks that avoids one
query plus 36 full-task processes per cycle. A three-set batch also amortizes the user-wide claim
index and eliminates two intervening poll sleeps. These are process-count observations and expected
savings, not measured real-backend latency or a promise about issue-intake elapsed time. Inventory
and per-command timeouts are unchanged; the batch bounds attempts rather than wall-clock duration.

## Test-first evidence

- `snapshot-red.log`: the public test expected two task inventories; unchanged production made
  three. `snapshot-green.log`: passed after cycle-local reuse, with both tasks read fresh again.
- `batch-red.log`: expected three distinct remote deletion attempts before the first provider turn;
  unchanged scheduling made one. `batch-green.log`: four snapshot/scheduling tests passed after
  batching and updating the previous one-set expectations. An initial GREEN attempt exceeded the
  test fixture's five-second wait while doing more native Git work; the new multi-cycle batch test
  now has a 15-second observation bound. Production deadlines were not changed.
- `receipt-stop-red.log`: a failed first receipt allowed the sibling to be deleted. The minimal
  correction stops the batch on receipt failure; `receipt-stop-green.log` passes.
- Safety checks cover incomplete inventories, malformed/failed full reads, fresh native status,
  changed associations/mappings after the first receipt, and a one-off fresh read failure that must
  leave later sets untouched. Five failing sets show bounded rotation and actual new-issue intake.
- Two cancellation cases stop during the fresh cleanup `get_task`, after discovery. A stubborn CLI
  transfers its own live pidfd; one SIGINT/SIGTERM yields exit 130, reaps that child, closes owned
  Foreman and preserves every resource. Existing receipt/restart and owned stop suites pass;
  native borrowed/managed lifecycle execution is limited by the tmux fixture failures below.
  No process scans or live factory controls are involved.

The controlled planning fixture holds its existing flock across call logging, counters and reply
selection and replaces state atomically. Occurrence-based faults run inside that lock. Test-side
state resets happen only with watch stopped. The deletion log appends each complete JSON record in
one `os.write`; first-provider socket gates prevent next-cycle read-count races.

The broad run exposed an existing GitHub fixture race: help/comments wrote the shared state by
truncation while `polls()` read it without the writer's lock. The observed empty-file JSON decode
error is in `broad.log`. The shared fixture now uses atomic replacement for those writes, matching
its poll update. This is a test-fixture correction, with no production or GitHub transport change.
The affected public intake test passed separately before the correction; final watcher/alert and
new cleanup tests exercise the corrected fixture.

## Commands and results

All scratch artifacts and test temporary directories are beneath
`/tmp/factory-cleanup-perf.XJ5htJ`. Commands use existing cached tools without synchronization,
installation or upgrades. Logs in that directory retain complete output.

```bash
export TMPDIR=/tmp/factory-cleanup-perf.XJ5htJ
export PYTHONDONTWRITEBYTECODE=1
export UV_PROJECT_ENVIRONMENT=/home/scott/.cache/uv/archive-v0/_9Pvk6v2zG3ZkCMG
export PYTHONPATH=src:tests
uv run --offline --no-sync python -m unittest test_cleanup_performance.CleanupSnapshotTests -v
uv run --offline --no-sync python -m unittest test_cleanup_performance.CleanupBatchTests -v
uv run --offline --no-sync python -m unittest \
  test_cleanup_performance.CleanupBatchTests.\
test_failed_receipt_storage_stops_the_remaining_batch -v
uv run --offline --no-sync python -m unittest test_cleanup_performance.CleanupCancellationTests -v
uv run --offline --no-sync python -m unittest \
  test_cleanup_performance test_cleanup_scheduling test_cleanup_receipts test_cleanup_review \
  test_completed_cleanup test_completed_cleanup_recovery test_cleanup_recovery \
  test_cleanup_boundaries test_watch_stop test_watcher_cancellation test_planning_watch -v
export NATIVE_PI_SDK=/home/scott/.pi/agent/install/releases/1.5.0/node_modules/\
@earendil-works/pi-coding-agent/dist/index.js
uv run --offline --no-sync python -m unittest discover -s tests -v
uv run --offline --no-sync python -m unittest \
  test_cleanup_performance test_watch test_watcher_alerts -v
/home/scott/.cache/uv/archive-v0/l3aQPynxEjP4xQFa/bin/ruff check \
  --cache-dir "$TMPDIR/ruff-cache" src tests
git diff --check
```

Validation results:

- Initial focused run: 110 tests, one failure caused by the old final-read fault fixture injecting
  at read three. Discovery reuse moves the fresh read to read two. Updated only that external fault
  timing; the targeted check passes (`final-read-fixture-green.log`).
- Final focused run: all 110 tests pass in 176.872 seconds (`focused-final.log`).
- Broad unfiltered run: 648 tests in 510.307 seconds; 585 pass, 59 fail, one error, three skips.
  Fifty failures stop in setup because native fixtures search `/usr/bin:/bin` for tmux while this
  host uses Nix. Seven require the unavailable `lint-imports` executable. One is the known
  `auto_approve false` versus `auto_approve=false` wording assertion. One is the obsolete final-read
  fault fixture fixed above. The error is the shared GitHub fixture read/write race fixed above.
  The three skips are explicitly Ubuntu-only tmux installation recipes. No exclusions or runtime
  changes were applied to that command. Native managed/borrowed execution is not claimed GREEN.
- The broad command started before the final test strengthening and fixture corrections; production
  source remained unchanged. Final focused/affected runs verify those test changes separately.
- An initial atomic-write helper moved an existing poll-delay insertion point and failed one of
  85 affected tests (`atomic-fixture-final.log`). The correction retains the original poll write
  and its delay hook, with atomic help/comment writes. No watcher production code changed.
- Final affected run: all 85 tests pass in 121.595 seconds (`atomic-fixture-green.log`), covering
  all ten new cleanup tests and both existing watcher/alert modules with the final fixture.
- Ruff over all source/tests and `git diff --check` pass. Widths, local document links, protected
  inputs and the map repeat check pass (`verification.log`, `ruff-final.log`).

Initial handoff source/test/resource manifest: `source.sha256`, 149 members, SHA256
`d7206bfca61a8567442eb873b7b9ab309b31c1fead7944dbda73232ca488fccc`.
This includes the preexisting approved prompt edits; the SQ correction manifest below supersedes it.

## Mycelium and preserved inputs

Reused the audited Mycelium 0.4.5 wheel and existing cached Click 8.1.8; no environment
or dependency installation. Initial help lacked Click on the test runtime path; explicitly adding
its cached path resolved that without modifying an environment. Its default exports full signatures
and relationship lists; this version has no `--detail` flag.

```bash
export PYTHONPATH=/home/scott/.cache/uv/archive-v0/wqd_0Wuk9G26z5MV:\
/home/scott/.cache/uv/archive-v0/Kb1KTQ-oI7XgaP3C
uv run --offline --no-sync python -m mycelium.cli analyze . -o "$TMPDIR/map.json" --quiet
uv run --offline --no-sync python -m mycelium.cli export "$TMPDIR/map.json" \
  -o "$TMPDIR/map.md" --max-classes 1000 --test-path tests
uv run --offline --no-sync python -m mycelium.cli export "$TMPDIR/map.json" \
  -o "$TMPDIR/map-repeat.md" --max-classes 1000 --test-path tests
cmp "$TMPDIR/map.md" "$TMPDIR/map-repeat.md"
```

The map includes 92 boxes in one class diagram. Its 13 unresolved external-base warnings remain;
known heuristic call-edge limitations and excluded archives remain documented in the overview.
Repeat exports match. Mermaid is checked as text, not rendered. The overview retains 499 lines and
separates implementation from unproven live behaviour.

Protected `FACTORY.md` remains SHA256
`ad342980f162cc61146ddaffa15267fcc2908ccefff847a362bfba0bf07ebf28`.
The existing pending plan, onboarding, Foreman and review prompt changes were copied before work.
Only the cleanup progress insertion extends `docs/plan.md`; the other three inputs remain byte
identical to those copies. `preexisting.diff` records their initial worktree changes.

Owned root: `/tmp/factory-cleanup-perf.XJ5htJ`, including baseline copies, logs, cached-tool
outputs, map JSON/exports, Ruff cache and source/resource inventories. Disposable test workspaces,
Git refs/worktrees/bare remotes and private sockets live under that root and use fixture teardown.
No worktree/branch was created in the actual repository and no external tracking resource exists.
All test workspaces are now removed and their owned child handles closed. Retained directories are
`jiti/` (SDK compilation cache) and `ruff-cache/`; `resource-list.txt` inventories retained files.
No pending design conflict remains within the serial-CLI implementation. Parallel reads remain a
separate lifecycle expansion; optimized latency and live behaviour await the final trial.

## First parent SQ and approved GREEN refactor

The parent analysis completed successfully but its quality gate failed with three new code smells:
analysis `ddeb668d-4da8-4cbb-bbb1-9237664510aa`, CE task
`2ae1100a-ca6d-4422-9bb2-397220aedb14`. Evidence is retained at
`/tmp/factory-cleanup-speed-parent.TQKs6H/initial-results.json` and `initial-scan.log` beside it.
Gate new violations: 3 against threshold 0; new duplication: 0.0%, passing its 3% threshold.

- `python:S3776`: cleanup `poll`, cognitive complexity 20 against limit 15 at scanned line 46.
  Extracted complete resource-claim/duplicate-reference index construction into `_claim_indexes`.
  Failure still returns no index before disposal; serial external reads, snapshots, batch rotation,
  alerts and fresh pre-disposal checks retain their existing order and semantics.
- `python:S5899`: `calls` test accessor at scanned line 54, reported as unused. Removed the accessor
  and inlined both call-log reads; no renaming/suppression or regression removal.
- `python:S3776`: GitHub `list_issues`, complexity 16 against limit 15 at scanned line 72.
  This predates cleanup and came from the notification fix. The approved minimal refactor extracts
  validated issue conversion into `_issue`. Issue validation/eligibility still precedes conversion;
  all eligible comment reads and validations finish before the result tuple returns. Endpoints,
  pagination, normalization, revisions, ordering and failure/retry behaviour are unchanged.

This is the authorized GREEN refactor after the parent's SQ RED. Existing public tests were run
before and after; no new private-method tests, transport, cache, dependency or baseline wording fix
was introduced. This handoff preceded the parent's passing pre-review scan and sole Opus review,
recorded below; this worker launched neither.

Evidence owned by this worker is retained under `/tmp/factory-cleanup-perf.XJ5htJ/sq-fixes/`.
Commands use the existing runtime and a scratch-local UV cache because this resumed turn has a
restricted filesystem/socket sandbox. No installation or synchronization occurred:

```bash
export TMPDIR=/tmp/factory-cleanup-perf.XJ5htJ
export UV_CACHE_DIR="$TMPDIR/sq-fixes/uv-cache"
export PYTHONDONTWRITEBYTECODE=1
export UV_PROJECT_ENVIRONMENT=/home/scott/.cache/uv/archive-v0/_9Pvk6v2zG3ZkCMG
export PYTHONPATH=src:tests
uv run --offline --no-sync python -m unittest \
  test_cleanup_performance test_cleanup_scheduling test_cleanup_receipts test_cleanup_review \
  test_watch_stop test_github_issue_changes test_watch_issue_changes -v
uv run --offline --no-sync python -m unittest \
  test_github_issue_changes test_cleanup_boundaries test_planning_adapter -v
/home/scott/.cache/uv/archive-v0/l3aQPynxEjP4xQFa/bin/ruff check \
  --cache-dir "$TMPDIR/sq-fixes/ruff-cache" src tests
git diff --check
```

The first command ran unchanged before and after (`before.log`, `after.log`): each ran 46 tests,
with all three public GitHub adapter tests passing and 43 fixture-setup errors at Unix socket bind
(`PermissionError: [Errno 1] Operation not permitted`). No watcher test body executed in those 43
cases. The parent's unrestricted focused rerun was pending then. The second command passes all
17 public adapter/Git tests in 1.979 seconds (`adapter-checks.log`). Ruff and diff checks pass.
No full unfiltered suite or parent script was run by this worker for this correction.

The refreshed Mycelium map still contains one full-detail diagram with 92 boxes and 13 external-base
warnings. Test filtering now excludes 4995 calls and 81 type relationships. Repeat exports match;
Mermaid is checked as text. The same cached exporter/options were used, with outputs in `sq-fixes/`.
The overview remains 499 lines; source pointers and cleanup/watcher ADRs reflect the extraction.
The new source manifest and final document/resource verification are recorded at handoff below.

### Parent baseline trial evidence

The parent baseline, before the final optimized trial, passed using the unchanged installed CLI,
an isolated local HTTP/SQLite backend and disposable real Git resources. Its own result is
`/tmp/factory-cleanup-speed-parent.TQKs6H/baseline-trial-3/result.json`:
three completed sets disposed in 112.445 seconds; 49 `get_task` calls and 79 total CLI calls
(1 project access, 1 tool catalog, 5 plan inventories, 10 full plans, 13 task inventories,
49 tasks).
Active resources/main were preserved; three receipts protected recreated dirty resources on restart.
Issue polling continued and one SIGINT exited 130. The parent reports the disposable workspace
removed and server stopped. This is baseline evidence, not a final optimized latency result or live
DinoLand adoption. This worker only read that result; parent scripts and resources were untouched.

### SQ correction handoff

Replacement source/test/resource manifest: `sq-fixes/source.sha256`, 149 members, SHA256
`e3202c4fdcb00df3cfb74183ee62f23eda2f1ccef0bf1ebb667626233645240d`.
Protected intent and pending onboarding/Foreman/review bytes still match the original copies;
the pending main plan remains preserved around the cleanup progress insertion. Final widths,
local links, 499-line overview, expected map source areas, 13 warnings and repeat export pass
(`sq-fixes/verification.log`). Ruff and diff checks pass. This identifies the pre-review snapshot;
the review-correction manifest below supersedes it.

That handoff requested the exact 46-case rerun, next SQ analysis, sole Opus review and final trial.
Later parent/reviewer results follow below. The sandbox failures establish no watcher regression
result; the earlier 110/85 passes cover the previous source snapshot only. All prior evidence is
retained. Additional owned resources are `sq-fixes/` logs, verification script, manifest, full map
and repeat export, `uv-cache/` and `ruff-cache/`; no server, Git worktree or long-lived child was
created here. `sq-fixes/resource-list.txt` lists retained files. Nothing was cleaned up.

## Sole Opus review and narrow corrections

The pre-review parent scan passed after the three initial smells were corrected: analysis
`b3e1f752-26be-43b6-b996-41cb35ca8274`, CE `e44682a8-5a1b-4c06-86a2-f7b15eaa4114`.
`pre-review-results.json` under `/tmp/factory-cleanup-speed-parent.TQKs6H/` reports gate OK,
zero issues/hotspots and 0.0% new duplication. No coverage was imported; the separately returned
`caycStatus` is `non-compliant`. The gate pass is not a coverage or final-source claim.

The ONE independent Opus review completed in session
`32b51615-4bed-4a77-8582-7e6ffa2130df`, requesting tests/docs changes with no production safety or
requirements defect. Its 139 focused tests passed in 227.681 seconds (`/tmp/opus-review.IrnSs8/`).
The parent SQ-refactor group had 31 passes and one scheduling timing failure among 32 tests;
`/tmp/factory-cleanup-speed-parent.TQKs6H/sq-fix-parent-tests.log` retains that failure. Opus timing
reproductions measured candidate cases at 3.56–4.57 seconds versus baseline 3.26–3.54 seconds.
The measured failure is the RED evidence for correcting test observation; no production deadline
or new test seam was needed. No reviewer was launched or resumed for these fixes.

- F1: both scheduling cases now wait for three complete deletion-attempt log records and healthy
  remote-ref absence, with a 15-second observation timeout. The first log now records deletion
  pushes, rather than default lookups. Only newline-terminated JSON records are read while the
  watcher runs, ignoring a trailing incomplete record until a later read. Assertions retain the
  first-three attempt order, cycle sequence `0, 0, 1`, per-cycle distinctness and the three-set cap,
  as well as healthy disposal and the denied remote's preservation. Names/comments describe
  same-batch progress and next-cycle retry. The existing five-set performance case establishes
  fair rotation beyond the batch limit; these two-set cases do not make that broader claim.
- F2: ADR/overview wording now states that discovery snapshots foreign ownership claims across the
  batch. Each selected owner/tasks/plan is read fresh; foreign claims are not refreshed per set.
  A repository's first required remote-default lookup in a cycle caches success/failure for later
  sets in that cycle. Lookup is lazy during disposal; it is not an eager cycle-start read.
  Existing non-atomic race limits remain. No lookup or authority behaviour changed.
- F3: assigned `self.cursor = key` explicitly at the start of the loop body, before disposal.
  This preserves failure/cancellation order and makes cursor advancement visible. The existing
  cycle-local task dictionary remains explicit, shared only by candidate discovery and indexing.
  New `_candidates` return-tuple plumbing or abstractions would add no needed behaviour or clarity,
  so that optional dataflow nit was left as documented local mutation.
- F4: current status distinguishes the failed initial scan, passed pre-review scan, completed sole
  review, these corrections, and the pending final parent validation/SQ/optimized backend trial.

The parent audited cached RECORD contents and locked versions for nine existing dependencies and
installed them offline only into its owned temporary test environment
`/tmp/factory-cleanup-speed-parent.TQKs6H/test-env-312`. No dependency graph or version changed;
this worker performed no installs. The parent's new environment has Import Linter. Its current
source run kept three contracts over 65 files/159 dependencies. The worker's earlier missing-tool
failures remain historical evidence for the previous cache, not an ongoing parent limitation.

### Final correction checks

All new worker outputs are under `/tmp/factory-cleanup-perf.XJ5htJ/review-fixes/`; prior logs and
manifests remain intact. The parent's environment is reused read-only with `--offline --no-sync`,
and cached Ruff remains separate. Commands:

```bash
export TMPDIR=/tmp/factory-cleanup-perf.XJ5htJ
export UV_CACHE_DIR="$TMPDIR/review-fixes/uv-cache"
export PYTHONDONTWRITEBYTECODE=1
export UV_PROJECT_ENVIRONMENT=/tmp/factory-cleanup-speed-parent.TQKs6H/test-env-312
export PYTHONPATH=src:tests
uv run --offline --no-sync python -m unittest test_cleanup_scheduling -v
uv run --offline --no-sync python -m unittest \
  test_cleanup_scheduling test_cleanup_performance -v
uv run --offline --no-sync python -m unittest \
  test_cleanup_performance test_cleanup_scheduling test_cleanup_receipts test_cleanup_review \
  test_watch_stop test_github_issue_changes test_watch_issue_changes test_cleanup_boundaries \
  test_planning_adapter -v
uv run --offline --no-sync python -m unittest test_architecture -v
"$UV_PROJECT_ENVIRONMENT/bin/lint-imports" --config pyproject.toml --no-cache --no-logo
/home/scott/.cache/uv/archive-v0/l3aQPynxEjP4xQFa/bin/ruff check \
  --cache-dir "$TMPDIR/review-fixes/ruff-cache" src tests
git diff --check
```

The before scheduling run stopped in socket setup for both cases (`scheduling-before.log`).
The after scheduling/performance run stopped in socket setup for all 12 cases
(`scheduling-performance.log`). The affected group ran 60 tests: 17 passed, 43 stopped in fixture
setup (`affected-group.log`, 1.861 seconds). Each blocked case has Unix socket bind
`PermissionError: [Errno 1] Operation not permitted`; no blocked test body executed. Parent's
unrestricted rerun remains necessary, without treating these errors as product failures or passes.

All seven architecture tests pass (`architecture-tests.log`, 9.721 seconds). Actual source import
checks also keep all three contracts, 65 files/159 dependencies (`imports.log`). Ruff and diff
checks pass. No unfiltered full suite, new scan, further review or real-backend trial ran here.
Final manifest/map/document verification and retained resource paths follow below.

### Final review-fix handoff

Final source/test/resource manifest: `review-fixes/source.sha256`, 149 members, SHA256
`14211db6664433e18d5194d4d8ea6590a3fbf5f4de834fc00ddccda0fe009241`.
Protected `FACTORY.md` and the three pending onboarding/Foreman/review files remain byte-identical
against the original copies. The preexisting main-plan changes remain intact around the cleanup
progress insertion. No source changed after this manifest; later changes were progress text only.

The cached Mycelium 0.4.5 refresh has 92 boxes, one full-detail diagram, 4998 filtered test calls,
81 filtered type relationships and 13 unchanged external-base warnings. Same-map repeat exports
match byte-for-byte. The 499-line overview, local document links and 100-column checks pass;
Mermaid was checked as text. All maps/scripts/logs remain in `review-fixes/`.

Owned resource paths retained until the parent finishes:

- `/tmp/factory-cleanup-perf.XJ5htJ/`: initial evidence, baseline copies and manifest.
- `/tmp/factory-cleanup-perf.XJ5htJ/sq-fixes/`: SQ-refactor evidence and prior manifest.
- `/tmp/factory-cleanup-perf.XJ5htJ/review-fixes/`: this correction's evidence, map, verification
  script, manifest and `resource-list.txt`; includes `uv-cache/` and `ruff-cache/`.
- `/tmp/factory-cleanup-perf.XJ5htJ/jiti/` and `ruff-cache/`: earlier retained tool caches.

Parent-owned `/tmp/factory-cleanup-speed-parent.TQKs6H/` and reviewer-owned
`/tmp/opus-review.IrnSs8/` were read only; their scripts/resources were untouched. No worker
worktree, server, external tracking resource or long-lived process was created for these fixes.
No evidence cleanup, new review, final SQ scan or optimized trial was launched. The parent owns
final unrestricted tests, adapted native checks, SQ and the real-backend trial.


## Final parent validation and cleanup

This section supersedes earlier pending handoffs above. The parent accepted the implementation's
review fixes after checking the final tests and scan, without another independent review pass.
The source/test/resource manifest remains 149 files, SHA256
`14211db6664433e18d5194d4d8ea6590a3fbf5f4de834fc00ddccda0fe009241`.
Only progress/architecture-status prose changed after this frozen source snapshot.

### Final scan

- Analysis: `cb9cb08a-62bf-4f54-915e-d05d6aefdbc8`.
- CE task: `919fd5ba-47ba-4e9a-b01b-0ab348966ede`, status `SUCCESS`.
- Assigned quality gate: `OK`; zero unresolved issues and security hotspots, bugs,
  vulnerabilities or code smells; duplication 0.0%.
- No coverage report was imported. The separate `caycStatus` remains `non-compliant`;
  passing this assigned gate does not establish coverage compliance.
- The parent checked the latest analysis identity and matched Sonar's stored source for all
  three changed production Python files against local source, allowing only final newline
  normalization. Scanner SCM metadata still names base commit `909aef0`; the scan covers the
  uncommitted working tree identified by the manifest, not a new commit.

SonarScanner CLI 8.3.0.16463 was downloaded from its official HTTPS distribution URL into the owned
temporary directory. Its SHA256 matched the previously audited artifact:
`565c5040aa77d35da4e1d64c48184174f3e7444ad6a99f23335a39223587bb56`.
Archive paths were checked before extraction. No global scanner or dependency upgrade occurred.
Context7 confirmed project settings, CLI operation and isolated environment options.

### Final automated checks

- Python 3.12: 648 tests discovered; 598 selected, **594 passed**, one known baseline failure,
  three platform skips. The 50 native lifecycle cases were explicitly selected separately.
  The remaining failure is `test_review_regressions.py:396`, which expects
  `auto_approve false` while unchanged guidance says `auto_approve=false`.
- All new cleanup tests and the reviewed scheduling corrections pass in that run, as do the
  architecture proofs and native SDK resource/worker checks. The three skips concern the
  Ubuntu 24.04-only package-installation recipe.
- An earlier parent run of the same 598 tests had one additional failure: the parent's long
  temporary directory exceeded a control-socket path limit. Repeating the complete selection
  with short owned `TMPDIR=/tmp/fcs.wuYQM2/full` removed that environment failure. No production
  code or test assertion was changed to make it pass.
- Native lifecycle: **50 passed**, no skips, in a private source copy. Only two fixture path
  settings were adapted to find this host's existing Nix tmux. Production source was identical;
  canonical fixtures still search `/usr/bin:/bin`. This is host-adapted evidence, not a claim that
  the unmodified native fixtures run on this host.
- Python 3.13: **115 focused tests passed**, covering cleanup, scheduling, receipts, stop and
  cancellation, planning recovery and GitHub issue/comment changes. This was not a second full
  discovery run.
- Final source import checks kept all three contracts over 65 files and 159 dependencies.
  Ruff, whitespace, document links/widths, protected inputs and Mycelium repeat-export checks pass.
  The overview remains 499 lines. No hosted CI or package release was run.

The parent used temporary environments containing existing locked dependency versions only.
Cached package RECORD digests were checked before offline, no-build reuse. Ruff used the existing
audited executable separately. No dependency declaration, lockfile or shared environment changed.

### Isolated unchanged-CLI/backend trial

Both baseline and final trials used the installed Forgetful 0.5.5 CLI without modifying it.
Each trial started its own loopback HTTP server and SQLite database with an isolated home,
no authentication credentials and no model calls. Every planning operation went through the CLI.
Git repositories, registered worktrees, local branches and bare remotes were real and disposable.
GitHub replies and the Foreman terminal were controlled; no live model compliance is claimed.

The real watcher first scaffolded two issues. One plan received three mapped worktrees and four
ordinary tasks; it was moved through the native draft-to-active-to-completed transitions.
The other plan remained active. The watcher ran with a 0.05-second test interval in both trials,
so this comparison largely excludes the additional savings from avoiding normal 30-second waits.

- Baseline `909aef0`: three sets confirmed in **112.445 seconds**, **79 CLI calls**, including
  **49 full-task reads**.
- Final source: the same scenario completed in **50.455 seconds**, **39 CLI calls**, including
  **22 full-task reads**.
- This one local comparison took **55.1% less time**. It is not a general latency guarantee.
  Calls counted include startup and intake/recovery work through the cleanup observation.
- Both trials confirmed absence of all three completed worktrees and their local/remote refs,
  retained the active plan's worktree and both refs, preserved the main checkout branch and HEAD,
  saved three durable receipts, continued issue polling and retained completed plan status.
- After recreating one confirmed name with a dirty file and local/remote branch, restarting the
  watcher preserved that human reuse and left its receipts unchanged.
- A single SIGINT stopped each watcher with exit 130. Each isolated server was stopped and waited
  for, and each entire disposable workspace was confirmed absent.

Two preliminary baseline setup attempts failed before cleanup: the first accidentally selected a
test-managed executable without a runtime receipt; the second attempted draft-to-completed
directly. Correcting only the disposable harness to use its external CLI executable and valid
native transitions produced the baseline above. Their test servers and workspaces were removed.

### Retained result and temporary-resource disposal

The maintained regression tests and this result record stay in the repository. Raw worker,
reviewer and parent logs, temporary scripts, source exports, scanner/JRE/cache, disposable package
environments and private native-test copies are temporary artifacts, not product files.

Owned temporary roots are `/tmp/factory-cleanup-perf.XJ5htJ`,
`/tmp/factory-cleanup-speed-parent.TQKs6H`, `/tmp/opus-review.IrnSs8` and
`/tmp/fcs.wuYQM2`. All four roots were removed and their absence was confirmed after validation.
Earlier paths and commands above describe historical evidence locations; raw artifacts are gone.
No test branch or worktree was created in the actual Factory repository. This work did not modify
Forgetful's source, stop/restart DinoLand, install this candidate there, commit or push.
