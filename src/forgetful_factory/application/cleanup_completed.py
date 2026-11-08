"""Completed-plan discovery and disposal, independent of issue intake and DoD prose."""
import json
import os
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from forgetful_factory.application.factory_records import FactoryRecords
from forgetful_factory.application.ports.cleanup_receipts import CleanupReceipts, CleanupSet
from forgetful_factory.application.ports.planning import PlanningReadError
from forgetful_factory.application.ports.worktrees import Worktrees
from forgetful_factory.application.watcher_problems import ScaffoldProblem, WatcherAlerts
from forgetful_factory.domain.models import FactoryError

_TARGET_KEYS = ('target', 'common-target', 'remote-target')
_RECEIPTS_ALERT_SUBJECT = 'cleanup:receipts'


@dataclass
class CompletedWork:
    plan_id: int
    reference: str
    task_id: int
    mappings: list[dict]


def _claim_path(value: str) -> str:
    try:
        return str(Path(value).resolve())
    except (OSError, RuntimeError, ValueError):
        # Invalid paths are still indexed conservatively; the Git boundary refuses them.
        return os.path.abspath(value)


class CleanupCompleted:
    def __init__(self, records: FactoryRecords, worktrees: Worktrees, receipts: CleanupReceipts):
        self.records = records
        self.worktrees = worktrees
        self.owners: dict[int, int] = {}
        self.receipts = receipts
        self.confirmed: set[CleanupSet] = set()
        self.cursor: tuple | None = None

    def poll(self, alerts: WatcherAlerts, report) -> None:
        try:
            self.confirmed = self.receipts.load()
        except FactoryError as error:
            alerts.send(_RECEIPTS_ALERT_SUBJECT, error, scope='cleanup',
                        code='cleanup_receipt_failed', retry='next_poll')
            return
        alerts.clear(_RECEIPTS_ALERT_SUBJECT)
        try:
            inventory = self.records.planning.plans()
        except FactoryError as error:
            alerts.send('cleanup:inventory', error, scope='cleanup',
                        code='cleanup_inventory_read_failed', retry='next_poll')
            return
        alerts.clear('cleanup:inventory')
        plans = self._read_plans(inventory, alerts)
        if plans is None or not any(self._in_scope(plan) for plan in plans):
            return
        candidates = self._candidates(plans, alerts)
        if candidates is None:
            return
        try:
            candidates = [w for w in candidates if any(
                not self._is_confirmed(w.plan_id, w.reference, m) for m in w.mappings)]
        except FactoryError as error:
            alerts.send(_RECEIPTS_ALERT_SUBJECT, error, scope='cleanup',
                        code='cleanup_receipt_failed', retry='next_poll')
            return
        if not candidates:
            return
        claims = defaultdict(set)
        references = defaultdict(set)
        # Summary conflicts can withhold authority, never grant it. An unreadable duplicate
        # does not make the other visible plan the primary identity.
        for summary in [*inventory, *plans]:
            if isinstance(summary.get('external_ref'), str):
                references[summary['external_ref']].add(summary['id'])
        identities = self._repository_identities(alerts)
        if identities is None:
            return
        for plan in plans:
            try:
                self._claims(self.records.planning.tasks(plan['id']), plan['id'],
                             claims, identities)
            except FactoryError as error:
                self._read_problem(plan['id'], error, alerts)
                return
        self.worktrees.begin_cleanup_cycle()
        pending = sorted((self._order(w, m), w, m) for w in candidates for m in w.mappings
                         if not self._is_confirmed(w.plan_id, w.reference, m))
        selected = next((item for item in pending if self.cursor is None or item[0] > self.cursor),
                        pending[0])
        self.cursor, work, mapping = selected
        self._dispose(work, mapping, claims, references, identities, alerts, report)

    def _read_plans(self, inventory: list[dict], alerts: WatcherAlerts) -> list[dict] | None:
        plans = []
        for summary in inventory:
            try:
                plan = self.records.planning.get_plan(summary['id'])
            except FactoryError as error:
                self._read_problem(summary['id'], error, alerts)
                return None
            plans.append(plan)
        return plans

    def _candidates(self, plans: list[dict], alerts: WatcherAlerts) -> list[CompletedWork] | None:
        candidates = []
        for plan in plans:
            if not self._in_scope(plan):
                continue
            try:
                candidates.append(self._candidate(plan, {}))
            except FactoryError as error:
                alerts.send(f'cleanup:{plan["id"]}', error, scope='cleanup',
                            code=getattr(error, 'code', 'cleanup_read_failed'), retry='next_poll',
                            plan_id=plan['id'], issue_id=plan['external_ref'])
                if isinstance(error, PlanningReadError) or getattr(error, 'code', '') in (
                        'ownership_invalid', 'mapping_invalid', 'cleanup_target_missing'):
                    return None
        return candidates

    def _candidate(self, plan: dict, identities: dict[str, str]) -> CompletedWork:
        reference = plan['external_ref']
        self.records.snapshot(self.records.context(plan), reference)
        owners = self.records.ownership(plan['id'], reference)
        if len(owners) != 1:
            raise ScaffoldProblem('ownership_ambiguous' if owners else 'ownership_missing',
                                  'Completed-plan cleanup needs one ownership task; '
                                  'reconcile the saved records.')
        pinned = self.owners.setdefault(plan['id'], owners[0]['id'])
        if pinned != owners[0]['id']:
            raise ScaffoldProblem('ownership_identity_changed',
                                  'Cleanup ownership was replaced; reconcile it.')
        mappings = json.loads(owners[0]['description'])['worktrees']
        seen = set()
        resources = set()
        for mapping in mappings:
            repository = self.records.mapping_repository(mapping, seen)
            self.records.check_source(repository)
            target = Path(_claim_path(mapping['path']))
            if any(Path(_claim_path(r.local_dir)).is_relative_to(target)
                   for r in self.records.config.repository):
                raise ScaffoldProblem('cleanup_path_invalid',
                                      'Cleanup path contains a configured repository root; '
                                      'preserve that checkout.', paths=(mapping['path'],))
            keys = {key for key in self._keys(mapping, identities)
                    if key[0] in ('path', 'branch', 'common-branch')}
            if keys & resources:
                raise ScaffoldProblem('cleanup_ownership_conflict',
                                      'Duplicate canonical path or feature branch in ownership; '
                                      'reconcile before cleanup.')
            resources.update(keys)
            if not isinstance(mapping.get('target_branch'), str) or not mapping['target_branch']:
                raise ScaffoldProblem('cleanup_target_missing',
                                      'Cleanup needs a reviewed target_branch mapping; '
                                      'reconcile old records before adoption.')
        return CompletedWork(plan['id'], reference, owners[0]['id'], mappings)

    @staticmethod
    def _read_problem(plan_id: int, error: FactoryError, alerts: WatcherAlerts) -> None:
        alerts.send(f'cleanup:{plan_id}', error, scope='cleanup', code='cleanup_read_failed',
                    retry='next_poll', plan_id=plan_id)

    def _in_scope(self, plan: dict) -> bool:
        if (plan.get('project_id') != self.records.config.forgetful.project_id
                or plan.get('status') != 'completed'):
            return False
        reference = plan.get('external_ref')
        return isinstance(reference, str) and any(
            re.fullmatch(r'github:' + re.escape(r.work_source.reference.casefold()) + r'#[1-9]\d*',
                         reference) for r in self.records.config.repository)

    def _repository_identities(self, alerts: WatcherAlerts) -> dict[str, str] | None:
        identities = {}
        for repository in self.records.config.repository:
            subject = f'cleanup:repository:{repository.local_dir}'
            try:
                # A readable local namespace still withholds authority when its origin is
                # wrong. Origin/source are separately required before that mapping's disposal.
                identity = self.worktrees.repository_identity(repository.local_dir)
            except FactoryError as error:
                alerts.send(subject, error, scope='cleanup', code='cleanup_read_failed',
                            retry='next_poll', paths=(repository.local_dir,))
                return None
            identities[_claim_path(repository.local_dir)] = identity
            alerts.clear(subject)
        return identities

    @staticmethod
    def _keys(mapping: dict, identities: dict[str, str]) -> set[tuple]:
        keys = set()
        if isinstance(mapping.get('path'), str):
            keys.add(('path', _claim_path(mapping['path'])))
        for field, kind in (('branch', 'branch'), ('target_branch', 'target')):
            name = mapping.get(field)
            if not isinstance(name, str):
                continue
            local = mapping.get('local_dir')
            if isinstance(local, str):
                root = _claim_path(local)
                keys.add((kind, root, name))
                if root in identities:
                    keys.add(('common-' + kind, identities[root], name))
            repository = mapping.get('repository')
            if isinstance(repository, str):
                keys.add(('remote-' + kind, repository.casefold(), name))
        return keys

    def _claims(self, tasks: list[dict], plan_id: int, claims: dict,
                identities: dict[str, str]) -> None:
        for task in tasks:
            for mapping in self._task_mappings(task):
                record = json.loads(task['description'])
                if self._is_confirmed(plan_id, record['external_ref'], mapping,
                                      workspace=record['workspace']):
                    continue
                root = _claim_path(mapping['local_dir'])
                if root not in identities:
                    identities[root] = self.worktrees.repository_identity(mapping['local_dir'])
                for key in self._keys(mapping, identities):
                    claims[key].add((plan_id, task['id']))

    @staticmethod
    def _task_mappings(task: dict) -> list[dict]:
        try:
            record = json.loads(task.get('description') or '{}')
        except (ValueError, TypeError) as error:
            if task.get('title') == 'Feature ownership':
                raise ScaffoldProblem(
                    'ownership_invalid', 'Invalid ownership JSON; all cleanup waits for repair.'
                ) from error
            return []
        marked = isinstance(record, dict) and record.get('kind') == 'factory-ownership'
        if not marked and task.get('title') != 'Feature ownership':
            return []
        if (not marked or not isinstance(record.get('workspace'), str)
                or not record['workspace'] or not isinstance(record.get('external_ref'), str)
                or not record['external_ref'] or not isinstance(record.get('worktrees'), list)):
            raise ScaffoldProblem('ownership_invalid',
                                  'Incomplete ownership claims; all cleanup waits for repair.')
        for mapping in record['worktrees']:
            CleanupCompleted._validate_claim_mapping(mapping)
        return record['worktrees']

    @staticmethod
    def _validate_claim_mapping(mapping: object) -> None:
        if not isinstance(mapping, dict) or any(
                not isinstance(mapping.get(field), str) or not mapping[field]
                for field in ('repository', 'local_dir', 'branch', 'path')):
            raise ScaffoldProblem('mapping_invalid',
                                  'Incomplete resource claims; all cleanup waits for repair.')
        if not isinstance(mapping.get('target_branch'), str) or not mapping['target_branch']:
            raise ScaffoldProblem('cleanup_target_missing',
                                  'Unknown claimed merge target; all cleanup waits for review.')

    @staticmethod
    def _overlaps(mapping: dict, claims: dict) -> bool:
        target = Path(_claim_path(mapping['path']))
        return any(key[0] == 'path' and Path(key[1]) != target and
                   (target.is_relative_to(key[1]) or Path(key[1]).is_relative_to(target))
                   for key in claims)

    def _dispose(self, work: CompletedWork, mapping: dict, claims: dict, references: dict,
                 identities: dict[str, str], alerts: WatcherAlerts, report) -> bool:
        identity = self._mapping_identity(work.plan_id, work.reference, mapping)
        if identity in self.confirmed:
            return True
        subject = f'cleanup:{work.plan_id}:{mapping["path"]}'
        try:
            completed = self._still_completed(work)
        except FactoryError as error:
            self._read_problem(work.plan_id, error, alerts)
            return False
        if not completed:
            return True
        try:
            self._check_namespaces(work.mappings, identities)
            if (len(references[work.reference]) != 1
                    or self._overlaps(mapping, claims)
                    or ('remote-target', mapping['repository'].casefold(),
                        mapping['branch']) in claims
                    or ('common-target', identities[_claim_path(mapping['local_dir'])],
                        mapping['branch']) in claims
                    or ('target', _claim_path(mapping['local_dir']),
                        mapping['branch']) in claims
                    or any(claims[key] != {(work.plan_id, work.task_id)}
                           for key in self._keys(mapping, identities)
                           if key[0] not in _TARGET_KEYS)):
                raise ScaffoldProblem('cleanup_ownership_conflict',
                                      'Competing cleanup ownership; reconcile all mappings. '
                                      'No affected resource is removed.')
            repository = self.records.mapping_repository(mapping, set())
            self.records.check_repository(repository)
            self.worktrees.dispose(repository.local_dir, mapping['branch'], mapping['path'],
                                   remote=repository.remote,
                                   target_branch=mapping['target_branch'])
            try:
                self.receipts.confirm(identity)
            except FactoryError as error:
                raise ScaffoldProblem('cleanup_receipt_failed', str(error)) from error
        except FactoryError as error:
            alerts.send(subject, error, scope='cleanup',
                        code=getattr(error, 'code', 'cleanup_operation_uncertain'),
                        retry='next_poll', plan_id=work.plan_id,
                        ownership_task_id=work.task_id, paths=(mapping['path'],))
            return True
        alerts.clear(subject)
        self.confirmed.add(identity)
        report(f'Cleanup confirmed for completed plan {work.plan_id}: '
               f'{mapping["path"]}; worktree, local and remote feature refs absent.')
        alerts.clear(f'cleanup:{work.plan_id}')
        return True

    @staticmethod
    def _order(work: CompletedWork, mapping: dict) -> tuple:
        return (work.plan_id, mapping['local_dir'], mapping['branch'], mapping['path'])

    def _check_namespaces(self, mappings: list[dict], identities: dict[str, str]) -> None:
        resources = set()
        for mapping in mappings:
            keys = {key for key in self._keys(mapping, identities)
                    if key[0] in ('path', 'branch', 'common-branch')}
            if keys & resources:
                raise ScaffoldProblem('cleanup_ownership_conflict',
                                      'Duplicate canonical cleanup namespaces; '
                                      'reconcile ownership.')
            resources.update(keys)

    def _mapping_identity(self, plan_id: int, reference: str, mapping: dict, *,
                          workspace: str | None = None) -> CleanupSet:
        connection = self.records.config.forgetful
        backend = connection.instance + ':' + (connection.server or connection.database)
        return CleanupSet(workspace or str(self.records.workspace), backend, plan_id, reference,
                          mapping['repository'].casefold(), mapping['local_dir'],
                          mapping['branch'], mapping['path'])

    def _is_confirmed(self, plan_id: int, reference: str, mapping: dict, *,
                      workspace: str | None = None) -> bool:
        identity = self._mapping_identity(plan_id, reference, mapping, workspace=workspace)
        if identity in self.confirmed:
            return True
        if any(identity.overlaps(saved) for saved in self.confirmed):
            raise ScaffoldProblem('cleanup_receipt_conflict',
                                  'A completed plan changed a confirmed resource identity; '
                                  'preserve reused names and reconcile its mapping.')
        return False

    def _still_completed(self, work: CompletedWork) -> bool:
        owners = self.records.ownership(work.plan_id, work.reference)
        if (len(owners) != 1 or owners[0]['id'] != work.task_id
                or json.loads(owners[0]['description'])['worktrees'] != work.mappings):
            raise ScaffoldProblem('ownership_identity_changed',
                                  'Cleanup ownership/mappings changed; reread next poll.')
        plan = self.records.planning.get_plan(work.plan_id)
        if plan.get('external_ref') != work.reference:
            raise ScaffoldProblem('plan_identity_changed',
                                  'Cleanup plan association changed; reconcile it.')
        self.records.snapshot(self.records.context(plan), work.reference)
        return self._in_scope(plan)
