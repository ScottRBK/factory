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
filtered by the caller's permissions and includes parameter names. Factory requires all twelve
planning operations, and both `create_plan` and `list_plans` must advertise `external_ref`.
Malformed or incomplete catalogs fail setup. This replaces twelve separate `tools info` processes
without removing the permission or compatibility checks. Catalogs are not cached across runs.

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
- Plan `context`: absolute `workspace`, initial `issue` snapshot and `ownership_create_started`.
- Ownership task `description`: `kind="factory-ownership"`, `workspace`, `external_ref` and
  `worktrees`. Each mapping contains `repository`, `local_dir`, `branch` and absolute `path`.
- Ownership task `assigned_agent`: the owner's real native Pi session ID, set by `claim_task`.

Agents preserve these fields while adding questions, notes, parent/session references and PR links.
The snapshot supports recovery when an issue is no longer in the open-issue poll. It is not a
complete copy of the issue history; agents reread current GitHub body and comments before acting.
Full ownership tasks are fetched because `query_tasks` summaries omit descriptions.

## Interrupted creation

Plan creation uses Forgetful's unique reference. After a failed create response, Factory rereads
that reference: the server may have committed the plan even though the response was lost.

Task creation has no unique key. Before creating ownership, Factory saves
`ownership_create_started=true` in plan context. After a failed response it rereads full tasks.
If exactly one valid ownership task exists, it reuses it. If the outcome is still unknown, it
stops, including after restart. Reconciliation requires checking the earlier request has stopped
and inspecting all tasks before clearing that marker. Duplicate or malformed ownership records
also stop work. Ordinary description/context updates are not compare-and-swap operations.

An ordinary issue gets a branch and worktree before ownership is saved. If task creation then
fails, Git state remains available for reconciliation. Nothing resets, forces or deletes work.

## Worktrees and epics

An additional case-insensitive `epic` label leaves repository/worktree choice to the owner. Other
issues get an initial worktree in their source repository. Both use native Git; no worktree
extension is required.

The Git adapter checks origin, registered path, branch and common Git directory. Existing matching
registrations can be reused after interruption. A missing or mismatched recorded worktree stops
rather than being silently recreated. Generated worktrees live under `.factory/worktrees/` and are
ignored by Git. Uncommitted changes in the original working copy are not copied into a new tree.

## Updates and restart

While running, the watcher remembers submitted issue revisions, so edits can produce another
notification using the same plan/task/worktree IDs. Terminal submission is the acknowledgement;
there is no durable agent-receipt record or custom message queue.

At restart, draft/active Factory plans for the configured repositories are recovered first,
including plans whose issues are closed. They are sent again to the new Foreman. `--new-only`
still forwards changes to recovered work, while baselining unrelated open matches. Duplicate
notifications after restart are expected; the Foreman must inspect current ownership before acting.

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
