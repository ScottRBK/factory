# Watcher problems and Foreman escalation

Status: approved follow-up implemented and revalidated; SonarQube triage and Opus review remain.
Back to [architecture](../architecture.md). [Work and evidence](../plans/watcher-problems.md).

## Decision

A planning safety check blocks unsafe work, not the supervising watcher. Foreman receives an alert
and discusses the problem with the user. Other plans continue when the failure can safely be
isolated. A shared planning problem pauses the affected factory operations while the watcher and
Foreman remain available. This refines the earlier fail-stop scaffold rule in
[issue polling](issue-watcher.md) and [issue planning](issue-planning.md).

No recorded worktree is silently recreated, reset, pruned or discarded. The watcher does not repair
Forgetful records, change task states, cancel owners or launch replacements in response to errors.
The existing plan-to-many-worktree relationship is unchanged. DinoLand's records are not part of
this code change.

## Classification and reporting

Known reconciliation conditions have explicit types and stable codes. Filesystem checks report
worktree facts without depending on issues or Forgetful. The application adds known issue, plan,
ownership-task and repository context. Exception message text is never used to choose a policy.

Complete inventories require unique positive integer IDs and exact nonnegative integer counts;
booleans are not IDs or counts. Full plan/task replies must match the requested identity and valid
associations before they can supply alert or notification identifiers. Malformed read replies pause
planning rather than becoming apparent safety facts. Valid plan statuses are `draft`, `active`,
`completed` and `archived`; unknown values stay pending until corrected. A complete lookup may
establish that a pinned plan is absent, allowing that plan to be isolated before its detail read.

All problem notifications use the existing `ForemanTerminal.send` boundary and a fixed prefix with
JSON-escaped data. They identify the affected scope, controlled explanation, known identifiers and
safe recovery action. A small code-to-explanation mapping supplies a plain-language cause; source,
planning-read and uncertain-write problems have different recovery guidance. Missing identities are
omitted. Alerts explicitly ask Foreman to discuss the problem with the user and do not authorize
dispatch or replacement. They are not ordinary work notifications. Raw subprocess output, traceback
text, credentials and issue bodies do not become agent-facing diagnostic messages. Operator
reporting remains available when agent delivery fails.

Unclassified operations that may have written do not acquire permission to repeat side effects.
They latch a pause for explicit reconciliation; known read-only recovery can retry safely.
Unexpected programming exceptions are not silently swallowed. A failed source read may be retried
without treating that source as up to date; other sources continue. Incomplete startup inventory
never authorizes new scaffolding.

Native/configuration prerequisites needed to establish a Foreman connection still apply. When a
Foreman cannot be started or reached, Factory cannot claim to have alerted it. Actual owner loss,
identity uncertainty and failed or unacknowledged sends retain their existing lifecycle safeguards.
There is no automatic replacement, repeated send or alternate tmux transport.

Explicit cancellation still ends watch. The native-command wrapper waits for its owned process
instead of re-entering an interrupted Python `communicate()` call, whose pipe bookkeeping may be
partially initialized. It retains the existing TERM, three-second grace and KILL sequence, discards
failed/cancelled output and closes capture pipes. AgentShell lifecycle adapters and deadlines are
unchanged. This is not evidence of universal detached-descendant cleanup.

## Pending work and recovery

Keep issue revisions, acknowledged identities, blocked records, pending pre-write lookups and alert
suppression separate in memory. Known plan/task IDs survive later issue edits and read failures.
A failed lookup without a known ID is retryable only when no write has been attempted; an ambiguous
lookup or unknown create outcome does not have that authority. Finding a saved plan always routes
to read-only recovery, not creation-capable setup. Both transport and malformed read failures use
the same policy; Git inspection is separate from its directory/worktree write boundary.

Sending an alert does not mark the issue revision as successfully submitted. An unchanged problem
is reported once per episode; a meaningful change or recurrence can be reported again. A restart
may repeat alerts, as it already may repeat normal issue notifications. There is no persistent
error ledger or exactly-once delivery claim.

Rechecking blocked work must use read-only operations on its known records. It must not call the
creation path again when a plan or task disappears. Freshly validate association, ownership,
worktree identity and cleanup evidence before an ordinary notification. Observe current plan status;
finished plans are not new work. Uncertain writes require reconciliation, not periodic replay.
The running watcher retains its startup configuration; editing Factory configuration requires a
deliberate watcher restart. Fixing remote access or a saved record can be observed by safe rechecks.

The blocked set is independent of GitHub's open-issue list. Revalidation must therefore work for an
unchanged issue revision, a recovered closed issue and `--new-only` startup. New-only baselining
must not consume recovered or blocked work as unrelated old issues. Safe recovery uses the normal
issue notification rather than an additional plan-resolution message.

## Interrupted-setup recovery

