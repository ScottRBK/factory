"""Private generated lifecycle data; canonical role files remain user-owned."""
import os
import shlex
import stat
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.resource_files import check_real_path


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


def factory_launcher(workspace: Path, python: str) -> Path:
    """Write the command in FACTORY_COMMAND: one path that runs this Factory.

    One path works with or without shell quotes, for every install method. It is written again
    at each Foreman start, so it always runs the Factory that started that Foreman.
    """
    directory = runtime_directory(workspace, create=True)
    launcher = directory / 'forgetful-factory'
    pending = directory / f'.forgetful-factory.{os.getpid()}.tmp'
    script = ('#!/bin/sh\n# Written by Forgetful Factory at each Foreman start.\n'
              f'exec {shlex.quote(python)} -m forgetful_factory "$@"\n')
    try:
        pending.unlink(missing_ok=True)
        descriptor = os.open(pending, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o700)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            os.fchmod(stream.fileno(), 0o700)
            stream.write(script)
        # A rename replaces a link in that place; it never writes through it.
        os.replace(pending, launcher)
    except OSError as error:
        raise FactoryError(f'Cannot write the Factory launcher {launcher}: {error}') from error
    return launcher.absolute()
