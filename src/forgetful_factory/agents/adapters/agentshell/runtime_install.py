"""The AgentShell extension runtime, synced from its reviewed upstream uv lock."""
import hashlib
import json
import shutil
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.installation import (
    LOCKS,
    SYNC_RECEIPT,
    check_uv,
    no_installer,
    run_install,
    runtime_ready,
    sync_fingerprint,
)

ROLE_PROBE = ('from agent_shell.shell import AgentShell; '
              'from agent_shell.tmux import TmuxExecutionHost')


class AgentShellRuntimeInstall:
    def __init__(self, workspace: Path, term_grace: float = 3):
        self.workspace = workspace
        self.project = workspace / '.factory/resources/agentshell/python'
        self.term_grace = term_grace

    def _inputs(self) -> tuple[Path, Path]:
        return self.project / 'pyproject.toml', self.project / 'uv.lock'

    def absent(self) -> list[str]:
        return []

    def unready(self) -> list[str]:
        return [] if self.ready() else ['agentshell-runtime']

    def ready(self) -> bool:
        return runtime_ready(self.project / '.venv', self._inputs(), ROLE_PROBE, self.term_grace)

    def describe(self, name: str) -> str | None:
        if name != 'agentshell-runtime':
            return None
        return ('Install the AgentShell extension runtime from its reviewed upstream uv lock? '
                'Uses existing Python and uv >=0.13.5 in the role directory. [y/N]: ')

    def install(self, name: str) -> None:
        if name != 'agentshell-runtime':
            raise no_installer()
        check_uv(self.workspace, self.term_grace)
        inputs = self._inputs()
        manifest = json.loads((LOCKS.parent / 'role-resources.json').read_text())
        for path in inputs:
            expected = manifest['agentshell']['files'][f'python/{path.name}']
            if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise FactoryError('AgentShell installation lock/project was edited; '
                                   'edits preserved. Restore reviewed inputs and rerun init.')
        runtime = self.project / '.venv'
        (runtime / SYNC_RECEIPT).unlink(missing_ok=True)
        fingerprint = sync_fingerprint(inputs)
        # package=false: only dependencies are installed, so no installed path refers to staging.
        # A standalone workspace prevents uv from inheriting repository workspace/source overrides.
        with TemporaryDirectory(prefix='factory-role-install-') as temporary:
            staging = Path(temporary)
            shutil.copyfile(inputs[1], staging / 'uv.lock')
            (staging / 'pyproject.toml').write_text(
                inputs[0].read_text() + '\n[tool.uv.workspace]\nmembers = []\n')
            run_install(['uv', 'sync', '--project', str(staging), '--locked', '--no-build',
                         '--no-dev', '--no-config', '--python', sys.executable,
                         '--no-python-downloads'], staging, self.term_grace,
                        extra_env={'UV_PROJECT_ENVIRONMENT': str(runtime)})
        (runtime / SYNC_RECEIPT).write_text(fingerprint)
