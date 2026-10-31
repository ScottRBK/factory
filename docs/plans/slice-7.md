# Slice 7: deployed E2E verification and automatic cleanup

Status: planned; no Slice 7 implementation or live cleanup is authorized by this document.
Back to [plan](../plan.md), [architecture](../architecture.md) and [intent](../../FACTORY.md).

## Outcome

A merged feature is complete only after the intended revisions are deployed to the E2E environment
and the deployed E2E tests pass. Foreman verifies that evidence and completes the Forgetful plan.
Factory then deletes that plan's worktrees, local feature branches and remote feature branches.

Plan completion is the cleanup authority. Cleanup does not ask the feature-owner to act, prove
process exit, repeat merge verification or decide whether local files are worth retaining.

This follows `FACTORY.md:144–153` and replaces the earlier owner-led cleanup proposal. Existing
Slice 6 cleanup records and guidance remain implemented behaviour until this slice replaces them.
The watch-status fix is separate work; this slice must not change its lifecycle or health contract.

## Agreed MVP decisions

- CI/CD deploys and runs E2E; Foreman verifies the results. Factory is not a deployment engine.
- Verify the actual merged revision, not an earlier feature head or PR synthetic merge commit.
- For multiple repositories, verify every deployed revision and the combination tested together.
- Failed deployment/E2E leaves the original plan open and creates or reuses a linked follow-up
  issue.
- Pending, missing, skipped required stages or inconclusive results are not success.
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

## Responsibilities and evidence

### Feature-owner: hand back after merge

- Record each repository's PR URL, actual merge commit, target branch and relevant workflow links.
- Preserve the ownership mapping: repository, local root, branch and absolute worktree path.
  Multi-repository work needs one valid mapping for each disposable feature worktree.
- Finish implementation, review and merge tasks. Leave deployment/E2E and overall ownership open.
- Report the handoff to Foreman. Do not delete worktrees or branches, or complete the plan at merge.
- Stop dispatching work against these resources before the final completion decision.

Use the ownership/task descriptions for detailed records. Keep plan context brief and preserve its
existing recovery JSON and 2,000-character limit. Do not add an unlimited evidence log to context.

### CI/CD: deploy, then test the deployment

- Follow each repository's workflow and environment policy. Do not introduce a universal platform.
- After required post-merge checks pass, deploy the intended revision to the isolated E2E
  environment.
- Expose deployed revision evidence, such as a release identifier, manifest or version endpoint.
- Run E2E against that deployed environment after deployment succeeds, not only a checkout server.
- For a multi-repository feature, record the deployed revision set used by joined-up E2E.
- Retain run links and artifacts outside disposable Factory worktrees.

A repository without this workflow or usable revision evidence is blocked, not implicitly verified.
Adding or changing its pipeline is explicit repository work, with dependency/action audits before
installation or upgrades. This slice does not deploy automatically to production or create releases.

### Foreman: verify and complete

For each affected repository, save evidence in the relevant verification task:

- PR and actual merged commit; workflow run, attempt and environment.
- Required deployment/E2E stage conclusions and links to logs or artifacts.
- Actual deployed revision and, where relevant, the full tested repository combination.
- The time and outcome of verification, plus any blocker or linked follow-up issue.

Check live provider evidence against those identities before marking verification tasks done.
A green run for a different revision, a successful deployment without deployed E2E, or an earlier
successful attempt does not satisfy the current verification task.

On failure, raise or reuse a follow-up issue linking the original issue, plan, revisions and failed
run. Check for an existing issue after an uncertain create response; do not create duplicates.
Do not automatically add intake labels or start repair work contrary to the existing intake policy.
The original plan stays open through repair and subsequent successful verification.

Keep unfinished verification monitored without depending on an issue edit. Use existing Foreman
coordination and the watcher notification path; restart must rediscover this work even if the issue
is closed. Notifications must not start a second owner or resume a busy owner concurrently.

