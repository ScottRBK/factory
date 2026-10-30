# Foreman Forgetful integration

## Status

Implemented for authorized internal use: Factory's configured server/project, Foreman-only loading,
automatic-memory opt-in/model controls, and planning with memory off. Full source checks, SonarQube
scans and actual Claude Code review through AgentShell are complete. The CLI and extension keep
their own authentication for now. See the [decision record](../adrs/foreman-memory.md).

Scott has now chosen server-only extension support first, with CLI/local support as a later slice.
This replaces the earlier proposal to block runtime integration on local/server parity and a
bundle of native CLI changes. The extension's current HTTP path is the starting point for the
server slice. The evidence below separates completed aggregate validation from earlier
configuration-only results. No live installation or automatic-memory enablement was performed.

Earlier configuration-only evidence:

- Source and dependency audits identified the incompatible managed Pi version, vulnerable inherited
  HTTP dependency, unbounded capture source reads and missing managed CLI composition contracts.
- The exact Pi 1.4.0 candidate with Undici overridden to 8.12.2 has conditional pre-install audit
  approval. Unrelated npm lock entries and Forgetful requirements are unchanged. Disposable runtime
  validation passed: 119 archives and 15,012 installed files verified, CLI/SDK and inert-extension
  checks passed, and five native Factory checks passed per Python. No adoption or global upgrade.
- The first TDD slice adds setup flags/prompts, exact native model selection and one-time scoped
  preferences. Seven new public tests plus three adjacent checks passed on Python 3.12.3/3.13.5,
  10 tests each, no skips, in 5.127s/4.468s. CLI-flag and missing-prompt reds are retained.
  Manual input was piped, not a real terminal; assisted default-off used controlled tmux.
- A preliminary shared SonarQube scan failed on one memory-validator complexity finding. After
  extracting that validation without changing behavior, a combined immutable snapshot passed 25
  focused setup/guidance/native checks per Python, no skips, in 10.326s/10.567s. A test assertion
  then received a formatting-only line wrap; final-byte checks are being completed separately.
- Fresh analysis `be3a4abd-3889-4cca-ac34-720d877173ae` completed successfully: assigned gate OK,
  zero unresolved issues and zero bugs/vulnerabilities/smells/hotspots, with 0.0% duplication.
  Gate/profile settings were unchanged; separate `caycStatus` remains non-compliant. This is a
  Factory source/test scan, not analysis of a future bundled TypeScript extension.
- Ruff and all three import contracts passed. The full-detail Mycelium map was refreshed and its
  repeated export matched; Mermaid was checked as text, not rendered.
- The final-byte phase-1 snapshot passed 25 focused checks on each Python, no skips, in
  10.381s/10.080s. An offline wheel/sdist build passed 72 RECORD checks and 69 source/resource byte
  comparisons. New and preserved tests are included. The delivered wheel was not replaced.
- Actual Claude Code Opus 5.5 approved that configuration/guidance snapshot, conditional on fixing
  misleading CLI wording before separate delivery. It independently ran the ten new tests on both
  Pythons, 19 adjacent manual-route tests and nine public CLI probes. An earlier AgentShell launch
  failed on unsupported Claude resource controls; that failed launch is not review evidence.
- The wording fix has two genuine public CLI reds, then greens: help and opt-in confirmation now
  say runtime memory is not yet active. The preference read-back reuses the protected JSON reader;
  a public file-safety characterization passes both before and after that change. Wildcard wording
  now says the exact `*` entry. Sequential full suites pass 491 tests per Python without skips:
  598.162s on 3.12.3 and 594.287s on 3.13.5. Exact unique test IDs match; all source hashes remain
  unchanged. Both runs forced 55 checked-hash source caches and used the privately audited Pi SDK.
  Only the owned runner's prerequisite path changed; canonical test tools remain untouched.
- Fresh post-review-fix analysis `22593daf-9dd3-4ae5-b2c2-18fa2bd8eeaa` passes the assigned gate
  with zero unresolved issues and 0.0% duplication. Separate `caycStatus` remains non-compliant.
  These results do not establish live memory integration or resolve the earlier shutdown mystery.
