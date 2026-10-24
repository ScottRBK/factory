"""Manual setup completion and launch through the public CLI in a real terminal."""
import json
import os
import pty
import shlex
import signal
import subprocess
import sys
import time

from lifecycle_support import LifecycleFixture
from test_init import INIT_SETTINGS, ROOT


class ManualLaunchTests(LifecycleFixture):
    def start_init(self, repo, *extra):
        master, slave = pty.openpty()
        self.addCleanup(os.close, master)
        output = repo / 'init-output.txt'
        command = [sys.executable, '-m', 'forgetful_factory', 'init', '--workspace', str(repo),
                   '--agentshell-python', str(self.interpreter), '--repo', str(repo),
                   *INIT_SETTINGS, '--planning-only', '--share-pi-profile',
                   '--forgetful-instance', 'local', '--forgetful-project', '12',
                   '--grill-me-skill', str(self.grill_skill), '--install-role-runtime', *extra]
        try:
            with output.open('w') as stream:
                process = subprocess.Popen(command, cwd=ROOT, env=self.env, stdin=slave,
                                           stdout=stream, stderr=stream, start_new_session=True)
        finally:
            os.close(slave)
        self.addCleanup(self.cleanup_init, process)
        return process, master, output

    def cleanup_init(self, process):
        if process.poll() is None:
            process.terminate()
        try:
            process.wait(timeout=30)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

    def wait_for_output(self, process, output, text):
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            if text in output.read_text():
                return
            if process.poll() is not None:
                self.fail(f'Init exited {process.returncode}: {output.read_text()}')
            time.sleep(0.02)
        self.fail(f'Missing {text!r}: {output.read_text()}')

    def test_yes_launches_after_issue_choice_and_releases_the_setup_lock(self):
        # Arrange
        repo = self.repo()
        self.state.write_text(json.dumps({'issues': [
            {'number': 1, 'title': 'Existing epic', 'state': 'open', 'body': 'Fixture',
             'html_url': 'https://github.com/team/app/issues/1',
             'labels': [{'name': 'factory'}, {'name': 'epic'}]},
        ]}))

        # Act
        process, terminal, output = self.start_init(repo)
        self.wait_for_output(process, output, 'Launch factory now? [y/N]: ')
        os.write(terminal, b'y\n')
        self.wait_for_output(process, output, 'Forward existing matches')

        # Assert: launch consent does not silently choose existing work or start an agent yet.
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        self.assertFalse((self.workspace / 'plans.json').exists())

        # Act
        os.write(terminal, b'e\n')
        self.wait_for_output(process, output, 'Submitted github:team/app#1 to Pi')
        process.send_signal(signal.SIGINT)
        process.wait(timeout=20)

        # Assert: public watch ran, acquired the lease and closed its owned fake Pi.
        text = output.read_text()
        self.assertEqual(process.returncode, 130, text)
        self.assertIn('Watch interrupted', text)
        self.assertNotIn('Setup is incomplete', text)
        self.assertNotIn('already running', text)
        log = (self.workspace / 'pi.jsonl').read_text()
        events = [json.loads(line) for line in log.splitlines()]
        self.assertEqual(len([event for event in events if 'started' in event]), 1)
        self.assertTrue(any('Factory issue notification' in event.get('input', '')
                            for event in events))
        retried = self.run_cli(repo)
        self.assertEqual(retried.returncode, 0, retried.stderr)
        self.assertTrue((repo / '.factory/setup-complete.json').exists())

    def test_assisted_finalization_skips_launch_offer_and_foreman_starts_its_watcher(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)

        # Act: even in a terminal, finalization must not ask to launch a second Foreman.
        process, terminal, output = self.start_init(repo, '--finalize', '--delegated-work-stopped')
        process.wait(timeout=15)

        # Assert
        self.assertEqual(process.returncode, 0, output.read_text())
        for text in (setup.stdout, output.read_text()):
            self.assertNotIn('Launch factory now?', text)
            self.assertNotIn('To start your factory later', text)
        role = repo / '.factory/agents/foreman'
        guidance = (role / 'skills/factory-maintenance/SKILL.md').read_text()
        self.assertIn('you start the watcher from this conversation', guidance)
        self.assertIn('Confirm whether to include existing matching issues', guidance)
        self.assertIn('not a separate CLI launch prompt', guidance)
        self.assertIn('watch --start --existing', guidance)
        self.assertIn('watch --start --new-only', guidance)
        self.assertIn('/reload', guidance)
        self.assertEqual(self.status(repo)['target'], original['target'])

        # Act: emulate Foreman's command from its role directory, without a model request.
        started = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'watch', '--start', '--new-only',
             '--workspace', str(repo)], cwd=role, env=self.env, capture_output=True,
            text=True, timeout=15)

        # Assert
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertEqual(self.status(repo)['target'], original['target'])
        self.assertEqual(self.status(repo)['watcher'], 'running')
        stopped = self.watch(repo, '--stop')
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        self.assertEqual(self.status(repo)['foreman'], 'ready')
        self.send_and_wait_for_exit(repo, original['target'])

    def test_eof_or_interrupt_at_launch_offer_keeps_completed_setup(self):
        for action, expected_code in (('eof', 0), ('interrupt', 130)):
            with self.subTest(action=action):
                # Arrange
                repo = self.repo(action)
                process, terminal, output = self.start_init(repo)
                self.wait_for_output(process, output, 'Launch factory now? [y/N]: ')

                # Act
                if action == 'eof':
                    os.write(terminal, b'\x04')
                else:
                    process.send_signal(signal.SIGINT)
                process.wait(timeout=10)

                # Assert
                text = output.read_text()
                self.assertEqual(process.returncode, expected_code, text)
                self.assertNotIn('Setup is incomplete', text)
                self.assertNotIn('For noninteractive init', text)
                self.assertIn('Factory setup complete.', text)
                self.assertTrue((repo / '.factory/setup-complete.json').exists())
                self.assertFalse((self.workspace / 'pi.jsonl').exists())

    def test_failed_validation_does_not_offer_launch_or_print_a_start_command(self):
        # Arrange
        repo = self.repo()
        self.env['PROFILE_FAIL'] = 'forgetful'

        # Act
        process, terminal, output = self.start_init(repo)
        process.wait(timeout=15)

        # Assert
        self.assertNotEqual(process.returncode, 0, output.read_text())
        self.assertNotIn('Launch factory now?', output.read_text())
        self.assertNotIn('To start your factory later', output.read_text())
        self.assertNotIn('Factory setup complete.', output.read_text())
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        self.assertFalse((self.workspace / 'pi.jsonl').exists())

    def test_printed_start_command_runs_from_another_directory_with_new_only_selection(self):
        # Arrange
        repo = self.repo("team's app")
        relative = os.path.relpath(self.interpreter, repo)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS,
                             '--agentshell-python', relative)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        command = shlex.split(setup.stdout.split('To start your factory later, run:\n', 1)[1]
                              .splitlines()[0])
        self.assertEqual(command[-2:], ['--agentshell-python', str(self.interpreter)])
        state = json.loads(self.state.read_text())
        state['issues'] = [
            {'number': 1, 'title': 'Existing epic', 'state': 'open', 'body': 'Fixture',
             'html_url': 'https://github.com/team/app/issues/1',
             'labels': [{'name': 'factory'}, {'name': 'epic'}]},
        ]
        self.state.write_text(json.dumps(state))
        output = self.workspace / 'copied-command-output.txt'

        # Act
        with output.open('w') as stream:
            process = subprocess.Popen(command, cwd=ROOT, env=self.env, stdin=subprocess.PIPE,
                                       stdout=stream, stderr=stream, text=True)
        self.addCleanup(self.cleanup_init, process)
        process.stdin.write('n\n')
        process.stdin.close()
        self.wait_for_output(process, output, 'Baseline team/app: 1 matching issues.')
        process.send_signal(signal.SIGINT)
        process.wait(timeout=20)

        # Assert
        self.assertEqual(process.returncode, 130, output.read_text())
        self.assertNotIn('Submitted', output.read_text())
        log = (self.workspace / 'pi.jsonl').read_text()
        events = [json.loads(line) for line in log.splitlines()]
        self.assertEqual(len([event for event in events if 'started' in event]), 1)
        self.assertFalse(any('Factory issue notification' in event.get('input', '')
                             for event in events))
        self.collect_owner_handles()
        self.assertIn(process.pid, self.owner_descriptors, 'Selected interpreter was not used')

    def test_noninteractive_init_only_prints_the_start_command_even_with_yes_input(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, input='y\ne\n')

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('To start your factory later, run:', result.stdout)
        self.assertNotIn('Launch factory now?', result.stdout)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        self.assertFalse((self.workspace / 'plans.json').exists())

    def test_manual_setup_offers_launch_and_default_no_keeps_setup_complete(self):
        # Arrange
        repo = self.repo("team's app")

        # Act
        process, terminal, output = self.start_init(repo)
        self.wait_for_output(process, output, 'Launch factory now? [y/N]: ')
        os.write(terminal, b'\n')
        process.wait(timeout=10)

        # Assert
        text = output.read_text()
        self.assertEqual(process.returncode, 0, text)
        self.assertIn('Factory setup complete.', text)
        heading = 'To start your factory later, run:\n'
        self.assertIn(heading, text)
        command = shlex.split(text.split(heading, 1)[1].splitlines()[0])
        self.assertEqual(command, [sys.executable, '-m', 'forgetful_factory', 'watch',
                                   '--workspace', str(repo), '--agentshell-python',
                                   str(self.interpreter)])
        self.assertIn('This watches GitHub issues and sends work to Foreman.', text)
        self.assertTrue((repo / '.factory/setup-complete.json').exists())
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        self.assertFalse((self.workspace / 'plans.json').exists())

    def test_repeated_init_in_terminal_does_not_consume_optional_launch_consent(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        receipt = repo / '.factory/setup-complete.json'
        before = receipt.read_bytes()

        # Act: no input is supplied; a repeated init must finish without asking to launch.
        process, _, output = self.start_init(repo)
        process.wait(timeout=10)

        # Assert
        self.assertEqual(process.returncode, 0, output.read_text())
        self.assertIn('already initialized', output.read_text())
        self.assertNotIn('Launch factory now?', output.read_text())
        self.assertNotIn('To start your factory later', output.read_text())
        self.assertEqual(receipt.read_bytes(), before)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
