# Issue planning and feature ownership

Status: Slices 4 and 5 implemented; local validation and independent review passed.
Back to [architecture](../architecture.md). [Validation](../plans/slices-4-5.md).

## Responsibilities

The watcher creates the initial Forgetful records and ordinary-issue worktree. It then sends
those references to the Foreman. It never launches a feature-owner itself.

The Foreman is the sole dispatcher. Its selected roster launches a Pi feature-owner, which claims
ownership, conducts grill-me, asks for clarification and plans the work. It may delegate research.
Implementation, PR review, merge and deployment execution belong to later slices.

Python code implements setup, issue intake and recovery of saved records. Agent instructions
implement the planning conversation and owner coordination. Tests of those instructions and launch
settings do not establish that a model will carry out the workflow correctly.

## Native Forgetful access

Init selects an existing project or creates one after the user confirms its name. The default
name is the workspace name; a Factory can cover multiple repositories. Creation uses native
`create_project` with a short description and type `development`. The returned numeric `id` is
saved as `forgetful.project_id`. There is no skip option: Forgetful plans require a project.
Creation permissions are needed only when creating, not when selecting an existing project.

A failed or interrupted create response may follow a successful server write. Factory does not
retry it; the user reruns init and checks the project list before choosing another create.
An interrupted creation retains exit code 130 and includes the same uncertain-outcome guidance.
A project is not deleted if subsequent setup fails. Existing configurations keep their saved
project and the explicit-edit policy; this change does not introduce migration or live watcher
reconfiguration.

Init and watch check access to that project and the required planning tools. The preflight uses
two sequential native CLI calls: `get_project` and `tools list`. Project access also verifies the
connection and native login, so preflight needs no separate user-profile request. Agents may still
request user information for context; their instructions retain that distinct step. The catalog is
filtered by the caller's permissions and includes parameter names. Planning-only factories require
all twelve planning operations; execution-enabled factories also require `verify_criterion` so the
owner can record checked acceptance criteria. Both `create_plan` and `list_plans` must advertise
`external_ref`. Malformed or incomplete catalogs fail setup. This replaces separate `tools info`
processes without removing permission or compatibility checks. Catalogs are not cached across runs.

Forgetful 0.5.5 supplies that field and its database uniqueness migration. Updating Factory's
bundled CLI does not update an existing executable or remote server.

Local commands set `PLANNING_ENABLED=true`. A remote server must enable planning and grant the
native user access. Watcher, Foreman and owner share the same executable, target, safe command cwd
and native CLI configuration directory. They do not copy credentials. An attended watcher may
open native browser login or refresh cached credentials. Cancellation and bounded command timeouts
stop work without deleting saved records or worktrees.

Forgetful 0.5.5's `get_current_user` response has no stable user ID, despite its tool documentation.
Factory checks native user access to the selected project; it does not pin an unavailable principal
ID, infer identity from a name, or decode tokens.

## Issue identity and saved records

The canonical reference is lowercase `github:owner/repo#number`. Lookups by `external_ref` are
user-wide, without project or status filters. Factory then checks the returned plan's project and
workspace. This catches a matching reference associated with another project instead of creating
a second plan. Multiple workspaces writing the same plan are unsupported; the workspace lease
cannot coordinate them.

Factory uses existing Forgetful text fields for a small JSON record:

- Plan `source_url`: GitHub issue URL.
- Plan `context`: absolute `workspace`, initial `issue` recovery snapshot and
  `ownership_create_started`. New snapshots keep the issue identity, title, URL, revision and epic
  flag, but replace the body with a provider/number/title placeholder. This applies to short and
  long issues; no body prefix or other truncated text is stored.
- Ownership task `description`: `kind="factory-ownership"`, `workspace`, `external_ref` and
  `worktrees`. Each mapping contains `repository`, `local_dir`, `branch` and absolute `path`.
  After verified merge, the owner can add per-mapping `cleanup` metadata; see below.
- Ownership task `assigned_agent`: the owner's real native Pi session ID, set by `claim_task`.

The placeholder says that the feature owner will update the description after reviewing the
issue/plan. Owner guidance instructs it to read the full current provider issue and comments
before enrichment, and to report failed reads as blockers. This is prompt guidance, not a
Python-enforced read or a guarantee of model compliance. Live notifications still carry the full
provider body. Recovery
without an open issue uses the saved placeholder. Old full-body snapshots remain readable in the
same JSON shape; no migration or recovery write is needed.

Forgetful defaults plan `context` to 2000 characters, including serialized JSON. Both initial
creation and the ownership-intent update use literal Unicode rather than ASCII escape expansion.
This removes body-size dependence without truncating metadata or changing recovery contracts.
Arbitrarily large workspace paths or other metadata can still exceed the server limit; this fix
neither truncates them nor adds a different storage scheme.

Agents preserve recovery fields while keeping added notes, session references and PR links brief.
Plan goal and task descriptions hold human planning detail within their own limits. Never copy the
full issue back into context or discard recovery fields to fit; a replacement description must
remain brief enough for the complete JSON record. Full ownership tasks are fetched because
`query_tasks` summaries omit descriptions. The snapshot supports recovery when an issue is no
longer in the open-issue poll; it does not replace current provider requirements or issue history.
See the [placeholder validation record](../plans/issue-plan-placeholder.md).

## Checks before fresh creation