Before final completion, save all delivery evidence and finish any required handoff. Then finish
verification and ownership tasks in the supported order, re-read the plan and confirm `completed`.
Forgetful may complete an active plan automatically when all tasks are done/cancelled and at least
one is done. Never cancel required verification tasks to get past this rule. No agent may rely on
writing evidence into the worktree after the last completion transition.

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

### 7A. Post-merge handoff and completion evidence

- [ ] Update Foreman/owner guidance to the responsibilities and disposal contract above.
- [ ] Preserve unfinished verification across restart and closed-issue recovery. Ensure continuing
      notifications do not depend on issue edits or create duplicate dispatches.
- [ ] Exercise one repository through merge, deployment evidence, deployed E2E and final completion.
- [ ] Cover failed/missing/stale results and linked follow-up reuse without completing the plan.
- [ ] Record what is deterministic code and what remains agent-guided, observed behaviour.

### 7B. Completed-plan cleanup through public watch

- [ ] Add completed-plan discovery to the existing watch loop, including completion during downtime.
- [ ] Implement target validation and worktree/local/remote removal through ports and Git adapters.
- [ ] Prove the disposable-files policy using a real temporary repository and bare local remote.
- [ ] Prove isolation from unrelated plans, main checkouts, invalid mappings and target branches.
- [ ] Cover partial cleanup, unavailable remotes, uncertain responses and restart reconciliation.
- [ ] Report problems through existing watcher alerts; keep cleanup distinct from status health.

### 7C. Multi-repository delivery and adoption

- [ ] Exercise the intended deployed revision combination and joined-up E2E before completion.
- [ ] Exercise cleanup of all mappings when one repository's deletion initially fails.
- [ ] Reconcile existing Slice 6 cleanup markers; accept proven absence without recreating work.
- [ ] Document that enabling this behaviour also processes eligible older completed Factory plans.
      Review those mappings before rollout; do not silently install it into a running factory.
- [ ] Refresh architecture/ADRs, roadmap decisions, setup docs and role guidance together.
- [ ] Validate the built wheel and run an explicitly approved disposable live trial.

## Validation plan

Confirm these public test boundaries before implementation, then use RED/GREEN vertical slices:

- Public watch CLI with isolated repositories and external Forgetful/provider fixtures: completion
  discovery, notifications, scoping, active/draft/archived plan exclusion and restart behaviour.
- Real native Git and a temporary bare remote: exact targets, dirty/untracked/ignored removal,
  additional-commit branch deletion, already-absent refs, partial failure and no unrelated deletion.
- Forgetful contract checks: manual and automatic completion shapes, full ownership reads and
  correct state when required verification tasks remain open. Do not invent fixture-only API fields.
- Explicit disposable live delivery: actual deployed revision evidence, deployed E2E, Foreman
  completion and automatic removal. This is required to observe agent behaviour; prompt wording
  assertions cannot prove that Foreman applies the completion rules.

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

- [ ] Update `docs/plan.md` Slice 7 and the old cleanup decisions to this approved policy.
- [ ] Update `docs/adrs/feature-delivery.md` and `docs/adrs/issue-planning.md`, keeping historical
      behaviour distinguishable from the implemented replacement.
- [ ] Link the implemented flow from `docs/architecture.md`; remove old owner-cleanup instructions.
- [ ] Explain disposable worktrees in setup/README and owner/Foreman resources before adoption.
- [ ] Demonstrate successful deployment/E2E and local/remote cleanup for the same completed plan.
- [ ] Demonstrate failed verification retains the original plan and resources.
- [ ] Demonstrate interrupted cleanup resumes without recreating work or deleting unrelated data.

Planning-only update: no code, running factory, Forgetful record, pipeline or worktree is changed
by this document. Other planning and architecture files are deliberately left untouched while the
watch-status implementation is editing them; reconcile the linked decisions when implementing
this slice. `FACTORY.md` remains user-owned and unchanged by this planning work.
