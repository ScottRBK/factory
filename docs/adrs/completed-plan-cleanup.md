# Completed-plan discovery and disposal

Status: Slice 7B and automated/local 7C implemented locally. Live adoption, model-following and
actual deployment/E2E trials are deferred. The approved per-set receipts, one-set rotation and
watch-stop correction are implemented locally. Parent SQ and review disposition remain pending;
see the [correction record](../plans/slice-7.md#approved-receipts-scheduling-and-watch-stop).
Back to [architecture](../architecture.md), [agreement](completion-agreement.md) and
[work record](../plans/slice-7.md#7b-and-automatedlocal-7c-implementation).

## Authority and boundaries

Foreman completes a plan only after its acceptance criteria and applicable human DoD agreement.
Only native Forgetful status `completed` authorizes disposal. The cleanup workflow does not read
Markdown, inspect PRs, compare commit heads, scan processes or dispatch an owner. Issue closure,
merge, archive, cancelled tasks and historical cleanup markers do not authorize deletion.
Completion makes the recorded resources disposable: dirty, untracked and ignored files, and local
or remote feature-branch commits, are removed without another prompt or recoverable trash. Evidence
must be saved outside worktrees first. Never reopen or continue the completed feature's work in
these resources. This does not grant permanent authority over new human resources after confirmed
cleanup. Durable per-set confirmation ends that authority across restarts as well as later polls.

`WatchFactory` calls a separate `CleanupCompleted` workflow after planning access and before
unfinished recovery/intake on every cycle. Startup is the first cycle. Closed issues, `--new-only`,
GitHub outages, archived unrelated work and a manual intake pause do not hide completion. Unreadable
planning access cannot authorize deletion. Existing terminal delivery failure, ownership/liveness,
workspace lease, status observation and managed-only stop contracts remain unchanged. Watch-local
SIGINT/SIGTERM handlers now start before native startup checks. A stop latch survives finalizer
exception loss; native-return, write, delivery and wait checkpoints observe it. Bounded owned close
and historical-status publication remain outside those guards; borrowed close only releases its
channel. See the [watch-stop tests](../../tests/test_watch_stop.py).

The CLI composes both workflows with the same planning/Git ports. `FactoryRecords` holds the
existing shared context, issue snapshot, ownership, mapping and repository/source checks extracted
from `ScaffoldIssue`; it has no lifecycle writes. Scaffolding remains an intake/recovery workflow.
`GitWorktrees` validates native Git identity and performs only one mapping's targeted disposal; it
has no planning, DoD or orchestration knowledge. Domain code has no raw Git or Forgetful tools.

## Full records and competing claims

Each cycle reads a complete user-wide plan inventory, then full plans, rather than trusting summary
status. A stale active summary cannot hide a completed full plan; a completed summary cannot
override an active full plan. An invalid/incomplete inventory permits no deletion. Any unreadable
full plan, task inventory, full claim-bearing task, malformed ownership/unknown target or required
namespace identity blocks ALL disposal for that cycle: independent resources cannot be proved.
Report the affected identity and retry reads next cycle; do not pause otherwise safe issue intake.
If there is no unconfirmed selected completed candidate, skip the claim index and Git namespaces.
Cleanup inventory alerts use their own subject/code and clear after recovery. They do not consume
or falsely describe the separate factory-intake alert episode.

Before disposal, check the full plan's selected project, canonical configured work source, exact
workspace context and matching saved issue identity. Fetch full tasks because summaries omit the
ownership description. Require exactly one valid ownership task, with matching plan, workspace,
external reference and mappings. Pin its ID during this run; a replacement is not accepted.

Index available full ownership records from all visible plans, including active, archived and
foreign plans. Check exact/overlapping paths, local branch namespaces from actual common Git
directories and remote branch namespaces from canonical GitHub work sources. Independent clones
can share a remote ref; linked roots with different worktree origins still share local refs.
Readable local identities withhold authority even when their origins are wrong; source/origin
validation remains mandatory before disposal. Feature-ref and merge-target collisions withhold
authority from affected resources. Summary duplicate references can also withhold
authority when a competing detail reply is unreadable; summaries never grant deletion authority.
A missing owner cannot authorize its own resources; an unreadable or invalid claim-bearing record
withholds all disposal, rather than being discarded from the index. No ownership is guessed from
issue/branch naming. Immediately before each mapping, reread its full owner/mappings and plan
status/association. A changed record waits for a fresh cycle; a non-completed plan is not disposed.

## Mapping and Git identity

Ownership mappings keep `repository`, `local_dir`, `branch` and absolute `path`, and now require
`target_branch` for cleanup. This is a short branch name, without `refs/heads/`. Ordinary intake
records the main checkout's symbolic branch as the initial target, and puts the worktree strictly
beneath that repository's `.factory/worktrees/`. New ordinary directories receive a local
`.gitignore` containing `*`; an existing ignore file is preserved. The workspace's own ignore rules
cannot cover independent repositories. An unreadable/detached initial target is a
retryable pre-write intake problem, not an uncertain write. Pass those validated preflight mappings
through plan/ownership creation; do not repeat target discovery after a planning write. Actual
worktree creation still validates native Git identity. The owner records each epic target and
corrects an initial target if a PR is retargeted before handoff. This is resource identity, not
an executable DoD schema. Existing unfinished records remain readable without migration.

Check configured root, origin and provider/source before disposal. Both effective fetch and push
URL lists must equal the single configured origin: a separate push URL must not delete a different
repository's ref. Git checks exact ref syntax, the root's current branch and the remote's advertised
symbolic default. Default, main-checkout and recorded merge-target branches are protected. An
unknown remote default blocks cleanup rather than guessing `main` or `master`. Cache each root's
successful or failed default read once per cleanup cycle. Read facts fresh next cycle. Cleanup-only
`ls-remote` and `push` close stdin, disable Git/askpass/credential-manager prompts and put the
effective
SSH command in batch mode, with a forced false askpass to prevent TTY fallback. Native configuration
and interactive OAuth are unchanged. A failed
network read is not an uncertain write. At most one pending resource set is attempted per cycle.
Round-robin ordering advances even when that attempt fails; a failed first set cannot starve its
siblings or later plans. This bounds disposal attempts, not inventory or claim-index cost, and
not the elapsed time of the several bounded native calls within one set.

Paths must be canonical, strictly beneath the owning repository's Factory directory, outside its
Git metadata, not the main checkout or a symlink escape. A path containing any configured
repository root is also protected, including an independent clone not listed by this Git directory.
Check registration, recorded branch,
actual worktree root/symbolic branch, expected common Git directory and the linked gitdir's
backlink.
An occupied unregistered path, stale/prunable registration, redirected Git identity, nested
registered checkout or locked worktree blocks removal. Force is allowed for contents, not locks.

## Fixed order and observed-state retry

1. Remove the exact registered worktree with native `git worktree remove --force`.
2. Confirm path/registration absence, then delete only its local feature branch with `branch -D`.
   Respect Git refusal when checked out elsewhere. Recheck local-ref absence; a still-registered
   branch also blocks remote disposal even if its local ref was manually deleted.
3. Query the exact remote feature ref and delete it with an explicit `:refs/heads/NAME` refspec.
4. Confirm actual remote-ref, local-ref and worktree absence.
5. Persist and fsync the set's terminal receipt before reporting success or releasing its names.

For unconfirmed mappings, already-absent resources need the same remaining identity checks. No
filesystem deletion, Git clean, pruning, resets, conditional SHA deletion, per-step journal or
native cleanup-marker mutation is added. Errors/timeouts can follow an actual write: report the
identity and reread facts on a later cycle/restart. Keep the completed plan and its evidence intact.
Independent mappings/plans get later turns after a partial failure. Success is not a lifecycle
health check or proof of agent receipt.

### Durable terminal authority

`CleanupReceipts` is an application port. The CLI wires `FileCleanupReceipts` to the separate
cleanup
workflow; Git does not know about receipts. `.factory/cleanup-finished.json` contains versioned
terminal set identities, not progress steps or a general registry. Its scope is the canonical
workspace, configured native backend target, native plan ID and external reference, canonical work
source, root, branch and worktree path. Native plan IDs are user-wide: the selected project and
ownership-task ID are validated before disposal, not mutable parts of a finished set's identity.
Changing only a target branch must not restore authority over a finished set. Same-plan resource
name reuse with a changed set/backend identity is a conflict requiring reconciliation. Configuration
aliases and workspace/backend moves do not get automatic migration or guessed backend identity.

Every set persists independently after final native absence checks. A sibling failure cannot
undo that confirmation. A later poll/restart skips the confirmed set even when human local/remote
refs now use its names. Finished sets no longer supply resource/target claims or cleanup Git work.
The plan itself is not marked finished: each poll still reads full plans and own mappings, allowing
pending siblings to be found without building a claim index when none remain.

The document is a private owned regular file. Symlinks, hardlinks, malformed/duplicate/unknown
fields, unsupported versions, copied workspace identities, unreadable storage and files above the
fixed 16 MiB safety limit withhold all disposal, not safe intake. Save by same-directory temporary
file, file fsync, atomic replace and directory fsync. Reading an existing receipt also syncs its
file/directory, settling a prior lost fsync acknowledgement before accepting terminal authority.
This uses the existing workspace lease, with no new lock, scheduler service or configuration.

If persistence fails after native disposal, do not report success. Names remain reserved until
durable confirmation. The next attempt rereads actual resources; refs recreated before that point
remain disposable under the still-unfinished cleanup authority. Legacy `removed`/`pending` records
never become terminal receipts without native proof. Preserve this file with the workspace: loss,
manual deletion or a valid but incorrect edit of authority storage is not detected or reconstructed
from legacy records. It is not a tamper-proof audit log. Never delete it to force a retry.

### Fair bounded attempts

Sort pending sets by plan ID, root, branch and path; choose the first key after the run-local
cursor, wrapping at the end. Advance before the selected attempt, including failed attempts.
Restarting starts a new rotation but does not erase terminal confirmations. Full claims and
required namespaces must be readable before any attempt. A final owner/status read failure spends
that cycle without disposal. No second set is attempted as a fallback within the cycle. Remote
default caching and per-command timeouts remain. This does not bound user-wide inventory size,
claim-index reads or total time spent in a single attempt.

These are targeted checks, not an atomic transaction or a process-use lock. No safety claim is made
for concurrent repository/path/ownership replacement between checks and native writes. The agreed
completion contract forbids continuing feature agents; cleanup does not prove their exit.

### Partial worktree removal and operator recovery

A lost acknowledgement after completed native deletion can reconcile from absence. A partial
filesystem removal is different: a missing `.git` link can leave a native registration that fails
identity validation, preserving refs but blocking retries. A simulated missing-link public test
reproduces that block. The reviewer's real signal attempts on tmpfs recovered; this does not prove
all filesystems/interrupt points recover autonomously.

Do not bypass the block. After explicit user approval, inspect the exact recorded path, native
registration/branch, expected common Git directory and administrative gitdir backlink. Preserve
remaining contents. Only if that exact administrative entry is verified, try native
`git worktree repair <exact-recorded-path>`. Reread root, branch, common directory and backlink
before allowing cleanup retries. If Git cannot repair it, agree a targeted per-resource recovery
with the user. No blanket prune/rm, guessed replacement registration, force bypass, rollback or
plan reopening is authorized by an alert.

## Historical records and explicit adoption

Open-plan Slice 6 `pending`/`removed` recovery remains read-only and never recreates absent trees.
For completed plans, those markers are history, not a journal or proof of branch/ref absence. Native
Git state determines what remains, including a remote ref left behind after a recorded removal.

Enabling this version also discovers eligible older completed plans. Before installing/restarting
it in an existing factory, explicitly review those plans, full ownership records and preserved or
edited role guidance with Scott. Reconcile repository/root/origin, actual target branch, path,
feature ref and competing ownership. Missing `target_branch` blocks cleanup; never infer it from
a name or set a placeholder. Older paths outside the owning repository's Factory directory need
explicit reconciliation, not automatic relocation. Do not clear an identity conflict to make a
removal pass. No live factory, DinoLand record or old completed mapping was adopted by this work.

## Validation limits

Public watch tests use external native Forgetful/provider fixtures, actual temporary repositories,
registered worktrees, bare remotes and a disposable SSH transport that runs native upload/receive
pack. They establish deterministic cleanup, failure isolation and recovery. Native lifecycle suites
cover plain/managed/status and owned/borrowed boundaries. These checks do not prove Foreman/owner
compliance, live deployment, deployed revision combinations or E2E evidence interpretation. Those
trials, live adoption, parent SonarQube and independent review remain separate gates.
