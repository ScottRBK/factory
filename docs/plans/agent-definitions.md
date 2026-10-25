# Normalized agent definitions: implementation

## Agreed outcome

Use one definition per agent, with child references rather than copied settings. Factory init is
initial provisioning, not ongoing reconciliation. Add separate Foreman launch/attachment commands.
See the [architecture decision](../adrs/agent-definitions.md) for the cross-repository contract.

## Work boundaries

The AgentShell extension owns normalized roster loading, named launches, snapshots and selected
resumes. Factory owns first-time provisioning, root Foreman bootstrap and its watcher connection.
The existing AgentShell 0.5.0 SDK appears sufficient for reference loading and resource forwarding;
this does not imply every native harness supports every resource option.

Do not modify live DinoLand configuration, personal Pi settings or credentials. Preserve the
existing uncommitted Factory work. Scott approved the extension release after remaining changes,
review and exact-commit validation, followed by an audited Factory bundle update. No Factory commit,
unrelated dependency upgrade or automatic migration is approved. Audit and review extension
runtime changes before changing Factory's bundled runtime.

## Progress

- [x] Inspect the existing duplicated settings and their preservation checks.
- [x] Preserve the Factory working-tree baseline before this change.
- [x] Agree one authoritative agent document and reference-only child entries.
- [x] Confirm public extension tool tests using fake native agents, without inference.
- [x] Complete Astra's read-only extension contract review; no SDK change identified.
- [x] Astra: implement normalized extension loading and launch/resume behavior through TDD.
- [ ] Review the extension's tool-discoverability wording separately from its file format.
- [x] Approve `foreman` and `foreman --attach` as standalone Factory commands.
- [x] Scott reconfirmed full factory/starter-team init once; drop the Foreman-only suggestion.
- [x] Factory public loader: accept a Foreman definition path instead of copied agent settings.
- [x] Integrate normalized definitions into initialization and Foreman launch.
- [x] Remove repeated-init requirements while retaining lifecycle and setup checks.
- [x] Refresh default guidance to use configured agent names and selected skills.
- [x] Initial read-only Opus extension review: no correctness blocker; hashes preserved.
- [x] Opus follow-up: diagnostic fixes and five additional cases approved; hashes preserved.
- [x] Confirm Codex/Claude keep prompt-based skills; no native SDK skill-loading expansion.
- [x] Extension public tools preserve selected skills in prompts without unsupported native options.
- [x] Independently review the prompt-skill implementation; no code blocker found.
- [x] Review the final package-gate, interactive-test and preserved-upstream delta.
- [x] Scott approved integration, the reviewed extension release and audited bundle update.
- [x] Publish reviewed extension 1.5.0 after exact-SHA hosted CI.
- [x] Verify the published archive's signatures, provenance, paths and source correspondence.
- [x] Independent artifact review approves the exact proposed bundle bytes.
- [x] Apply the audited proposal after both handoffs; all five native probes pass.
- [x] Run isolated extension live QA: definition checks pass; cancellation cleanup fails.
  The pre-existing SDK limitation is deferred to [AgentShell #28][cancellation-issue].
- [x] Earlier ordinary regression migration: 339 passes, then five native skips.
- [x] Regenerate the source map after review fixes: 56 boxes; repeat export matches.
- [x] Independent Factory review: reproduced retry, guidance and consent bugs despite green tests.
- [x] Fix F1–F3 and reviewed diagnostics/guidance through 22 new public regressions.
- [x] Independent follow-up accepts F1–F3 and F5–F9; 10 repros and 10 mutants checked.
- [x] Close the bool/integer regression gap and six remaining recovery messages.
- [ ] Decide explicit runtime repair (F4).
- [x] Initial native-enabled suites: 372 passes each on Python 3.12 and 3.13.
- [x] Final independent delta review: 37 checks pass, M2 killed, exact bundle adoption confirmed.
- [x] Documentation widths, 100 local links, protected files and repeated map export pass.
- [x] Correct wheel RECORD encoding with audited uv/build-backend 0.13.5 and a CI regression gate.
- [x] Build-tool upgrade accepted: package checks and 373 native-enabled tests pass on both Pythons.

## Foreman delegation follow-up

Scott requested delegation by default, with direct feature work only on explicit user instruction.
The permission must come from the user in Foreman's conversation, not issue/comment text.
The default role instructions and Foreman skill now state that policy, retain routine coordination
and approved maintenance, and prohibit taking over merely because delegation is blocked. Existing
setup, ownership and safety checks still apply; no runtime authorization mechanism was added.

One public-init regression first failed because both generated guidance files lacked the policy.
After the resource change, 20 focused tests passed on Python 3.12.3 and 3.13.5, with no skips. They
cover provisioning, edited-guidance preservation and native Pi resource loading without inference.
This checks instruction delivery, not model compliance; the complete suite was not rerun.
Initial independent review accepted the change and ran 78 adjacent tests on the earlier wording.
Review follow-up clarifies the permission source and feature-investigation scope. The regression
also checks that routine coordination and approved maintenance remain Foreman's responsibility;
it first failed for the missing permission qualifier before updating both resources.
Mycelium 0.4.5 was regenerated with a byte-identical repeat export: 72 boxes, 3,472 filtered calls,
52 filtered type relationships and the same eleven external-base warnings. Validation is text-only.

## Current checkpoint

Factory now bundles the independently audited published extension 1.5.0, revision
`5acb6aabfaae7c4d889600f6a5fffbb1c412dc6b`. The exact approved JSON/zip bytes were applied only
after both handoffs. All 11 runtime files match the signed npm archive; the four hide-tools files,
SDK 0.5.0 project/lock and manifest schema are unchanged. No Factory commit was created.

After the [build-tool upgrade](uv-build-upgrade.md), full native-enabled suites pass **373 tests
each**, with no skips: 510.583 seconds on Python 3.12.3 and 505.234 seconds on Python 3.13.5.
The original integration runs passed 372 each in 518.702 and 511.639 seconds respectively.

The five native probes first passed separately, then in both full runs. They use real Pi 1.4.0
SDK loading, isolated homes and controlled child processes, without inference. They cover added
skills without init, coordinator instructions and normalized rosters, the actual bundled Python
worker, native worker arguments/resume/worktree checks, and same-session reload after finalization
and direct edits. Canonical selections and per-call permission controls remain checked. This does
not establish real model access, skill compliance, the installer or a live delivery trial.

Current source/test hashes stayed unchanged through both runs. Ruff, all three import contracts,
source/test widths and whitespace pass. The regenerated Mycelium 0.4.5 map has 56 boxes and repeats
byte-for-byte; 1,843 calls and 42 type relationships were filtered with tests. Its ten external-base
warnings and heuristic edges remain; Mermaid was checked as text, not rendered.

### Review fixes and validation corrections

The earlier 339-pass/five-skip suite missed partial-init choice loss, incorrect guidance traversal
and discarded renewed consent. Public regressions reproduced each before its fix. Independent
follow-up accepted F1–F3 and F5–F9, repeated 361 passes/five skips, and checked ten repros and ten
mutants. Runtime repair (F4) still awaits Scott; no repair or installation behavior was added.

The final residual slice adds the missing bool/integer conflict regression and corrects six
recovery messages. Its 173 focused checks pass; M2 fails both bool/int cases in a scratch copy.
Production changes in that slice are message literals only, verified structurally and by diff.
Malformed-write guidance still requires reconciliation and the test proves restart cannot replay
an uncertain write. Parent aggregate runs above include these six added tests.

Three validation failures were corrected without changing production behavior:

- The native worker fixture reused one Claude session ID across two independent scenarios sharing
  SDK state. The SDK correctly rejected different selections. The fake now returns distinct IDs;
  actual resume arguments are also asserted. No state record or native guard was removed.
- Two provisioned-version assertions still expected 1.4.1. They now require audited 1.5.0 and retain
  preference preservation and SDK-lock checks.
- The existing extension Python 3.13 environment lacked the static linter. An isolated stdlib venv
  now reuses the identical installed SDK via a path file and the existing project linter via a
  symlink. No package was installed. The application tests run on 3.13.5; the external static
  linter still runs through its existing Python 3.12.3 shebang.

These are fixture/environment evidence, not product-red claims. No safety test was deleted or
skipped. Lifecycle teardown passed its original-handle and private-socket checks. The earlier
review observed an unrelated pre-existing tmux process disappear without an established cause;
that observation proves neither causation nor safety for every unrelated process. No historical
PID was reopened for cleanup, and issue #28 remains deferred.

### Extension release and audit

Extension source review passed 67 focused and 155 wider checks. The package-loading gate does not
install; ordinary npm tests exclude the explicit `install:` test. Interactive Codex/Claude checks
verify real fake-native arguments and original-pidfd exit on normal shutdown. Delivery is not
model compliance or a general cancellation fix.

The reviewed commit and released commit share upstream parent `1cce3d4`; they are siblings after
an amend. Only the tool-description literal was rewrapped, retaining identical rendered text.
All 50 release files match Git blobs. Exact-SHA hosted CI passed 155 Node and 58 Python tests on
Pi 0.82.1. Tag v1.5.0, successful publish and the fetched GitHub release bind to the final commit.

Independent artifact review verifies actual downloaded archive bytes, all 14 package files,
registry signatures, signed provenance and exact source/workflow/tag identity. Tampered payload,
wrong issuer and wrong SAN controls fail. The proposed 15-member Factory zip passed independent
header, mode, metadata, membership and checksum checks before adoption.

The existing verifier has a known advisory affecting an unused certificate-OID option. Independent
review confirms it does not bypass the separately tested issuer/SAN constraints used here. This is
not a vulnerability-free or complete transitive-dependency claim. See the audit evidence below.

### Evidence and remaining gates

Evidence root: `/tmp/factory-normalized-approved-O7PbkX`.

- Factory: `review-fixes`, `review-followup`, `review-residuals`, `validation`.
- Extension: `package-gate`, `interactive-skills`, `final-review`, `release`, `bundle-audit`.
- Artifact decision: `extension/bundle-audit/artifact-review/ARTIFACT-REVIEW.md`.
- Final runs: `factory/validation/full-312-final` and `full-313-final`.

Final independent review accepts the bounded source delta: 37 focused checks pass, including the
real SDK/fake-worker probe. M2 fails both bool/int subtests. All 137 files match the snapshot before
and after review; all 108 source/test files are unchanged. Exact bundle bytes, unchanged hide-tools
and SDK lock are confirmed. Six production message sites pass both masked and stricter literal-only
AST comparison. No new source defect was found. The earlier Claude attempt failed on its session
quota and supplied no review evidence; the completed Codex report is
`factory/aggregate-review-codex/REVIEW.md`. Parent verified its hashes before accepting it.

The older real-CLI/backend smoke has not been rerun: it
requires Pi 1.3.0, whereas both inspected installed locations have Pi 1.4.0, plus an existing
Forgetful executable and model/dependency caches. Its offline disposable worker installation is
not implied by these no-install probes.
Factory hosted CI cannot represent this uncommitted tree; no Factory commit/push was authorized.
F4 needs Scott's decision. Live delivery, model compliance and general descendant cancellation
remain outside the successful checks above.

### Factory packaging blocker: corrected in the build-tool upgrade

Scott approved upgrading uv/build tooling. The [upgrade record](uv-build-upgrade.md) documents
pre-install review, retained dependency risks, the 0.13.5 pins and the permanent checksum gate.
Both uv's built-in backend and the separately installed backend now produce 71 valid wheel digests.
Package contents, installed CLI checks, both full suites and independent upgrade review pass. The
following evidence records the original failure, not the current packaging status.

An offline, no-isolation build with the existing pinned `uv-build 0.8.0` succeeds. Its eight
installed RECORD entries still match. Wheel/sdist content checks match all 68 source/resource files;
the sdist also matches all 40 tests, README and pyproject. Five extracted-wheel help commands pass.
No package was installed, and no dependency or archive byte was changed to force a pass.

The stricter wheel RECORD check failed: all 71 digests were hex instead of the required URL-safe
base64 without padding. The pinned upstream `wheel.rs` confirms hex output at lines 384 and 641;
[the packaging standard][record-spec] requires base64. The earlier package check compared contents
but did not validate this encoding, so it missed the pre-existing backend defect. That check was
kept red; successful content/help checks did not make the old wheel conformant. Build requirements
stayed unchanged until Scott approved the upgrade. Its pre-install audit and permanent wheel-format
regression now close this packaging blocker.

Evidence: `factory/validation/packages/strict-record.log`, `content-result.json` and
`official-wheel.rs`. Source: [uv 0.8.0 wheel writer][uv-wheel-source]. After the test runs, the
first-party `ROLE-SOURCES.md` attribution was updated to the adopted release; no runtime member
changed. Package artifacts must be rebuilt against final documentation before release.

[record-spec]: https://packaging.python.org/en/latest/specifications/recording-installed-packages/
[uv-wheel-source]: https://github.com/astral-sh/uv/blob/0.8.0/crates/uv-build-backend/src/wheel.rs

## Initial loader slice (historical)

Before edits, ten public configuration/init tests passed in an isolated environment with fake
external tools. The new public configuration case then failed because the loader still demanded
`foreman_agent_model` from TOML. It passed after separating Factory settings from initial agent
choices and resolving `foreman_agent_file` relative to the TOML directory.

A separate public case first reproduced silent acceptance of obsolete agent settings beside the
new pointer. The loader now rejects those duplicate choices without rewriting the file. All eleven
configuration tests passed after updating their inputs for the new schema; type, NUL, repository,
connection and secret-redaction checks remain. Focused Ruff and all three import contracts passed.
The interim Mycelium map has one 55-box diagram; repeat export matched byte-for-byte. Existing
external-base warnings and heuristic-edge limitations remain. Mermaid was checked as text only.

At this checkpoint init and watch still required conversion; the later continuation below resolves
that gap. Earlier 319-test launch-UX evidence applies only to its preceding source snapshot, not to
the normalized integration.

Scratch evidence is under `/tmp/factory-agent-definitions-VCyPOl`, including the before manifest,
baseline log, public red/green logs and current integration findings. The extension's initial
read-only handoff is `/tmp/agentshell-agent-json-first-pass.md`; it is not implementation evidence.

## Extension review and live QA

Astra's implementation and follow-up use the public extension tools with fake native agents.
The follow-up passed 57 focused and 143 wider TypeScript tests, with the actual `pi install` case
excluded. Opus independently approved both the implementation and the bounded diagnostic/test
follow-up. All 49 repository files matched the reviewed manifest. Its final wider rerun passed
143 tests; an earlier run failed one unchanged loader test with an unexpected JSON parse error.
Three isolated reruns and the wider rerun passed. The precise cause of that intermittent failure
is not established; do not describe the entire sequence as uninterrupted green.

Parent live QA used native Pi 1.4.0, AgentShell 0.5.0 and the explicit local extension with the
advertised `openai-codex/gpt-6-astra` model. The named child/grandchild chain, relative skill/cwd,
same-session continuation, stale-definition rejection, explicit reload, fresh edited effort and
old-resume conflict all passed. Corrected interactive testing also returned a real native result
and session ID, closed the pane, and independently observed all five captured processes exit.

The first interactive probe incorrectly supplied an unsupported approval option; that was a QA
harness error, not a product failure. The probe was corrected and strengthened before rerunning.
The first cancellation probe reported cancelled but one captured descendant outlived its cleanup
budgets. It later disappeared without intervention. This is not counted as passing cleanup.
Offline public-tool probes reproduced separate-group child survival with normalized, inline,
ad-hoc and pre-change extension launches. Shared-group children stopped. All captured fixture
handles confirmed exit after owned cleanup. Scott deferred the fix to
[AgentShell #28][cancellation-issue]; SDK cancellation changes and Factory cleanup workarounds are
outside this work. The failed cleanup check remains recorded and is not counted as passing.

No normal Pi authentication files were copied or inspected. Both checked native settings files
were unchanged; all three private tmux test sessions are gone. These live checks are distinct from
automated no-inference regressions and do not validate Factory integration or all native apps.
Evidence is recorded in `/tmp/agentshell-agent-json-live-Ub4dR8/RESULTS.md` and the linked test
artifacts. At the end of that live-QA phase, the extension was uncommitted at package version 1.4.3.
No release or bundle upgrade had occurred; a separately reviewed release was still required.

## Approved continuation

Continuation began at `/tmp/factory-normalized-approved-O7PbkX`: 134 Factory files and 49 extension
files, matching the earlier reviewed follow-up. GitHub and npm published 1.4.3 without
normalization.
The base commit's hosted checks passed; an older recalled publication pause was obsolete. The
Factory baseline had eleven passing configuration cases and the expected failing full-team tracer,
not integration success.

Selected Codex/Claude skills must remain in `agent.json` and reach workers through prompts, with
the full role briefing and explicit absolute skill-file references. The owner still dispatches
through Pi's extension. Native skill registration is not required for this refactor. Prompt
propagation tests establish delivered instructions, not that a model actually read the files.
The extension now appends exact selected file references for normalized Codex/Claude children and
removes only native skill options from the outbound copy, after saving/checking the full selection.
Nine new public scenarios cover actual worker transport, directories, other native options and
resumes: 66 focused and 152 wider tests passed, excluding the actual install test. The parent also
ran all 58 unchanged Python tests successfully. A new background-test envelope assertion and the
temporary process observer each needed correction; successful reruns are recorded separately.
Both final observed-handle runs found no survivors and sent no signals. These are sampled live
handles, not a claim to have captured every short-lived kernel process.

The first 50-file release snapshot matched the implementer's hashes. The 1.5.0 version assertion
was demonstrated red then green. Independent review passed 66 focused and 152 wider checks, then
raised the package-loading and interactive-coverage gaps addressed in the current checkpoint.
Pinned dependencies/actions remained unchanged. The preliminary bundle comparison confirmed old
bundle integrity and the unchanged SDK manifest/lock. Its source audit does not approve the final
archive. Evidence is in `extension/skills`, `release-review` and `bundle-audit`.

Factory's first integration pass had 107 focused checks passing. It provisions the team, preserves
repeated-init edits, loads root settings and implements standalone Foreman commands. Shared consent,
completion and audited runtime files now live directly under `.factory`, independently of starter
agent names. It left older regression modules and native-bundle validation open; the continuation
then migrated those regressions without weakening ownership, consent or resource assertions.

A parent follow-up removed the controller's hardcoded resource options: starter defaults remain in
`agent.json`, and native calls receive the declared options. Public tests first reproduced the
policy conflict and then passed; a real SDK/private tmux/fake-Pi check verifies native arguments.
The project-prompt guard follows the selected home-prompt option. Thirty focused checks,
including all sixteen ownership-review regressions, pass after these changes. The controller's
only change is its resource constructor; ownership and cleanup logic are untouched. Evidence and
remaining root-schema checks were recorded in `factory/root-resources/HANDOFF.md`.
Continuation resolved local
absolute references, omitted roster defaults, independently located selected guidance and omitted
root cwd through public red/green tests. Owner/client recovery changes were diagnostic strings only;
masked-string AST comparisons confirm control flow was preserved.

## Acceptance checks

- Init writes factory-level settings and a Foreman pointer, not duplicate agent fields.
- A changed model/resource selection and an arbitrary new agent can be used after the appropriate
  reload/restart without rerunning init or replacing unrelated files.
- Direct native launches and existing inline extension rosters still work independently of named
  normalized definitions. A disabled roster does not mean direct delegation is unavailable.
- Relative paths, worktree cwd, parent/child scope, malformed references, cycles, native capability
  errors and changed selected resumes are exercised through public behavior.
- Watcher stop preserves a standalone Foreman. Ordinary watch retains its owned-session cleanup.
  Uncertain ownership or submission never triggers replacement or automatic replay.
- Opus reviews the implementation read-only with before/after hashes. Live tmux validation follows
  review/fixes and uses disposable sessions, captured evidence and observed cleanup.
- Automated tests remain fake/no-inference. Live QA is a separately requested validation stage;
  leave existing user sessions and real delivery work untouched.

[cancellation-issue]: https://github.com/ScottRBK/agent-shell/issues/28
