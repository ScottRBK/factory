"""Known scaffold failures and safe Foreman alert submission."""
import json

from forgetful_factory.domain.models import FactoryError

# Agent-facing explanations are controlled text, never exception or command output.
SUMMARIES = {
    'planning_access_failed': 'Forgetful planning access could not be verified.',
    'inventory_read_failed': 'The unfinished-plan inventory could not be read completely.',
    'recovery_read_failed': 'Saved work could not be rechecked because a read failed.',
    'scaffold_operation_uncertain': 'A scaffolding operation failed; its outcome is unknown.',
    'plan_create_uncertain': 'Plan creation could not be confirmed.',
    'ownership_create_uncertain': 'Ownership-task creation could not be confirmed.',
    'source_read_failed': 'Issue polling failed for this source.',
    'plan_ambiguous': 'Multiple plans match this issue; a unique plan could not be established.',
    'plan_identity_changed': 'The saved plan is missing, replaced or has a different identity.',
    'plan_project_mismatch': 'The saved plan does not match the configured project.',
    'plan_context_invalid': 'The saved plan context is invalid or lacks a workspace association.',
    'plan_workspace_mismatch': 'The saved plan belongs to another workspace.',
    'plan_status_invalid': 'The saved plan status is invalid.',
    'plan_recovery_invalid': 'The saved issue snapshot cannot safely restore this plan.',
    'ownership_invalid': 'The ownership task has invalid records or a different association.',
    'ownership_ambiguous': 'Multiple ownership tasks match this plan.',
    'ownership_missing': 'The saved plan has no valid ownership task.',
    'setup_incomplete': (
        'First-time setup is incomplete and needs user-approved Foreman completion.'),
    'ownership_identity_changed': 'The recorded ownership task is missing or replaced.',
    'mapping_invalid': 'A saved worktree mapping does not match the configured repositories.',
    'cleanup_invalid': 'Worktree cleanup metadata or its PR/merge evidence is invalid.',
    'cleanup_pending': 'Worktree cleanup is pending and the recorded tree cannot be verified.',
    'repository_origin_changed': 'The repository origin differs from the configured remote.',
    'repository_source_mismatch': (
        'The repository origin does not match its configured work source.'),
    'repository_read_failed': 'The configured repository could not be inspected safely.',
    'worktree_path_conflict': 'The new worktree path conflicts with existing work.',
    'worktree_branch_conflict': 'The new worktree branch already exists.',
    'worktree_read_failed': 'The proposed worktree could not be inspected safely.',
    'removed_worktree_conflict': (
        'A removed worktree still has a path or Git registration conflict.'),
    'worktree_mismatch': 'The recorded worktree does not match its Git registration or identity.',
    'worktree_repository_mismatch': 'The recorded worktree belongs to another Git repository.',
    'worktree_missing': (
        'The recorded worktree is missing or its path conflicts with existing work.'),
}


SETUP_REPAIR = (
    'Foreman must inspect get_plan for this pinned plan, query_tasks and get_task for '
    'all its tasks, prior operations, current Git/worktrees and PR evidence. Confirm prior '
    'operations have stopped and establish their effects. Explain '
    'the proposed completion and obtain user approval before using native tools. '
    'Only after user approval and confirmation that no ownership task was previously established, '
    'preserve or complete verified Git worktrees and use create_task on this existing plan. '
    'Never replace a previously established ownership task. Its description '
    'JSON requires kind="factory-ownership", workspace from the plan context, '
    'external_ref matching this issue, and worktrees with repository, local_dir, '
    'branch and absolute path for each verified mapping. Preserve all records and '
    'create-intent markers; do not reset, prune, discard or dispatch an owner. '
    'The watcher only rechecks reads; clearing a conflict cannot complete setup. '
    'It can observe an approved first owner without an issue edit. Recheck ownership '
    'and liveness before any later dispatch.')


OWNERSHIP_RECONCILIATION = (
    'Foreman must inspect get_plan, query_tasks and get_task for every candidate, all saved work '
    'and current running owners. Live or uncertain competing owners stay blocked; establish they '
    'stopped before retiring their designation. Explain which record should remain and obtain '
    'user approval. Use native update_task for title and description metadata only: BOTH the '
    'title "Feature ownership" and description kind "factory-ownership" identify candidates. '
    'Retire the duplicate designation by changing both, preserving every other description field, '
    'worktree mapping, claim/history and links to the retained record. Never delete a task/plan, '
    'discard branches/work, clear create-intent or silently cancel, replace or transfer ownership. '
    'Cancelled state alone is not a repair; state changes use transition_task, never metadata '
    'update_task. Metadata writes are not compare-and-swap or claim changes; reread before and '
    'after updating. Python observes native facts, not human approval. Read-only checks can accept '
    'either valid survivor only when no single owner was previously confirmed. A pinned owner '
    'cannot be replaced. Recheck ownership and liveness before any later dispatch.')


