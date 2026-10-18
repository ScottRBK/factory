from pathlib import Path

from forgetful_factory.adapters.command import run_command
from forgetful_factory.domain.models import FactoryError


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
    @staticmethod
    def _repository_entries(repository: str, remote: str) -> tuple[Path, list[dict]]:
        root = Path(repository).resolve()
        actual = run_command(['git', '-C', str(root), 'remote', 'get-url', 'origin'])
        if actual != remote:
            raise FactoryError('Repository origin changed; reconcile factory.toml and the '
                               'recorded worktree before continuing. Existing work is preserved.')
        output = run_command(['git', '-C', str(root), 'worktree', 'list', '--porcelain', '-z'])
        return root, _worktree_entries(output)

    def verify_removed(self, repository: str, branch: str, path: str, *, remote: str) -> None:
        _, entries = self._repository_entries(repository, remote)
        target = Path(path)
        conflict = FactoryError(f'Removed worktree cleanup conflicts with path or registration: '
                                f'{target}; reconcile the cleanup record. '
                                'Existing work is preserved.')
        if any(parent.is_symlink() for parent in (target, *target.parents)) or target.exists():
            raise conflict
        try:
            registered = any(Path(entry['worktree']).resolve() == target.resolve()
                             or entry.get('branch') == f'refs/heads/{branch}' for entry in entries)
        except (OSError, RuntimeError, ValueError, KeyError) as error:
            raise conflict from error
        if registered:
            raise conflict

    def ensure(self, repository: str, branch: str, path: str, *, recorded: bool,
               remote: str) -> None:
        root, entries = self._repository_entries(repository, remote)
        target = Path(path)
        match = next((e for e in entries if e.get('worktree') == str(target)), None)
        if match:
            if (match.get('branch') != f'refs/heads/{branch}' or not target.is_dir()
                    or 'prunable' in match or target.is_symlink()):
                raise FactoryError(f'Recorded worktree mismatch: {target}; '
                                   'reconcile without reset.')
            common = run_command(['git', '-C', str(target), 'rev-parse',
                                  '--path-format=absolute', '--git-common-dir'])
            expected = run_command(['git', '-C', str(root), 'rev-parse',
                                    '--path-format=absolute', '--git-common-dir'])
            if common != expected:
                raise FactoryError(f'Worktree belongs to another repository: {target}.')
            try:
                actual_branch = run_command(['git', '-C', str(target), 'symbolic-ref', 'HEAD'])
                actual_root = run_command(['git', '-C', str(target), 'rev-parse',
                                           '--show-toplevel'])
                gitdir = Path(run_command(['git', '-C', str(target), 'rev-parse',
                                           '--absolute-git-dir'])).resolve()
                # The registry alone does not prove the target uses its registered HEAD/index.
                if (actual_branch != match['branch'] or Path(actual_root).resolve() != target
                        or gitdir.parent != Path(expected).resolve() / 'worktrees'
                        or Path((gitdir / 'gitdir').read_text().rstrip('\n')).resolve()
                        != target / '.git'):
                    raise ValueError('Target Git identity differs from registration')
            except (OSError, ValueError, FactoryError) as error:
                raise FactoryError(f'Recorded worktree mismatch: {target}; '
                                   'reconcile branch/root/gitdir without reset. '
                                   'Existing work is preserved.') from error
            return
        if recorded or target.exists() or target.is_symlink():
            raise FactoryError(f'Recorded worktree missing or conflicting: {target}; '
                               'restore/reconcile it explicitly. Existing work is preserved.')
        # Git refuses existing branches and conflicting registrations; never force/reset/delete.
        target.parent.mkdir(parents=True, exist_ok=True)
        run_command(['git', '-C', str(root), 'worktree', 'add', '-b', branch, str(target), 'HEAD'])
