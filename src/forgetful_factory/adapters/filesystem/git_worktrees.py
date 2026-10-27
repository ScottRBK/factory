from pathlib import Path

from forgetful_factory.adapters.command import run_command
from forgetful_factory.application.ports.worktrees import WorktreeProblem, WorktreeReadError
from forgetful_factory.domain.models import FactoryError

_INSPECTION_ERROR = ('Cannot inspect worktree paths; reconcile filesystem access. '
                     'Existing work is preserved. ')


def _worktree_entries(output: str) -> list[dict]:
    entries = []
    entry = {}
    for field in output.split('\0'):
        if not field:
            if entry:
                entries.append(entry)
                entry = {}
        else:
            key, _, value = field.partition(' ')
            entry[key] = value
    return entries


class GitWorktrees:
    def __init__(self, command_timeout: float = 30):
        self.command_timeout = command_timeout

    def _read_git(self, arguments: list[str]) -> str:
        try:
            return run_command(arguments, timeout=self.command_timeout)
        except FactoryError as error:
            raise WorktreeReadError(str(error)) from error

    def inspect(self, repository: str, branch: str, path: str, *, remote: str) -> None:
        try:
            self._inspect(repository, branch, path, recorded=False, remote=remote)
        except OSError as error:
            raise WorktreeReadError(_INSPECTION_ERROR + str(error)) from error

    def _repository_entries(self, repository: str, remote: str) -> tuple[Path, list[dict]]:
        root = Path(repository).resolve()
        actual = self._read_git(['git', '-C', str(root), 'remote', 'get-url', 'origin'])
        if actual != remote:
            raise WorktreeProblem(
                'repository_origin_changed', 'Repository origin changed; reconcile factory.toml '
                'and the recorded worktree before continuing. Existing work is preserved.')
        output = self._read_git(
            ['git', '-C', str(root), 'worktree', 'list', '--porcelain', '-z'])
        return root, _worktree_entries(output)

    def verify_removed(self, repository: str, branch: str, path: str, *, remote: str) -> None:
        try:
            self._verify_removed(repository, branch, path, remote=remote)
        except OSError as error:
            raise WorktreeReadError(_INSPECTION_ERROR + str(error)) from error

    def _verify_removed(self, repository: str, branch: str, path: str, *, remote: str) -> None:
        _, entries = self._repository_entries(repository, remote)
        target = Path(path)
        conflict = WorktreeProblem(
            'removed_worktree_conflict',
            f'Removed worktree cleanup conflicts with path or registration: {target}; '
            'reconcile the cleanup record. Existing work is preserved.', path)
        if any(parent.is_symlink() for parent in (target, *target.parents)) or target.exists():
            raise conflict
        try:
            registered = any(Path(entry['worktree']).resolve() == target.resolve()
                             or entry.get('branch') == f'refs/heads/{branch}' for entry in entries)
        except (RuntimeError, ValueError, KeyError) as error:
            raise conflict from error
        if registered:
            raise conflict

    def ensure(self, repository: str, branch: str, path: str, *, recorded: bool,
               remote: str) -> None:
        try:
            creation = self._inspect(repository, branch, path, recorded=recorded, remote=remote)
        except OSError as error:
            raise WorktreeReadError(_INSPECTION_ERROR + str(error)) from error
        if creation is None:
            return
        root, target = creation
        try:
            # This is the write boundary. Failures after it never become retryable reads.
            target.parent.mkdir(parents=True, exist_ok=True)
            run_command(['git', '-C', str(root), 'worktree', 'add', '-b',
                         branch, str(target), 'HEAD'], timeout=self.command_timeout)
        except OSError as error:
            raise FactoryError('Cannot prepare worktree paths; reconcile filesystem state '
                               'before continuing. Existing work is preserved. ' + str(error)) \
                from error

    def _inspect(self, repository: str, branch: str, path: str, *, recorded: bool,
                 remote: str) -> tuple[Path, Path] | None:
        root, entries = self._repository_entries(repository, remote)
        target = Path(path)
        match = next((e for e in entries if e.get('worktree') == str(target)), None)
        if match:
            self._validate_registered_worktree(root, target, branch, path, match)
            return None
        if recorded:
            raise WorktreeProblem(
                'worktree_missing', f'Recorded worktree missing or conflicting: {target}; '
                'restore/reconcile it explicitly. Existing work is preserved.', path)
        if target.exists() or any(parent.is_symlink() or
                                  (parent.exists() and not parent.is_dir())
                                  for parent in (target, *target.parents)):
            raise WorktreeProblem('worktree_path_conflict',
                                  f'New worktree path conflicts with existing work: {target}.',
                                  path)
        branches = self._read_git(['git', '-C', str(root), 'for-each-ref',
                                   '--format=%(refname)', 'refs/heads/']).splitlines()
        if f'refs/heads/{branch}' in branches:
            raise WorktreeProblem('worktree_branch_conflict',
                                  f'New worktree branch already exists: {branch}.', path)
        return root, target

    def _validate_registered_worktree(self, root: Path, target: Path, branch: str, path: str,
                                      match: dict) -> None:
        self._validate_registration(target, branch, path, match)
        expected = self._validate_common_directory(root, target, path)
        self._validate_target_identity(target, path, match, expected)

    @staticmethod
    def _validate_registration(target: Path, branch: str, path: str, match: dict) -> None:
        if (match.get('branch') != f'refs/heads/{branch}' or not target.is_dir()
                or 'prunable' in match or target.is_symlink()):
            raise WorktreeProblem('worktree_mismatch', f'Recorded worktree mismatch: {target}; '
                                  'reconcile without reset.', path)

    def _validate_common_directory(self, root: Path, target: Path, path: str) -> str:
        common = self._read_git(['git', '-C', str(target), 'rev-parse',
                                 '--path-format=absolute', '--git-common-dir'])
        expected = self._read_git(['git', '-C', str(root), 'rev-parse',
                                   '--path-format=absolute', '--git-common-dir'])
        if common != expected:
            raise WorktreeProblem('worktree_repository_mismatch',
                                  f'Worktree belongs to another repository: {target}.', path)
        return expected

    def _validate_target_identity(self, target: Path, path: str, match: dict,
                                  expected: str) -> None:
        try:
            actual_branch = self._read_git(
                ['git', '-C', str(target), 'symbolic-ref', 'HEAD'])
            actual_root = self._read_git(
                ['git', '-C', str(target), 'rev-parse', '--show-toplevel'])
            gitdir = Path(self._read_git(
                ['git', '-C', str(target), 'rev-parse', '--absolute-git-dir'])).resolve()
            # The registry alone does not prove the target uses its registered HEAD/index.
            if (actual_branch != match['branch'] or Path(actual_root).resolve() != target
                    or gitdir.parent != Path(expected).resolve() / 'worktrees'
                    or Path((gitdir / 'gitdir').read_text().rstrip('\n')).resolve()
                    != target / '.git'):
                raise ValueError('Target Git identity differs from registration')
        except ValueError as error:
            raise WorktreeProblem('worktree_mismatch', f'Recorded worktree mismatch: {target}; '
                                  'reconcile branch/root/gitdir without reset. '
                                  'Existing work is preserved.', path) from error
