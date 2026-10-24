"""Private generated lifecycle data; canonical role files remain user-owned."""
import os
import stat
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import check_real_path
from forgetful_factory.domain.models import FactoryError


def runtime_directory(workspace: Path, *, create: bool = False) -> Path:
    directory = workspace / '.factory/runtime/foreman'
    check_real_path(directory)
    if create:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    if directory.exists():
        info = directory.stat()
        if (not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) & 0o077):
            raise FactoryError(f'Foreman runtime must be a private owned directory: {directory}')
    return directory