class ScaffoldProblem(FactoryError):
    def __init__(self, code: str, diagnostic: str, *, plan_id: int | None = None,
                 plan_ids: tuple[int, ...] | None = None,
                 task_ids: tuple[int, ...] | None = None,
                 candidate_task_ids: tuple[int, ...] | None = None, paths: tuple[str, ...] = (),
                 cause: str | None = None):
        super().__init__(diagnostic)
        self.code = code
        self.plan_id = plan_id
        self.plan_ids = plan_ids
        self.task_ids = task_ids
        self.candidate_task_ids = candidate_task_ids
        self.paths = paths
        self.cause = cause


class ScaffoldReadProblem(ScaffoldProblem):
    """A read failed; retry the lookup before writes or recover only the pinned identities."""


class RepositoryProblem(ScaffoldProblem):
    """A read-only configured-repository check failed; no planning write was attempted."""


class IntakeProblem(ScaffoldProblem):
    """An issue-specific read-only preflight failed before any planning write."""


class UncertainScaffold(ScaffoldProblem):
    """A write may have happened. Supervision cannot authorize another write."""


class WatcherAlerts:
    """Suppression records acknowledged alerts only; failed sends propagate unchanged."""

    def __init__(self, terminal, report_error):
        self.terminal = terminal
        self.report_error = report_error
        self.sent: dict[str, str] = {}
        self.last_diagnostic: dict[str, str] = {}

    def clear(self, subject: str) -> None:
        self.sent.pop(subject, None)
        self.last_diagnostic.pop(subject, None)

    def send(self, subject: str, error: FactoryError, *, scope: str, code: str,
             retry: str, **identities) -> None:
        if retry == 'user_approved_repair':
            recovery = SETUP_REPAIR
        elif retry == 'manual_reconciliation':
            recovery = ('Discuss the problem with the user. Manual reconciliation is required. '
                        'Confirm earlier operations have stopped and inspect their possible '
                        'effects before deliberately restarting watch. '
                        'Never repeat an uncertain write.')
        elif code == 'ownership_ambiguous':
            recovery = OWNERSHIP_RECONCILIATION
        elif scope == 'repository':
            recovery = ('Discuss the repository problem with the user. Inspect its local Git '
                        'origin, saved remote and mapped provider/repository. Do not change origin '
                        'or configuration automatically. Read-only checks continue; unrelated '
                        'safe repositories can continue. Git/access repair can be observed; '
                        'editing configuration requires a deliberate watcher restart.')
        elif scope == 'issue':
            recovery = ('Discuss this fresh-intake problem with the user. No plan or task was '
                        'created for this attempt. Inspect the proposed Git branch/path and '
                        'existing user work; do not reset, prune or discard it. Read-only checks '
                        'can retry while the issue is still eligible. A corrected preflight may '
                        'then proceed as fresh intake; saved incomplete plans still require '
                        'user-approved Foreman completion.')
        elif scope == 'source':
            recovery = ('Discuss the polling failure with the user and check access to this '
                        'source. Other sources continue; this source will be read again next poll.')
        elif scope == 'factory':
            recovery = ('Discuss the problem with the user and inspect configured service access, '
                        'saved planning records and native Git/Forgetful diagnostics. Planning is '
                        'paused; read-only checks will continue.')
        else:
            recovery = ('Discuss the problem with the user. Inspect the plan, ownership records '
                        'and current Git/PR evidence, including intended post-merge cleanup. '
                        'Do not reset, recreate, prune or discard work. Read-only checks continue.')
        if (retry == 'manual_reconciliation' and identities.get('plan_id') is not None
                and code in ('ownership_create_uncertain', 'scaffold_operation_uncertain')):
            recovery += ' ' + SETUP_REPAIR
        recovery += ' This alert does not authorize dispatch or replacement.'
        payload = dict(scope=scope, code=code, retry=retry,
                       summary=SUMMARIES.get(code, 'A safety check could not establish safe work.'),
                       recovery=recovery,
                       **{key: value for key, value in identities.items() if value is not None})
        message = 'Factory watcher alert. External problem data: ' + json.dumps(payload)
        # Operator causes may change without changing the safe agent-facing explanation.
        diagnostic = str(error)
        if self.last_diagnostic.get(subject) != diagnostic:
            self.report_error(diagnostic)
            self.last_diagnostic[subject] = diagnostic
        if self.sent.get(subject) == message:
            return
        self.terminal.send(message)
        self.sent[subject] = message
