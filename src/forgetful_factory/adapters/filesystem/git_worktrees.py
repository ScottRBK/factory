import os
import shlex
import subprocess
from pathlib import Path

from forgetful_factory.adapters.command import run_command
from forgetful_factory.application.ports.worktrees import WorktreeProblem, WorktreeReadError
from forgetful_factory.application.watch_stop import check_watch_stop
from forgetful_factory.domain.models import FactoryError

_ABSOLUTE_PATH_FORMAT = '--path-format=absolute'
_BRANCH_REF_PREFIX = 'refs/heads/'
_FACTORY_WORKTREES_DIRECTORY = '.factory/worktrees'
_REFNAME_FORMAT = '--format=%(refname)'
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
        self.cleanup_defaults: dict[str, list[str] | FactoryError] = {}

    def begin_cleanup_cycle(self) -> None:
        self.cleanup_defaults.clear()

    def repository_identity(self, repository: str) -> str:
        try:
            root = Path(repository).resolve()
            actual = self._read_git(['git', '-C', str(root), 'rev-parse', '--show-toplevel'])
            if root != Path(repository) or Path(actual).resolve() != root:
                raise WorktreeReadError('Cannot identify a symlinked/non-root repository.')
            common = self._read_git(['git', '-C', str(root), 'rev-parse',
                                     _ABSOLUTE_PATH_FORMAT, '--git-common-dir'])
            return str(Path(common).resolve())
        except (OSError, RuntimeError, ValueError) as error:
            raise WorktreeReadError('Cannot identify repository common Git directory: '
                                    + str(error)) from error

    def target_branch(self, repository: str) -> str:
        ref = self._read_git(['git', '-C', repository, 'symbolic-ref', 'HEAD'])
        if not ref.startswith(_BRANCH_REF_PREFIX):
            raise WorktreeReadError('Cannot record merge target from detached repository HEAD.')
        return ref.removeprefix(_BRANCH_REF_PREFIX)

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
            check_watch_stop()
            # This is the write boundary. Failures after it never become retryable reads.
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.parent == root / _FACTORY_WORKTREES_DIRECTORY:
                try:
                    with (target.parent / '.gitignore').open('x', encoding='utf-8') as ignored:
                        ignored.write('*\n')
                except FileExistsError:
                    pass  # Preserve existing local ignore rules, including user edits.
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
                                   _REFNAME_FORMAT, _BRANCH_REF_PREFIX]).splitlines()
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
                                 _ABSOLUTE_PATH_FORMAT, '--git-common-dir'])
        expected = self._read_git(['git', '-C', str(root), 'rev-parse',
                                   _ABSOLUTE_PATH_FORMAT, '--git-common-dir'])
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

    def dispose(self, repository: str, branch: str, path: str, *, remote: str,
                target_branch: str) -> None:
        try:
            self._dispose(repository, branch, path, remote=remote, target_branch=target_branch)
        except (OSError, ValueError, RuntimeError) as error:
            raise WorktreeProblem('cleanup_path_invalid',
                                  f'Cannot establish safe cleanup paths; reconcile: {error}',
                                  path) from error

    def _disposal_state(self, repository: str, branch: str, path: str, *, remote: str,
                        target_branch: str) -> tuple[Path, Path, dict | None]:
        root, entries = self._repository_entries(repository, remote)
        target = Path(path)
        self._validate_disposal_origin(root, remote, path)
        self._validate_disposal_path(root, target, repository, path)
        self._validate_disposal_refs(root, branch, target_branch, path)
        if any(Path(e['worktree']).resolve() != target and
               Path(e['worktree']).resolve().is_relative_to(target) for e in entries):
            raise WorktreeProblem('cleanup_path_invalid',
                                  'Cleanup path contains another registered worktree; reconcile.',
                                  path)
        match = next((e for e in entries if Path(e['worktree']).resolve() == target), None)
        if match is not None:
            if 'locked' in match:
                raise WorktreeProblem('cleanup_locked', 'Cleanup worktree is locked; reconcile '
                                      'it without forced unlocking.', path)
            self._validate_registered_worktree(root, target, branch, path, match)
        elif target.exists():
            raise WorktreeProblem('cleanup_path_invalid',
                                  'Cleanup path exists without matching registration; reconcile.',
                                  path)
        return root, target, match

    def _validate_disposal_origin(self, root: Path, remote: str, path: str) -> None:
        for options in (['--all'], ['--push', '--all']):
            urls = self._read_git(['git', '-C', str(root), 'remote', 'get-url',
                                  *options, 'origin']).splitlines()
            if urls != [remote]:
                raise WorktreeProblem('repository_origin_changed',
                                      'Cleanup fetch/push destinations differ from the '
                                      'configured origin; reconcile without deletion.', path)

    def _validate_disposal_path(self, root: Path, target: Path, repository: str,
                                path: str) -> None:
        if (root != Path(repository) or target != target.resolve()
                or any(p.is_symlink() for p in (target, *target.parents))
                or target == root / _FACTORY_WORKTREES_DIRECTORY
                or not target.is_relative_to(root / _FACTORY_WORKTREES_DIRECTORY)
                or root == target or root.is_relative_to(target)
                or target.is_relative_to(root / '.git')
                or Path(self._read_git(['git', '-C', str(root), 'rev-parse',
                                       '--show-toplevel'])) != root):
            raise WorktreeProblem('cleanup_path_invalid',
                                  'Cleanup path/root identity is unsafe; reconcile it.', path)

    def _validate_disposal_refs(self, root: Path, branch: str, target_branch: str,
                                path: str) -> None:
        # Ref syntax is checked before passing recorded values to write commands.
        for name in (branch, target_branch):
            self._read_git(['git', 'check-ref-format', f'refs/heads/{name}'])
        main = self._read_git(['git', '-C', str(root), 'symbolic-ref', 'HEAD'])
        default = self._remote_default(root)
        if (len(default) != 1 or f'refs/heads/{branch}' in
                (main, default[0], f'refs/heads/{target_branch}')):
            raise WorktreeProblem('cleanup_protected_branch',
                                  'Cleanup cannot remove a default, main-checkout or merge-target '
                                  'branch, or establish the remote default; reconcile it.', path)

    def _network_git(self, arguments: list[str]) -> str:
        # Only cleanup network operations opt in. Native sign-in and other commands are unchanged.
        env = dict(os.environ, GIT_TERMINAL_PROMPT='0', GIT_ASKPASS='/bin/false',
                   SSH_ASKPASS='/bin/false', SSH_ASKPASS_REQUIRE='force', GCM_INTERACTIVE='Never')
        command = env.get('GIT_SSH_COMMAND')
        if command is None:
            command = (shlex.quote(env['GIT_SSH']) if env.get('GIT_SSH') else self._read_git(
                ['git', '-C', arguments[2], 'config', '--get', '--default',
                 'ssh', 'core.sshCommand']))
        variant = env.get('GIT_SSH_VARIANT') or self._read_git(
            ['git', '-C', arguments[2], 'config', '--get', '--default', 'auto', 'ssh.variant'])
        batch = '-batch' if variant in ('plink', 'tortoiseplink') else '-o BatchMode=yes'
        env['GIT_SSH_COMMAND'] = command + ' ' + batch
        return run_command(arguments, timeout=self.command_timeout, env=env,
                           stdin=subprocess.DEVNULL)

    def _network_read(self, arguments: list[str]) -> str:
        try:
            return self._network_git(arguments)
        except FactoryError as error:
            raise WorktreeProblem('cleanup_network_read_failed', str(error)) from error

    def _remote_default(self, root: Path) -> list[str]:
        key = str(root)
        if key not in self.cleanup_defaults:
            try:
                advertised = self._network_read(['git', '-C', key, 'ls-remote', '--symref',
                                             'origin', 'HEAD'])
            except FactoryError as error:
                self.cleanup_defaults[key] = error
            else:
                self.cleanup_defaults[key] = [
                    line.split('\t')[0].removeprefix('ref: ')
                    for line in advertised.splitlines()
                    if line.startswith('ref: refs/heads/') and line.endswith('\tHEAD')]
        result = self.cleanup_defaults[key]
        if isinstance(result, FactoryError):
            raise result
        return result

    def _dispose(self, repository: str, branch: str, path: str, *, remote: str,
                 target_branch: str) -> None:
        root, target, match = self._disposal_state(repository, branch, path, remote=remote,
                                                  target_branch=target_branch)
        if match is not None:
            # One force permits dirty/ignored content; never use two forces to bypass locks.
            run_command(['git', '-C', str(root), 'worktree', 'remove', '--force', str(target)],
                        timeout=self.command_timeout)
        # Reread actual state after each stage, including on subsequent calls after uncertainty.
        root, _, match = self._disposal_state(repository, branch, path, remote=remote,
                                              target_branch=target_branch)
        if match is not None:
            raise WorktreeProblem('cleanup_worktree_remaining',
                                  'Cleanup worktree removal is unconfirmed; recheck next poll.',
                                  path)
        ref = f'refs/heads/{branch}'
        branches = self._read_git(['git', '-C', str(root), 'for-each-ref',
                                   _REFNAME_FORMAT, _BRANCH_REF_PREFIX]).splitlines()
        if ref in branches:
            # Git itself refuses a branch checked out in another registered worktree.
            run_command(['git', '-C', str(root), 'branch', '-D', '--', branch],
                        timeout=self.command_timeout)
        root, _, _ = self._disposal_state(repository, branch, path, remote=remote,
                                          target_branch=target_branch)
        self._verify_local_ref_absent(root, ref, path)
        _, entries = self._repository_entries(repository, remote)
        if any(e.get('branch') == ref for e in entries):
            raise WorktreeProblem('cleanup_branch_in_use',
                                  'Feature branch is still registered in another checkout; '
                                  'reconcile without removing that checkout.', path)
        refs = self._network_read(['git', '-C', str(root), 'ls-remote', '--heads', 'origin', ref])
        if refs:
            self._network_git(['git', '-C', str(root), 'push', 'origin', f':{ref}'])
        if self._network_read(['git', '-C', str(root), 'ls-remote', '--heads', 'origin', ref]):
            raise WorktreeProblem('cleanup_remote_remaining',
                                  'Remote feature ref removal is unconfirmed; recheck next poll.',
                                  path)

        _, _, match = self._disposal_state(repository, branch, path, remote=remote,
                                           target_branch=target_branch)
        if match is not None:
            raise WorktreeProblem('cleanup_worktree_remaining',
                                  'Worktree registration returned during cleanup; '
                                  'recheck next poll.',
                                  path)
        self._verify_local_ref_absent(root, ref, path)

    def _verify_local_ref_absent(self, root: Path, ref: str, path: str) -> None:
        refs = self._read_git(['git', '-C', str(root), 'for-each-ref',
                               _REFNAME_FORMAT, _BRANCH_REF_PREFIX]).splitlines()
        if ref in refs:
            raise WorktreeProblem('cleanup_local_remaining',
                                  'Local feature ref absence is unconfirmed; recheck next poll.',
                                  path)
