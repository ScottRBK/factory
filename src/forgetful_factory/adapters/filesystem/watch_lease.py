import fcntl
import os
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


class WorkspaceWatchLease:
    """An advisory directory lock: no PID files, stale markers, or config rewrites."""

    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.directory = workspace / '.factory'

    @contextmanager
    def hold(self) -> Iterator[None]:
        # Lock the existing workspace even before init creates .factory. Also retain the
        # original directory lock so an already-running watcher remains protected.
        with self._hold_directory(self.workspace):
            if self.directory.exists() or self.directory.is_symlink():
                with self._hold_directory(self.directory):
                    yield
            else:
                yield

    @contextmanager
    def _hold_directory(self, directory: Path) -> Iterator[None]:
        try:
            descriptor = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except OSError as error:
            raise FactoryError(
                f'Cannot lock factory directory {directory}: {error}'
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