- The final offline wheel/sdist again passed 72 RECORD checks and 69 source/resource comparisons.
  No package was installed or delivered. Ruff, three import contracts and 100-column checks pass.
- A native Claude follow-up passed all 12 new tests on each Python and inspected five public CLI
  probes, but reached its 50-turn limit without a verdict. That run is not counted as approval.
  A separate actual Claude Code Opus 5.5 text-only closure reviewed the supplied exact source and
  evidence, closed M1/L1/L2/N1/N2 and approved this slice with no remaining blocker. It did not
  rerun tools/tests. All 159 frozen files remained unchanged. Optional suggestions remain optional.
- The earlier request for broad upstream CLI work is superseded by Scott's server-first decision.
  Running Forgetful instances and DinoLand remain untouched.

## Server connection investigation after implementation approval

Scott approved the action list, including asking before authentication changes. Read-only source
inspection found that Forgetful 0.5.5 already accepts the native OAuth token on REST: both paths
use the same server verifier. The current public CLI has no authenticated REST interface, while
the extension only supports a static bearer token or no authentication.

A native authenticated-request helper was proposed on the mistaken assumption that both clients
must share one login. Scott clarified that they keep their own authentication and that Forgetful
should not be changed now. The helper proposal is withdrawn; it is not an approval blocker.
The extension retains its existing HTTP transport and authentication. Revisit using the CLI as
its transport in the later slice, including local support and any authentication implications.

No production code, tests, dependencies, live state or credentials changed during this
investigation. The existing audit still blocks unchanged-extension enablement. Runtime tests,
new scans, packages and final integration review have not run; the earlier results remain scoped
to the configuration/guidance slice. Evidence is in the `server-runtime/` directory under the
existing temporary evidence root. Its report predates the separate-auth clarification: its source
findings remain evidence, but its shared-login recommendation is superseded. See the
[authentication decision](../adrs/foreman-memory.md).

## Runtime implementation and intermediate checks

The exact Pi 1.4.0 / Undici 8.12.2 lock passed independent promotion review for internal installer
use, following disposable validation and fresh advisory checks. The product installer now uses
that unchanged archive; Forgetful requirements are unchanged. No actual runtime was installed or
upgraded. Two public init regressions had genuine reds before the version/lock and experimental
Milo-parser fixes. Focused Python 3.12 checks passed 59 tests before the second fix, then five
checks including both new tests after it. The current focused Python 3.13 run passed all 60 checks
in 30.870s. These are not final full-suite or integration results.

Factory and extension changes are staged in isolated snapshots. The Factory corrections preserve
custom native CLI paths, edited/unselected roots, renamed/external definitions and existing resource
checks. Ten public compatibility/configuration tests passed sequentially on Python 3.12 and 3.13
in 3.675s and 3.322s. Protected watcher tests and the shared connection validator remain unchanged.
At this intermediate stage, the aggregate combined these changes with the parent's runtime-lock/
Milo fixes, but the main working tree and extension bundle had not yet been updated.

The separate validation-tooling audit approved an exact 77-package development closure before an
offline, scripts-disabled install of its 51 Linux-applicable packages. Esbuild and TSX ran without
install hooks. The original baseline `npm run check` passed architecture 23/23, typecheck and
970 tests, with 368 declared opt-in skips. No product lock or runtime dependency changed.

The changed extension then passed the original checks: architecture 23/23, typecheck, and 984
passed tests out of 1,352, with 368 opt-in skips. The 28 controlled terminal tests passed separately
using private tmux sockets and loopback-only services. The default-suite skips comprise 332 backend
opt-ins, those 28 terminal tests, two compaction-plugin opt-ins and six real-model opt-ins. They are
not all paid-model tests. The earlier loader failures, two type errors, temporary queue-loader
substitution and overly long tmux socket path remain separate evidence. The final queue test is
byte-identical to the original TSX version; no test file was excluded from the successful check.

