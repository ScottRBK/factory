"""tmux for AgentShell sessions. Only Ubuntu 24.04 x86_64 has a reviewed automatic recipe."""
import os
import platform
import re
import shutil
from pathlib import Path

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.executables import executable_path
from forgetful_factory.shared.installation import no_installer, run_install


def ubuntu_tmux() -> bool:
    try:
        release = platform.freedesktop_os_release()
        return (release.get('ID') == 'ubuntu' and release.get('VERSION_ID') == '24.04'
                and platform.machine() == 'x86_64')
    except OSError:
        return False


class TmuxInstall:
    def __init__(self, workspace: Path, term_grace: float = 3):
        self.workspace = workspace
        self.term_grace = term_grace

    def absent(self) -> list[str]:
        found = shutil.which('tmux', path=executable_path(self.workspace))
        return ['tmux'] if found is None else []

    def unready(self) -> list[str]:
        return []

    def describe(self, name: str) -> str | None:
        if name == 'tmux' and ubuntu_tmux():
            return ('Install Ubuntu tmux 3.4-1ubuntu0.1 using apt-get --no-upgrade '
                    '--no-install-recommends? This is a privileged system install and may add '
                    'OS dependencies; no apt update runs. [y/N]: ')
        # Other hosts require a reviewed manual installation.
        return None

    def install(self, name: str) -> None:
        if name != 'tmux' or not ubuntu_tmux():
            raise no_installer()
        directory = self.workspace / '.factory'
        args = ['apt-get', 'install', '--yes', '--no-upgrade', '--no-install-recommends',
                'tmux=3.4-1ubuntu0.1']
        preview = run_install(['apt-get', '--simulate', *args[1:]], directory, self.term_grace)
        if not re.search(r'(?m)^0 upgraded, \d+ newly installed, 0 to remove', preview):
            raise FactoryError('tmux installation would upgrade/remove packages, or the '
                               'transaction could not be verified; nothing was installed.')
        if os.geteuid() != 0:
            args[:0] = ['sudo', '--stdin']
        run_install(args, directory, self.term_grace, interactive=True)
