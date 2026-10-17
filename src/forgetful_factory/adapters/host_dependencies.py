"""Consent is owned by the init workflow. These recipes use reviewed, frozen dependency graphs."""
import hashlib
import json
import os
import platform
import re
import shutil
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from forgetful_factory.adapters.filesystem.resource_files import write_new
from forgetful_factory.adapters.sensitive_command import run_owned
from forgetful_factory.domain.models import FactoryError

SYNC_RECEIPT = '.factory-sync'
FORGETFUL_REQUIREMENTS = 'forgetful-requirements.txt'
PI_INPUTS = ('package.json', 'package-lock.json')
LOCKS = Path(__file__).resolve().parents[1] / 'resources/install-locks.zip'


def executable_path(workspace: Path) -> str:
    runtime = workspace / '.factory/runtime'
    return os.pathsep.join((str(runtime / 'pi/node_modules/.bin'),
                            str(runtime / 'forgetful/bin'), os.environ.get('PATH', '')))


def sync_fingerprint(inputs: tuple[Path, ...]) -> str:
    return hashlib.sha256(b'\0'.join(path.read_bytes() for path in inputs)).hexdigest()


def runtime_ready(runtime: Path, inputs: tuple[Path, ...], probe: str) -> bool:
    """A successful locked sync and a usable package are both required; no install here."""
    try:
        if (not (runtime / 'pyvenv.cfg').is_file()
                or (runtime / SYNC_RECEIPT).read_text() != sync_fingerprint(inputs)):
            return False
        run_owned([str(runtime / 'bin/python'), '-I', '-B', '-c', probe], runtime,
                  dict(os.environ), timeout=10)
    except (OSError, FactoryError):
        return False
    return True


ROLE_PROBE = ('from agent_shell.shell import AgentShell; '
              'from agent_shell.tmux import TmuxExecutionHost')
FORGETFUL_PROBE = ('import app; import importlib.util; '
                   'assert importlib.util.find_spec("main") is not None')


