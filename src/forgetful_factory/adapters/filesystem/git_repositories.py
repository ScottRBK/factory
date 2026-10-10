from pathlib import Path

from forgetful_factory.adapters.command import run_command
from forgetful_factory.domain.models import FactoryError


class GitRepositories:
    def origin(self, path: Path) -> str:
        if path != path.resolve():
            raise FactoryError(f'Symlinked repository paths are not supported: {path}')
        if not path.is_dir():
            raise FactoryError(f'Repository directory does not exist: {path}')
        try:
            root = run_command(['git', '-C', str(path), 'rev-parse', '--show-toplevel'])
        except FactoryError as error:
            raise FactoryError(f'Repository {path}: {error}') from error
        if Path(root).resolve() != path.resolve():
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
