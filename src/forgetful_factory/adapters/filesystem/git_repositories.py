from pathlib import Path

from forgetful_factory.adapters.command import run_command
from forgetful_factory.domain.models import FactoryError


def _resolve_repository(path: Path) -> Path:
    try:
        return path.resolve()
    except (OSError, RuntimeError) as error:
        # Path.resolve reports symlink loops as RuntimeError on Python 3.12.
        raise FactoryError(f'Cannot inspect repository path {path}: {error}') from error


class GitRepositories:
    def origin(self, path: Path) -> str:
        resolved = _resolve_repository(path)
        if path != resolved:
            raise FactoryError(f'Symlinked repository paths are not supported: {path}')
        if not path.is_dir():
            raise FactoryError(f'Repository directory does not exist: {path}')
        try:
            root = run_command(['git', '-C', str(path), 'rev-parse', '--show-toplevel'])
        except FactoryError as error:
            raise FactoryError(f'Repository {path}: {error}') from error
        if _resolve_repository(Path(root)) != resolved:
            raise FactoryError(f'Choose a Git repository root, not a subdirectory: {path}')
        try:
            return run_command(['git', '-C', str(path), 'remote', 'get-url', 'origin'])
        except FactoryError as error:
            raise FactoryError(f'Repository {path}: cannot read origin: {error}') from error

    def discover(self, workspace: Path) -> list[Path]:
        candidates = [workspace, *sorted(workspace.iterdir())]
        return [path for path in candidates
                if path.is_dir() and not path.is_symlink() and
                (path / '.git').exists() and not (path / '.git').is_symlink()]
