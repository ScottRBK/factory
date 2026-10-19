"""Recover only Factory-owned local skill-list changes; never regenerate role rosters."""
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    check_skill_file,
    read_generated_json,
    replace_generated_json,
)
from forgetful_factory.domain.models import FactoryError

ROLES = ('foreman', 'feature-owner', 'research', 'implementation', 'review')


class SkillRegistration:
    def __init__(self, directory: Path):
        self.directory = directory
        self.path = directory / 'skill-registration.json'

    def _error(self) -> FactoryError:
        return FactoryError('Conflicting or malformed skill registration receipt/selections: '
                            f'{self.path}. Files preserved; reconcile the recorded skill lists '
                            'with resources.json and the parent roster before rerunning init.')

    @staticmethod
    def _strings(value) -> bool:
        return (isinstance(value, list) and all(isinstance(v, str) and v and '\x00' not in v
                                               for v in value)
                and len(value) == len(set(value)))

    def _owned(self, role: str, value: str) -> bool:
        path = Path(value)
        root = self.directory / role / 'skills'
        bundled = (role, 'factory-maintenance') if role == 'foreman' else (role,)
        return (path.is_absolute() and path.parent.parent == root and path.name == 'SKILL.md'
                and path.parent.name not in (*bundled, '.', '..'))

    def _absolute(self, role: str, values: list[str]) -> list[str]:
        return [str(Path(v) if Path(v).is_absolute() else self.directory / role / v)
                for v in values]

    def read(self) -> dict:
        check_real_path(self.path)
        if not self.path.exists():
            return {'version': 1, 'managed': {}, 'pending': {}}
        try:
            receipt = read_generated_json(self.path)
            if (not isinstance(receipt, dict) or set(receipt) != {'version', 'managed', 'pending'}
                    or type(receipt['version']) is not int or receipt['version'] != 1):
                raise ValueError('Invalid receipt schema')
            managed, pending = receipt['managed'], receipt['pending']
            if not isinstance(managed, dict) or not isinstance(pending, dict):
                raise ValueError('Invalid role maps')
            for role, values in managed.items():
                if (role not in ROLES or not self._strings(values)
                        or any(not self._owned(role, v) for v in values)):
                    raise ValueError('Invalid ownership')
            for role, change in pending.items():
                if (role not in ROLES or not isinstance(change, dict)
                        or set(change) != {'before', 'after', 'parent_before'}
                        or not self._strings(change['before'])
                        or not self._strings(change['after'])):
                    raise ValueError('Invalid pending change')
                before, after = change['before'], change['after']
                owned = managed.get(role, [])
                if (any(v not in owned for v in before if v not in after)
                        or any(not self._owned(role, v) for v in after if v not in before)):
                    raise ValueError('Change is outside managed local skills')
                if ([v for v in before if v not in owned]
                        != [v for v in after if v in before and v not in owned]):
                    raise ValueError('Change reorders manual skills')
                parent = change['parent_before']
                if parent is not None:
                    if not self._strings(parent):
                        raise ValueError('Invalid parent skills')
                    remaining = [v for v in parent if v not in owned]
                    if remaining != [v for v in self._absolute(role, before) if v not in owned]:
                        raise ValueError('Parent change includes manual skills')
            return receipt
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise self._error() from error

    def _parent(self, role: str, files: dict) -> list | None:
        if role == 'foreman':
            return None
        parent = 'foreman' if role == 'feature-owner' else 'feature-owner'
        path = self.directory / parent / 'roster.json'
        if path not in files:
            files[path] = read_generated_json(path)
        entries = [r for r in files[path]['roster']['roles'] if r['name'] == role]
        if len(entries) != 1:
            raise self._error()
        entry = entries[0]
        if role in ('implementation', 'review') and entry['agent_type'] != 'pi':
            return None
        return entry['resources']['skills']

    def _resources(self, role: str, files: dict) -> list:
        path = self.directory / role / 'resources.json'
        if path not in files:
            files[path] = read_generated_json(path)
        skills = files[path]['skills']
        if not self._strings(skills):
            raise self._error()
        return skills

    def update(self, changes: dict[str, list[str]]) -> None:
        receipt = self.read()
        if receipt['pending']:
            raise self._error()
        files = {}
        for role, after in changes.items():
            before = self._resources(role, files)
            parent = self._parent(role, files)
            # Only missing, proven automatic selections may differ from the child list.
            absent = [v for v in receipt['managed'].get(role, []) if not Path(v).exists()]
            if parent is not None and (
                    [v for v in parent if v not in absent]
                    != [v for v in self._absolute(role, before) if v not in absent]):
                raise self._error()
            receipt['pending'][role] = {'before': before.copy(), 'after': after,
                                        'parent_before': parent.copy() if parent is not None
                                        else None}
        if not changes:
            return
        replace_generated_json(self.path, receipt)
        self._finish()

    def _finish(self) -> None:
        receipt = self.read()
        files = {}
        changed = set()
        for role, change in receipt['pending'].items():
            before, after = change['before'], change['after']
            current = self._resources(role, files)
            parent = self._parent(role, files)
            expected_parent = self._absolute(role, after)
            if (current not in (before, after)
                    or (parent is None) != (change['parent_before'] is None)
                    or (parent is not None
                        and parent not in (change['parent_before'], expected_parent))):
                raise self._error()
            owned = [v for v in after if v in receipt['managed'].get(role, []) or v not in before]
            for value in owned:
                check_real_path(Path(value))
                if Path(value).exists():
                    check_skill_file(Path(value))
            receipt['managed'][role] = owned
            if current != after:
                current[:] = after
                changed.add(self.directory / role / 'resources.json')
            if parent is not None and parent != expected_parent:
                parent[:] = expected_parent
                parent_role = 'foreman' if role == 'feature-owner' else 'feature-owner'
                changed.add(self.directory / parent_role / 'roster.json')
        # Every current list was checked before the first write. Each write pins real parents.
        for path in sorted(changed, key=lambda path: (path.name != 'resources.json', path)):
            replace_generated_json(path, files[path])
        if receipt['pending']:
            receipt['pending'] = {}
            replace_generated_json(self.path, receipt)

    def recover(self) -> None:
        try:
            self._finish()
            receipt = self.read()
            changes = {}
            for role, owned in receipt['managed'].items():
                for value in owned:
                    check_real_path(Path(value))
                missing = [v for v in owned if not Path(v).exists()]
                if missing:
                    skills = self._resources(role, {})
                    changes[role] = [v for v in skills if v not in missing]
            self.update(changes)
        except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
            raise self._error() from error
