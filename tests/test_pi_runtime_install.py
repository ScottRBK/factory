"""Audited managed Pi installation through public Factory init; installers are controlled."""
import shutil
import sys

from profile_support import INSTALLER, events
from test_init import INIT_SETTINGS, InitFixture


class PiRuntimeInstallTests(InitFixture):
    def test_consented_pi_installation_disables_scripts_and_checks_engine_requirements(self):
        # Arrange: only the external installer is simulated.
        repo = self.repo()
        (self.bin / 'pi').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        manager = self.bin / 'npm'
        manager.write_text(INSTALLER)
        manager.chmod(0o755)
        log = self.workspace / 'installer.jsonl'
        self.env.update(PATH=str(self.bin), PROFILE_INSTALL_LOG=str(log))

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')

        # Assert: observe installation consent and safe installer options, not dependency versions.
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Install Pi', result.stdout)
        calls = [event for event in events(log) if event['name'] == 'npm']
        self.assertEqual(len(calls), 1)
        self.assertIn('--ignore-scripts', calls[0]['args'])
        self.assertIn('--engine-strict', calls[0]['args'])

    def test_pi_processes_do_not_enable_the_unaudited_experimental_http_parser(self):
        # Arrange: an inherited experimental switch must not alter the audited runtime policy.
        repo = self.repo()
        (self.bin / 'pi').unlink()
        for name, target in (('git', shutil.which('git')), ('python3', sys.executable)):
            (self.bin / name).symlink_to(target)
        manager = self.bin / 'npm'
        manager.write_text(INSTALLER)
        manager.chmod(0o755)
        log = self.workspace / 'profile.jsonl'
        self.env.update(PATH=str(self.bin), PROFILE_LOG=str(log), UNDICI_USE_MILO='1')

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\n')

        # Assert: observe actual public Pi subprocess inputs, not Factory's environment helper.
        self.assertEqual(result.returncode, 0, result.stderr)
        pi_calls = [event for event in events(log) if event['name'] == 'pi']
        self.assertTrue(any(event['args'] == ['--version'] for event in pi_calls))
        self.assertTrue(any(event['args'] == ['--no-approve', '--list-models']
                            for event in pi_calls))
        self.assertTrue(all(event['milo'] is None for event in pi_calls), pi_calls)
