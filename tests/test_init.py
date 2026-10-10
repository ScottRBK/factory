import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]

GH = '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
import time
import signal

state_path = Path(os.environ['GH_STATE'])
state = json.loads(state_path.read_text())
args = sys.argv[1:]
if args[:1] == ['api']:
    host = args[args.index('--hostname') + 1] if '--hostname' in args else \
        os.environ.get('GH_HOST', 'github.com')
    if host != 'github.com':
        sys.exit('wrong GitHub host: ' + host)
    endpoint = args[1].split('?', 1)[0]
    source = '/'.join(endpoint.split('/')[1:3])
    state.setdefault('calls', []).append(args)
    state_path.write_text(json.dumps(state))
    if source == state.get('denied'):
        sys.exit('HTTP 403 access denied')
    if endpoint == state.get('malformed'):
        print('{bad json')
        sys.exit(0)
    if endpoint.endswith('/labels'):
        if '--method' in args:
            name = args[args.index('-f') + 1].split('=', 1)[1]
            if name == state.get('interrupt_create'):
                os.kill(os.getppid(), signal.SIGINT)
                time.sleep(1)
            if name == state.get('timeout_create'):
                time.sleep(35)
            if name == state.get('fail_create'):
                sys.exit('HTTP 403 label creation denied')
            state.setdefault('labels', {}).setdefault(source, []).append(
                {'name': name, 'color': 'ededed', 'description': 'Factory work'})
            state.setdefault('created', []).append([source, name])
            state_path.write_text(json.dumps(state))
            if 'concurrent_config' in state:
                target = Path(state['concurrent_config']['path'])
                target.parent.mkdir(exist_ok=True)
                target.write_text(state['concurrent_config']['content'])
            if 'symlink_factory' in state:
                Path(state['symlink_factory']['path']).symlink_to(
                    state['symlink_factory']['target'], target_is_directory=True)
            print(json.dumps([] if name == state.get('malformed_create') else {'name': name}))
        else:
            pages = state.get('pages', {}).get(source)
            labels = state.get('labels', {}).get(source, [])
            if pages is not None:
                print(json.dumps(pages if '--paginate' in args and '--slurp' in args
                                 else pages[0]))
            else:
                print(json.dumps([labels] if '--slurp' in args else labels))
    else:
        print(json.dumps({'full_name': source}))
else:
    sys.exit('unexpected gh command: ' + repr(args))
'''


class InitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name)
        self.bin = self.workspace / 'bin'
        self.bin.mkdir()
        (self.bin / 'gh').write_text(GH)
        (self.bin / 'gh').chmod(0o755)
        self.state = self.workspace / 'gh-state.json'
        self.state.write_text('{}')
        self.env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'),
                        PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        GH_STATE=str(self.state))

    def git(self, path, *args):
        return subprocess.run(['git', '-C', str(path), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def repo(self, name='app', remote='git@github.com:team/app.git'):
        path = self.workspace / name
        path.mkdir()
        self.git(path, 'init', '-q')
        self.git(path, 'remote', 'add', 'origin', remote)
        return path

    def run_cli(self, cwd, *args, input='', timeout=10):
        return subprocess.run([sys.executable, '-m', 'forgetful_factory', 'init', *args],
                              cwd=cwd, env=self.env, input=input, text=True,
                              capture_output=True, timeout=timeout)

    def settings(self):
        return ('--label', 'factory', '--foreman-model', 'provider/model',
                '--foreman-effort', 'high')

    def load(self, workspace):
        from forgetful_factory.configuration import load_configuration
        return load_configuration(workspace)

    def test_single_repo_initializes_and_loads_actual_path_and_remote(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings())
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.load(repo)
        self.assertEqual(config.watcher_label, ('factory',))
        self.assertEqual(config.foreman_agent_model, 'provider/model')
        self.assertEqual(config.foreman_agent_effort, 'high')
        saved = tomllib.loads((repo / '.factory' / 'factory.toml').read_text())
        self.assertEqual(saved['repository'], [{
            'local_dir': str(repo), 'remote': 'git@github.com:team/app.git',
            'provider': 'github', 'source': 'team/app',
        }])
        self.assertNotIn('repositories', saved)
        reference = config.repository[0]
        self.assertEqual(reference.local_dir, str(repo))
        self.assertEqual(reference.remote, 'git@github.com:team/app.git')
        self.assertEqual(reference.work_source.provider, 'github')
        self.assertEqual(reference.work_source.reference, 'team/app')
        self.assertIn('Created team/app: factory', result.stdout)

    def test_old_repository_format_is_preserved_with_conversion_guidance(self):
        # Arrange
        repo = self.repo()
        path = repo / '.factory' / 'factory.toml'
        path.parent.mkdir()
        settings = '''watcher_label = ["factory"]
