"""Fsynced completion receipts, per set and per plan, in one small workspace-owned document.

Version 2 adds the plans list. Version 1 files still load, with no plans; a save writes
version 2.
"""
import json
import os
import stat
from collections.abc import Collection
from dataclasses import asdict, fields
from pathlib import Path

from forgetful_factory.factory.ports import CleanupPlan, CleanupSet, FinishedCleanup
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.resource_files import (
    check_real_path,
    replace_generated_json,
)
from forgetful_factory.shared.watch_stop import check_watch_stop

_LIMIT = 16 * 1024 * 1024


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate receipt field')
        value[key] = item
    return value


def _identity(value: object, kind: type, paths: tuple[str, ...]):
    names = {field.name for field in fields(kind)}
    if (not isinstance(value, dict) or set(value) != names
            or type(value.get('plan_id')) is not int or value['plan_id'] < 1
            or any(not isinstance(value[key], str) or not value[key] or
                   any(ord(c) < 32 for c in value[key]) for key in names - {'plan_id'})
            or any(not Path(value[key]).is_absolute() for key in paths)):
        raise ValueError('Incomplete cleanup receipt identity')
    return kind(**value)


def _rows(value: dict, key: str, kind: type, paths: tuple[str, ...], workspace: str) -> list:
    if not isinstance(value[key], list):
        raise ValueError('Unknown receipt format')
    rows = [_identity(row, kind, paths) for row in value[key]]
    if any(row.workspace != workspace for row in rows):
        raise ValueError('Receipt workspace changed; reconcile copied storage')
    if len(set(rows)) != len(rows):
        raise ValueError('Duplicate completion receipts')
    return rows


def _sorted(rows) -> list[dict]:
    return [asdict(row) for row in sorted(
        rows, key=lambda row: json.dumps(asdict(row), sort_keys=True))]


class FileCleanupReceipts:
    def __init__(self, workspace: Path):
        self.workspace = str(workspace)
        self.path = workspace / '.factory/cleanup-finished.json'

    def load(self) -> FinishedCleanup:
        try:
            return self._load()
        except (OSError, ValueError, TypeError, RecursionError, FactoryError) as error:
            raise FactoryError('Cleanup completion receipts cannot be read durably; preserve '
                               'them and reconcile storage before any further disposal.') from error

    def _load(self) -> FinishedCleanup:
        check_real_path(self.path)
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except FileNotFoundError:
            return FinishedCleanup(frozenset(), frozenset())
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or stat.S_IMODE(info.st_mode) & 0o077 or info.st_nlink != 1):
                raise ValueError('Receipts must be a private owned regular file')
            data = stream.read(_LIMIT + 1)
            if len(data) > _LIMIT:
                raise ValueError('Oversized completion receipts')
            value = json.loads(data, object_pairs_hook=_unique_object)
            if (not isinstance(value, dict) or type(value.get('version')) is not int
                    or set(value) != {1: {'version', 'finished'},
                                      2: {'version', 'finished', 'plans'}}.get(value['version'])):
                raise ValueError('Unknown receipt format')
            resources = _rows(value, 'finished', CleanupSet, ('workspace', 'local_dir', 'path'),
                              self.workspace)
            plans = (_rows(value, 'plans', CleanupPlan, ('workspace',), self.workspace)
                     if 'plans' in value else [])
            # Settle a prior lost fsync acknowledgement before treating the receipt as final.
            os.fsync(stream.fileno())
        directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        return FinishedCleanup(frozenset(resources), frozenset(plans))

    def confirm(self, resource: CleanupSet) -> None:
        check_watch_stop()
        finished = self.load()
        self._save(finished.sets | {resource}, finished.plans,
                   'Cleanup absence was observed but its completion receipt is unconfirmed. '
                   'Names remain reserved; retry fresh native facts after repairing receipt '
                   'storage.')

    def confirm_plans(self, plans: Collection[CleanupPlan]) -> None:
        check_watch_stop()
        finished = self.load()
        self._save(finished.sets, finished.plans | set(plans),
                   'Every cleanup set of the completed plans is confirmed, but their plan '
                   'receipts are unconfirmed. Cleanup reads the plans again next poll; repair '
                   'receipt storage.')

    def _save(self, resources, plans, problem: str) -> None:
        value = {'version': 2, 'finished': _sorted(resources), 'plans': _sorted(plans)}
        try:
            if len((json.dumps(value, indent=2) + '\n').encode()) > _LIMIT:
                raise ValueError('Completion receipts exceed their storage limit; preserve them')
            check_watch_stop()
            replace_generated_json(self.path, value)
            check_watch_stop()
        except (OSError, ValueError, FactoryError) as error:
            raise FactoryError(problem) from error
