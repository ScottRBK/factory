"""Managed Forgetful CLI 0.5.5 in .factory/runtime/forgetful, from hashed requirements."""
import os
import shutil
from pathlib import Path

from forgetful_factory.planning.model import ForgetfulConnection
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.executables import executable_path
from forgetful_factory.shared.installation import (
    SYNC_RECEIPT,
    check_uv,
    install_environment,
    install_locks,
    no_installer,
    require_manager,
    run_install,
    runtime_ready,
)
from forgetful_factory.shared.sensitive_command import run_owned

FORGETFUL_REQUIREMENTS = 'forgetful-requirements.txt'
FORGETFUL_PROBE = ('import app; import importlib.util; '
                   'assert importlib.util.find_spec("main") is not None')


class ForgetfulInstall:
    def __init__(self, workspace: Path, connection: ForgetfulConnection, term_grace: float = 3):
        self.workspace = workspace
        self.connection = connection
        self.directory = workspace / '.factory/runtime/forgetful'
        self.term_grace = term_grace
        self._was_absent = False

    def _required(self) -> bool:
        return self.connection.method == 'cli' or self.connection.instance == 'local'

    def _selected(self) -> str | None:
        return shutil.which(self.connection.executable, path=executable_path(self.workspace))

    def absent(self) -> list[str]:
        self._was_absent = self._required() and self._selected() is None
        return [self.connection.executable] if self._was_absent else []

    def unready(self) -> list[str]:
        """Only the managed CLI is checked; another executable belongs to the user.

        A CLI that the last absent() call missed is not probed, even if it has appeared since.
        """
        selected = self._selected()
        if (self._required() and selected == str(self.directory / 'bin/forgetful')
                and not self._was_absent
                and not runtime_ready(self.directory, (self.directory / FORGETFUL_REQUIREMENTS,),
                                      FORGETFUL_PROBE, self.term_grace)):
            return ['forgetful']
        return []

    def describe(self, name: str) -> str | None:
        if name != 'forgetful':
            return None
        # The workflow requests this description before asking for installation consent.
        python = self._python()
        return ('Install Forgetful CLI 0.5.5 in .factory/runtime/forgetful?\n'
                'This adds the command-line tool; it does not start another server.\n'
                f'Downloads from PyPI using existing Python 3.12:\n  {python}\n'
                'Proceed? [y/N]: ')

    def _python(self) -> str:
        """Preflight an existing 3.12 independently of Factory's own interpreter."""
        check_uv(self.workspace, self.term_grace)
        try:
            env = install_environment()
            python = run_owned(
                ['uv', 'python', 'find', 'cpython@3.12', '--system', '--no-project',
                 '--no-config', '--no-python-downloads', '--offline', '--no-cache'],
                self.workspace, env, timeout=10, term_grace=self.term_grace).strip()
            path = Path(python)
            if (not python.isprintable() or not path.is_absolute() or not path.is_file()
                    or not os.access(path, os.X_OK)):
                raise ValueError('Invalid Python discovery result')
            version = run_owned(
                [python, '-I', '-B', '-S', '-c',
                 'import sys; print(sys.implementation.name, *sys.version_info[:2])'],
                self.workspace, env, timeout=10, term_grace=self.term_grace)
            if version.strip() != 'cpython 3 12':
                raise ValueError('Incompatible Python')
            return python
        except (FactoryError, OSError, ValueError) as error:
            raise FactoryError('Forgetful CLI needs an already installed Python 3.12 (CPython). '
                               'Make it discoverable on PATH as python3.12, then rerun init. '
                               'No Python was downloaded; setup is incomplete.') from error

    def install(self, name: str) -> None:
        if name != 'forgetful':
            raise no_installer()
        require_manager('uv')
        python = self._python()
        fingerprint = install_locks(self.directory, (FORGETFUL_REQUIREMENTS,))
        # No managed-Python download and no source build hooks. Never alter system Python.
        run_install(['uv', 'venv', '--no-config', '--allow-existing', '--no-python-downloads',
                     '--python', python, str(self.directory)], self.directory, self.term_grace)
        run_install(['uv', 'pip', 'sync', '--no-config',
                     '--python', str(self.directory / 'bin/python'),
                     '--require-hashes', '--only-binary', ':all:',
                     str(self.directory / FORGETFUL_REQUIREMENTS)], self.directory,
                    self.term_grace)
        (self.directory / SYNC_RECEIPT).write_text(fingerprint)
