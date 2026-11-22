# Definition of Done agreement and completion handoff

Setup saves a confirmed Markdown agreement. Role guidance assigns final verification to Foreman,
including deployment and deployed E2E when the agreement requires them. Python handles setup and
[completed-plan disposal](completed-plan-cleanup.md). The controlled live trial covering
deployment, E2E, failure and restart remains unverified. See
[current evidence](../plan.md#current-status).

Back to [architecture](../architecture.md),
[delivery](feature-delivery.md) and [work record](../plans/slice-7.md#7a-local-implementation).

## One human agreement per workspace

Use `$FACTORY_WORKSPACE/.factory/definition_of_done.md`. The name follows `FACTORY.md`; `.factory`
already owns the workspace's durable configuration and shared agent resources. This puts the file
outside feature worktrees under each repository's `.factory/worktrees`, and also supports a grouped
workspace. One Markdown document can name different repository requirements and shared checks.
No configurable location, inheritance, TOML policy fields, front matter or parser is introduced.

The file is the persistent project/programme agreement, not feature acceptance criteria. Both must
be met. Foreman reads it before planning, before completion and after restart. It supplies the text
and absolute path with the issue, plan and repository context to the feature-owner. The owner notes
applicable shared requirements briefly in existing tasks, separate from feature acceptance criteria.
Preserve ownership/recovery JSON and the plan context's 2000-character limit. No structured policy
snapshot or version registry is needed. Chat history and optional memory are not authoritative.

Only user-approved changes are allowed. Foreman must ask whether a change applies to open plans and
record the decision/reason in those tasks before changing them. Without that approval, their earlier
requirements remain. An approved removal can retire an unneeded check; it is never evidence that
an unrun check passed. New plans use the updated workspace agreement.

## Setup and recovery

First manual setup offers three starting points and a discussion route:

1. Independent review, required repository/PR checks and confirmed merge.
2. The above plus deployment of the actual merged revisions.
3. The above plus deployed E2E after deployment, against an isolated test environment.
4. Discuss requirements and prerequisites with Foreman; this is not a fourth completion policy.

The presets are UI conveniences, not an exhaustive policy enum. Deployment presets ask for the
actual environment and workflow names. Setup explains their required revision/run evidence and
that it has not checked the workflows. If prerequisites are missing or unclear, decline and discuss
rather than confirming an unusable agreement. Every preset keeps independent review and repository
gates. Show the entire proposed Markdown and obtain explicit confirmation before saving. Blank,
invalid, EOF and declined answers never select merge-only. A different file created during that
confirmation is preserved and reported as a conflict, not silently accepted.

The CLI saves configuration before the final access check and completion receipt. If input ends
during DoD selection, the saved configuration survives and first setup stays incomplete. Even with
all setup flags supplied, the user must confirm the agreement or discuss it with Foreman. Run
`init --finalize` in a terminal to resume. Choosing discussion starts the setup Foreman without a
receipt or a placeholder policy file.
Assisted setup leaves agreement to its real conversation. Finalization can start that conversation
when no owner exists; it never replaces a live/uncertain owner. An existing owner gets an attach
instruction instead. A confirmed conversation save is ordinary Markdown; finalization preserves it.

Ordinary repeated init preserves existing files and edited skills. It skips prompts and external
checks, including agreement creation for older ready workspaces.
Foreman must ask about a missing, unclear or conflicting agreement before handing off work. The
CLI checks that an existing file can be preserved. The setup receipt cannot establish what the
agreement requires, whether the user approved its contents or whether a model followed it.

## Delivery and completion

The owner retains implementation, independent review and merge responsibilities. It records PRs,
actual merge commits, target branches, workflow links and all ownership mappings, then hands back.
The owner leaves only the required post-merge checks open. Excluded deployment or E2E checks
need no placeholder tasks. Ownership stays open for Foreman, even for merge-only delivery.

Foreman verifies live evidence against both acceptance criteria and the applicable agreement.
Required deployment evidence must identify actual merged revisions. Required deployed E2E must
identify the deployed combination tested after deployment; one workflow source SHA is not enough
for multiple applications. Record run, attempt, stage, environment, artifact, time and outcome in
existing ownership/verification tasks outside worktrees. Missing, stale, pending, skipped required
or inconclusive evidence blocks completion. Failures retain the original plan and create or reuse
a linked follow-up issue. An uncertain create response requires lookup before retry, and existing
intake consent still applies to repair work.

Finish verification and ownership in supported order with fresh versions and verified criteria;
read back the plan and set completed with native `update_plan` if needed, then confirm its status.
Forgetful can auto-complete active plans when all tasks are done or cancelled and at least one is
done. Never cancel a still-required check to trigger that rule. Save all evidence before the last
completion transition. When deployment is required, Foreman verifies evidence from the deployment
workflow. The Python CLI does not parse the agreement or run deployments.

## Cleanup boundary

Neither Foreman nor owner deletes resources. The watcher now independently discovers full completed
plans and disposes of validated worktrees/local/remote feature refs, without interpreting the DoD.
Dirty, untracked and ignored files and extra branch commits are disposable after completion. Save
evidence elsewhere before the last task transition. Cleanup offers no further prompt or trash.
Missing identity or conflicting ownership blocks affected cleanup. Native facts, not historical
pending/removed markers, determine which resources remain. Open-plan marker recovery stays read-only
and never recreates work. See the [cleanup ADR](completed-plan-cleanup.md) for checks and retries.

Existing edited guidance is preserved. Before enabling this version on an existing factory, review
older completed plans and actual ownership mappings with Scott, including target_branch and paths
beneath the owning repository's Factory directory. Missing identity needs explicit reconciliation;
no policy or old mapping is silently adopted. Lifecycle/status, managed-only stop, workspace leases,
uncertain delivery and owner-liveness safeguards remain.

## Validation boundary

Public init tests establish preset persistence, explicit confirmation, no default, preservation and
first-init recovery. Isolated native tmux tests with a fake Pi cover discussion launch, blocked
watching until finalization, unchanged Foreman identity and preservation of the confirmed file.
Public watch regression establishes closed-issue/new-only recovery of unfinished verification,
unchanged mappings/evidence, no duplicate scaffolding and no policy-file mutation. It does not prove
agent dispatch/completion, evidence interpretation, follow-up reuse or policy-change conversations.
Those require separately approved disposable live trials. See the work record for exact checks.
