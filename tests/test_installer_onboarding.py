"""Installer onboarding at the public init CLI, using external uv/Python doubles."""
import json
import shutil
import subprocess
import sys

from profile_support import events
from test_init import INIT_SETTINGS, InitFixture


class InstallerOnboardingTests(InitFixture):
    def setUp(self):
        super().setUp()
        (self.bin / 'forgetful').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        self.log = self.workspace / 'install.jsonl'
        self.preflight_log = self.workspace / 'preflight.jsonl'
        self.env.update(PATH=str(self.bin), PROFILE_INSTALL_LOG=str(self.log),
                        PROFILE_PREFLIGHT_LOG=str(self.preflight_log))

    def assert_preflight_stopped(self, repo, result, diagnostic):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(diagnostic, result.stderr)
        self.assertIn('rerun init', result.stderr)
        self.assertNotIn('Install ', result.stdout)
        self.assertNotIn('[y/N]', result.stdout)
        self.assertNotIn('TOP_SECRET', result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(events(self.log), [])
        self.assertFalse((repo / '.factory/runtime').exists())

    def test_missing_uv_stops_before_install_consent(self):
        # Arrange
        repo = self.repo()
        (self.bin / 'uv').unlink()
        # Act: refusal would hide the prerequisite error if the prompt came first.
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
        # Assert
        self.assert_preflight_stopped(repo, result, 'uv >=0.13.5')
        self.assertIn('PATH', result.stderr)

    def test_malformed_discovery_output_stops_before_install_consent(self):
        non_executable = self.bin / 'not executable'
        non_executable.write_text('not Python')
        outputs = ('', 'python3.12', str(self.bin), str(non_executable), '/missing/python3.12',
                   str(self.bin / 'installed python3.12') + '\nextra output')
        for index, output in enumerate(outputs):
            with self.subTest(output=output):
                # Arrange
                repo = self.repo('malformed-' + str(index))
                self.env['PROFILE_PYTHON_FIND_RESULT'] = output
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
                # Assert
                self.assert_preflight_stopped(repo, result, 'Python 3.12')
                self.assertFalse(any(e['name'] == 'python' for e in events(self.preflight_log)))

    def test_wrong_or_unusable_discovered_python_stops_before_install_consent(self):
        settings = ({'PROFILE_PYTHON_PROBE_OUTPUT': 'cpython 3 13'},
                    {'PROFILE_PYTHON_PROBE_OUTPUT': 'cpython 3 11'},
                    {'PROFILE_PYTHON_PROBE_OUTPUT': 'pypy 3 12'},
                    {'PROFILE_PYTHON_PROBE_OUTPUT': 'malformed version'},
                    {'PROFILE_PYTHON_PROBE_FAIL': '1'})
        for index, setting in enumerate(settings):
            with self.subTest(setting=setting):
                # Arrange
                repo = self.repo('probe-' + str(index))
                self.env.update(setting)
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
                # Assert
                self.assert_preflight_stopped(repo, result, 'Python 3.12')
                for key in setting:
                    del self.env[key]

    def test_refusal_after_read_only_discovery_makes_no_package_changes(self):
        # Arrange
        repo = self.repo()
        self.env.update(UV_PYTHON='3.13', UV_PYTHON_DOWNLOADS='automatic',
                        UV_CONFIG_FILE='/wrong/uv.toml', UV_NO_VERIFY_HASHES='1',
                        PIP_INDEX_URL='https://unreviewed.invalid',
                        NPM_CONFIG_IGNORE_SCRIPTS='false',
                        NODE_OPTIONS='--invalid-option', VIRTUAL_ENV='/wrong',
                        CONDA_PREFIX='/wrong')
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('declined', result.stderr)
        self.assertIn('Install Forgetful CLI 0.5.5 in .factory/runtime/forgetful?', result.stdout)
        self.assertIn('does not start another server', result.stdout)
        self.assertIn('Downloads from PyPI using existing Python 3.12:', result.stdout)
        self.assertIn(str(self.bin / 'installed python3.12'), result.stdout)
        self.assertIn('[y/N]', result.stdout)
        self.assertNotIn('wheel hashes', result.stdout)
        self.assertTrue(all(len(line) <= 100 for line in result.stdout.splitlines()))
        self.assertEqual(events(self.log), [])
        self.assertFalse((repo / '.factory/runtime').exists())
        calls = events(self.preflight_log)
        discovery = next(e for e in calls if e['args'][:2] == ['python', 'find'])
        for flag in ('--no-config', '--no-project', '--no-python-downloads', '--offline',
                     '--no-cache', '--system'):
            self.assertIn(flag, discovery['args'])
        self.assertIn('cpython@3.12', discovery['args'])
        for call in calls:
            if call['name'] == 'uv':
                self.assertEqual(call['config_env'], [])
                self.assertFalse(call['virtual_env'])
                self.assertFalse(call['node_options'])
        probe = next(e for e in calls if e['name'] == 'python')
        self.assertEqual(probe['args'][:4], ['-I', '-B', '-S', '-c'])

    def test_unsupported_or_failed_uv_stops_before_install_consent(self):
        settings = ({'PROFILE_UV_VERSION': 'uv 0.8.0'},
                    {'PROFILE_UV_VERSION': 'unexpected output'},
                    {'PROFILE_UV_VERSION': 'uv 0.13.5rc1'},
                    {'PROFILE_UV_VERSION': 'uv 0.13.5\nextra output'},
                    {'PROFILE_UV_VERSION_FAIL': '1'})
        for index, setting in enumerate(settings):
            with self.subTest(setting=setting):
                # Arrange
                repo = self.repo('version-' + str(index))
                self.env.update(setting)
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
                # Assert
                self.assert_preflight_stopped(repo, result, 'uv >=0.13.5')
                for key in setting:
                    del self.env[key]

    def test_uv_below_security_baseline_stops_before_any_install(self):
        for index, version in enumerate(('0.13.1', '0.13.3', '0.13.4')):
            with self.subTest(version=version):
                # Arrange: even an affirmative input must not bypass the audited uv minimum.
                repo = self.repo('security-version-' + str(index))
                self.log.unlink(missing_ok=True)
                self.preflight_log.unlink(missing_ok=True)
                self.env['PROFILE_UV_VERSION'] = 'uv ' + version
                # Act
                result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
                # Assert: no installer execution or consent prompt, not just different wording.
                self.assertEqual(events(self.log), [])
                self.assertNotIn('[y/N]', result.stdout)
                self.assert_preflight_stopped(repo, result, 'uv >=0.13.5')
                self.assertEqual([event['args'] for event in events(self.preflight_log)],
                                 [['--version']])
                self.assertFalse((repo / '.factory/factory.toml').exists())
                self.assertFalse((repo / '.factory/setup-complete.json').exists())
                self.preflight_log.unlink()
                del self.env['PROFILE_UV_VERSION']

    def test_no_python312_stops_before_install_consent(self):
        # Arrange
        repo = self.repo()
        (self.bin / 'installed python3.12').unlink()
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
        # Assert
        self.assert_preflight_stopped(repo, result, 'Python 3.12')
        self.assertIn('already installed', result.stderr)
        self.assertIn('PATH', result.stderr)

    def test_failed_discovery_stops_before_install_consent(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_PYTHON_FIND_FAIL'] = '1'
        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        # Assert
        self.assert_preflight_stopped(repo, result, 'Python 3.12')

    def assert_watch_incomplete(self, repo):
        self.state.write_text('{}')
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(repo),
             '--new-only'], cwd=repo, env=self.env, capture_output=True, text=True, timeout=5)
        self.assertNotEqual(result.returncode, 0)
        self.assertRegex(result.stderr, 'incomplete|run init first')
        self.assertEqual(json.loads(self.state.read_text()), {})

    def test_repeated_init_preserves_damaged_runtime_without_preflight_and_watch_still_blocks(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
        self.assertEqual(setup.returncode, 0, setup.stderr)
        runtime = repo / '.factory/runtime/forgetful'
        (runtime / 'bin/.fixture-package').unlink()
        original = {p: p.read_bytes() for p in runtime.rglob('*') if p.is_file()}
        self.log.unlink()
        self.env['PROFILE_PYTHON_FIND_FAIL'] = '1'
        # Act
        result = self.run_cli(repo, input='y\n')
        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn('[y/N]', result.stdout)
        self.assertEqual(events(self.log), [])
        self.assertEqual({p: p.read_bytes() for p in runtime.rglob('*') if p.is_file()}, original)
        self.assert_watch_incomplete(repo)

    def test_failed_install_blocks_watch_until_consented_retry_completes(self):
        for stage in ('venv', 'pip'):
            with self.subTest(stage=stage):
                # Arrange
                repo = self.repo(stage)
                runtime = repo / '.factory/runtime/forgetful'
                self.env['PROFILE_INSTALL_FAIL'] = stage
                # Act
                failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
                # Assert
                self.assertNotEqual(failed.returncode, 0)
                self.assertIn('setup is incomplete', failed.stderr)
                self.assertFalse((runtime / '.factory-sync').exists())
                self.assert_watch_incomplete(repo)
                # Arrange
                del self.env['PROFILE_INSTALL_FAIL']
                # Act
                refused = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='n\n')
                retry = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')
                calls = events(self.log)
                unchanged = self.run_cli(repo)
                # Assert
                self.assertIn('declined', refused.stderr)
                self.assertEqual(retry.returncode, 0, retry.stderr)
                self.assertIn('Forgetful: connected', retry.stdout)
                self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
                self.assertEqual(events(self.log), calls)
                self.assertTrue((runtime / '.factory-sync').is_file())
