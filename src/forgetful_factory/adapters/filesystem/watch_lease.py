import fcntl
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


class WorkspaceWatchLease:
    """An advisory directory lock: no PID files, stale markers, or config rewrites."""

    def __init__(self, workspace: Path):
        self.directory = workspace / '.factory'

    @contextmanager
    def hold(self) -> Iterator[None]:
        try:
            descriptor = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except OSError as error:
            raise FactoryError(
                f'Cannot lock factory directory {self.directory}: {error}'
            ) from error
        try:
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise FactoryError(
                    'A watcher is already running for this workspace. '
                    'Stop it before starting another; it was left untouched.'
                ) from error
            except OSError as error:
                raise FactoryError(f'Cannot lock factory directory: {error}') from error
            yield
        finally:
            os.close(descriptor)