Scott chose Foreman-led completion with user approval, not automatic watcher completion. A plan
may exist even though initial intake stopped before its ownership task was created. Absence of a
creation marker is not permission for the watcher to create that task or recreate a worktree.
Normal uninterrupted setup for a genuinely new issue remains automatic. An already saved incomplete
plan needs approved repair even if the watcher first discovers it after startup.

The alert must explain that this needs an approved repair, not merely another poll. Foreman first
checks the pinned plan, all tasks, Git state and any earlier operations, then explains the proposed
completion and obtains the user's approval. It preserves valid work and mappings, uses native tools
for the approved action, and does not clear create-intent evidence to bypass an uncertain outcome.
A missing previously known ownership identity is not interchangeable with never having established
one. `setup_incomplete` requests `user_approved_repair`, with native tool and record-field guidance
in the alert itself. Read-only checks can observe the first valid owner after approved completion.
That identity is pinned even when its worktree mapping still fails validation. Rechecks never
select a replacement for a pinned task. A latched uncertain write still requires reconciliation
before a deliberate restart.
No automatic repair, new reset flag or new authorization ledger is introduced.

## Implemented follow-up after the second review

Scott approved three corrections after the second Opus review. They are implemented and covered
by the current 465-test suites, not the earlier 446-test snapshot:

- A retained pre-write lookup may discover saved work even after its issue closes. If it finds no
  plan, fresh creation additionally requires the issue to appear in the current successful poll
  with the watched labels. A stale issue copy is not creation authority.
- Multiple ownership candidates are evidence for reconciliation, not a confirmed owner. Foreman
  inspects their records, work and running agents, proposes the record to keep, and obtains user
  approval. It retires the duplicate's ownership designation while preserving history and work.
  Both the title and JSON ownership marker need correction; changing task state alone does not
  remove the designation. No deletion, claim transfer or cancellation is implied. An uncertain or
  competing live owner leaves the work blocked. The watcher may observe a single valid survivor
  when it had no prior confirmed owner; a previously confirmed identity must not be replaced.
- After connecting to Foreman, validate each configured local directory's origin against both the
  saved remote and mapped work source before creating plans. An origin/mapping mismatch alerts
  Foreman and pauses the affected repository, not supervision or unrelated safe repositories.
  Recheck before each new plan and inspect its derived branch/worktree path before creating that
  plan. Startup checks cannot cover later Git changes or all future issue-specific paths. Checks
  are read-only; do not rewrite Git or configuration. Preserve precise controlled failure causes.

The application reuses the `LocalRepositories` and `WorkSourceResolver` ports for repository
checks; provider parsing stays outside the filesystem adapter. `Worktrees.inspect` exposes a
read-only check separately from `ensure` and its write boundary. Repository pauses and fresh-issue
preflight failures have distinct types from saved-plan failures and uncertain writes. Duplicate
candidate IDs are reporting evidence, separate from a confirmed ownership pin. Malformed ownership
records retain their earlier conservative handling; that case was not broadened into replacement
authority. A confirmed sole owner is still pinned before later worktree validation.

A corrected pre-write problem can resume fresh eligible intake because no setup was started.
Existing incomplete plans still require approved native completion. Checks at the write boundary
remain necessary; a successful earlier read cannot authorize replay after an uncertain write.
Configuration remains a startup snapshot, so editing it requires a deliberate watcher restart.

## Foreman responsibilities

Foreman explains what failed, what is paused and what needs deciding, then examines current
Forgetful, Git and PR evidence with the user. A missing worktree may be intentional post-merge
cleanup with incorrectly recorded metadata, rather than permission to recreate it. Preserve all
repository mappings and outstanding deployment/E2E work.

An alert cannot pause an already-running owner. Foreman checks current ownership and liveness,
waits for busy runs to return before resuming, and never replaces an uncertain owner. Agents retain
their natural response format and existing task states. The new JSON is machine-originated input,
not a mandatory agent response schema.

Updated starter guidance describes this workflow. Existing user-edited skills remain preserved;
setup is not an automatic guidance upgrade. Alerts must provide useful recovery context even when
the selected skill predates the new template. Tests of instructions and terminal submission do not
prove a live model will follow them.

## Validation boundary

Public checks use watch CLI sessions, captured external terminal messages and temporary Git/native
backend fixtures. They cover isolated and shared pauses, recovery without issue edits, closed and
new-only cases, deduplication, preservation and uncertain delivery/write protection. No dependency,
AgentShell SDK or bundled extension upgrade is required.

AgentShell [0.5.0's terminal contract][terminal-contract] says success establishes input submission,
not agent acknowledgement or completion. Paste and Enter can be interrupted separately; failed
transport must not cause automatic replay. Factory keeps its existing owned/borrowed terminal
boundaries. Context7 was unavailable; the versioned official documentation was used instead.

[terminal-contract]:
  https://github.com/ScottRBK/agent-shell/blob/v0.5.0/docs/examples.md