Independent source review found a missing runtime case: Pi's `PI_PACKAGE_DIR` can redirect both
`getPackageDir()` and `VERSION`. Wrong-version/parser tests did not exercise that override, so their
green results did not prove the running host was checked. The native regression reproduced an
actual selected-project HTTP request under misleading metadata. Managed mode now rejects the
override before activity. The corrected immutable candidate again passed architecture 23/23,
typecheck, 984 default tests and all 28 controlled terminal tests. Mycelium was regenerated
with 278 boxes and no missing in-scope calls; repeat output matched, without rendered-Mermaid proof.

The explicit TypeScript analysis `aad2accd-e661-4df3-bbc0-39e137a311d2` completed successfully but
failed its assigned gate on ten new findings. It reported 59 unresolved issues, including the 49
baseline findings. Corrections are limited to the new findings; the scan, profile and gate are not
weakened. The exact-source audit was subsequently repeated for the v7 candidate below.

Capture URL policy is awaiting Scott's answer; a blanket removal has not been approved. The audit
separates this live-enablement question from inert internal inclusion. Current source preserves
URL inspection with hard bounds. Evidence is under `implementation/` in the temporary evidence
root. The aggregate checks described below supersede these intermediate results.

## Final extension candidate

The v7 candidate removes the unnecessary post-close pathname permission change. A public native Pi
panel regression first proved that the old code broadened a stricter creation mask from `0400` to
`0600`, then passed after removal. The ordinary owner-only save test remains. No private mocks,
native interception or new dependency was used. Earlier tests covered files already unsafe at
startup or before save; they did not exercise concurrent replacements during save.

Scott explicitly accepted the remaining local path-replacement limitation rather than adding
workspace containment work. Existing checks stay intact. The second audit finding is deferred,
not fixed; the documentation no longer claims complete containment during concurrent changes.
Earlier frozen candidates and failed delegated attempts remain recorded separately.

Exact v7 source passes the unchanged `npm run check`: architecture 23/23, typecheck, and 989 of
1,357 tests, with 368 declared opt-in skips and no failures. All 28 controlled terminal tests pass
separately without skips. The skipped backend, plugin and real-model checks retain their existing
opt-in boundaries; no live backend or paid-model validation is claimed. All 181 frozen files match
before and after. Fresh TypeScript analysis `7cc65e96-236f-4c53-810b-097b1bc528ef` passes the
assigned gate with zero new issues, 49 unchanged baseline findings and zero new duplication.

Independent exact-source approval accepted the revised scope, with the remaining local race
explicitly recorded. The internal bundle now includes all 40 approved runtime files and preserves
all 15 existing members. Twenty-one focused Factory/native resource checks pass without skips.
The earlier build-only wheel did not contain this extension. It remains separate historical
build evidence, not validation of the integrated plans wheel.

## Final aggregate validation

Actual Claude review through AgentShell found one incorrect test expectation: the new optional
extension was treated as mandatory. The first complete run reproduced that failure: 503 tests,
one failure and one skip on Python 3.12 in 638.007s; Python 3.13 was not started. The skip occurred
because network isolation mapped the test process to root, excluding a non-root installer case.
Those failures remain retained, not relabelled as successful validation.

The false optional-extension subcase was removed without weakening required guidance/AgentShell
checks. Existing positive unselected-root regressions remain. Focused selection had missed this
modified planning test; the corrected selection includes that whole module. The external runner
now configures loopback first, then preserves the actual non-root UID in a nested user namespace.
No product code, fixture, loader, assertion deadline or CI limit changed. Twelve focused tests,
including the previously skipped installer case, pass on both Pythons without skips.

The corrected immutable source passes all 503 tests sequentially, with zero skips: 638.017s on
Python 3.12.3 and 619.997s on Python 3.13.5. Unique inventories match; 160 source-file hashes and
the canonical runner stayed unchanged. Both runs forced 55 checked-hash source caches. No real
backend, model-provider product validation or personal credential access was used.

