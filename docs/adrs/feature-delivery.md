# Implementation, review and merge

Status: Slice 6's delivery responsibilities remain; its earlier validation predates normalized
agent definitions. Factory now uses [child-owned agent files](agent-definitions.md) and audited
extension 1.5.0. Native SDK/fake-worker checks pass; live delivery is still unverified. Runtime
repair policy and final checks remain open. Back to [architecture](../architecture.md).
[Progress and checks](../plans/slice-6.md).

## Responsibilities

The feature-owner coordinates implementation, independent review and merge. The watcher still
only scaffolds and notifies; the Foreman remains the sole dispatcher of feature-owners.
Implementation and review workers report to their owner and do not update Forgetful.

The owner plans the actual feature changes, affected repositories, acceptance criteria and tests.
Generic tasks named Implementation, Review and Merge do not replace that detail. A small feature
may need only one implementation task; larger features need a useful breakdown and dependencies.

Scott agreed that clear requirements are sufficient to proceed. There is no separate mandatory
plan-approval round unless the repository requires one. Unresolved decisions still go back to the
user. This does not grant permission to bypass native tool approvals or repository protections.

## Role configuration

The Foreman dispatches owners; each owner launches workers through the AgentShell extension. There
is no Python worker controller. Each worker's `agent.json` owns its name, harness (`agent_type`),
model, effort and resource selections. The owner's roster contains only child file references.
Starter names are templates; later names are arbitrary. Worker definitions omit cwd so the owner's
call supplies the assigned worktree. Every non-Pi child has a disabled, empty roster.

Init provisions the configured starter team once. Its worker menu offers Pi, Codex and Claude Code;
that menu does not define the full set of native app capabilities. The wizard does not ask for skill
paths. Optional initial skill flags are saved in the worker's `agent.resources.skills`, not TOML.
Add files beneath a selected directory or edit that selection directly. Reload affected parent
snapshots before new launches; do not rerun init to register skills. Bundled guidance still requires
TDD. A root Foreman launch-setting change requires restart.

