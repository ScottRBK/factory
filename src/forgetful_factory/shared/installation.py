"""Install plumbing for locked tool runtimes. Consent is owned by the init workflow."""
import hashlib
import os
import re
import shutil
import zipfile
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.resource_files import write_new
from forgetful_factory.shared.resources import resource_root
from forgetful_factory.shared.sensitive_command import run_owned

SYNC_RECEIPT = '.factory-sync'
LOCKS = resource_root() / 'install-locks.zip'


def sync_fingerprint(inputs: tuple[Path, ...]) -> str:
    return hashlib.sha256(b'\0'.join(path.read_bytes() for path in inputs)).hexdigest()


def runtime_ready(runtime: Path, inputs: tuple[Path, ...], probe: str,
                  term_grace: float = 3) -> bool:
    """A successful locked sync and a usable package are both required; no install here."""
    try:
        if (not (runtime / 'pyvenv.cfg').is_file()
                or (runtime / SYNC_RECEIPT).read_text() != sync_fingerprint(inputs)):
            return False
        run_owned([str(runtime / 'bin/python'), '-I', '-B', '-c', probe], runtime,
                  dict(os.environ), timeout=10, term_grace=term_grace)
    except (OSError, FactoryError):
        return False
    return True


def install_environment(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {key: value for key, value in os.environ.items()
           if not key.upper().startswith(('UV_', 'PIP_', 'NPM_CONFIG_'))
           and key not in ('NODE_OPTIONS', 'VIRTUAL_ENV', 'CONDA_PREFIX', 'UNDICI_USE_MILO')}
    return dict(env, LC_ALL='C', **(extra or {}))


def run_install(args: list[str], cwd: Path, term_grace: float, *, interactive: bool = False,
                extra_env: dict[str, str] | None = None) -> str:
    try:
        return run_owned(args, cwd, install_environment(extra_env),
                         timeout=600, login=interactive, term_grace=term_grace)
    except FactoryError as error:
        raise FactoryError('Dependency installation failed; setup is incomplete. '
                           'Check the package manager and rerun init. '
                           'Diagnostics withheld to protect registry credentials.') from error


def check_uv(workspace: Path, term_grace: float) -> None:
    message = ('Installation requires an existing audited uv >=0.13.5. '
               'Select a working uv on PATH and rerun init; setup is incomplete. '
               'No upgrade was performed.')
    try:
        output = run_owned(['uv', '--version'], workspace, install_environment(), timeout=10,
                           term_grace=term_grace)
    except FactoryError as error:
        raise FactoryError(message) from error
    version = re.fullmatch(r'uv (\d+)\.(\d+)\.(\d+)(?: \([^\r\n]+\))?', output.strip())
    if version is None or tuple(map(int, version.groups())) < (0, 13, 5):
        raise FactoryError(message)


def require_manager(manager: str) -> None:
    if shutil.which(manager) is None:
        raise FactoryError(f'Installation failed: install {manager} '
                           'from a reviewed source first.')


def install_locks(directory: Path, names: tuple[str, ...]) -> str:
    """Write the reviewed lock files and drop the old receipt; return the new fingerprint."""
    with zipfile.ZipFile(LOCKS) as archive:
        for name in names:
            target = directory / name
            expected = archive.read(name).decode()
            write_new(target, expected)
            if target.read_text() != expected:
                raise FactoryError('Installation lock was edited; it was preserved. '
                                   'Review it before retrying installation.')
    (directory / SYNC_RECEIPT).unlink(missing_ok=True)
    return sync_fingerprint(tuple(directory / name for name in names))


def no_installer() -> FactoryError:
    return FactoryError('No reviewed automatic installer for this executable.')