class HostDependencies:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.runtime = workspace / '.factory/runtime'

    def pi_ready(self, pi_home: str) -> bool:
        directory = self.runtime / 'pi'
        try:
            inputs = tuple(directory / name for name in PI_INPUTS)
            if (directory / SYNC_RECEIPT).read_text() != sync_fingerprint(inputs):
                return False
            env = self._environment({
                'PI_OFFLINE': '1',
                'PI_CODING_AGENT_DIR': pi_home,
            })
            env.pop('FORGETFUL_TOKEN', None)
            version = run_owned([str(directory / 'node_modules/.bin/pi'), '--version'],
                                directory, env, timeout=10)
            return version.strip() == '1.2.0'
        except (OSError, FactoryError):
            return False

    @staticmethod
    def _ubuntu_tmux() -> bool:
        try:
            release = platform.freedesktop_os_release()
            return (release.get('ID') == 'ubuntu' and release.get('VERSION_ID') == '24.04'
                    and platform.machine() == 'x86_64')
        except OSError:
            return False

    def description(self, command: str) -> str | None:
        if command == 'agentshell-runtime':
            return ('Install the AgentShell extension runtime from its reviewed upstream uv lock? '
                    'Uses existing Python and uv >=0.13.1 in the role directory. [y/N]: ')
        if command == 'pi':
            return ('Install Pi 1.2.0 in .factory/runtime/pi with the reviewed npm lock? '
                    'Uses existing Node/npm; npm scripts are disabled. [y/N]: ')
        if command == 'forgetful':
            # The workflow requests this description before asking for installation consent.
            python = self._forgetful_python()
            return ('Install Forgetful CLI 0.5.5 in .factory/runtime/forgetful?\n'
                    'This adds the command-line tool; it does not start another server.\n'
                    f'Downloads from PyPI using existing Python 3.12:\n  {python}\n'
                    'Proceed? [y/N]: ')
        if command == 'tmux' and self._ubuntu_tmux():
            return ('Install Ubuntu tmux 3.4-1ubuntu0.1 using apt-get --no-upgrade '
                    '--no-install-recommends? This is a privileged system install and may add '
                    'OS dependencies; no apt update runs. [y/N]: ')
        # Other hosts and explicitly named executables require a reviewed manual installation.
        return None

    def _environment(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        env = {key: value for key, value in os.environ.items()
               if not key.upper().startswith(('UV_', 'PIP_', 'NPM_CONFIG_'))
               and key not in ('NODE_OPTIONS', 'VIRTUAL_ENV', 'CONDA_PREFIX')}
        return dict(env, LC_ALL='C', **(extra or {}))

    def _run(self, args: list[str], cwd: Path, *, interactive: bool = False,
             extra_env: dict[str, str] | None = None) -> str:
        try:
            return run_owned(args, cwd, self._environment(extra_env),
                             timeout=600, login=interactive)
        except FactoryError as error:
            raise FactoryError('Dependency installation failed; setup is incomplete. '
                               'Check the package manager and rerun init. '
                               'Diagnostics withheld to protect registry credentials.') from error

    def _check_uv(self) -> None:
        message = ('Installation requires an existing audited uv >=0.13.1. '
                   'Select a working uv on PATH and rerun init; setup is incomplete. '
                   'No upgrade was performed.')
        try:
            output = run_owned(['uv', '--version'], self.workspace, self._environment(), timeout=10)
        except FactoryError as error:
            raise FactoryError(message) from error
        version = re.fullmatch(r'uv (\d+)\.(\d+)\.(\d+)(?: \([^\r\n]+\))?', output.strip())
        if version is None or tuple(map(int, version.groups())) < (0, 13, 1):
            raise FactoryError(message)

    def _forgetful_python(self) -> str:
        """Preflight an existing 3.12 independently of Factory's own interpreter."""
        self._check_uv()
        try:
            env = self._environment()
            python = run_owned(
                ['uv', 'python', 'find', 'cpython@3.12', '--system', '--no-project',
                 '--no-config', '--no-python-downloads', '--offline', '--no-cache'],
                self.workspace, env, timeout=10).strip()
            path = Path(python)
            if (not python.isprintable() or not path.is_absolute() or not path.is_file()
                    or not os.access(path, os.X_OK)):
                raise ValueError('Invalid Python discovery result')
            version = run_owned(
                [python, '-I', '-B', '-S', '-c',
                 'import sys; print(sys.implementation.name, *sys.version_info[:2])'],
                self.workspace, env, timeout=10)
            if version.strip() != 'cpython 3 12':
                raise ValueError('Incompatible Python')
            return python
        except (FactoryError, OSError, ValueError) as error:
            raise FactoryError('Forgetful CLI needs an already installed Python 3.12 (CPython). '
                               'Make it discoverable on PATH as python3.12, then rerun init. '
                               'No Python was downloaded; setup is incomplete.') from error

    def _install_tmux(self) -> None:
        args = ['apt-get', 'install', '--yes', '--no-upgrade', '--no-install-recommends',
                'tmux=3.4-1ubuntu0.1']
        preview = self._run(['apt-get', '--simulate', *args[1:]], self.runtime.parent)
        if not re.search(r'(?m)^0 upgraded, \d+ newly installed, 0 to remove', preview):
            raise FactoryError('tmux installation would upgrade/remove packages, or the '
                               'transaction could not be verified; nothing was installed.')
        if os.geteuid() != 0:
            args[:0] = ['sudo', '--stdin']
        self._run(args, self.runtime.parent, interactive=True)

    def _install_role_runtime(self) -> None:
        self._check_uv()
        project = self.workspace / '.factory/agents/foreman/resources/agentshell/python'
        inputs = (project / 'pyproject.toml', project / 'uv.lock')
        manifest = json.loads((LOCKS.parent / 'role-resources.json').read_text())
        for path in inputs:
            expected = manifest['agentshell']['files'][f'python/{path.name}']
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise FactoryError('AgentShell installation lock/project was edited; '
                                   'edits preserved. Restore reviewed inputs and rerun init.')
        runtime = project / '.venv'
        (runtime / SYNC_RECEIPT).unlink(missing_ok=True)
        fingerprint = sync_fingerprint(inputs)
        # package=false: only dependencies are installed, so no installed path refers to staging.
        # A standalone workspace prevents uv from inheriting repository workspace/source overrides.
        with TemporaryDirectory(prefix='factory-role-install-') as temporary:
            staging = Path(temporary)
            shutil.copyfile(inputs[1], staging / 'uv.lock')
            (staging / 'pyproject.toml').write_text(
                inputs[0].read_text() + '\n[tool.uv.workspace]\nmembers = []\n')
            self._run(['uv', 'sync', '--project', str(staging), '--locked', '--no-build',
                       '--no-dev', '--no-config', '--python', sys.executable,
                       '--no-python-downloads'], staging,
                      extra_env={'UV_PROJECT_ENVIRONMENT': str(runtime)})
        (runtime / SYNC_RECEIPT).write_text(fingerprint)

    def install(self, command: str) -> None:
        if command == 'tmux' and self._ubuntu_tmux():
            self._install_tmux()
            return
        if command == 'agentshell-runtime':
            self._install_role_runtime()
            return
        if command not in ('pi', 'forgetful'):
            raise FactoryError('No reviewed automatic installer for this executable.')
        manager = 'npm' if command == 'pi' else 'uv'
        if shutil.which(manager) is None:
            raise FactoryError(f'Installation failed: install {manager} '
                               'from a reviewed source first.')
        python = self._forgetful_python() if command == 'forgetful' else None
        directory = self.runtime / command
        with zipfile.ZipFile(LOCKS) as archive:
            names = (PI_INPUTS if command == 'pi' else
                     (FORGETFUL_REQUIREMENTS,))
            for name in names:
                target = directory / name
                expected = archive.read(name).decode()
                write_new(target, expected)
                if target.read_text() != expected:
                    raise FactoryError('Installation lock was edited; it was preserved. '
                                       'Review it before retrying installation.')
        (directory / SYNC_RECEIPT).unlink(missing_ok=True)
        fingerprint = sync_fingerprint(tuple(directory / name for name in names))
        if command == 'pi':
            self._run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund',
                       '--engine-strict', '--userconfig=/dev/null', '--globalconfig=/dev/null',
                       '--registry=https://registry.npmjs.org'], directory)
        else:
            # No managed-Python download and no source build hooks. Never alter system Python.
            self._run(['uv', 'venv', '--no-config', '--allow-existing', '--no-python-downloads',
                       '--python', python, str(directory)], directory)
            self._run(['uv', 'pip', 'sync', '--no-config',
                       '--python', str(directory / 'bin/python'),
                       '--require-hashes', '--only-binary', ':all:',
                       str(directory / FORGETFUL_REQUIREMENTS)], directory)

        (directory / SYNC_RECEIPT).write_text(fingerprint)