Final Python analysis `3d9b4457-dc06-40a4-a119-e8c1b5027ed5` passes its assigned gate with zero
unresolved findings and zero new duplication. The separate `caycStatus` remains non-compliant;
no gate/profile settings were changed. The TypeScript result above retains 49 baseline findings.

Actual Claude closure through AgentShell approved B1 and the documentation correction, conditional
on the remaining parent gates. Session: `f42f1a1f-2f2a-462f-a6d1-78b5864393ea`. It reviewed supplied
source/diffs, not independently executed tests or hash checks; the parent verified unchanged
production/bundle bytes and the two changed test/ADR files. Optional follow-ups include not offering
unavailable memory choices and directly testing the watcher's inactive-memory notice.

Offline wheel/sdist checks pass: 72 wheel RECORD checksums, all 69 source/resource files and 53
sdist test files match. Five extracted-wheel help commands pass without installation or Foreman
startup.
The nested bundle has 55 safe unique members: all 40 approved Forgetful runtime files match exactly,
and the 15 prior members remain unchanged. The managed entrypoint is present; post-create `chmod`
is absent and owner-only creation remains. Validated wheel SHA-256:
`09ed5cf213357d7be232536d10528d6b0fa5725fbc745759c8dd5abf30ffd366`.

Ruff and all three import contracts pass. Mycelium 0.4.5 was regenerated after the test correction:
72 boxes and no missing in-scope endpoints; tests filter 3,574 calls and 56 relationships.
Repeated exports are byte-identical. Known external-base warnings remain; this is text validation,
not a rendered Mermaid proof. The overview remains under 500 lines; changed lines stay within 100.

The historical Python 3.13 shutdown timeout remains unexplained; these successful runs do not
establish a fix. Hosted CI, live adoption and capture-URL policy remain separate. No installation,
watcher launch or public redistribution is authorized by the internal build.

## Server-only acceptance contract

- Use the existing HTTP-backed planning/recall/capture components for Factory's configured server
  and explicit project. Verify API availability and the extension's independently authenticated
  access to that project. Do not reuse the CLI login or change Forgetful as a prerequisite.
- Explain server-only extension support during setup and in runtime status. Refuse local extension
  opt-in clearly while preserving ordinary local CLI planning and existing edited settings. Do not
  start a server or select a different backend to make a local configuration appear supported.
- Keep model selection and automatic recall/capture opt-in; planning remains available when memory
  is off. Factory owns server/project selection; the extension owns its authentication. No second
  target selector, implicit personal-settings fallback, copied credentials or project guessing.
- Resolve capture source-read safety and bundle/select only audited artifacts for Foreman, leaving
  child resources unchanged. The private patched-Pi validation is not permission for live adoption.
- Prove server/project routing, authenticated access, local refusal, ordinary local setup, disabled
  memory behavior and rerun preservation through the agreed public Factory/native SDK boundaries.
- Repeat immutable-source tests, package checks, Python and explicit TypeScript scans, and actual
  independent Claude review after implementation. Complete suites must run sequentially.
- Arrange deliberate live adoption separately. A configured server with no usable API must fail
  clearly, without a backend update or fallback performed on the user's behalf.

## Later slice: shared CLI transport and local support

- Revisit making the extension use the configured native Forgetful CLI as Factory does. This
  transport change is deferred, not part of current implementation. Local mode should use the
  selected SQLite database, normally `.factory/data/forgetful.db`, without creating a second
  database or starting an HTTP server. Explicitly selected existing databases must be reused.
- Preserve server mode, fixed projects, setup choices and queued-work safety. Agree authentication
  reuse as part of the later design rather than requiring it for the current HTTP integration.
- Validate local/remote CLI behavior and local startup cost. Reassess account identification,
  background authentication and failure reporting; make only demonstrated upstream changes.
- Add public CLI/tool tests for these behaviors when implementing this later slice, alongside
  Factory init and native extension tests. Include wrong-target prevention and uncertain-write
  handling, not only successful requests. Respect the agreed test-seam approval boundary.
