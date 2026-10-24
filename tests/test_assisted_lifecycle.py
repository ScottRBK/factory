"""Lifecycle behavior through public CLI and native terminal boundaries."""
import json
import os
import select
import signal
import subprocess
import sys

from lifecycle_support import LifecycleFixture, pidfd_open
from test_init import INIT_SETTINGS


class AssistedLifecycleTests(LifecycleFixture):
    def notification(self, name):
        path = self.workspace / name
        os.mkfifo(path)
        descriptor = os.open(path, os.O_RDWR | os.O_NONBLOCK)
        self.addCleanup(os.close, descriptor)
        return str(path), descriptor

    def test_assisted_init_exits_with_surviving_foreman_and_incomplete_setup(self):
        # Arrange
        repo = self.repo()

        # Act
        result = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)

        # Assert
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Setup is incomplete', result.stdout)
        self.assertIn('attach-session', result.stdout)
        status = self.status(repo)
        self.assertEqual(status['foreman'], 'ready')
        self.assertEqual(status['setup'], 'incomplete')
        self.assertEqual(status['watcher'], 'stopped')
        self.assertFalse((repo / '.factory/setup-complete.json').exists())
        definition = repo / '.factory/agents/foreman/agent.json'
        self.assertEqual(json.loads(definition.read_text())['roster'],
                         {'enabled': True,
                          'roles': [{'agent_file': '../feature-owner/agent.json'}]})
        launch = json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[0])
        self.assertEqual(launch['roster'], str(definition))
        blocked = self.watch(repo, '--new-only')
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse((self.workspace / 'plans.json').exists())
        duplicate = self.foreman(repo)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn('--attach', duplicate.stderr)
        self.assertEqual(self.status(repo)['target'], status['target'])
        self.send(status['target'], 'EXIT_FAKE')

    def test_finalize_then_watch_stop_preserves_same_foreman_and_lease(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        blocked = self.watch(repo, '--start', '--new-only')
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse((self.workspace / 'plans.json').exists())
        finalize = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(finalize.returncode, 0, finalize.stderr)

        # Act
        start = self.watch(repo, '--start', '--new-only', '--interval', '0.1')

        # Assert
        self.assertEqual(start.returncode, 0, start.stderr)
        running = self.status(repo)
        self.assertEqual(running['watcher'], 'running')
        self.assertEqual(running['target'], original['target'])
        duplicate = self.watch(repo, '--start', '--existing')
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn('already', duplicate.stderr)
        during = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertNotEqual(during.returncode, 0)
        self.assertIn('watcher', during.stderr)
        stopped = self.watch(repo, '--stop')
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        after = self.status(repo)
        self.assertEqual(after['watcher'], 'stopped')
        self.assertEqual(after['foreman'], 'ready')
        self.assertEqual(after['target'], original['target'])
        repeat = self.watch(repo, '--stop')
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        again = self.run_cli(repo, '--delegated-work-stopped')
        self.assertEqual(again.returncode, 0, again.stderr)
        self.send(original['target'], 'EXIT_FAKE')

    def test_foreman_exit_stops_watcher_and_completed_setup_can_restart_standalone(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        started = self.watch(repo, '--start', '--new-only')
        self.assertEqual(started.returncode, 0, started.stderr)

        # Act: fake Pi exits; tmux keeps the terminal until AgentShell finishes cleanup.
        self.send_and_wait_for_exit(repo, original['target'])

        # Assert: public init can take the released lease; no replacement appeared.
        again = self.run_cli(repo, '--finalize')
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(self.status(repo)['foreman'], 'stopped')
        self.assertEqual(self.status(repo)['watcher'], 'stopped')
        before = (repo / '.factory/factory.toml').read_bytes()
        instructions = repo / '.factory/agents/foreman/AGENTS.md'
        custom = instructions.read_text() + '\nPreserve the team review checklist.\n'
        instructions.write_text(custom)
        relaunched = self.foreman(repo, timeout=20)
        self.assertEqual(relaunched.returncode, 0, relaunched.stderr)
        after = self.status(repo)
        self.assertNotEqual(after['target'], original['target'])
        self.assertEqual(after['setup'], 'complete')
        self.assertEqual((repo / '.factory/factory.toml').read_bytes(), before)
        self.assertEqual(instructions.read_text(), custom)
        self.send(after['target'], 'EXIT_FAKE')

    def test_uncertain_owner_state_never_authorizes_replacement_or_pid_signals(self):
        # Arrange: a failed previous launch has no captured terminal and a reused-looking PID.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        state = repo / '.factory/runtime/foreman/owner.json'
        state.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        content = {'workspace': str(repo), 'run_id': 'old-owner', 'foreman': 'starting',
                   'target': None, 'watcher': 'stopped', 'pid': os.getpid()}
        state.write_text(json.dumps(content))

        # Act
        result = self.foreman(repo)

        # Assert
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('uncertain', result.stderr)
        self.assertEqual(json.loads(state.read_text()), content)
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        # A dead owner must not prevent ordinary validation/repair without launching a session.
        repaired = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(repaired.returncode, 0, repaired.stderr)

    def test_changed_pane_is_preserved_and_cannot_receive_watcher_delivery(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        before = self.status(repo)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        descriptor = pidfd_open(before['owner_pid'])
        self.addCleanup(os.close, descriptor)

        # Act: replace only the disposable fixture pane, retaining its numeric pane ID.
        changed = subprocess.run([self.tmux, '-S', str(self.socket), 'respawn-pane', '-k',
                                  '-t', before['target']['pane_id'], '/bin/cat'],
                                 env=self.env, capture_output=True, text=True, timeout=5)
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertTrue(select.select([descriptor], [], [], 15)[0],
                        'Owner did not detect pane loss')
        start = self.watch(repo, '--start', '--existing')
        assisted = self.foreman(repo)

        # Assert: identity uncertainty never authorizes a replacement or cleanup of the new pane.
        self.assertNotEqual(start.returncode, 0)
        self.assertNotEqual(assisted.returncode, 0)
        self.assertFalse((self.workspace / 'plans.json').exists())
        pane = subprocess.run([self.tmux, '-S', str(self.socket), 'display-message', '-p',
                               '-t', before['target']['pane_id'], '#{pane_pid}'],
                              env=self.env, capture_output=True, text=True, timeout=5)
        self.assertEqual(pane.returncode, 0, pane.stderr)
        self.assertNotEqual(int(pane.stdout.strip()), before['target']['pane_pid'])

    def test_changed_control_socket_is_preserved_even_when_original_owner_exits(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        descriptor = pidfd_open(original['owner_pid'])
        self.addCleanup(os.close, descriptor)
        endpoint = repo / '.factory/runtime/foreman/control.sock'
        endpoint.unlink()
        endpoint.write_text('Preserve replacement path.\n')

        # Act
        unavailable = self.watch(repo, '--status')
        duplicate = self.foreman(repo)
        self.send(original['target'], 'EXIT_FAKE')
        self.assertTrue(select.select([descriptor], [], [], 15)[0], 'Owner cleanup did not finish')

        # Assert
        self.assertEqual(unavailable.returncode, 0, unavailable.stderr)
        offline = json.loads(unavailable.stdout)
        self.assertEqual(offline['observation'], 'saved')
        self.assertEqual(offline['foreman'], 'unknown')
        self.assertIn('socket identity is invalid', offline['warning'])
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(endpoint.read_text(), 'Preserve replacement path.\n')

    def test_cancellation_before_ready_closes_launch_and_releases_lease(self):
        # Arrange: fake Pi announces process startup but withholds its session-ready event.
        repo = self.repo()
        self.env['FAKE_PI_NO_READY'] = '1'
        self.env['FAKE_PI_NOTIFY'] = str(self.workspace / 'started.fifo')
        os.mkfifo(self.env['FAKE_PI_NOTIFY'])
        # Open both ends so the child can acknowledge without polling files/processes.
        notify = os.open(self.env['FAKE_PI_NOTIFY'], os.O_RDWR | os.O_NONBLOCK)
        self.addCleanup(os.close, notify)
        from test_init import ROOT
        args = [sys.executable, '-m', 'forgetful_factory', 'init', '--workspace', str(repo),
                '--agentshell-python', str(self.interpreter),
                '--repo', str(repo), *INIT_SETTINGS, '--assisted', '--share-pi-profile',
                '--forgetful-instance', 'local', '--forgetful-project', '12', '--planning-only',
                '--grill-me-skill', str(self.grill_skill), '--install-role-runtime']
        process = subprocess.Popen(args, cwd=ROOT, env=self.env, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.poll() is None and process.kill())
        self.assertTrue(select.select([notify], [], [], 10)[0], 'Fake Pi did not start')
        os.read(notify, 100)
        self.collect_owner_handles()
        self.assertEqual(len(self.owner_descriptors), 1)
        owner = next(iter(self.owner_descriptors.values()))

        # Act
        process.send_signal(signal.SIGINT)
        stdout, stderr = process.communicate(timeout=20)

        # Assert
        self.assertEqual(process.returncode, 130, stdout + stderr)
        self.assertTrue(select.select([owner], [], [], 5)[0], 'Cancelled owner did not exit')
        self.env.pop('FAKE_PI_NO_READY')
        self.env.pop('FAKE_PI_NOTIFY')
        repair = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(repair.returncode, 0, repair.stderr)
        relaunched = self.foreman(repo, timeout=20)
        self.assertEqual(relaunched.returncode, 0, relaunched.stderr)
        self.send(self.status(repo)['target'], 'EXIT_FAKE')

    def test_owner_delivers_issue_and_survives_closed_init_terminal(self):
        # Arrange: init uses a disposable terminal for diagnostics, never the owner's descriptors.
        import pty

        from test_init import ROOT
        repo = self.repo()
        path, notification = self.notification('input.fifo')
        self.env['FAKE_PI_INPUT_NOTIFY'] = path
        master, slave = pty.openpty()
        args = [sys.executable, '-m', 'forgetful_factory', 'init', '--workspace', str(repo),
                '--agentshell-python', str(self.interpreter),
                '--repo', str(repo), *INIT_SETTINGS, '--assisted', '--share-pi-profile',
                '--forgetful-instance', 'local', '--forgetful-project', '12', '--planning-only',
                '--grill-me-skill', str(self.grill_skill), '--install-role-runtime']
        try:
            result = subprocess.run(args, cwd=ROOT, env=self.env, stdin=subprocess.DEVNULL,
                                    stdout=slave, stderr=slave, timeout=15)
            self.assertEqual(result.returncode, 0)
        finally:
            os.close(slave)
            os.close(master)
        original = self.status(repo)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        state = json.loads(self.state.read_text())
        state['issues'] = [{'number': 1, 'title': 'Fixture epic', 'state': 'open',
                            'body': 'A no-inference notification',
                            'html_url': 'https://github.com/team/app/issues/1',
                            'labels': [{'name': 'factory'}, {'name': 'epic'}]}]
        self.state.write_text(json.dumps(state))

        # Act
        start = self.watch(repo, '--start', '--existing')

        # Assert: native fake Pi saw actual literal AgentShell-delivered notification text.
        self.assertEqual(start.returncode, 0, start.stderr)
        self.assertTrue(select.select([notification], [], [], 10)[0], 'No terminal delivery')
        os.read(notification, 100)
        stopped = self.watch(repo, '--stop')
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        lines = [json.loads(line)
                 for line in (self.workspace / 'pi.jsonl').read_text().splitlines()]
        self.assertEqual(len([line for line in lines if 'started' in line]), 1)
        delivered = ''.join(line.get('input', '') for line in lines)
        self.assertIn('Factory issue notification', delivered)
        self.assertIn(sys.executable, lines[0]['command'])
        self.assertEqual(self.status(repo)['target'], original['target'])
        self.send_and_wait_for_exit(repo, original['target'])

    def test_stop_escalates_only_known_frozen_watcher_and_releases_lease(self):
        # Arrange: a controlled external executable freezes its calling watcher after readiness.
        repo = self.repo()
        path, notification = self.notification('frozen.fifo')
        self.env['GH_FREEZE_NOTIFY'] = path
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        started = self.watch(repo, '--start', '--new-only')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertTrue(select.select([notification], [], [], 10)[0], 'Watcher did not freeze')
        original = self.status(repo)

        # Act
        stopped = self.watch(repo, '--stop', timeout=15)

        # Assert
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        self.assertIn('uncertain', stopped.stdout)
        self.assertEqual(self.status(repo)['foreman'], 'ready')
        self.assertEqual(self.status(repo)['target'], original['target'])
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_restart_refuses_unacknowledged_delivery_after_watcher_stop(self):
        # Arrange: hold one native tmux operation while the owner remains responsive to control.
        repo = self.repo()
        notify_path, notification = self.notification('delivery.fifo')
        release_path, release = self.notification('release.fifo')
        marker = self.workspace / 'first-delivery'
        (self.bin / 'tmux').write_text(
            f'#!{sys.executable}\n'
            'import os, sys\nfrom pathlib import Path\n'
            f'marker = Path({str(marker)!r})\n'
            'if "load-buffer" in sys.argv and not marker.exists():\n'
            '    marker.touch()\n'
            f'    with open({notify_path!r}, "w") as f: f.write("waiting\\n")\n'
            f'    with open({release_path!r}) as f: f.readline()\n'
            f'os.execv({self.tmux!r},\n'
            f'         [{self.tmux!r}, "-S", {str(self.socket)!r}, *sys.argv[1:]])\n')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        state = json.loads(self.state.read_text())
        state['issues'] = [{'number': 1, 'title': 'Fixture epic', 'state': 'open', 'body': '',
                            'html_url': 'https://github.com/team/app/issues/1',
                            'labels': [{'name': 'factory'}, {'name': 'epic'}]}]
        self.state.write_text(json.dumps(state))
        started = self.watch(repo, '--start', '--existing')
        self.assertEqual(started.returncode, 0, started.stderr)
        try:
            self.assertTrue(select.select([notification], [], [], 10)[0], 'No delivery started')
            self.assertEqual(self.status(repo)['foreman'], 'ready')

            # Act
            stopped = self.watch(repo, '--stop')
            restarted = self.watch(repo, '--start', '--existing')

            # Assert: a previous send's acknowledgement cannot be attributed to a new watcher.
            self.assertEqual(stopped.returncode, 0, stopped.stderr)
            self.assertNotEqual(restarted.returncode, 0)
            self.assertIn('delivery', restarted.stderr)
        finally:
            os.write(release, b'continue\n')
            self.watch(repo, '--stop')
            self.send_and_wait_for_exit(repo, self.status(repo)['target'])
