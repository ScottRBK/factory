"""Managed Pi: Pi 1.4.0 from the reviewed npm lock in .factory/runtime/pi."""
import shutil
from pathlib import Path

from forgetful_factory.agents.adapters.pi.native_home import saved_pi_home
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.executables import executable_path
from forgetful_factory.shared.installation import (
    SYNC_RECEIPT,
    install_environment,
    install_locks,
    no_installer,
    require_manager,
    run_install,
    sync_fingerprint,
)
from forgetful_factory.shared.sensitive_command import run_owned

PI_INPUTS = ('package.json', 'package-lock.json')


class PiInstall:
    def __init__(self, workspace: Path, term_grace: float = 3):
        self.workspace = workspace
        self.directory = workspace / '.factory/runtime/pi'
        self.term_grace = term_grace

    def absent(self) -> list[str]:
        return ['pi'] if shutil.which('pi', path=executable_path(self.workspace)) is None else []

    def unready(self) -> list[str]:
        """Only the managed Pi is checked; another Pi on PATH belongs to the user."""
        managed = self.directory / 'node_modules/.bin/pi'
        if shutil.which('pi', path=executable_path(self.workspace)) != str(managed):
            return []
        home = saved_pi_home(self.workspace)
        return ['pi'] if Path(home).is_dir() and not self.ready(home) else []

    def ready(self, pi_home: str) -> bool:
        try:
            inputs = tuple(self.directory / name for name in PI_INPUTS)
            if (self.directory / SYNC_RECEIPT).read_text() != sync_fingerprint(inputs):
                return False
            env = install_environment({
                'PI_OFFLINE': '1',
                'PI_CODING_AGENT_DIR': pi_home,
            })
            env.pop('FORGETFUL_TOKEN', None)
            version = run_owned([str(self.directory / 'node_modules/.bin/pi'), '--version'],
                                self.directory, env, timeout=10, term_grace=self.term_grace)
            return version.strip() == '1.4.0'
        except (OSError, FactoryError):
            return False

    def describe(self, name: str) -> str | None:
        if name != 'pi':
            return None
        return ('Install Pi 1.4.0 in .factory/runtime/pi with the reviewed npm lock? '
                'Uses existing Node/npm; npm scripts are disabled. [y/N]: ')

    def install(self, name: str) -> None:
        if name != 'pi':
            raise no_installer()
        require_manager('npm')
        fingerprint = install_locks(self.directory, PI_INPUTS)
        run_install(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund',
                     '--engine-strict', '--userconfig=/dev/null', '--globalconfig=/dev/null',
                     '--registry=https://registry.npmjs.org'], self.directory, self.term_grace)
        (self.directory / SYNC_RECEIPT).write_text(fingerprint)