- Remove the local-support restriction only when the CLI-backed extension is validated. Do not
  silently migrate existing factories or change a live Forgetful deployment.

The earlier nine-path test-runtime improvement remains preserved and uncommitted. No commit, push,
main-instance update or credential migration occurred. No live Foreman inference or delivery was
validated; the separate Claude Code reviews did use the requested review model.
Evidence: `/tmp/factory-foreman-forgetful-2ptedi1m/`.

## Runtime alignment

Scott rejected Factory's private runtime policy after the DinoLand trial found that the current
standard Pi could load the normal extension but the managed wrapper refused it. Factory must follow
Pi and the extension's supported dependencies. He also rejected regression assertions about exact
dependency versions. These decisions supersede the earlier override and runtime-guard approval;
they do not change Factory's server/project authority or authorize live installation.

Implemented changes:

- Removed the managed wrapper's Pi/Undici metadata gate, including its `PI_PACKAGE_DIR` refusal.
  The other 54 resource files are byte-identical. Updated the member hash and complete local-patch
  digest against the same immutable extension base.
- Removed the npm root override. The installer retains reproducible Pi selection and restores the
  HTTP dependency declared by upstream. Only the Undici lock entry changes; Python requirements
  and other npm entries are unchanged. Existing environment defaults remain unchanged.
- Removed version assertions from the existing init test. It still checks consent and installer
  safety options. No version-specific regression test was added. The existing native test checks
  actual extension loading and a request to the selected project, without calling a model.

Supply-chain review before changing the lock:

- Official registry metadata confirms Pi 1.4.0 declares Undici 8.10.2. The restored archive's
  SHA-512 integrity and npm registry signature verify. Its MIT package has no runtime dependencies
  or installation hooks. No package was installed or executed during archive inspection.
- Fresh OSV queries report eight advisories for that dependency. They remain unresolved findings,
  not proof of exposure through this integration. Upstream alignment is not a clean security audit.
  The older clean result for the overridden dependency must not be reused for this lock.
- Context7 tools and CLI were unavailable. Published package metadata and installed upstream source
  were used directly; no documentation tool was downloaded.

Validation:

- The unchanged native project-access test failed before the fix: no HTTP request reached the
  fixture project. It passes after removing the gate on standard Pi. The six focused installer and
  native-resource checks pass, including real Pi loading with isolated homes and loopback REST.
- Final selected suites on Python 3.12.16 and 3.13.18 each ran 467 tests: 464 passed and three
  Ubuntu-24.04-only checks skipped. The runs took 258.431s and 262.066s. Another 48 native lifecycle
  tests remain excluded because their fixture requires tmux in `/usr/bin` or `/bin`; this host
  uses Nix. These are not complete-suite or hosted-CI passes.
- The first selected runs had seven setup failures because their interpreter directories lacked
  the `lint-imports` entry point. Disposable environments now point to existing dependencies and
  the existing real checker. No fixture or production change was made for that problem. The final
  runs include all seven architecture tests. The repository's old virtual environment also points
  at system Python 3.14 after migration; it was not repaired or used for final validation.
- Ruff and all three import contracts pass. The cached Mycelium 0.4.5 exporter regenerated the map;
  its default retains full member detail. Explicit test filtering retains 77 production boxes in
  one diagram, and the repeat export is byte-identical. Mermaid was checked as text, not rendered.
  Bundled TypeScript inside the zip is not part of that Python map; native loading covers it here.
- An offline build using the existing cached backend produced a wheel and source archive in the
  evidence directory. All 75 wheel RECORD hashes, 72 wheel/source-resource comparisons and 128
  source-archive file comparisons pass. All 55 bundled-resource hashes match the manifest.

No live runtime, DinoLand resources, shared Pi settings, authentication or memory preferences were
changed. No model inference, commit or push occurred. The earlier review and TypeScript scan apply
to the earlier snapshot; no fresh independent review or TypeScript scan is claimed for this change.
The existing files in `dist/` were not replaced. Evidence, archives and exact source/lock diffs are
under `/tmp/factory-pi-alignment-YYrJLb/`.