foreman_agent_model = "provider/model"
foreman_agent_effort = "high"
'''
        old_table = (f'[repositories.{json.dumps(str(repo))}]\n'
                     f'local_dir = {json.dumps(str(repo))}\n'
                     'remote = "git@github.com:team/app.git"\n'
                     'provider = "github"\nsource = "team/app"\n')
        for suffix in ('', old_table.replace(old_table.splitlines()[0], '[[repository]]')):
            with self.subTest(mixed_formats=bool(suffix)):
                contents = settings + old_table + suffix
                path.write_text(contents)
                # Act
                result = self.run_cli(repo)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Replace each [repositories.', result.stderr)
                self.assertIn('[[repository]]', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(path.read_text(), contents)
                self.assertEqual(json.loads(self.state.read_text()).get('calls', []), [])

    def test_repeated_local_directory_is_rejected_before_github_calls(self):
        # Arrange
        repo = self.repo()
        result = self.run_cli(repo, '--repo', '.', *self.settings())
        self.assertEqual(result.returncode, 0, result.stderr)
        path = repo / '.factory' / 'factory.toml'
        contents = path.read_text()
        duplicate = contents[contents.index('[[repository]]'):]
        path.write_text(contents + '\n' + duplicate)
        self.state.write_text('{}')
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Duplicate repository local_dir', result.stderr)
        self.assertIn(str(repo), result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(path.read_text(), contents + '\n' + duplicate)
        self.assertEqual(json.loads(self.state.read_text()).get('calls', []), [])

    def test_invalid_settings_fail_before_any_labels_or_config(self):
        # Arrange
        repo = self.repo()
        cases = [('--label', '  '), ('--foreman-model', ' '), ('--foreman-effort', '')]
        for flag, value in cases:
            with self.subTest(flag=flag):
                settings = list(self.settings())
                settings[settings.index(flag) + 1] = value
                # Act
                result = self.run_cli(repo, '--repo', '.', *settings)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('nonblank', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
                self.assertFalse((repo / '.factory').exists())

    def test_all_repositories_and_label_reads_preflight_before_creating(self):
        # Arrange
        first = self.repo()
        second = self.repo('other', 'https://github.com/team/other.git')
        for state in ({'denied': 'team/other'},
                      {'malformed': 'repos/team/other/labels'},
                      {'malformed': 'repos/team/other'}):
            with self.subTest(state=state):
                self.state.write_text(json.dumps(state))
                # Act
                result = self.run_cli(self.workspace, '--repo', str(first),
                                      '--repo', str(second), *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('team/other', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
                self.assertFalse((self.workspace / '.factory').exists())

    def test_paginated_labels_match_case_insensitively_and_are_untouched(self):
        # Arrange
        repo = self.repo()
        label = {'name': 'Factory', 'color': '123abc', 'description': 'Keep this'}
        self.state.write_text(json.dumps({'labels': {'team/app': [label]},
                                          'pages': {'team/app': [[], [label]]}}))
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'FACTORY')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads(self.state.read_text())
        self.assertEqual(state.get('created', []), [])
        self.assertEqual(state['labels']['team/app'], [label])
        self.assertIn('Reused team/app: factory', result.stdout)
        self.assertEqual(self.load(repo).watcher_label, ('factory',))

    def test_wildcard_never_created_and_mixed_concrete_labels_are_ensured(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', '--label', '*',
                              '--label', 'factory', '--foreman-model', 'provider/model',
                              '--foreman-effort', 'high')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.state.read_text())['created'], [['team/app', 'factory']])
        self.assertEqual(self.load(repo).watcher_label, ('*', 'factory'))
        self.assertIn('Wildcard', result.stdout)

    def test_repeat_loads_existing_bytes_and_conflicting_flags_fail_before_github(self):
        # Arrange
        repo = self.repo()
        initial = self.run_cli(repo, '--repo', '.', *self.settings())
        self.assertEqual(initial.returncode, 0, initial.stderr)
        config_path = repo / '.factory' / 'factory.toml'
        config_path.write_text('# Hand edited comment\n' + config_path.read_text())
        original = config_path.read_bytes()
        # Act
        repeated = self.run_cli(repo)
        # Assert
        self.assertEqual(repeated.returncode, 0, repeated.stderr)
        self.assertEqual(config_path.read_bytes(), original)
        self.assertEqual(json.loads(self.state.read_text())['created'], [['team/app', 'factory']])
        self.assertIn('Reused', repeated.stdout)
        for flags in (('--label', 'other'), ('--foreman-model', 'other/model'),
                      ('--foreman-effort', 'max'), ('--repo', str(self.workspace))):
            with self.subTest(flags=flags):
                # Arrange
                before = self.state.read_bytes()
                # Act
                conflict = self.run_cli(repo, *flags)
                # Assert
                self.assertNotEqual(conflict.returncode, 0)
                self.assertIn('edit', conflict.stderr.lower())
                self.assertEqual(self.state.read_bytes(), before)
                self.assertEqual(config_path.read_bytes(), original)

    def test_existing_config_revalidates_current_origins_and_invalid_settings(self):
        # Arrange
        repo = self.repo()
        initial = self.run_cli(repo, '--repo', '.', *self.settings())
        self.assertEqual(initial.returncode, 0, initial.stderr)
        path = repo / '.factory' / 'factory.toml'
        original = path.read_text()
        cases = [
            (original, 'https://github.com/team/changed.git'),
            (original.replace('provider = "github"', 'provider = "other"'),
             'git@github.com:team/app.git'),
            (original.replace('source = "team/app"', 'source = "team/wrong"'),
             'git@github.com:team/app.git'),
            (original.replace('watcher_label = ["factory"]', 'watcher_label = true'),
             'git@github.com:team/app.git'),
            ('[broken', 'git@github.com:team/app.git'),
            (original.replace(f'local_dir = "{repo}"', r'local_dir = "\u0000"'),
             'git@github.com:team/app.git'),
            (original.replace('watcher_label = ["factory"]',
                              r'watcher_label = ["first", "bad\u0000label"]'),
             'git@github.com:team/app.git'),
        ]
        for contents, remote in cases:
            with self.subTest(contents=contents, remote=remote):
                path.write_text(contents)
                self.git(repo, 'remote', 'set-url', 'origin', remote)
                before = self.state.read_bytes()
                # Act
                result = self.run_cli(repo)
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(self.state.read_bytes(), before)
                self.assertEqual(path.read_text(), contents)
                if 'provider = "other"' in contents:
                    self.assertIn('Unsupported work-tracking provider', result.stderr)
                    self.assertIn('other', result.stderr)
                    self.assertIn('github', result.stderr)

    def test_interactive_group_selection_confirms_remotes_and_includes_worktrees(self):
        # Arrange
        app = self.repo('app')
        other = self.repo('other', 'https://github.com/team/other.git')
        self.git(app, '-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                 'commit', '--allow-empty', '-m', 'temporary fixture')
        worktree = self.workspace / 'worktree'
        self.git(app, 'worktree', 'add', '-b', 'fixture', str(worktree))
        (self.workspace / 'linked').symlink_to(other, target_is_directory=True)
        deep = self.workspace / 'deep'
        deep.mkdir()
        nested = deep / 'nested'
        nested.mkdir()
        self.git(nested, 'init', '-q')
        # Act
        result = self.run_cli(self.workspace, input='2,3\ny\nfactory\nprovider/model\nhigh\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        references = self.load(self.workspace).repository
        self.assertEqual({item.local_dir for item in references}, {str(other), str(worktree)})
        self.assertIn('https://github.com/team/other.git', result.stdout)
        self.assertIn('git@github.com:team/app.git', result.stdout)
        self.assertNotIn(str(nested), result.stdout)
        self.assertNotIn(str(self.workspace / 'linked'), result.stdout)

    def test_noninteractive_eof_explains_required_flags_without_traceback(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        for flag in ('--repo', '--label', '--foreman-model', '--foreman-effort'):
            self.assertIn(flag, result.stderr)
        self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])
        self.assertFalse((repo / '.factory').exists())

    def test_invalid_local_repositories_fail_with_path_before_github(self):
        # Arrange
        good = self.repo()
        missing_origin = self.repo('missing-origin')
        self.git(missing_origin, 'remote', 'remove', 'origin')
        unsupported = self.repo('unsupported', 'git@gitlab.com:team/app.git')
        subdirectory = good / 'folder'
        subdirectory.mkdir()
        plain = self.workspace / 'plain'
        plain.mkdir()
        linked = self.workspace / 'linked'
        linked.symlink_to(good, target_is_directory=True)
        for bad in (missing_origin, unsupported, subdirectory, plain, linked,
                    self.workspace / 'does-not-exist'):
            with self.subTest(path=bad):
                # Act
                result = self.run_cli(self.workspace, '--repo', str(good),
                                      '--repo', str(bad), *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(str(bad), result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(json.loads(self.state.read_text()), {})
                self.assertFalse((self.workspace / '.factory').exists())

    def test_label_creation_failure_reports_kept_partial_progress_and_retry_reuses(self):
        # Arrange
        repo = self.repo()
        self.state.write_text(json.dumps({'fail_create': 'second'}))
        # Act
        failed = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'second')
        # Assert
        self.assertNotEqual(failed.returncode, 0)
        self.assertNotIn('Traceback', failed.stderr)
        self.assertIn('Created team/app: factory', failed.stderr)
        self.assertIn('second', failed.stderr)
        self.assertIn('kept', failed.stderr.lower())
        self.assertFalse((repo / '.factory' / 'factory.toml').exists())
        self.assertEqual(json.loads(self.state.read_text())['created'], [['team/app', 'factory']])
        # Arrange
        state = json.loads(self.state.read_text())
        del state['fail_create']
        self.state.write_text(json.dumps(state))
        # Act
        retry = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'second')
        # Assert
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.assertIn('Reused team/app: factory', retry.stdout)
        self.assertEqual(json.loads(self.state.read_text())['created'],
                         [['team/app', 'factory'], ['team/app', 'second']])

    def test_symlinked_storage_is_rejected_before_remote_changes(self):
        # Arrange
        outside = self.workspace / 'outside'
        outside.mkdir()
        target = outside / 'factory.toml'
        target.write_text('keep me')
        for kind in ('directory', 'config', 'dangling-config', 'non-directory'):
            with self.subTest(kind=kind):
                repo = self.repo(kind)
                factory = repo / '.factory'
                if kind == 'directory':
                    factory.symlink_to(outside, target_is_directory=True)
                elif kind == 'non-directory':
                    factory.write_text('keep me too')
                else:
                    factory.mkdir()
                    destination = target if kind == 'config' else outside / 'missing'
                    (factory / 'factory.toml').symlink_to(destination)
                # Act
                result = self.run_cli(repo, '--repo', '.', *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('.factory', result.stderr)
                self.assertEqual(target.read_text(), 'keep me')
                self.assertFalse((outside / 'missing').exists())
                self.assertEqual(json.loads(self.state.read_text()), {})

    def test_concurrent_config_or_storage_symlink_is_never_overwritten(self):
        from test_configuration import VALID
        # Arrange
        outside = self.workspace / 'outside'
        outside.mkdir()
        for kind in ('config', 'symlink'):
            with self.subTest(kind=kind):
                repo = self.repo(kind)
                path = repo / '.factory' / 'factory.toml'
                contents = VALID.replace('provider/model', 'other/model')
                contents = contents.replace('/existing/repo', str(repo))
                state = ({'concurrent_config': {'path': str(path), 'content': contents}}
                         if kind == 'config' else
                         {'symlink_factory': {'path': str(path.parent), 'target': str(outside)}})
                self.state.write_text(json.dumps(state))
                # Act
                result = self.run_cli(repo, '--repo', '.', *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('Created team/app: factory', result.stderr)
                self.assertIn('Saving', result.stderr)
                if kind == 'config':
                    self.assertEqual(path.read_text(), contents)
                    self.assertEqual(self.load(repo).foreman_agent_model, 'other/model')
                    self.assertEqual(list(path.parent.iterdir()), [path])
                else:
                    self.assertEqual(list(outside.iterdir()), [])

    def test_multiple_local_copies_preserve_both_paths_and_ensure_source_once(self):
        # Arrange
        first = self.repo()
        second = self.repo('copy', 'https://github.com/Team/App.git')
        # Act
        result = self.run_cli(self.workspace, '--repo', str(first), '--repo', str(second),
                              '--repo', str(first), *self.settings())
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.load(self.workspace)
        self.assertEqual({item.local_dir for item in config.repository},
                         {str(first), str(second)})
        self.assertEqual({item.remote for item in config.repository},
                         {'git@github.com:team/app.git', 'https://github.com/Team/App.git'})
        self.assertEqual(json.loads(self.state.read_text())['created'], [['team/app', 'factory']])

    def test_toml_roundtrip_preserves_unicode_quotes_spaces_and_escapes(self):
        # Arrange
        repo = self.repo('space "café" 😀')
        workspace = self.workspace / 'factory workspace'
        workspace.mkdir()
        model = 'provider/"β" 😀\\variant\nnext\x7f'
        label = 'factory "café" \\support'
        # Act
        result = self.run_cli(repo, '--workspace', str(workspace), '--repo', '.',
                              '--label', label, '--foreman-model', model,
                              '--foreman-effort', 'very high')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.load(workspace)
        self.assertEqual(config.foreman_agent_model, model)
        self.assertEqual(config.watcher_label, (label,))
        self.assertEqual(config.foreman_agent_effort, 'very high')
        self.assertEqual(next(iter(config.repository)).local_dir, str(repo))
        self.assertFalse((repo / '.factory').exists())

    def test_missing_or_nonexecutable_tools_have_actionable_errors(self):
        # Arrange
        repo = self.repo()
        (self.bin / 'python3').symlink_to(sys.executable)
        self.env['PATH'] = str(self.bin)
        for tool in ('git', 'gh', 'gh-not-executable'):
            with self.subTest(tool=tool):
                git_link = self.bin / 'git'
                if tool != 'git' and not git_link.exists():
                    git_link.symlink_to(shutil.which('git'))
                gh = self.bin / 'gh'
                if tool == 'gh':
                    gh.unlink()
                if tool == 'gh-not-executable':
                    gh.write_text(GH)
                    gh.chmod(0o644)
                # Act
                result = self.run_cli(repo, '--repo', '.', *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('git' if tool == 'git' else 'gh', result.stderr)
                self.assertIn('install' if tool != 'gh-not-executable' else 'executable',
                              result.stderr.lower())
                self.assertFalse((repo / '.factory').exists())

    def test_github_origin_uses_github_com_despite_environment_host(self):
        # Arrange
        repo = self.repo()
        self.env['GH_HOST'] = 'enterprise.example.com'
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings())
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.state.read_text())['created'], [['team/app', 'factory']])

    def test_unsupported_origins_cannot_be_used_as_api_paths(self):
        # Arrange
        repo = self.repo()
        remotes = ['git@github.com:../app.git', 'https://github.com/team/../app.git',
                   'https://enterprise.example.com/team/app.git',
                   'https://github.com/team/app.git?token=value',
                   'https://github.com/team/..', 'git@github.com:team/.git']
        for remote in remotes:
            with self.subTest(remote=remote):
                self.git(repo, 'remote', 'set-url', 'origin', remote)
                # Act
                result = self.run_cli(repo, '--repo', '.', *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Unsupported origin', result.stderr)
                self.assertEqual(json.loads(self.state.read_text()), {})
                self.assertFalse((repo / '.factory').exists())

    def test_non_utf8_settings_are_rejected_before_label_creation(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, '--repo', '.', '--label', 'factory',
                              '--foreman-model', 'provider/\udcff', '--foreman-effort', 'high')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('Unicode', result.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertFalse((repo / '.factory').exists())

    def test_repository_path_with_trailing_space_is_stored_exactly(self):
        # Arrange
        repo = self.repo('app with trailing space ')
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings())
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(next(iter(self.load(repo).repository)).local_dir, str(repo))

    def test_malformed_create_response_reports_uncertainty_and_does_not_save(self):
        # Arrange
        repo = self.repo()
        self.state.write_text(json.dumps({'malformed_create': 'second'}))
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'second')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('malformed', result.stderr.lower())
        self.assertIn('Created team/app: factory', result.stderr)
        self.assertIn('may have completed', result.stderr)
        self.assertFalse((repo / '.factory' / 'factory.toml').exists())
        self.assertEqual(json.loads(self.state.read_text())['created'],
                         [['team/app', 'factory'], ['team/app', 'second']])

    def test_timeout_reports_partial_progress_and_retry_guidance(self):
        # Arrange
        repo = self.repo()
        self.state.write_text(json.dumps({'timeout_create': 'slow'}))
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'slow',
                              timeout=45)
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('timed out after 30 seconds', result.stderr)
        self.assertIn('Created team/app: factory', result.stderr)
        self.assertIn('rerun init', result.stderr)
        self.assertFalse((repo / '.factory' / 'factory.toml').exists())

    def test_ctrl_c_during_creation_reports_partial_progress_cleanly(self):
        # Arrange
        repo = self.repo()
        self.state.write_text(json.dumps({'interrupt_create': 'second'}))
        # Act
        result = self.run_cli(repo, '--repo', '.', *self.settings(), '--label', 'second')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('interrupted', result.stderr.lower())
        self.assertIn('Created team/app: factory', result.stderr)
        self.assertIn('kept', result.stderr.lower())
        self.assertFalse((repo / '.factory' / 'factory.toml').exists())

    def test_interactive_single_repo_can_watch_all_without_creating_labels(self):
        # Arrange
        repo = self.repo()
        # Act
        result = self.run_cli(repo, input='\ny\n*\nprovider/model\nhigh\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        config = self.load(repo)
        self.assertEqual(config.watcher_label, ('*',))
        self.assertEqual(next(iter(config.repository)).local_dir, str(repo))
        self.assertEqual(json.loads(self.state.read_text()).get('created', []), [])

    def test_discovery_from_nonroot_child_never_selects_parent_repository(self):
        # Arrange
        repo = self.repo()
        child = repo / 'ordinary-child'
        child.mkdir()
        # Act
        result = self.run_cli(child, *self.settings())
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('No local repository roots', result.stderr)
        self.assertIn('--repo', result.stderr)
        self.assertEqual(json.loads(self.state.read_text()), {})
        self.assertFalse((child / '.factory').exists())

    def test_workspace_must_exist_before_any_remote_changes(self):
        # Arrange
        repo = self.repo()
        for workspace in (self.workspace / 'missing', self.state):
            with self.subTest(workspace=workspace):
                # Act
                result = self.run_cli(repo, '--repo', '.', '--workspace', str(workspace),
                                      *self.settings())
                # Assert
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Workspace', result.stderr)
                self.assertEqual(json.loads(self.state.read_text()), {})


if __name__ == '__main__':
    unittest.main()
