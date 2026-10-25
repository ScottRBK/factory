"""Run owned processes without persisting or repeating potentially secret diagnostics."""
import contextlib
import os
import signal
import subprocess
import sys
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


def run_owned(args: list[str], cwd: Path, env: dict[str, str], *, login: bool = False,
              timeout: float | None = None) -> str:
    interactive = login and sys.stdin.isatty()
    try:
        process = subprocess.Popen(args, cwd=cwd, env=env, text=True,
                                   stdin=None if interactive else subprocess.DEVNULL,
                                   stdout=None if interactive else subprocess.PIPE,
                                   stderr=None if interactive else subprocess.PIPE,
                                   start_new_session=True)
    except OSError as error:
        raise FactoryError('Cannot start Pi/Forgetful; check the configured executable.') from error
    try:
        stdout, _ = process.communicate(timeout=timeout or (300 if login else 45))
    except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
        try:
            # KeyboardInterrupt can leave communicate's pipe bookkeeping half-initialized.
            # Failed/cancelled output is discarded; do not re-enter communicate to drain it.
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        finally:
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    stream.close()
        if isinstance(error, KeyboardInterrupt):
            raise
        raise FactoryError('Forgetful operation timed out; setup is incomplete. '
                           'Check the role in Pi/CLI, then retry the failed command. '
                           'Incomplete saved setup needs init --finalize.') from error
    if process.returncode:
        raise FactoryError('Forgetful sign-in/check failed or was cancelled; setup is incomplete. '
                           'Inspect the role using Pi/CLI, then retry the failed command. '
                           'Incomplete saved setup needs init --finalize. '
                           'External diagnostics withheld: they can contain credentials.')
    return stdout or ''


