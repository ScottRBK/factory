"""Bundled role resources: verified package bytes and explicit workspace updates."""
import hashlib
import json
import os
import shutil
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.resource_files import check_real_path
from forgetful_factory.shared.resources import resource_root

PACKAGE_RESOURCES = resource_root()


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def bundled_files() -> dict[str, bytes]:
    """Return each bundled file by workspace path, after its archive checksum passes."""
    manifest = json.loads((PACKAGE_RESOURCES / 'role-resources.json').read_text())
    files = {}
    with zipfile.ZipFile(PACKAGE_RESOURCES / 'role-resources.zip') as archive:
        for name, source in manifest.items():
            for relative, digest in source['files'].items():
                member = f'{name}/{relative}'
                data = archive.read(member)
                if _digest(data) != digest:
                    raise FactoryError('Bundled role resource checksum failed; reinstall factory.')
                files[member] = data
    return files


@dataclass(frozen=True)
class ResourceUpdate:
    """Bundle paths grouped by what an update does to them; current files are not listed."""
    directory: Path
    files: dict[str, bytes]
    add: tuple[str, ...]
    replace: tuple[str, ...]
    edited: tuple[str, ...]


def plan_update(directory: Path) -> ResourceUpdate:
    """Read-only. A file is unedited when its hash matches any version Factory shipped for it."""
    files = bundled_files()
    shipped = json.loads((PACKAGE_RESOURCES / 'role-resources-history.json').read_text())
    # The history must also record the current bundle, so the next release recognizes it.
    if any(_digest(data) not in shipped.get(member, ()) for member, data in files.items()):
        raise FactoryError('Bundled role resource history is incomplete; reinstall factory.')
    add, replace, edited = [], [], []
    for member, data in files.items():
        path = directory / member
        check_real_path(path)
        if not path.exists():
            add.append(member)
        elif not path.is_file():
            raise FactoryError(f'Role resource must be a regular file: {path}. '
                               'Nothing was changed.')
        elif (digest := _digest(path.read_bytes())) != _digest(data):
            (replace if digest in shipped[member] else edited).append(member)
    return ResourceUpdate(directory, files, tuple(add), tuple(replace), tuple(edited))


def _back_up(update: ResourceUpdate, backups: Path) -> Path:
    backups.mkdir(parents=True, exist_ok=True, mode=0o700)
    stamp = datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')
    backup = Path(tempfile.mkdtemp(prefix=f'{stamp}-', dir=backups))
    for member in update.edited:
        target = backup / member
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        shutil.copy2(update.directory / member, target)
    return backup


def apply_update(update: ResourceUpdate, backups: Path) -> Path | None:
    """Replace edited files too, after copying them under a new folder in backups.

    Every new file is staged, and edited files are backed up, before any file is renamed into
    place. A rerun completes an interrupted update.
    """
    staged: dict[Path, Path] = {}
    try:
        for member in (*update.add, *update.replace, *update.edited):
            path = update.directory / member
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            descriptor, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp',
                                                     dir=path.parent)
            staged[path] = Path(temporary)
            with os.fdopen(descriptor, 'wb') as stream:
                stream.write(update.files[member])
        backup = _back_up(update, backups) if update.edited else None
        for path, temporary in staged.items():
            os.replace(temporary, path)
    finally:
        for temporary in staged.values():
            temporary.unlink(missing_ok=True)
    return backup
