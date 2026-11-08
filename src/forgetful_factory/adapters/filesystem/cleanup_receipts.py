"""Fsynced per-set completion receipts in one small workspace-owned document."""
import json
import os
import stat
from dataclasses import asdict, fields
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    replace_generated_json,
)
from forgetful_factory.application.ports.cleanup_receipts import CleanupSet
from forgetful_factory.application.watch_stop import check_watch_stop
from forgetful_factory.domain.models import FactoryError

_LIMIT = 16 * 1024 * 1024


def _unique_object(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('Duplicate receipt field')
        value[key] = item
    return value


def _resource(value: object) -> CleanupSet:
    names = {field.name for field in fields(CleanupSet)}
    if (not isinstance(value, dict) or set(value) != names
            or type(value.get('plan_id')) is not int or value['plan_id'] < 1
            or any(not isinstance(value[key], str) or not value[key] or
                   any(ord(c) < 32 for c in value[key]) for key in names - {'plan_id'})
            or any(not Path(value[key]).is_absolute()
                   for key in ('workspace', 'local_dir', 'path'))):
        raise ValueError('Incomplete cleanup receipt identity')
    return CleanupSet(**value)


class FileCleanupReceipts:
    def __init__(self, workspace: Path):
        self.workspace = str(workspace)
        self.path = workspace / '.factory/cleanup-finished.json'

    def load(self) -> set[CleanupSet]:
        try:
            return self._load()
        except (OSError, ValueError, TypeError, RecursionError, FactoryError) as error:
            raise FactoryError('Cleanup completion receipts cannot be read durably; preserve '
                               'them and reconcile storage before any further disposal.') from error

    def _load(self) -> set[CleanupSet]:
        check_real_path(self.path)
        try:
            fd = os.open(self.path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        except FileNotFoundError:
            return set()
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                    or stat.S_IMODE(info.st_mode) & 0o077 or info.st_nlink != 1):
                raise ValueError('Receipts must be a private owned regular file')
            data = stream.read(_LIMIT + 1)
            if len(data) > _LIMIT:
                raise ValueError('Oversized completion receipts')
            value = json.loads(data, object_pairs_hook=_unique_object)
            if (not isinstance(value, dict) or set(value) != {'version', 'finished'}
                    or type(value['version']) is not int or value['version'] != 1
                    or not isinstance(value['finished'], list)):
                raise ValueError('Unknown receipt format')
            resources = [_resource(row) for row in value['finished']]
            if any(row.workspace != self.workspace for row in resources):
                raise ValueError('Receipt workspace changed; reconcile copied storage')
            if len(set(resources)) != len(resources):
                raise ValueError('Duplicate completion receipts')
            # Settle a prior lost fsync acknowledgement before treating the receipt as final.
            os.fsync(stream.fileno())
        directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        return set(resources)

    def confirm(self, resource: CleanupSet) -> None:
        check_watch_stop()
        resources = self.load()
        resources.add(resource)
        value = {'version': 1, 'finished': [asdict(row) for row in sorted(
            resources, key=lambda row: json.dumps(asdict(row), sort_keys=True))]}
        try:
            if len((json.dumps(value, indent=2) + '\n').encode()) > _LIMIT:
                raise ValueError('Completion receipts exceed their storage limit; preserve them')
            check_watch_stop()
            replace_generated_json(self.path, value)
            check_watch_stop()
        except (OSError, ValueError, FactoryError) as error:
            raise FactoryError('Cleanup absence was observed but its completion receipt is '
                               'unconfirmed. Names remain reserved; retry fresh native facts '
                               'after repairing receipt storage.') from error
