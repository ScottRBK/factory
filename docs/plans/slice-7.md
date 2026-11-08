# Slice 7: Definition of Done and automatic cleanup

Status: 7A/B and automated/local 7C implemented locally under Scott's explicit authorization.
One independent review, implementation corrections and final parent SonarQube verification are
complete. See [final local validation](#parent-final-local-validation) for evidence and limits.
The full suite retains one known baseline failure. Live trials/adoption remain deferred.
No commit, push or live factory change is authorized by this work.
Back to [plan](../plan.md), [architecture](../architecture.md) and [intent](../../FACTORY.md).

## Outcome

A plan is complete when its acceptance criteria and the agreed Definition of Done (DoD) are met.
The DoD is a project/programme contract written in `definition_of_done.md` and referenced by the
Foreman skill. It is not a replacement for a particular plan's acceptance criteria. Foreman checks
the required evidence and completes the Forgetful plan. Deployment and deployed E2E are required
only when the DoD says so; their absence is not an automatic blocker or an automatic pass.
Factory then deletes that plan's worktrees, local feature branches and remote feature branches.

Plan completion is the cleanup authority. Cleanup does not ask the feature-owner to act, prove
process exit, repeat merge verification or decide whether local files are worth retaining.

This follows `FACTORY.md:23–32,69,151–167`: agree the DoD at setup,
pass it to the feature-owner, and have Foreman check it before completion. Deployment/E2E is an
example of DoD activities, not a universal requirement. Existing Slice 6 cleanup guidance remains
historical behaviour. New roles leave resources for the completed-plan watcher and hand back to
Foreman; old cleanup records remain readable. Completed-plan disposal is now implemented locally.
The separate watch-status contract remains unchanged.

## Agreed MVP decisions

- Offer three starting presets and a discussion route; save the confirmed DoD as Markdown.
- The Foreman skill points to that file. No TOML policy schema, policy parser or policy engine.
- All presets retain independent review and required repository/PR checks; none bypass merge gates.
- CI/CD runs agreed deployment/E2E stages; Foreman verifies evidence. Factory is not a deployer.
- For required post-merge checks, verify the actual merged revision, not an earlier feature head
  or PR synthetic merge commit. Joined-up E2E must identify the deployed repository combination.
- Failed required verification leaves the plan open and creates or reuses a linked follow-up issue.
- Pending, missing, skipped required stages or inconclusive results are not success. Checks that
  the agreement explicitly does not require must not leave placeholder tasks blocking completion.
- Only Forgetful status `completed` triggers cleanup. Issue closure, merge, archive or cancelled
  tasks alone are not cleanup signals.
- Everything inside a Factory worktree is disposable after plan completion, including changed,
  untracked and ignored files. Required reports and artifacts must be saved elsewhere beforehand.
- Cleanup removes the recorded local and remote feature branches even if they contain extra commits.
  The completion decision authorizes disposal; cleanup does not compare their heads with the PR.
- No process scans, worktree-use locks, worker-launch changes or GitHub merge rechecks for MVP.
- No new completion event service, per-resource cleanup journal or conditional-ref deletion scheme.
- Keep basic target checks: delete only the recorded Factory resources, never the main checkout,
  target branch, another plan's resources or an arbitrary path supplied in a text field.

This deliberately trusts Foreman's completion decision. It does not prove that all processes have
exited. Agents and users must not continue using, reopen or reuse a completed plan's worktrees or
branches. Mistaken completion can discard work; document that consequence clearly at setup and in
role guidance. Plan completion is not a recoverable trash operation.

## Agree a Definition of Done in plain Markdown

During repository setup, offer:

1. **After merge:** independent review, required PR checks and merge.
2. **After merge and deployment:** also confirm the intended merged revision was deployed.
3. **After merge, deployment and E2E:** also confirm E2E passed against that deployment.
4. **Discuss with Foreman:** inspect existing workflows and agree what fits the project.

These are starting points, not an exhaustive list of allowed policies. Discussion can settle a
more suitable agreement, such as package-specific checks. It is a route to a decision, not a fourth
completion rule. Never infer merge-only from missing tests or silently select a weaker preset.

Both routes save a user-confirmed `definition_of_done.md` outside disposable feature worktrees and
add its location to the Foreman skill. For a grouped workspace, the same file can name repositories
with different requirements and any shared checks. Do not introduce an inheritance system.

Use ordinary prose, without mandatory fields or machine-readable front matter. Make clear which
project/programme or repositories it covers, what completion requires, what evidence counts and
what is not required. Keep feature-specific acceptance criteria in their own plans, not in the DoD.
Name an environment or workflow when needed to remove ambiguity. For example:

> Features in this repository are complete after independent review, required PR checks and merge.
> Deployment and deployed E2E are not completion requirements yet. Foreman records the merge and
> check results before completing the plan.

This example is not an adopted policy for DinoLand or any existing workspace. Do not create or
replace a live agreement as part of this proposal.

The Foreman skill must point to the workspace file and instruct Foreman to:

- Read it before planning feature work and before declaring completion, including after restart.
- Ask if it is missing, unclear or conflicts with repository requirements. Setup discussion may
  continue, but clarify the agreement before handing off feature work; do not invent a default.
- Explain missing prerequisites for the chosen checks and get confirmation before saving it.
- Preserve an existing agreement during repeated setup. Change it only with user agreement.
- Pass the DoD with the issue, plan and repository context to the feature-owner. Record applicable
  shared requirements briefly in existing plan/task descriptions, separate from feature acceptance
  criteria. No new structured policy snapshot is needed.
- When requirements change, ask whether the change applies to existing open plans. Keep their
  previously agreed requirements unless the user approves a change; record that decision there.

A user-approved change may remove a previously required check from an open plan. Record the reason
before retiring its task; do not describe an unrun check as passed or cancel it merely to get
completion. New plans use the updated agreement. No policy version registry is needed.

This is agent-guided behaviour, not Python enforcement of Markdown. Conversation history and
optional memory are not the authoritative agreement. Cleanup does not read or interpret this file;
it continues to trust Forgetful plan completion.

## Responsibilities and evidence

### Feature-owner: hand back after merge

- Record each repository's PR URL, actual merge commit, target branch and relevant workflow links.
- Preserve the ownership mapping: repository, local root, branch and absolute worktree path.
  Multi-repository work needs one valid mapping for each disposable feature worktree.
- Finish implementation, review and merge tasks. Leave required post-merge checks and overall
  ownership open for Foreman. Do not add deployment/E2E tasks when the agreement excludes them.
- Report the handoff to Foreman. Do not delete resources or complete the plan yourself. Foreman
  can accept merge-only work after checking its agreed evidence; deployment is not always needed.
- Stop dispatching work against these resources before the final completion decision.

Use the ownership/task descriptions for detailed records. Keep plan context brief and preserve its
existing recovery JSON and 2,000-character limit. Do not add an unlimited evidence log to context.

### CI/CD: provide the agreed checks

- Follow each repository's workflow and environment policy. Do not introduce a universal platform.
- When deployment is required, deploy the intended revision to the agreed environment after
  required post-merge checks pass. Expose a release identifier, manifest or other revision evidence.
- When deployed E2E is required, run it after deployment succeeds, against that environment rather
  than only a checkout server. Use an isolated test environment for those tests.
- For required joined-up E2E, record the deployed revision set tested together.
- Retain required run links and artifacts outside disposable Factory worktrees.

A missing required workflow or unusable revision evidence blocks verification. An absent deployment
or E2E workflow does not block a plan whose agreement does not require it. Adding or changing a
pipeline is explicit repository work, with dependency/action audits before installation or upgrades.
This slice does not automatically deploy to production, create releases or disable existing jobs.

### Foreman: verify and complete

Read the DoD and the plan's acceptance criteria and recorded shared requirements. Resolve any
unapproved difference before completion. Do not treat satisfying the DoD as proof that feature
acceptance criteria are met. Save evidence in the existing ownership/verification task:

- PR, actual merged commit, independent review and required final-revision check results.
- Required post-merge workflow run, attempt, stage conclusions, environment and artifact links.
- Actual deployed revision and tested repository combination, when those checks are required.
- The time and outcome of verification, plus any blocker or linked follow-up issue.

Check live provider evidence against the required identities before marking tasks done. A green run
for a different revision or an earlier successful attempt does not satisfy current verification.
Deployment without E2E is sufficient only when E2E is not required by the agreement. Merge-only
work needs no deployment/E2E tasks and can finish after Foreman's handoff and evidence check.

On required verification failure, raise or reuse a follow-up issue linking the original issue, plan,
revisions and failed run or missing prerequisite. Check for an existing issue after an uncertain
create response; do not create duplicates.
Do not automatically add intake labels or start repair work contrary to the existing intake policy.
The original plan stays open through repair and subsequent successful verification.

Keep unfinished verification monitored without depending on an issue edit. Use existing Foreman
coordination and the watcher notification path; restart must rediscover this work even if the issue
is closed. Notifications must not start a second owner or resume a busy owner concurrently.

Before final completion, save all delivery evidence and finish any required handoff. Then finish
verification and ownership tasks in the supported order, re-read the plan and confirm `completed`.
Forgetful may complete an active plan automatically when all tasks are done/cancelled and at least
one is done. Never cancel still-required verification tasks to get past this rule. Any user-approved
requirements change must be recorded before task changes can trigger completion. No agent may rely
on writing evidence into the worktree after the last completion transition.

## Completion detection: reuse polling

Use the existing watch cycle and native Forgetful CLI. No subscription is required for MVP.

1. On startup and each normal watch cycle, discover completed Factory plans for this workspace.
2. Read their full plan and ownership records. Filter by project, workspace and configured sources;
   do not treat every completed plan visible to the Forgetful user as Factory-owned work.
3. Keep this completed-plan path separate from unfinished-plan recovery. It must never scaffold a
   replacement worktree or dispatch implementation for completed work.
4. Process cleanup candidates independently of GitHub issue polling. Closed issues and `--new-only`
   must not hide them. GitHub intake failure must not invalidate readable completion evidence.
5. If Forgetful cannot establish status or ownership, perform no deletion for that candidate and
   report the problem through the existing watcher alert path.

A small in-memory set may suppress repeated successful cleanup during one run. On restart, list
completed plans again and reconcile resource absence. Do not rely on an event received only once,
an agent message, or the original issue remaining open.

### Why not subscribe to Forgetful events now?

Local Forgetful source at revision `8d9d6ba` emits plan `updated` activity with a status change,
including auto-completion through the task service. Its optional REST activity stream could carry
these events, but the documented facility is experimental, can drop events, and needs recovery.
Factory already supports local and remote planning through its native CLI, so polling avoids a new
REST connection/authentication path and works when activity tracking is disabled.

Evidence checked for this plan, not a claim about the running server's configuration:

- Forgetful `docs/api_reference.md:1042–1064,1190–1231`: activity and stream recovery.
- Forgetful `app/services/plan_service.py:120–161`: updated plan activity emission.
- Forgetful `app/services/task_service.py:484–509`: task-driven plan completion.
- Forgetful `docs/tool_reference.md:1654–1675`: native `list_plans` and status filtering.

Context7 CLI was unavailable; these are local upstream documentation/source checks. No dependency,
server setting or activity subscription was installed or changed. An event-driven improvement can
come later, but would still need reconciliation after missed events or downtime.

## Cleanup contract

### Identify the targets, without re-approving the delivery

For each ownership mapping, check:

- It belongs to the selected completed Factory plan and workspace; conflicting ownership blocks it.
- The local repository and configured remote match the recorded repository.
- The absolute path is strictly beneath that repository's Factory-managed worktree directory.
- Git registration names that exact path and branch, with the expected shared Git directory.
- The path is not the main checkout or a symlink escape. The branch is a valid, exact feature ref,
  not the default or recorded merge-target branch. Never use wildcard branch deletion.

Missing or contradictory identity data produces a cleanup error, not a guessed target. Do not
invent missing epic mappings. A missing target after prior deletion is different from an occupied
path that no longer matches the saved mapping.

These checks restrict what can be deleted. They do not recheck clean status, process liveness,
merge state or whether the branch contains additional work. Mapping checks remain necessary even
though the contents of a correctly identified worktree are disposable.

### Remove and report

1. Read the completed plan and validate its mappings before destructive operations.
2. Remove each recorded worktree using targeted native Git operations. Dirty, untracked and ignored
   contents are deliberately removable under the disposable-worktree policy; ordinary non-forced
   removal cannot implement that requirement. Allow the force needed for contents, not a blanket
   filesystem delete or an override of locked/mismatched registrations.
3. Delete that mapping's local feature branch, including unmerged local commits. Respect Git's
   refusal to delete a branch still checked out in a different worktree; do not remove that tree.
4. Delete the same named feature branch from the configured remote. Do not delete the base branch,
   remote repository, tags or unrelated refs. Remote deletion is not conditional on a saved SHA.
5. Report completion only when the worktree registration/path and both branch refs are absent.
   Already-absent resources count as complete after confirming the remaining mapping identity.

Use fixed operation order and observed resource state for retries, not a new transaction journal.
If a command fails or its response is uncertain, report the affected plan/resource and recheck
absence on a later cycle before attempting that operation again. Continue with independent plans;
do not mislabel failed access as successful deletion or stop all issue intake.

A crash between removals is allowed to leave partial cleanup. Startup reconciliation finishes the
remaining resources. No rollback or automatic recreation is required. Cleanup errors do not reopen
a successfully delivered plan or erase its evidence; they remain visible watcher problems until
resolved. No broad worktree pruning, forced resets of the main checkout or process termination.

## Implementation sequence: complete one vertical slice at a time

### 7A. Agreement, handoff and completion evidence

- [x] Offer the three presets and Foreman discussion during setup; show and confirm the resulting
      Markdown agreement. Preserve existing files and avoid a silent default for older workspaces.
- [x] Point the Foreman skill at `definition_of_done.md` and pass the DoD to feature-owners with
      each handoff. Keep shared DoD requirements distinct from feature-specific acceptance criteria.
      Keep persistence as plain Markdown, not a new TOML schema or machine-interpreted policy.
- [ ] Exercise merge-only completion without deployment/E2E tasks or a deployment environment.
- [ ] Exercise deployment-only completion without E2E, then deployed E2E when explicitly required.
- [ ] Observe a discussed agreement and an approved policy change, including open-plan handling.
- [x] Update Foreman/owner guidance to the responsibilities and disposal contract above.
- [x] Preserve unfinished required verification across restart and closed-issue recovery. Continuing
      notifications must not depend on issue edits or create duplicate dispatches.
- [ ] Cover failed/missing/stale required results and follow-up reuse with the plan kept open.
- [x] Record what is deterministic code and what remains agent-guided, observed behaviour.

### 7B. Completed-plan cleanup through public watch

- [x] Add completed-plan discovery to the existing watch loop, including completion during downtime.
- [x] Implement target validation and worktree/local/remote removal through ports and Git adapters.
- [x] Prove the disposable-files policy using a real temporary repository and bare local remote.
- [x] Prove isolation from unrelated plans, main checkouts, invalid mappings and target branches.
- [x] Cover partial cleanup, unavailable remotes, uncertain responses and restart reconciliation.
- [x] Report problems through existing watcher alerts; keep cleanup distinct from status health.

### 7C. Multi-repository delivery and adoption

- [ ] Exercise different agreed requirements across repositories in one plan. Verify the intended
      deployed revision combination and joined-up E2E when the agreement requires those checks.
- [x] Exercise cleanup of all mappings when one repository's deletion initially fails.
- [x] Reconcile existing Slice 6 cleanup markers; accept proven absence without recreating work.
- [x] Document that enabling this behaviour also processes eligible older completed Factory plans.
      Review those mappings before rollout; do not silently install it into a running factory.
- [x] Refresh architecture/ADRs, roadmap decisions, setup docs and role guidance together.
- [ ] Validate the built wheel and run an explicitly approved disposable live trial.

## Validation plan

Confirm these public test boundaries before implementation, then use RED/GREEN vertical slices:

- Public setup CLI and temporary workspaces: preset selection, confirmed agreement persistence,
  discussion handoff, no silent default and preservation of existing Markdown. Do not test exact
  prompt phrases as proof that an agent follows the agreement.
- Public watch CLI with isolated repositories and external Forgetful/provider fixtures: completion
  discovery, notifications, scoping, active/draft/archived plan exclusion and restart behaviour.
  Completed plans use the same cleanup path regardless of the agreement's wording or preset.
- Real native Git and a temporary bare remote: exact targets, dirty/untracked/ignored removal,
  additional-commit branch deletion, already-absent refs, partial failure and no unrelated deletion.
- Forgetful contract checks: manual and automatic completion shapes, full ownership reads and
  correct state when required verification tasks remain open. Do not invent fixture-only API fields.
- Explicit disposable live trials: merge-only without an E2E suite, deployment-only, and required
  deployed E2E with actual revision evidence. Observe Foreman completion and automatic removal.
  Also observe missing/unclear agreements and a policy change with open plans. These trials are
  needed to assess agent behaviour; prompt assertions cannot prove it follows the agreement.

Include regressions for closed issues, `--new-only`, completion while watch is stopped, a failing
GitHub intake poll, two repositories with partial cleanup, wrong origin/path/branch, symlink escape,
conflicting mappings, remote denial and a crash after worktree removal but before branch deletion.
Automated regression tests must not require live user repositories, credentials, shared runners
or deployed family data. The separately approved live trial uses an isolated test environment.

Run relevant and full suites, Ruff, import contracts and package checks. Refresh the Mycelium map
after code changes and review the architecture overview. Run SonarQube and inspect its gate/findings
before independent Claude Opus review; do not change rules/exclusions to hide new problems. Record
exact source/scan/test evidence and distinguish local validation from hosted CI and live delivery.

## Documentation and completion checklist

- [x] Check implementation against the DoD and cleanup intent in user-owned `FACTORY.md`;
      do not modify it without explicit instruction.
- [x] Update `docs/plan.md` Slice 7 and the old cleanup decisions to this approved proposal.
- [x] Document the presets, discussion route, agreement location and handling of open-plan changes.
      Clearly distinguish agent guidance from runtime enforcement.
- [x] Update `docs/adrs/feature-delivery.md` and `docs/adrs/issue-planning.md`, keeping historical
      behaviour distinguishable from the implemented replacement.
- [x] Link the implemented flow from `docs/architecture.md`; remove old owner-cleanup instructions.
- [x] Explain disposable worktrees in setup/README and owner/Foreman resources before adoption.
- [ ] Demonstrate completion and local/remote cleanup for each preset, without treating absent
      optional deployment/E2E as failure or falsely claiming those checks ran.
- [ ] Demonstrate failed required verification retains the original plan and resources.
- [x] Demonstrate interrupted cleanup resumes without recreating work or deleting unrelated data
      through public watch and real disposable Git repositories; live adoption remains deferred.

Historical planning-only boundary: the original proposal changed no code or live resources.
Scott subsequently authorized local 7A implementation only. The record below supersedes that
planning-only status; the approved 7B/7C contract above is preserved. `FACTORY.md` remains
user-owned
and unchanged by this implementation.


## 7A local implementation

Scope: first vertical slice only. No live factory, pipeline, task, agreement, branch or worktree was
changed. No commit, push, dependency addition/upgrade, wheel installation, SonarQube run or
independent
review was performed. Parent coordinates final SQ and one independent review after all Slice 7 work.

### Implemented boundary

- `cli/definition_of_done.py:9` offers three starting presets plus real Foreman discussion. It shows
  and confirms the Markdown before saving `.factory/definition_of_done.md`. Deployment presets ask
  for environment/workflow names and explain prerequisites without claiming to inspect them.
- `cli/main.py:759,822` keeps configuration-save/receipt-last recovery. First incomplete setup can
  finalize the agreement or start a setup conversation; a live/uncertain owner is never replaced.
  Assisted setup leaves policy to its conversation. Ordinary repeated init remains a no-op.
- Existing agreement/skill bytes are preserved. A file created during confirmation is not silently
  accepted as the proposed agreement. There is no policy enum, TOML schema, Markdown interpreter,
  approval ledger or immutable snapshot framework. Read-only file checks do not establish approval.
- Foreman/owner/maintenance guidance covers agreement reads and handoff, distinct acceptance
criteria,
  brief historical task requirements, explicit open-plan change decisions, required evidence,
  missing/stale/skipped blockers, follow-up reuse and Foreman-owned completion for every agreement.
- New guidance removes owner deletion authority and retains resources until 7B. Historical cleanup
  marker validation/recovery remains unchanged. No lifecycle/status/managed-stop code changed.
- [The dedicated ADR](../adrs/completion-agreement.md) explains the path and intermediate rollout.
  README, roadmap, delivery/planning ADRs and architecture distinguish this from implemented
cleanup.

Checked 7A boxes above mean implemented setup/guidance or observed Python recovery, not observed
model compliance. Merge-only/deployment-only/E2E completion, evidence interpretation, follow-up
reuse,
a real discussed agreement and approved policy changes with open plans still need expressly approved
disposable live trials. Those observations remain unchecked; prompt assertions are not substitutes.

### RED/GREEN sequence

Approved seams: public init/watch, external provider/native CLI fixtures, real temporary Git, and
native isolated tmux with fake Pi and no inference. No new private-method or agent-compliance phrase
tests were added. Each new production behaviour followed its own failing test and minimal change:

1. Confirmed merge agreement: RED missing file; GREEN saved shown Markdown outside worktrees.
2. Deployment starting point: RED rejected choice; GREEN named environment/workflow and revision
   evidence, with deployed E2E explicitly excluded.
3. Required deployed E2E starting point: RED rejected choice; GREEN deployment-first and tested
   repository-combination requirements persisted.
4. Discussion: RED rejected choice; GREEN setup Foreman launched without agreement/receipt, watching
   blocked, and a simulated confirmed conversation save survived finalization in the same terminal.
5. Interrupted saved setup discussion: RED returned an unusable launch instruction; GREEN
finalization
   starts the existing assisted flow when no owner exists, without a default agreement.
6. Concurrent agreement save during confirmation: RED silently accepted different text and completed
   setup; GREEN preserved the other file, reported conflict and withheld the first-setup receipt.

The last issue was possible because the reused write-new helper deliberately preserves existing
files for idempotent resource setup. That is not sufficient for confirming one particular agreement.
A content comparison now rejects the conflict; a public held-input regression covers that boundary.
This is not a new policy parser or a claim of protection against arbitrary concurrent file edits.

RED/GREEN logs: `/tmp/factory-7a/01-{red,green}.log` through `06-{red,green}.log`.
Other setup regressions cover no choice, blank/invalid choice, decline, missing old agreement,
pre-existing custom Markdown/skill preservation, finalization without reprovisioning and symlink
refusal. Public watch regression checks closed/new-only recovery with an open required verification
task and merge handoff evidence: same plan/owner/mappings, no duplicate scaffolding or policy write.
It passes existing recovery code; no watcher policy machinery was necessary.

Shared setup fixtures now supply an explicit merge-agreement choice/confirmation. Project/terminal
fixtures supply those answers only after their existing prompts. Existing worker-guidance assertions
for universal E2E and owner-removal instructions were removed because those instructions are now
superseded. Remaining historical phrase checks are packaging/guidance checks, not behavioural proof.
The known `auto_approve false` versus `auto_approve=false` baseline is not changed.

### Tools and local evidence

Context7 CLI is unavailable and the official-docs-fallback skill is not installed. The companion
skill's fallback was used: existing CLI help and official pinned Forgetful `v0.5.5` source confirm
`PlanUpdate.status` for explicit completion when task-driven completion does not occur. Evidence is
`/tmp/factory-7a/forgetful-plan-contract.txt` and `forgetful-doc-revision.txt`. No live native call
or
record access was needed. The cached, previously audited Mycelium 0.4.5 exporter was reused
directly;
registry-offline uvx could not resolve its cache entry, so no install/upgrade was attempted.

Ruff and all three import contracts pass (60 files, 131 dependencies). The seven existing import
proof tests pass, retaining direct/indirect violation checks without changing the dependency graph.
Cached uv_build 0.13.5 builds wheel/sdist offline; all 77 wheel RECORD checksums pass. All 74
package
source/resource files match wheel bytes, all 59 Python test files match sdist bytes, and Python
files
compile in memory. The wheel imports and public init help run directly from its ZIP without install.
Logs: `/tmp/factory-7a/final-{ruff,imports,build,package,package-coverage,wheel-help}.log`.

Mycelium: one nonempty full-detail class diagram, 81 boxes, 12 existing external-base warnings;
3973 test calls and 68 test type relationships filtered. Same-map repeat export is byte-identical.
Mermaid is checked as text, not rendered. No bundled third-party archive was expanded. Map, export
and repeat evidence: `/tmp/factory-7a/final-map*`. Architecture remains below 500 lines.

Full-suite and final documentation evidence are recorded in the handoff below after validation.

### Validated 7A handoff

Final source manifest: `/tmp/factory-7a/validated-source.sha256` (135 files), SHA256
`e8207550129ea6bc995aa9e73e7d2b9e247fab9795625260fc5473f4421953ee`.
`FACTORY.md` still matches the captured user bytes, SHA256
`ad342980f162cc61146ddaffa15267fcc2908ccefff847a362bfba0bf07ebf28`.
The approved completion-detection/cleanup sections above match the initial proposal byte-for-byte.

Full source-defined suites ran sequentially on Python 3.12.16 and 3.13.18 in the frozen private
copy:
each ran 562 cases, with 558 passes, one known baseline guidance failure and three OS-specific
skips.
Times: 367.985 seconds on 3.12; 371.966 seconds on 3.13. All 50 native lifecycle cases passed.
The 3.13 suite uses the existing cached 3.12 import-linter executable for graph checks; its Python
tests and AgentShell processes run on 3.13.
The private copy changes exactly one fixture line: `tests/lifecycle_support.py:97` uses the existing
Nix tmux path instead of `/usr/bin:/bin`. No assertions or product source differ. The exact diff is
`/tmp/factory-7a/validated-fixture.diff`; source comparison is `validated-source-check.log`.

The single failure remains
`test_review_regressions.GeneratedGuidanceTests.`
`test_owner_guidance_uses_explicit_permission_and_its_own_selected_definition`: the historical test
expects `auto_approve false` while the unchanged policy text uses `auto_approve=false`. The supplied
unchanged-HEAD reproduction remains applicable; that expectation was not edited. The three skips
are the existing Ubuntu-24.04-only tmux installation scenarios, listed with reasons in result JSON.
No shutdown timeout recurred in these two runs; the earlier intermittent cause remains unproved.
No full-suite GREEN or coverage claim is made.

Commands and evidence:

```bash
# Interpreter environments reuse existing audited packages; no sync or install.
UV_PROJECT_ENVIRONMENT=/tmp/factory-pi-alignment-YYrJLb/python312 \
  NATIVE_PI_SDK=/home/scott/.pi/agent/install/releases/1.4.0/node_modules/\
@earendil-works/pi-coding-agent/dist/index.js \
  uv run --project /tmp/factory-7a/validated --locked --no-sync python \
  /tmp/factory-7a/test-runner.py --root /tmp/factory-7a/validated --selection all \
  --result /tmp/factory-7a/validated-312-result.json
# Repeat with /tmp/factory-status-python313 and the 313 result path.
```

Runner, exact commands and full result/ID lists are in `/tmp/factory-7a/run-validated-full.sh`,
`test-runner.py`, `validated-{312,313}.log`, `validated-{312,313}-ids.json` and
`validated-{312,313}-result.json`. The runner uses source-defined unittest discovery and records all
selected/excluded IDs. It resets inherited ignored SIGINT before subprocess tests. An initial
background diagnostic without that reset was aborted; its launch context broke signal-based test
teardown, not agreement behaviour. The separately named diagnostic logs remain available.

The first complete attempt found six stale fixture answer streams, in addition to the baseline.
Those old tests ended input after optional prompts; agreement answers could be consumed by earlier
memory/setup prompts. Tests now provide each answer explicitly or preserve intended EOF. Assertions
were not weakened. The six corrections pass in `fixture-corrections-312.log`; the final full reruns
above include them on both Pythons. Earlier `final-*` logs cover the pre-correction test snapshot.

Current Ruff, import, build, package and byte-comparison evidence uses the `validated-*` prefix.
`validated-dist/` contains the rebuilt wheel/sdist; all 77 RECORD checksums, 74 source/resource
files,
59 Python test files and 119 in-memory compilation checks pass. Both Pythons also pass all 12 new
public 7A tests against an unpacked wheel without installing it:
`/tmp/factory-7a/wheel-focused-{312,313}.log`. These include real isolated tmux/fake Pi, no
inference,
and the same one-line host fixture adjustment. Current doc checks are `validated-docs.log`:
472 overview lines, touched Markdown within 100 columns, existing local links and protected hashes.
Current map/repeat evidence is `validated-map*`: 81 boxes, 12 known warnings, 3973 test calls and
68 test type relationships filtered; byte-identical repeat, text inspection only.

7B/7C remain unimplemented. Next work is completed-plan discovery and scoped native Git cleanup,
then multi-repository cleanup/revision-combination trials, adoption reconciliation and explicitly
approved disposable live validation. Agent compliance, hosted CI, parent SQ and independent review
remain unverified. No new subagents were dispatched, so there are no new native subagent session
IDs.


## 7B and automated/local 7C implementation

Scott's later instruction authorized local 7B and automated/local 7C after parent verification of
all 135 files in the 7A source manifest. This supersedes the earlier 7A-only boundary for local
implementation. The approved completion-detection/cleanup contract above and protected `FACTORY.md`
are unchanged. No live factory, DinoLand, credential, global setting or pipeline was changed. No
package was added/upgraded/installed, wheel installed, commit made or push performed. SQ and the
single independent Opus review are left to the parent after combined-source validation.

### Implemented responsibilities

- A separate `CleanupCompleted` workflow polls complete native inventory and full plans at startup
  and each cycle, before unfinished recovery/intake. Full completed status is authoritative; neither
  summary status, Markdown, issue closure, archive nor a historical marker grants disposal.
- Shared `FactoryRecords` extracts existing context/snapshot/ownership/mapping/repository checks
  from scaffolding. Intake and cleanup share validation without making `ScaffoldIssue` a general
  lifecycle manager. Git adapters do not fetch plans or decide completion.
- Full ownership tasks establish mappings and available competing claims across visible plans.
  Missing ownership blocks its plan; path/ref/target collisions block affected resources.
  Compare actual common Git directories for shared local refs, and canonical GitHub work sources
  for shared remote refs. A readable local namespace protects claims even with a wrong origin.
  Review correction: unreadable/invalid claim-bearing records or required namespaces block all
  disposal for that cycle, not ordinary safe intake. Do not drop failed records from the claim
index.
- New ordinary intake records target_branch from the main checkout's symbolic branch and places
  work beneath that repository's `.factory/worktrees/`. An unreadable initial target pauses fresh
  intake before any write and recovers after repair. Owners record epic/actual retargeted PR
  targets. New ordinary trees get a local `.gitignore` containing `*`, preserving any existing
  file. Workspace ignore rules do not cover secondary repositories. Cleanup requires reviewed target
  identity, without imposing a schema on the human DoD Markdown.
- Git validates canonical roots/paths, exact fetch AND push destinations, protected branch names,
  native registration/common gitdir/backlink, actual root/branch and absence. Locks, symlink
  escapes, occupied/prunable paths and mismatched identities are not forced. Nested registered
  trees and any configured main checkout, including independent clones, are protected.
- Remove exact worktree with one force for disposable contents, then local feature branch, then
  exact remote feature ref. Respect checked-out-elsewhere refusal, including registered symbolic
  branches with an already-deleted local ref. Confirm local absence before remote removal, and all
  remaining facts before reporting success. Extra commits, dirty/untracked/ignored files are
  allowed.
- Failures/timeouts may follow actual writes. Later cycles/restarts reread state; no rollback,
  recreation, reopening, marker mutation, transaction journal, generic clean/prune/reset, process
  scan/use-lock/signal or repeated merge check is added. Setup and role guidance now explain actual
  disposal. Neither owner nor Foreman deletes resources; Foreman still owns completion.
- Historical open-plan pending/removed checks remain read-only. Completed old mappings can finish
  actual local/remote disposal despite those markers. Native remote absence is independently read.
  Before live adoption, review eligible older completed plans, actual targets/paths/ownership and
  edited guidance with Scott. Nothing was silently adopted or deployed by this local work.

See [the cleanup ADR](../adrs/completed-plan-cleanup.md) for structure, checks and known limits.
Checks are targeted native operations, not an atomic transaction. Completion forbids concurrent
resource reuse; no claim is made that cleanup proves all agents exited or prevents a concurrent
repository/path replacement between its reads and writes.

### Public-boundary TDD and regression changes

All new cases use public setup/watch and actual native Git under disposable fixtures. The external
Forgetful/provider programs expose native tool contracts; query summaries omit ownership text.
A disposable SSH transport routes only fixture repositories to native Git upload/receive-pack and
actual bare remotes. It cannot reach DinoLand or a live GitHub repository. The general watcher
fixture now explicitly disables SSH/network prompting unless a test supplies this local transport.

RED/GREEN logs live in `/tmp/factory-7bc/`. The initial behaviour failed because no cleanup ran.
Subsequent tracer tests found/fixed unmanaged paths, contradictory saved issue identity, overlapping
ownership, stale completion during reads, separate push destinations, another mapping's protected
target, embedded-NUL service paths, absent-but-registered branches, unconfirmed local-ref deletion,
individual record failure isolation, summary-hidden completion, unreadable duplicate identity and
pre-write target-read classification. Final probes also found/fixed secondary-root ignore rules,
shared remote refs across independent clones, shared local refs across linked roots with distinct
or wrong origins, and a configured independent checkout nested in disposable contents. Earlier
fixtures used one local root per source and did not expose those shared-namespace risks. These
public regressions now inspect native Git and filesystem state, not helper internals. Recovery
probes already passed with the existing observed-state implementation: no extra cleanup journal or
watcher policy machinery was needed.

Three existing regression assumptions needed deliberate changes:

- Five intake-only tests now stage archived-to-active instead of completed-to-active. This keeps
  exclusion from startup recovery without authorizing disposal or reusing completed work.
- Three manual-pause tests previously required the complete native call-log bytes not to change.
  They now prove saved plans/tasks AND all create/update calls are unchanged, while permitting
  mandatory independent completed-plan polling during the intake pause.
- Missing-plan recovery still reports its absent pinned identity and never writes. Its old exact
  full-read count now permits/proves independent discovery reads; saved records and write-call
  equality remain asserted. Dedicated cleanup tests cover both stale-summary directions.

These changes are not agent-compliance phrase tests. The historical auto-approval wording assertion
is untouched. Failure blocking, evidence interpretation, real follow-up reuse and policy-change
conversations remain model-guided and need separately approved live trials.

### Validation and handoff

Final source/test/resource identity, exact commands, RED/GREEN logs, supported-interpreter full
results, package/compile/import checks and map repeat-export are in the combined handoff:
`/tmp/factory-7abc-handoff.md`. The validation artifact root is `/tmp/factory-7bc/`.
The full-suite source copy differs only in native tmux discovery, as documented below; no assertion
is changed in that copy. The known baseline wording failure and existing OS skips are reported
explicitly, not described as a GREEN full suite. Definitive evidence follows.

The combined canonical manifest is `/tmp/factory-7bc/verified-source.sha256`: 139 files, SHA256
`f05bf0658c5e9fe32719c92d410960438e90994782960cc9a108b00323467b52`. The execution copy is
`/tmp/factory-7bc/verified-source/`. Earlier final/delivery prefixes are preliminary snapshots.

- Python 3.12.16: 598 selected, 594 pass, one known failure, three OS skips; 462.008 seconds.
- Python 3.13.18: 598 selected, 594 pass, one known failure, three OS skips; 465.568 seconds.
- All 50 native lifecycle cases passed on each interpreter; no exclusions or errors.

The sole failure remains the existing auto-approval wording assertion in
`tests/test_review_regressions.py:379`: `auto_approve false` versus `auto_approve=false`.
The three skips are existing Ubuntu-24.04-only tmux installer tests. Result/ID JSON and full logs:
`/tmp/factory-7bc/verified-{312,313}-{result,ids}.json` and `verified-{312,313}.log`.
The private copy changes only `tests/lifecycle_support.py:97` native tmux discovery from
`/usr/bin:/bin` to the existing `/home/scott/.nix-profile/bin`; no assertion changes.
`verified-source-fixture.log` and `verified-fixture.diff` record the byte comparison and exact diff.
The runner restores ordinary SIGINT handling for subprocess fixtures.

The final focused source run passed 101 tests. All 48 combined new tests passed on both interpreters
from unpacked wheel imports/resources, without installation: `verified-wheel-focused-*.log`.
Offline wheel/sdist checks verify 79 wheel checksums, all 76 package files against the wheel, all
139 manifest members against the sdist (including native JS fixtures), and compilation of 123
Python files. Ruff passes; all three import contracts hold across 62 files/144 dependencies; seven
architecture proof tests pass. Logs use the `verified-*` prefix under `/tmp/factory-7bc/`.

The final cached Mycelium 0.4.5 map has 85 boxes. Test filtering removes 4575 calls and 71 type
relationships. Twelve existing external-base warnings remain. Raw and normalized repeats are
byte-identical; only two source-index prose entries were wrapped for width. The overview is 497
lines. Mermaid was checked as text, not rendered. Protected intent/approved prose, Markdown width,
local file links, canonical source identity and `git diff --check` pass.

Live deployment/deployed-E2E combinations, actual agent compliance, older completed-plan adoption
and disposable live delivery are deferred. Parent arranges actual SQ on the combined frozen source,
then one independent Claude Opus review. No reviewer or SQ job was launched in this delegated scope.

### Parent SQ correction: ready for rescan

Parent verified the 139-file f05bf065 manifest and protected intent, ran actual SonarQube analysis
`ecffb889-18f8-4af2-9e93-e30a5da43a21`, and fetched all 26 changed Python files from the server.
Their contents matched except terminal newlines. CE succeeded; the assigned gate failed for five
maintainability findings: four duplicated literals and agreement-entry cognitive complexity 16/15.
There were no bugs, vulnerabilities or hotspots; no coverage was imported. The existing gate is
`Sonar way sans code coverage`; its separate `caycStatus` is `non-compliant`. Binary-ZIP encoding
and missing-blame warnings remain recorded. Parent evidence is in
`/tmp/factory-7bc/sq-results-1.json`,
`sq-inspection-1.log` and `sq-scan-1.log`.

Only two Python files changed from that verified source. `git_worktrees.py:7-10` now names the exact
existing absolute-path option, branch-ref prefix, Factory directory and refname format as module
constants. `cli/definition_of_done.py:57-81` extracts the deployment prerequisites/agreement
section.
The entry point at lines 9-54 retains preservation, discussion/no-file routing, proposal,
confirmation and concurrent-save safeguards. No prompt, Markdown, path, Git argument, setup or
cleanup behavior changes. No rule/gate/exclusion/configuration change, suppression, test weakening,
dependency or generalized policy engine was added.

The artifact root is `/tmp/factory-7bc/sq-refactor-1/`. Before and after the refactor, all 48 public
Slice 7 tests passed on both Pythons; tests and packaged resources remain byte-identical to
f05bf065.
Static AST expansion also reproduces the original adapter and agreement bodies; this supports the
refactor review and does not replace public tests. The corrected-source full outcomes are:

- Python 3.12.16: 598 selected, 594 pass, one known failure, three OS skips; 453.437 seconds.
- Python 3.13.18: 598 selected, 594 pass, one known failure, three OS skips; 453.594 seconds.
- All 50 native lifecycle cases passed on each interpreter; no exclusions or errors.

The same baseline wording failure and the same three Ubuntu-24.04-only skips remain explicit;
full suites are not GREEN. All 598 IDs match the previous selection, with native SDK enabled
without inference. Logs and machine outcomes are `full-{312,313}.log` and
`full-{312,313}-{ids,result}.json` under the artifact root. The private source copy retains only
the approved native tmux lookup substitution at `tests/lifecycle_support.py:97`; no assertions
change.

The new canonical manifest is `source.sha256`, 139 files, SHA256
`b9ebbeb4fc798e33120741369fc211674e2fe1f45e7fd93ec7132e712163d614`; execution copy: `source/`.
Earlier source manifests, evidence and packages remain unchanged. The earlier handoff is preserved
as `handoff-before.md`; the updated combined handoff remains `/tmp/factory-7abc-handoff.md`.

Ruff passes; all three import contracts hold across 62 files/144 dependencies; seven boundary proof
tests pass. All 48 combined tests pass from the unpacked corrected wheel on each Python, without
installation. Offline build checks verify 79 wheel checksums, all 76 package members, all 139
manifest members in the sdist (including native JS fixtures) and compilation of 123 Python files.
The cached Mycelium refresh keeps 85 boxes, 4575 test calls/71 type relationships filtered and the
12 existing external-base warnings. Raw and normalized repeat exports match. Only relevant source
anchors changed in the 497-line overview; ADR anchors needed no change. Mermaid was checked as text,
not rendered. Protected intent/approved prose, width/local file links and diff checks pass.

This snapshot is ready for the parent's new rescan, then the single independent Opus review.
Neither was launched by this worker, and no new gate pass or review approval is claimed. Live
adoption/model-following/deployment/E2E gates remain deferred. No live change, installation,
dependency upgrade, credential read, global setting change, commit or push was performed.

## Opus review corrections: held decisions

Independent review requested changes (session `b184cf5e-a2c7-46e9-8b5a-74bff18f8a4b`). The previous
b9ebbeb4 source passed the parent's actual SQ analysis `fb0d9846-6186-4234-9f21-3fe369a7d9a0`;
that scan is stale after these corrections. No new reviewer or SQ scan was launched by this worker.

The current artifact root is `/tmp/factory-7bc/review-fixes-1/`; earlier handoffs/evidence remain
preserved. Public CLI tests independently reproduce claim loss, in-run human-ref deletion, redundant
Git/default reads, suppressed cleanup alert episodes and repeated post-write target discovery.
`f1-*-red.log`, `f2-run-red.log`, `f3-cache-red.log`, `f5-red.log`, `f6-red.log`, `f7-red.log`,
`f9-red.log` and `f10-red.log` record pre-fix failures; matching GREEN logs record scoped fixes.
`f1-final-read-red.log` additionally catches a claim read failing during the final check before
another plan's disposal. This now stops the remainder of that cleanup cycle.

- F1: incomplete full-plan/task/claim/namespace evidence withholds all disposal. Native issue intake
  can still progress. Missing targets are unknown claims, not records to silently ignore.
- F2: confirmed mapping/finished-plan sets prevent in-run retries and preserve fresh human refs.
  Durability is HELD: `f2-restart-held.log` independently proves the new watcher still deletes those
  human refs. Proposed per-plan final records need explicit approval, and do not by themselves
  preserve partial-mapping confirmations across restart. No schema, receipt or journal was added.
- F3: no claim/Git index without an unconfirmed selected completed candidate; each root's advertised
  default read, including a failure, is cached once per cycle. Finished plans incur no later cleanup
  Git calls. Bounded fair retries are HELD: the proposed one-mapping round-robin policy is not
  approved or implemented. Multiple slow roots can still delay intake; no cycle-time bound is
claimed.
- F4: Foreman appended guidance now requires deployment/E2E only when the human agreement does.
  Source guidance was audited for this contradiction. This is not a model-following proof.
- F5: cleanup inventory uses a distinct subject/code/scope and clears its own episode on recovery.
  Startup shared outages can truthfully send both cleanup and factory-intake notices. Existing tests
  now check the two exact episodes, retaining no-write, identity, raw-diagnostic and recovery
checks.
- F6: carry validated preflight mappings through the planning writes. No second target discovery
  after plan creation; actual worktree creation checks remain.
- F7: missing-link simulation stays fail-closed, with precise user-approved targeted native repair
  guidance. It is not a real crash reproduction or a universal autonomous-recovery claim.
- F8: repair guidance names reviewed `target_branch` and strict owning-repository Factory paths.
  Legacy approved repair remains readable; no automatic target guess/backfill is introduced.
- F9: EOF explains terminal agreement and saved-setup `init --finalize`, without a policy default.
- F10: only cleanup networking closes stdin and disables interactive credentials/SSH prompts.
  Preserve effective SSH commands/configuration and native interactive OAuth. Read timeouts are
  distinct from uncertain writes. Tests exercise both inherited prompt settings and configured SSH.

The old invalid-full-task test's expected independent disposal was wrong: the unreadable task can
hide a claim. It now proves global withholding, native preservation and identity-bearing alerts.
Duplicate-reference/unreadable-detail and incomplete-inventory tests assert the corrected diagnostic
and separate episodes; they do not accept disposal or weaken saved-state checks. One new EOF test
covers the user-visible repair message. The unchanged auto-approval wording failure is still
explicit.

Current source freeze and final validation outcomes are recorded below when available. No live
factory/DinoLand/Forgetful/GitHub/pipeline changes, adoption, install, dependency change, credential
read, global setting change, commit or push is authorized or performed. All scratch evidence stays
outside the repository. The protected intent and approved cleanup prose remain byte-identical.

### Corrected freeze and final validation

Here `$R` is `/tmp/factory-7bc/review-fixes-1/`; `$F` is `$R/final/`.

The current canonical manifest is `/tmp/factory-7bc/review-fixes-1/final/source.sha256`, 140 files,
SHA256 `c766d6edb4eef5ae1474a6a5bfd8b7c0d3ffda4e03adbe7b18518254b4ea6f63`.
This includes new/untracked files. `source/` beside that manifest is the execution copy; the only
private delta remains the native tmux-discovery path substitution. Earlier `review-fixes-1/source/`
and `pre-width/` artifacts are preliminary, not this freeze. Final full outcomes are:

- Python 3.12.16: 614 selected, 610 pass, 1 failure(s), three OS skips; 478.992s.
- Python 3.13.18: 614 selected, 609 pass, 2 failure(s), three OS skips; 492.410s.
- All 50 designated native lifecycle cases passed per interpreter, SDK enabled without
  inference; no exclusions or test errors. This does not erase the additional plain-watch
  shutdown failure on Python 3.13.
- All 64 public Slice 7/review tests passed from the unpacked final wheel on each Python
  (96.917s / 98.392s), without installation.

The Python 3.13 run additionally failed
`test_watch_status_review.PlainWatchAdmissionTests`, method
`test_uncertain_owner_refusal_preserves_prior_plain_discovery`.
Its arrangement failed to stop the first plain watcher: a 15s shutdown timeout, with
`KeyboardInterrupt` reported as ignored in `Popen.__del__`, before the refusal assertions ran.
This is not declared pre-existing or dismissed as harmless. Five unchanged targeted reruns on each
Python passed on both b9ebbeb4 and the final source (20 passes total), with native SDK enabled;
`$R/shutdown-{before,after}-{312,313}.log`. They do NOT replace or clear the recorded full-run
failure.
No out-of-scope lifecycle code/fixture fix or test weakening was made. Parent needs to decide its
investigation/disposition. The preliminary d00e8d14 full runs had only the known wording failure;
they do not supersede this final-source result.

The first background held-restart attempt inherited ignored SIGINT and failed fixture shutdown;
`$F/f2-restart-held.log` and `$F/completion.txt` retain that runner failure. The scratch
reproduction
runner was corrected to restore ordinary SIGINT, as the full-suite runner already does. The valid
current-source reproduction is `$F/f2-restart-held-foreground.log`: both new refs exist before
restart and both disappear afterward. No production or canonical fixture was changed for this.

The combined handoff is `/tmp/factory-7abc-handoff.md`, with adjacent checksum. RED/GREEN and native
process-count evidence remain under the review artifact root. Source, metadata and document
manifests identify the final handoff. Ruff and three import contracts pass (62 files/145
dependencies);
all seven architecture proof tests pass. Offline package checks verify 79 checksums, 76 canonical
package files, all 140 manifest members in the sdist and compilation of 124 Python files.

Mycelium 0.4.5 exports repeat identically: 86 boxes including a new module container (no new
production class), 4747 test calls/72 type relationships filtered and 12 known external-base
warnings.
The overview is 499 lines; source anchors and cleanup ADR describe in-run confirmation, global claim
withholding, noninteractive networking, operator repair and the held durability/work-bound
decisions.
Mermaid is checked as text, not rendered. Protected intent/approved prose, 100-column width, local
links and diff checks pass. No new reviewer/SQ/live operation, installation or dependency change,
commit or push was performed. This remains an interim correction handoff, not completion/approval.


## Approved receipts, scheduling and watch stop

Scott approved all three follow-ups after the c766d6ed handoff and the independent shutdown
investigation. Earlier held-policy and unsafe-restart statements above describe that historical
source, not the approved implementation now in progress. The former per-plan-only proposal is
superseded: each worktree/local-branch/remote-ref set confirms independently.

- Implemented a `CleanupReceipts` port and private `.factory/cleanup-finished.json` storage.
  Only native final absence proof permits a terminal entry; persist/fsync before success reporting.
  Pending sets reserve names and reread native resources after interruption/write failure. Terminal
  sets survive restart/sibling failure and protect later human reuse. Invalid or unreadable storage
  blocks all disposal while safe issue intake continues. No step journal or native marker mutation.
- Implemented at most one pending set attempt per cycle, with a run-local round-robin cursor that
  advances on failure. Keep global unknown-claim withholding, namespace protections, default caching
  and per-command timeouts. No claim index without pending candidates; no cleanup Git for terminal
  sets. The bound is on attempts, not inventory cost or total wall-clock time.
- Implemented watch-scoped stop intent before SIGINT/SIGTERM raises KeyboardInterrupt. Normal-flow
  checks after native helpers and before writes/delivery/waits preserve the request if CPython
  discards the exception in a finalizer. Signal handlers are restored; setup/OAuth and managed-only
  controls retain their prior scope. Finally-based owned close is not blocked by the stop latch;
  borrowed close still releases only its channel. CPython's unraisable diagnostic is not suppressed.

The public tests use disposable native CLI/provider fixtures, real Git/bare repositories and
controlled actual Popen finalizer timing. They do not replace Popen, product handlers or OS signals.
Each stop case sends exactly one signal and requires exit 130, owned Foreman close, no issue
submission and truthful saved status. Ordinary-call controls and both signals remain covered.

Evidence is under `/tmp/factory-7bc/approved-fixes-1/`; continuation evidence uses `resume-1/`.
Original RED/GREEN and full-run failures remain untouched. The first stop-test RED also had an
incorrect historical-status assertion; `stop-corrected-red.log` corrects that test before product
changes and isolates the two actual finalizer failures. Legacy removed/pending cases now use
separate fresh fixtures and wait for durable confirmation; recreating disposable refs after a
confirmed cleanup would contradict the newly approved terminal-authority rule. No assertion about
native facts or unchanged ownership evidence was removed.

Final source identity, complete interpreter/wheel/lint/import/package/map checks and limitations
will be recorded in the combined handoff. No installation, dependency change, live operation,
commit/push, extra reviewer or worker SonarQube scan is authorized. Parent runs the final actual
SonarQube analysis on the verified new freeze. Live adoption/model/deployment/E2E trials remain
open.


The startup extension of the deterministic signal test found a remaining gap: handlers were
installed after `build_watcher`, whose GitHub readiness check already runs a native process.
`resume-1/stop-startup-red.log` proves SIGINT could be discarded there; SIGTERM used the default
termination instead of the watch cancellation path. Install both handlers before that build,
inside the same watch scope. Eight timing cases now pass on both interpreters, including startup
without launching Foreman, ordinary calls, and completed Git/Forgetful finalizers. This adds no
new lifecycle ownership path. The first full runs under `validation/` cover the earlier candidate;
a second frozen candidate must complete full validation before the final handoff.


### Approved correction validation and final source

The approved three-item implementation is complete locally. Final canonical source/test/resource
manifest: `/tmp/factory-7bc/approved-fixes-1/final/source.sha256`, 146 members, SHA256
`1f476555e4d3d0bd1caf531a9629e791bae14fa2a23ee55a9b943a0965645bad`.
The full-suite execution copy under `validation-2/source/` matches every canonical member except
one disclosed private fixture lookup: native tmux uses `/home/scott/.nix-profile/bin` instead of
`/usr/bin:/bin`. The final canonical snapshot has no fixture modification. No test is excluded.

- Python 3.12.16: 631 selected, 627 pass, one known failure, three OS skips; 558.280s. All 50 native
  lifecycle cases pass, no exclusions/errors.
- Python 3.13.18: 631 selected, 627 pass, one known failure, three OS skips; 564.295s. All 50 native
  lifecycle cases pass, no exclusions/errors.
- Unpacked wheel: 81/81 pass per interpreter, no skips/errors/failures; 122.206s / 123.200s. SDK
  enabled without inference; no installation.

Full logs/selected IDs/results: `/tmp/factory-7bc/approved-fixes-1/validation-2/`.
Wheel logs/results/package hashes: `/tmp/factory-7bc/approved-fixes-1/package/`.
All eight deterministic one-signal cases pass on both interpreters, including native startup,
Git/Forgetful completed finalizers, ordinary-call controls and both SIGINT/SIGTERM. The former
plain-watch admission shutdown case also passes in both full runs. CPython's unraisable diagnostic
is not suppressed; historical c766 failures remain failures in their original evidence.
The known unchanged auto_approve wording assertion is at `tests/test_review_regressions.py:396`.
The three skips retain their Ubuntu-24.04-only installer reasons. These full suites are not GREEN.

Ruff and all three import contracts pass (65 files/159 dependencies); seven architecture proof
cases pass. Wheel checks validate 82 RECORD checksums, all 79 canonical package files, all 146
source/test/resource members in the sdist and compilation of 130 Python files. The sdist README
matches byte-for-byte; its reformatted TOML has equal parsed values. uv.lock/docs are not sdist
members and have separate canonical metadata/document manifests. No installation was performed.

Mycelium 0.4.5 was reused from its existing cache: 92 boxes, one full-detail diagram, 4870 test
calls/76 type relationships filtered, 13 known external-base warnings. Same-map exports match;
only overlong source-index prose is wrapped. The overview is 499 lines. Mermaid is checked as
text, not rendered. Source anchors, 100-column prose/code, local links, original approved cleanup
prose and FACTORY.md byte preservation are checked. No runtime dependency or tool was upgraded.

The first 877c34a9 candidate's complete 629-case runs are retained under `validation/`; they
precede the startup signal extension and do not validate the final source. Final runs were queued
on those exact owned PIDs, then wheel checks followed final full runs; no duplicate full suites
ran concurrently. Added/replaced test IDs are recorded in the final evidence. Final validation
prose is added after testing; source/resource hashes and README/configuration metadata stay fixed.

The combined handoff is `/tmp/factory-7abc-handoff.md`, with adjacent checksum, the full F1–F10
resolution list, line anchors and exact validation identities. Parent still runs actual SQ on this
freeze and decides review closure. No release, independent approval, hosted CI, coverage, live
adoption, model compliance, deployment/E2E trial, commit or push is claimed. Preserve durable
receipt
storage; its local filesystem/trusted-data limits and explicit old-plan adoption remain in the ADR.


## Parent SQ maintainability correction

Parent verified the 146-member `1f476555` snapshot, metadata/docs and protected intent, then ran
actual SonarQube analysis `b22d7d73-141f-4728-848e-05214f4c712f`, CE task
`ef398eb6-1364-4ec6-bbb3-3eda3458e278`. CE succeeded; the assigned gate failed on four
maintainability findings. No bugs, vulnerabilities or hotspots were reported. No coverage was
imported; the separate `caycStatus` is non-compliant. Parent verified the server source for all 38
changed Python files against canonical source, apart from terminal-newline normalization.
Evidence remains `/tmp/factory-7bc/sq-results-3.json`, `sq-inspection-3.log` and `sq-scan-3.log`.

The authorized correction changes only three Python files, without changing behavior:

- S1192: give the three identical receipt-alert subjects one meaningful module constant.
- Two S1172 findings: keep the required two-argument signal callback, explicitly naming its unused
  inputs `_signum` and `_frame`. No fake reads, warning suppression or lost callback arguments.
- S5899: `CleanupReceiptFixture.prepared` is used by five inherited calls in six receipt tests.
  It is not an unused or undiscovered test. Extract the same arrangement into the ordinary
  module function `prepare_completed_set(fixture)` and call it explicitly at those five sites.
  Do not turn the helper into an automatically discovered test or drop its behavior/assertions.

All 68 public cleanup/scheduling/stop tests pass before and after on Python 3.12 and 3.13, including
all eight deterministic one-signal cases. All 631 discovered test IDs and 50 native cases are
unchanged. Supplemental AST comparison proves equivalence after only the constant substitution,
the two parameter names and the receiver/helper-call extraction. No artificial RED is needed for
these behavior-preserving refactors. Existing RED evidence remains untouched.

New evidence uses `/tmp/factory-7bc/sq-refactor-2/`; earlier `1f476555` evidence is immutable.
A new source freeze, complete dual-interpreter/native/wheel validation and package/map/document
checks are required. Parent will rescan that new identity. No worker SQ or additional reviewer is
authorized. F1–F10 are implemented with their documented limits, not independently approved;
local checks do not grant release/live-adoption approval or erase the baseline wording failure.


### Maintainability correction: verified new freeze

All four requested source corrections are implemented; parent rescan is pending, not approved.
The new 146-member canonical source/test/resource manifest is
`/tmp/factory-7bc/sq-refactor-2/final/source.sha256`, SHA256
`191cc46edd9f810370f86d0a0175277dd7e2d1ff14c03c163af5373c4c22d003`.
Only cleanup_completed.py, watch_stop.py and test_cleanup_receipts.py differ from 1f476555.
No test ID changed: no helper became a test and no case/assertion was removed or weakened.

- Python 3.12.16: **631 selected, 627 pass, one known failure, three OS skips**; 507.834s. All 50
  native lifecycle cases pass; no exclusions/errors.
- Python 3.13.18: **631 selected, 627 pass, one known failure, three OS skips**; 514.262s. All 50
  native lifecycle cases pass; no exclusions/errors.
- Python 3.12.16: **81/81 unpacked-wheel cases pass**, no errors/skips/failures; 122.048s. SDK
  enabled without inference, no installation.
- Python 3.13.18: **81/81 unpacked-wheel cases pass**, no errors/skips/failures; 123.008s. SDK
  enabled without inference, no installation.

Logs and result identities are under `/tmp/factory-7bc/sq-refactor-2/validation/` and `package/`.
Before/after focused logs each pass 68 cases, including all eight deterministic one-signal cases,
with identical IDs on both interpreters. AST equivalence is supplemental. No artificial RED was
created for this pure refactor. All 631 full IDs and 50 designated native cases are unchanged.
The sole baseline failure remains at `tests/test_review_regressions.py:396`; three Ubuntu-24.04-only
installer skips retain their reasons. Full suites are not GREEN. The private native-tmux fixture
lookup remains the sole execution delta, disclosed in fixture.diff.
Canonical fixtures are unchanged.
Native SDK checks use no inference. No old full-run failure or 1f476555 artifact is overwritten.

Ruff and three import contracts pass (65 files/159 dependencies); all seven architecture proof
cases pass within each full run. Package checks verify 82 RECORD hashes, 79 canonical package files,
all 146 members in the sdist and compilation of 130 Python files. Sdist README bytes and parsed TOML
match canonical metadata; uv.lock/docs have separate manifests and are not sdist members.
Mycelium 0.4.5 cached exports repeat identically: 92 boxes, one full-detail diagram,
4870 test calls/76 type relationships filtered, 13 external-base warnings. The overview stays at 499
lines.
Mermaid is checked as text, not rendered. Width, links, protected prose, FACTORY.md and diff checks
pass. No dependency/tool installation or upgrade is made.

The combined handoff `/tmp/factory-7abc-handoff.md` contains exact fixes, F1–F10 implementation
closure, source anchors, results and limits. Parent owns the next actual SQ analysis and review
closure. No worker SQ/reviewer, release/final approval, hosted CI/coverage, live adoption, model
compliance, deployment/E2E operation, commit or push is claimed. The previous actual SQ remains a
failed gate on 1f476555 with separate non-compliant CayC status and no imported coverage.

## Parent final local validation

This entry supersedes earlier pending-scan and held-decision entries; their evidence remains
historical. The final source manifest contains 146 source/test/resource files:
`/tmp/factory-7bc/sq-refactor-2/final/source.sha256`, SHA256
`191cc46edd9f810370f86d0a0175277dd7e2d1ff14c03c163af5373c4c22d003`.
Parent verified every member before and after the scan, plus metadata, documents and protected
FACTORY.md bytes. This closing plan update changes documentation only, not the scanned source.

- Actual SQ analysis: `083634d8-0664-452f-8c44-c2e468734377`.
- Compute task: `e44e9aed-7d10-4260-9148-a452f863688a`, status `SUCCESS`.
- Assigned gate `Sonar way sans code coverage`: `OK`; zero unresolved issues or hotspots, bugs,
  vulnerabilities or code smells. No coverage was imported; separate `caycStatus` remains
  `non-compliant`. Rules, exclusions and gate settings were not changed.
- Build string binds the manifest above. Parent retrieved all 38 changed Python files from SQ
  and matched canonical content, apart from terminal-newline normalization.
- Evidence: `/tmp/factory-7bc/sq-results-4.json`, `sq-inspection-4.log` and `sq-scan-4.log`.
- Parent checked both full-run result records: 631 selected, 627 passed, one unchanged wording
  failure and three existing OS skips per interpreter; no excluded IDs. All 50 native lifecycle
  cases and 81 unpacked-wheel cases passed on each interpreter. The private Nix tmux lookup
  adjustment remains disclosed above. These results are not a full-suite GREEN or hosted CI.

One independent Opus review was performed before corrections. Implementation supplied fixes and
public regression evidence for F1–F10, including the approved durable per-set receipts and fair
scheduling. The lost-stop defect has eight deterministic one-signal cases passing on both
interpreters. Parent accepts those implementation dispositions for this local handoff on the
recorded evidence. No second reviewer pass, substitute owner code review or independent approval
of the corrected snapshot is claimed.

Live adoption, old completed-mapping review, model compliance, deployment/E2E and deployed
multi-repository verification remain separate work requiring authorization. Preserve receipt
storage; unfinished names remain reserved, and partial native removal can require targeted
operator-approved recovery. No installation, live operation, dependency change, commit or push
was performed. Local implementation and validation are complete with the stated baseline failure
and live-validation limits, not release approval.

## Research cwd guidance correction

The approved narrow follow-up updates Foreman startup/maintenance and feature-owner templates.
Starter research retains configured role cwd and native instructions; calls omit a cwd override and
pass absolute repository/worktree and AGENTS.md paths for read-only inspection. Implementation and
review worktree rules apply to those responsibilities. Custom valid definitions stay authoritative;
a conflicting call alone cannot authorize removing cwd. Genuine conflicts go through maintenance.
Native permission defaults and liveness/no-concurrent-resume safeguards are unchanged. See the
[delivery ADR](../adrs/feature-delivery.md#role-configuration).

Approved seams: public setup's delivered guidance/configuration and native dispatch. One new setup
regression was RED before template changes (four missing-guidance/example assertions), then GREEN.
An initial test-authoring key error was corrected before the recorded RED; it was not a product
failure. Guidance assertions check delivered content, not model compliance. The existing native
dispatch test now includes a renamed research entry, no cwd override, rejection of a conflicting
override, preserved definition bytes, and actual role cwd. Real SDK instruction loading at that
observed cwd retains role AGENTS.md content. Implementation/review still receive assigned worktrees;
existing session/permission checks pass. Native characterization was already GREEN without a runtime
fix. Child CLIs are controlled protocol doubles; this is not a live Pi/model instruction-following
trial or proof of full native child inference behavior.

Evidence directory: `/tmp/factory-research-cwd.zJzf3c`. Python 3.12.16 and AgentShell 0.5.0 use an
existing cached environment; the repo venv points to a changed system interpreter. No installs,
dependency changes or runtime configuration changes were made. Exact test commands (same setup
command for RED and GREEN):

```bash
export UV_PROJECT_ENVIRONMENT=/home/scott/.cache/uv/archive-v0/_9Pvk6v2zG3ZkCMG
export PYTHONPATH=src:tests
uv run --offline --no-sync python -m unittest \
  test_factory_maintenance.FactoryMaintenanceTests.\
test_setup_delivers_cwd_guidance_consistent_with_starter_definitions -v
export NATIVE_PI_SDK=/home/scott/.pi/agent/install/releases/1.4.0/node_modules/\
@earendil-works/pi-coding-agent/dist/index.js
uv run --offline --no-sync python -m unittest test_native_workers -v
uv run --offline --no-sync python -m unittest \
  test_factory_maintenance test_worker_setup test_native_roles test_native_workers -v
.venv/bin/ruff check tests/test_factory_maintenance.py tests/test_native_workers.py
```

Logs: `red-setup.log`, `green-setup.log`, `native-dispatch.log`, `focused.log`, `ruff.log`.
All 22 focused cases pass without skips; Ruff passes. The cached Context7 CLI supplied official
Pi v1.4.0 SDK documentation (`context7-sdk.log`). No new dependency or supply-chain intake occurred.
Mycelium 0.4.5 was reused from its audited cache: 92 boxes, one full-detail diagram, 4873 test calls
and 76 type relationships filtered, 13 unchanged external-base warnings. Repeat exports match;
only test-filtering counts changed. Mermaid was checked as text, not rendered. Architecture remains
499 lines and within 100 columns. Map extraction does not expand bundled third-party archives.

Protected `FACTORY.md` SHA256 before and after:
`ad342980f162cc61146ddaffa15267fcc2908ccefff847a362bfba0bf07ebf28`.
DinoLand instructions/configurations were only read and hashed. Its research agent.json remains
`d38b3857df7e45ac6a1e5fd88c0899488b37519aca4c8104490bdc27b63bce9a`.
The worker supplied precise guidance-only patch hunks without editing live copies. The parent then
repeated all 22 focused checks successfully and applied those three hunks to DinoLand's Foreman
AGENTS.md, maintenance skill and owner skill. Prewrite comparisons, reverse-patch checks and agent
configuration hashes confirm the narrow patch and unchanged settings. Existing custom text remains,
including a pre-existing 104-column repository URL; all added lines are within 100 columns. Parent
backups and validation are in `/tmp/factory-research-cwd-guidance.OOoe1e`. Fresh-session model
compliance remains untested; this patch is not broader Slice 7 installation or adoption.
No watcher/owner restart, external planning mutation, inference trial, second review, commit or push
was performed. The expensive full Slice 7 suite was not rerun. Its known `auto_approve false` versus
`auto_approve=false` wording failure and native tmux fixture/Nix path limitation remain unchanged.