The owner reads the selected worker definition and supplies the full role, task, worktree and review
briefing, including absolute selected skill references and instructions to read them before work.
Normalized extension 1.5 source also supplies deterministic references for Codex/Claude children.
It strips only outbound native `skills`, retaining the complete canonical saved selection and all
other resource options. Unsupported other options still fail through native checks. This is prompt
skill delivery, not native skill registration or proof of model compliance. Pi and OpenCode retain
native selected-skill support. Factory now bundles the audited published runtime; see
[validation limits](../../README.md#current-source-and-release-boundary).

Worker instructions and selected local skills must reach the native harness without replacing
repository instructions. Pi-specific resource options cannot be passed to a harness that does not
support them. Native profiles, settings, tools and permission controls remain relevant; task
instructions are not a sandbox. No skill or package download is needed for role selection.
Factory does not provision browser/computer-use tools for workers.

Native permissions must allow worktree edits, access to the original repository's Git metadata,
and the network/tool operations needed for push, CI and GitHub reviews. AgentShell 0.5's Codex
`workspace-write` default may block the external Git directory or network; Claude's noninteractive
permissions may block its tools. Setup checks do not establish these permissions. Agents report
blocked work instead of silently switching approval or sandbox policy.

Older factories must not silently gain execution authority. Preserve existing configuration and
edited guidance. Enabling workers requires an explicit `execution_enabled` change in TOML,
suitable child definitions/references, and reconciliation of incompatible guidance. Stop delegated
work and reload affected parents before new launches. Ordinary init does not activate workers or
renew a fingerprint. Existing/DinoLand factories have no automatic migration.

## From implementation to merge

1. The owner gives an implementation worker the specific task, acceptance criteria, repository,
   worktree, applicable instructions and dependencies. It records the launch separately from a
   returned native session ID.
2. The worker uses TDD, runs local checks, commits and pushes its changes, then opens or reuses the
   repository PR. It checks the intended repository/head/base and follows repository templates and
   the owner's PR content guidance. The owner coordinates one feature PR per repository and names
   the PR-opening task when workers share a branch. After uncertain creation, the worker reuses a
   matching open PR; closed/merged PRs need reconciliation, not automatic reopening. The worker owns
   the CI correction loop and reports task IDs, the PR URL, exact commit, tests and CI evidence.
   Failed or unavailable checks mean blocked, not complete.
3. The owner verifies the returned PR and exact-commit evidence, records the PR in plan context and
   launches a separate review worker on that PR. Review findings identify the reviewed commit. The
   owner decides what needs fixing according to the requirements and repository rules;
   implementation workers make and validate the fixes.
   Create feature-specific fix tasks rather than reopening completed implementation prerequisites.
   Review remains pending until fixes and current-commit CI evidence are verified.
4. ADRs and other required documentation are included before final validation. The owner rechecks
   the final PR head, required checks, review findings and repository approvals before merging.
   Changed commits need current evidence; an earlier green commit is not sufficient.
5. Merge uses the expected head commit and the repository's merge policy, without bypassing
   protections. A queued or scheduled merge is not a completed merge. Multiple repositories merge
   in a compatible order; partial progress is recorded rather than treated as an atomic operation.
6. After confirmed merge, the owner removes only worktrees and branches proven safe to remove.
   Active processes, uncommitted changes, uncertain merge status or unpushed work mean preserve
   and report. It reports the merged revisions and PRs to the Foreman.

Independent agent review does not establish a second GitHub identity. If both agents use the same
account, findings can be posted as comments; they do not satisfy a required external approval.
Native approval restrictions and branch protections must be respected.

The delivery contract assigns PR creation to implementation. The worker opens the PR before
waiting for PR-triggered CI; it need not wait for checks that cannot start without a PR. Required
checks still must pass before implementation is complete. Draft status follows repository rules
and owner guidance, with no factory-wide draft-only requirement. Opening a PR grants no approval
or merge authority: the owner retains independent review and merge control.

## Durable state and recovery

Forgetful remains the durable record for tasks, worktree mappings, PRs and evidence. Native session
IDs and transient AgentShell Job IDs are different. A missing job record, silence or timeout does
not establish that a worker stopped. Check saved work and actual process status before resuming
or replacing it. Preserve work and report uncertainty rather than launch a competing worker.

The owner uses the native task APIs and current versions for transitions and claims. Forgetful
0.5.5's `update_task` cannot change `assigned_agent`; `claim_task` accepts only `todo` or `waiting`
and moves the task to `doing`. A worker's native ID may arrive only with its completed result.
Record launch intent separately and leave an unknown identity unset. Any later claim must use the
real returned ID and an eligible state, not an invented assignment API or a Job ID.

The owner records an in-flight task as `doing` without inventing a worker identity. Once the actual
native ID returns, it can transition through `waiting`, claim with that ID and the current version,
then verify evidence and criteria before marking it done. Each transition still requires eligible
state and satisfied dependencies. Interrupted transitions are reconciled from the current task.

Selected-session resume depends on the owning parent history and unchanged canonical child
selections. Full child definitions and parent membership are snapshots; reload adopts edits for
new launches, while changed selections fail resumes of older selected sessions. Skill contents
and directory membership are resolved again, not frozen by a settings fingerprint. AgentShell
0.5.0's Codex resume command does not forward its per-call approval/sandbox option. If the effective
native policy cannot be established as suitable, report that limit and use a fresh worker only
after confirming the previous one stopped. Do not silently enable bypass permissions.

## Worktree cleanup and restart

The plan remains active after merge, so watcher restart must still recover it after safe worktree
removal. Each ownership mapping can carry a `cleanup` object with `state`, `pull_request_url` and
`merge_commit`. The original repository, local directory, branch and path remain as history.
Use the canonical GitHub PR URL and the actual full lowercase Git commit SHA from verified merge
evidence. Repository matching is case-insensitive, as on GitHub; the recorded URL is preserved.

The owner saves `pending` before removal, then `removed` only after verifying absence of the path
and its worktree registration. It coordinates updates and preserves every other mapping/field;
Forgetful description updates are not compare-and-swap operations.

The watcher validates the marker's shape; it does not verify the GitHub merge or CI evidence.
Its `Worktrees` port delegates read-only origin/path/registration checks to the Git adapter:

- No marker: existing worktree validation remains required; missing work is never recreated.
- `pending`: the tree must still validate. If missing, stop for interrupted-cleanup reconciliation.
- `removed`: the path must be absent, with no registration at that path or for that branch.
  Occupied paths, symlinks, stale registrations and changed origins stop without mutation.

The recovered notification retains the mapping and status. Foreman/owner must inspect actual PR
and task state, not launch implementation into a removed/pending tree. Partial epic cleanup keeps
separate status for each repository. This fixes restart after cleanup; it does not implement
post-merge deployment monitoring.

## Completion boundary

Slice 6 ends at verified merge and safe cleanup. Deployment, end-to-end verification and final
plan completion remain Slice 7. Keep that work and the long-lived ownership task unfinished so
Forgetful cannot automatically complete the plan at merge.

Python validates setup and resource selection; agent guidance describes delivery and recovery.
Automated wiring tests cannot establish that a model follows the whole workflow. The agreed live
trial will use a disposable GitHub repository selected with Scott after automated checks pass.

Native cancellation remains limited by [agent-shell#28][cancellation]. No workaround is provided;
confirm process exit before resuming or replacing a worker.

[cancellation]: https://github.com/ScottRBK/agent-shell/issues/28