After Foreman is ready, watch checks each configured local root and origin against its saved
remote and work source. Known repository problems pause affected work and alert Foreman; safe
repositories continue. Git/access correction can be observed, while configuration edits require a
restart. Before each new plan, fresh intake repeats repository checks and, for ordinary issues,
checks the proposed branch/worktree path without creating it. A pre-write conflict creates no plan.
A retained failed lookup can discover saved work after closure, but fresh creation requires the
issue to appear in the current successful open/labelled poll. These checks do not repair existing
incomplete plans or remove the checks at the actual write boundary.

## Interrupted creation

Plan creation uses Forgetful's unique reference. After a failed create response, Factory rereads
that reference: the server may have committed the plan even though the response was lost.

Task creation has no unique key. Before creating ownership, Factory saves
`ownership_create_started=true` in plan context. After a failed response it rereads full tasks.
If exactly one valid ownership task exists, it reuses it. If the outcome is still unknown, planning
pauses and Foreman is alerted; the watcher remains alive without repeating the operation. The saved
marker still prevents task-create replay after restart. Reconciliation requires checking the earlier
request has stopped and inspecting all tasks before resolving that marker. Startup and blocked-plan
recovery are read-only: a missing ownership record is never automatically synthesized, even if a
marker is cleared. Scott chose user-approved Foreman completion for incomplete first-time setup,
implemented under the [watcher problem contract](watcher-problems.md). The alert explains the native
repair and required approval rather than implying polling alone completes it. Read-only recovery
can observe a first ownership identity established by approved repair, including closed/new-only
work. It pins that identity before mapping validation and refuses a replacement. Duplicate or
malformed ownership records block their plan. Valid duplicate candidates are not a confirmed pin.
Foreman inspects their work and running agents, proposes which to retain and obtains user approval.
Retiring the extra designation changes both its title and ownership kind, preserving other fields,
history, claims and work. Merely cancelling its state is not enough. Read-only recovery can observe
either single valid survivor only when no sole owner had already been confirmed; it never replaces
a confirmed owner. Unknown or competing live ownership stays blocked. Ordinary description/context
updates are not compare-and-swap operations or authority to transfer a claim.

An ordinary issue gets a branch and worktree before ownership is saved. If task creation then
fails, Git state remains available for reconciliation. Nothing resets, forces or deletes work.

## Worktrees and epics

An additional case-insensitive `epic` label leaves repository/worktree choice to the owner. Other
issues get an initial worktree in their source repository. Both use native Git; no worktree
extension is required.

The Git adapter checks origin, registered path, branch and common Git directory. Initial intake can
reuse an existing matching registration; saved incomplete plans require approved Foreman completion.
A missing or mismatched recorded worktree blocks its plan and alerts Foreman, without stopping
unrelated plans or the watcher. It is never silently recreated. Generated worktrees live under
`.factory/worktrees/`, ignored by Git. Uncommitted changes in the original working copy are not
copied into a new tree.

Slice 6 adds an optional cleanup record for safely removed, merged worktrees. The owner saves the
canonical matching GitHub PR URL, full merge SHA and `pending` intent before removal; it records
`removed` only after confirming path and registration absence. On restart, only a valid `removed`
record permits absence. The adapter checks the origin and refuses occupied paths, symlinks or
remaining registrations. Missing unmarked or pending work remains blocked for reconciliation.

The watcher does not delete worktrees or verify GitHub merge evidence. It preserves the reported
cleanup metadata in the notification so the Foreman can inspect unfinished post-merge work without
launching into a removed tree. The
[cleanup record](feature-delivery.md#worktree-cleanup-and-restart) describes these checks.

## Updates and restart

While running, the watcher remembers submitted issue revisions, so edits can produce another
notification using the same plan/task/worktree IDs. Terminal submission is the acknowledgement;
there is no durable agent-receipt record or custom message queue.

At restart, draft/active Factory plans for the configured repositories are recovered first,
including plans whose issues are closed. They are sent again to the new Foreman. `--new-only`
still forwards changes to recovered work, while baselining unrelated open matches. Duplicate
notifications after restart are expected; the Foreman must inspect current ownership before acting.

[Problem alerts](watcher-problems.md) are independent of successful issue submissions. Blocked
records are re-read by their known identities, including closed issues absent from GitHub polling.
Revalidation never calls the creation path and does not change ownership or task state. Repairs can
therefore produce a normal notification without an issue revision change. Completed plans do not
become new work. An alert itself cannot pause a busy owner or authorize dispatch/replacement.

## Ownership and safe continuation

The owner reads its own native Bash `PI_SESSION_ID`, fetches the current ownership task and calls
`claim_task` with the current version. Competing assignments or version conflicts stop work.
Clarification returns control to the Foreman; the same stopped conversation can later resume
with answers. Busy owners are not resumed concurrently.

Selected-session resume depends on the owning parent's native history and unchanged selection.
A native session ID alone is insufficient: Pi can create a new conversation for a missing ID.
A missing job, silence, timeout or retained interactive result does not prove the previous process
stopped. Unknown liveness leaves work pending rather than starting a duplicate.

After confirmed exit, Foreman may arrange a replacement using the saved plan. Resetting a task to
`todo` retains the old `assigned_agent` in Forgetful; the replacement must freshly claim it with its
own ID and version. There is no `release_task` operation. Automatic recovery across unrelated
Foreman histories is not implemented.

The ownership task stays `doing` through planning, and the plan remains open. Implementation tasks
must not depend on completion of that long-lived task. Deployment/E2E work stays unfinished so
Forgetful cannot complete the plan before the later verification stage.
