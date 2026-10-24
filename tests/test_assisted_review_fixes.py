"""Review regressions through public Factory commands and isolated native processes."""
import json
import os
import select
import shlex
import signal
import socket
import subprocess
import sys
import time

from lifecycle_support import LifecycleFixture, pidfd_open, pidfd_send_signal
from test_init import INIT_SETTINGS


class AssistedReviewFixes(LifecycleFixture):
    def test_failed_wait_preserves_live_pi_and_later_observes_its_actual_exit(self):
        repo = self.repo()
        gate = self.workspace / 'fail-wait'
        path, notification = self.notification('wait-watcher.fifo')
        (self.bin / 'tmux').write_text(
            f'#!{sys.executable}\nimport os, sys\nfrom pathlib import Path\n'
            f'gate = Path({str(gate)!r})\n'
            'if gate.exists() and sys.argv[-1] == "#{pane_id}":\n'
            '    gate.unlink()\n'
            '    sys.exit("fixture transient wait query error")\n'
            f'os.execv({self.tmux!r},\n'
            f'         [{self.tmux!r}, "-S", {str(self.socket)!r}, *sys.argv[1:]])\n')
        gh = self.bin / 'gh'
        gh.write_text(gh.read_text().replace(
            "        print(json.dumps([state.get('issues', [])]))",
            f'        with open({path!r}, "w") as f: f.write(str(os.getppid()))\n'
            "        print(json.dumps([state.get('issues', [])]))"))
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        launch = json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[0])
        pi = pidfd_open(launch['started'])
        self.addCleanup(os.close, pi)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        self.assertEqual(self.watch(repo, '--start', '--new-only').returncode, 0)
        self.assertTrue(select.select([notification], [], [], 5)[0])
        watcher = pidfd_open(int(os.read(notification, 100)))
        self.addCleanup(os.close, watcher)

        gate.touch()
        self.assertTrue(select.select([watcher], [], [], 10)[0])
        self.assertFalse(select.select([pi], [], [], 0)[0], 'Live Pi was stopped by query loss')
        state = self.status(repo)
        self.assertEqual(state['foreman'], 'unknown')
        self.assertEqual(state['observation'], 'live')
        self.assertEqual(state['target'], original['target'])
        self.assertIn('exit observation failed', state['warning'])
        self.assertNotEqual(self.watch(repo, '--start', '--new-only').returncode, 0)
        self.send_and_wait_for_exit(repo, original['target'])
        self.assertEqual(self.status(repo)['foreman'], 'stopped')

    def test_unvalidated_worker_handle_cannot_authorize_owner_exit(self):
        repo = self.repo()
        counter = self.workspace / 'capture-count'
        (self.bin / 'tmux').write_text(
            f'#!{sys.executable}\nimport os, subprocess, sys\nfrom pathlib import Path\n'
            f'counter = Path({str(counter)!r})\n'
            f'command = [{self.tmux!r}, "-S", {str(self.socket)!r}, *sys.argv[1:]]\n'
            'if any("#{pane_pid}" in arg for arg in sys.argv):\n'
            '    count = int(counter.read_text()) + 1 if counter.exists() else 1\n'
            '    counter.write_text(str(count))\n'
            '    if count == 2:\n'
            '        result = subprocess.run(command, capture_output=True, text=True)\n'
            '        fields = result.stdout.rstrip("\\n").split("\\t")\n'
            '        fields[4] = str(os.getpid())\n'
            '        print("\\t".join(fields))\n'
            '        sys.exit(result.returncode)\n'
            f'os.execv({self.tmux!r}, command)\n')
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertNotEqual(setup.returncode, 0)
        self.assertIn('could not be validated alive', setup.stderr)
        original = self.status(repo)
        self.assertEqual(original['foreman'], 'unknown')
        self.assertEqual(original['observation'], 'live')
        owner = self.owner_descriptors[original['owner_pid']]
        worker = pidfd_open(original['target']['pane_pid'])
        self.addCleanup(os.close, worker)
        launch = json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[0])
        pi = pidfd_open(launch['started'])
        self.addCleanup(os.close, pi)
        self.assertFalse(select.select([pi], [], [], 0)[0], 'Uncertain capture killed live Pi')
        self.assertNotEqual(self.watch(repo, '--start', '--new-only').returncode, 0)
        killed = subprocess.run([self.tmux, '-S', str(self.socket), 'kill-pane', '-t',
                                 original['target']['pane_id']], env=self.env,
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(killed.returncode, 0, killed.stderr)
        self.assertTrue(select.select([worker], [], [], 10)[0])
        self.assertFalse(select.select([owner], [], [], 1)[0])
        state = self.status(repo)
        self.assertEqual(state['foreman'], 'unknown')
        self.assertEqual(state['observation'], 'live')
        self.assertIn('could not be validated alive', state['warning'])
        self.assertNotEqual(self.foreman(repo).returncode, 0)

    def test_closed_foreman_pane_owner_exits_unknown_before_fixture_cleanup(self):
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        owner = self.owner_descriptors[original['owner_pid']]

        killed = subprocess.run([self.tmux, '-S', str(self.socket), 'kill-pane', '-t',
                                 original['target']['pane_id']], env=self.env,
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(killed.returncode, 0, killed.stderr)
        # This observation must happen before teardown can signal any fixture-owned process.
        self.assertTrue(select.select([owner], [], [], 15)[0], 'Closed-pane owner did not exit')
        state = self.status(repo)
        self.assertEqual(state['observation'], 'saved')
        self.assertEqual(state['foreman'], 'unknown')
        self.assertEqual(state['target'], original['target'])
        self.assertIn('owner.json', state['recovery'])
        self.assertIn(f'--workspace {shlex.quote(str(repo))}', state['recovery'])
        self.assertNotEqual(self.foreman(repo).returncode, 0)

    def test_cancelled_init_allows_bounded_slow_controller_cleanup(self):
        # Controlled interpreter models the controller's eight-second open plus eight-second
        # close allowance. The inherited tracking shim pins its actual owner before notification.
        repo = self.repo()
        notify_path, notification = self.notification('slow-open.fifo')
        shim = self.interpreter.read_text().rsplit('os.execv(', 1)[0]
        self.interpreter.write_text(shim +
            'import json, time\n'
            'if "--check" in sys.argv:\n'
            '    print("Factory AgentShell ready")\n'
            '    sys.exit(0)\n'
            'json.loads(sys.stdin.readline())\n'
            f'with open({notify_path!r}, "w") as notify: notify.write("opening\\n")\n'
            'sys.stdin.read()\n'
            'time.sleep(15.5)\n'
            'print(json.dumps({"kind": "stopped"}), flush=True)\n')
        process = subprocess.Popen([
            sys.executable, '-m', 'forgetful_factory', 'init', '--workspace', str(repo),
            '--repo', str(repo), *INIT_SETTINGS, '--assisted', '--share-pi-profile',
            '--agentshell-python', str(self.interpreter), '--forgetful-instance', 'local',
            '--forgetful-project', '12', '--planning-only', '--grill-me-skill',
            str(self.grill_skill), '--install-role-runtime'], env=self.env,
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertTrue(select.select([notification], [], [], 10)[0])
            self.collect_owner_handles()
            self.assertEqual(len(self.owner_descriptors), 1)
            owner = next(iter(self.owner_descriptors.values()))
            began = time.monotonic()
            process.send_signal(signal.SIGINT)
            stdout, stderr = process.communicate(timeout=40)
            self.assertEqual(process.returncode, 130, stdout + stderr)
            self.assertTrue(select.select([owner], [], [], 1)[0], 'Owner still running')
            self.assertGreater(time.monotonic() - began, 15)
            self.assertLess(time.monotonic() - began, 35)
            state = self.status(repo)
            self.assertEqual(state['foreman'], 'stopped')
            self.assertEqual(state['observation'], 'saved')
        finally:
            if process.poll() is None:
                process.kill()
                process.communicate()

    def test_normal_foreman_exit_reports_saved_stop_without_uncertain_recovery(self):
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        self.send_and_wait_for_exit(repo, original['target'])

        state = self.status(repo)
        self.assertEqual(state['foreman'], 'stopped')
        self.assertEqual(state['observation'], 'saved')
        self.assertEqual(state['target'], original['target'])
        self.assertNotIn('recovery', state)
        self.assertNotIn('uncertain', state.get('warning', ''))
        final = self.run_cli(repo, '--finalize')
        self.assertEqual(final.returncode, 0, final.stderr)
        retry = self.foreman(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])

    def test_legacy_owned_watch_exports_workspace_for_shared_foreman_guidance(self):
        # Arrange
        repo = self.repo()
        configured = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(configured.returncode, 0, configured.stderr)
        notify_path, notification = self.notification('legacy-start.fifo')
        self.env['FAKE_PI_NOTIFY'] = notify_path

        # Act: ordinary watch still owns a new Foreman and its shutdown.
        process = subprocess.Popen([
            sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(repo),
            '--new-only'], env=self.env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertTrue(select.select([notification], [], [], 10)[0], 'Pi did not launch')
            launch = json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[0])
            # Assert
            self.assertEqual(launch['workspace'], str(repo))
            self.assertEqual(shlex.split(launch['command']),
                             [sys.executable, '-m', 'forgetful_factory'])
        finally:
            process.terminate()
            stdout, stderr = process.communicate(timeout=15)
            self.assertEqual(process.returncode, 130, stdout + stderr)

    def test_malformed_controller_output_is_uncertain_with_clean_startup_diagnostic(self):
        # Arrange: an external interpreter passes preflight then emits a nonobject frame.
        repo = self.repo()
        interpreter = self.bin / 'malformed-controller'
        interpreter.write_text(
            f'#!{sys.executable}\nimport sys\n'
            'print("Factory AgentShell ready" if "--check" in sys.argv else "[]")\n')
        interpreter.chmod(0o700)

        # Act
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted',
                              '--agentshell-python', str(interpreter), timeout=20)

        # Assert: no cleanup result was received; do not infer no native launch from that.
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('controller message', failed.stderr)
        status = self.status(repo)
        self.assertEqual(status['foreman'], 'unknown')
        self.assertNotIn('Traceback', (repo / '.factory/runtime/foreman/owner.log').read_text())
        self.assertNotEqual(self.foreman(repo).returncode, 0)

    def test_malformed_owner_reply_is_reported_cleanly_without_changing_saved_identity(self):
        # Arrange: a private fixture endpoint replaces an unavailable owner, never a real service.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        runtime = repo / '.factory/runtime/foreman'
        saved = {'workspace': str(repo), 'run_id': 'fixture', 'foreman': 'starting',
                 'watcher': 'stopped', 'target': None}
        state_file = runtime / 'owner.json'
        state_file.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        state_file.write_text(json.dumps(saved))
        endpoint = runtime / 'control.sock'
        with socket.socket(socket.AF_UNIX) as server:
            server.bind(str(endpoint))
            endpoint.chmod(0o600)
            server.listen()
            server.settimeout(10)
            invalid_target = json.dumps({**saved, 'foreman': 'ready', 'target': {}}).encode()
            for command, payload in ((['watch', '--start', '--new-only'], b'[]\n'),
                                     (['init', '--attach'], invalid_target + b'\n')):
                # Act
                process = subprocess.Popen([
                    sys.executable, '-m', 'forgetful_factory', *command, '--workspace', str(repo)],
                    env=self.env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, text=True)
                try:
                    with server.accept()[0] as channel:
                        channel.settimeout(5)
                        self.assertTrue(channel.recv(10000))
                        channel.sendall(payload)
                    stdout, stderr = process.communicate(timeout=10)
                    # Assert
                    self.assertNotEqual(process.returncode, 0, stdout)
                    self.assertIn('Invalid Foreman control reply', stderr)
                    self.assertNotIn('Traceback', stderr)
                    self.assertEqual(json.loads(state_file.read_text()), saved)
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.communicate()

    def test_malformed_control_requests_reply_cleanly_and_preserve_owner(self):
        # Arrange
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)

        # Act / Assert: invalid JSON, nonobjects, missing fields and an oversized frame.
        for payload in (b'not json\n', b'[]\n', b'null\n', b'{}\n', b'x' * 70000 + b'\n'):
            with self.subTest(payload=payload[:20]), socket.socket(socket.AF_UNIX) as channel:
                channel.settimeout(5)
                channel.connect(str(repo / '.factory/runtime/foreman/control.sock'))
                channel.sendall(payload)
                reply = channel.makefile('rb').readline(10000)
                self.assertTrue(reply, 'Invalid requests must get a bounded diagnostic')
                self.assertIn('error', json.loads(reply))
        self.assertEqual(self.status(repo)['target'], original['target'])
        log = (repo / '.factory/runtime/foreman/owner.log').read_text()
        self.assertNotIn('Traceback', log)
        self.send_and_wait_for_exit(repo, original['target'])

    def test_malformed_borrowed_reply_fails_cleanly_and_releases_workspace_lease(self):
        # Arrange: the public watcher is connected to a controlled external owner endpoint.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS)
        self.assertEqual(setup.returncode, 0, setup.stderr)

        # Act / Assert
        for payload in (b'[]\n', b'{"kind":7}\n', b'not json\n', b'x' * 70000 + b'\n'):
            with self.subTest(payload=payload[:20]):
                parent, child = socket.socketpair()
                process = subprocess.Popen([
                    sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(repo),
                    '--new-only', '--owner-fd', str(child.fileno())], env=self.env,
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    text=True, pass_fds=(child.fileno(),))
                child.close()
                try:
                    parent.settimeout(10)
                    self.assertIn(b'ready', parent.recv(10000))
                    parent.sendall(payload)
                    stdout, stderr = process.communicate(timeout=10)
                    self.assertNotEqual(process.returncode, 0, stdout)
                    self.assertIn('Error:', stderr)
                    self.assertNotIn('Traceback', stderr)
                finally:
                    parent.close()
                    if process.poll() is None:
                        process.kill()
                        process.communicate()
        repair = self.run_cli(repo, '--finalize')
        self.assertEqual(repair.returncode, 0, repair.stderr)

    def test_foreman_runtime_commands_address_workspace_from_role_cwd(self):
        # Arrange
        repo = self.repo()
        missing = self.watch(repo, '--start', '--new-only')
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn(f'foreman --workspace {shlex.quote(str(repo))}', missing.stderr)
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        launch = json.loads((self.workspace / 'pi.jsonl').read_text().splitlines()[0])

        # Act: follow the always-loaded guidance from the actual Foreman working directory.
        self.assertEqual(launch['workspace'], str(repo))
        status = subprocess.run(shlex.split(launch['command']) + [
            'watch', '--status', '--workspace', launch['workspace']], cwd=launch['cwd'],
            env=self.env, capture_output=True, text=True, timeout=10)

        # Assert
        self.assertEqual(status.returncode, 0, status.stderr)
        self.assertEqual(json.loads(status.stdout)['setup'], 'complete')
        self.assertEqual(json.loads(status.stdout)['target'], original['target'])
        agents = (repo / '.factory/agents/foreman/AGENTS.md').read_text()
        self.assertIn('watch --status --workspace "$FACTORY_WORKSPACE"', agents)
        self.assertIn(f'--workspace {shlex.quote(str(repo))}', setup.stdout)
        self.send_and_wait_for_exit(repo, original['target'])

    def notification(self, name):
        path = self.workspace / name
        os.mkfifo(path)
        descriptor = os.open(path, os.O_RDWR | os.O_NONBLOCK)
        self.addCleanup(os.close, descriptor)
        return str(path), descriptor

    def test_unavailable_identity_query_preserves_terminal_and_actual_exit_observation(self):
        # Arrange: fail a single identity query after the watcher is known to be running.
        repo = self.repo()
        gate = self.workspace / 'fail-query'
        watcher_path, watcher_notification = self.notification('identity-watcher.fifo')
        (self.bin / 'tmux').write_text(
            f'#!{sys.executable}\n'
            'import os, sys\nfrom pathlib import Path\n'
            f'gate = Path({str(gate)!r})\n'
            'if gate.exists() and any("#{pane_pid}" in arg for arg in sys.argv):\n'
            '    gate.unlink()\n'
            '    print("fixture identity query unavailable", file=sys.stderr)\n'
            '    sys.exit(1)\n'
            f'os.execv({self.tmux!r},\n'
            f'         [{self.tmux!r}, "-S", {str(self.socket)!r}, *sys.argv[1:]])\n')
        gh = self.bin / 'gh'
        gh.write_text(gh.read_text().replace(
            "        print(json.dumps([state.get('issues', [])]))",
            f'        with open({watcher_path!r}, "w") as f: f.write(str(os.getppid()))\n'
            "        print(json.dumps([state.get('issues', [])]))"))
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        original = self.status(repo)
        started = self.watch(repo, '--start', '--new-only')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertTrue(select.select([watcher_notification], [], [], 5)[0])
        watcher = pidfd_open(int(os.read(watcher_notification, 100)))
        self.addCleanup(os.close, watcher)

        # Act
        gate.touch()
        self.assertTrue(select.select([watcher], [], [], 10)[0], 'Watcher did not stop')

        # Assert: query failure is uncertainty, not native exit or permission to destroy Pi.
        after = self.status(repo)
        self.assertEqual(after['observation'], 'live')
        self.assertEqual(after['foreman'], 'unknown')
        self.assertEqual(after['target'], original['target'])
        self.assertIn('uncertain', after['warning'])
        retry = self.watch(repo, '--start', '--new-only')
        self.assertNotEqual(retry.returncode, 0)
        self.send_and_wait_for_exit(repo, original['target'])
        self.assertEqual(self.status(repo)['foreman'], 'stopped')

    def test_native_send_timeout_stops_watcher_but_preserves_conversation(self):
        # Arrange: block real AgentShell load-buffer past its native five-second deadline.
        repo = self.repo()
        notify_path, notification = self.notification('delivery.fifo')
        release_path, release = self.notification('release.fifo')
        watcher_path, watcher_notification = self.notification('watcher.fifo')
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
        gh = self.bin / 'gh'
        gh.write_text(gh.read_text().replace(
            "        print(json.dumps([state.get('issues', [])]))",
            f'        with open({watcher_path!r}, "w") as f: f.write(str(os.getppid()))\n'
            "        print(json.dumps([state.get('issues', [])]))"))
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        original = self.status(repo)
        state = json.loads(self.state.read_text())
        state['issues'] = [{'number': 1, 'title': 'Fixture epic', 'state': 'open', 'body': '',
                            'html_url': 'https://github.com/team/app/issues/1',
                            'labels': [{'name': 'factory'}, {'name': 'epic'}]}]
        self.state.write_text(json.dumps(state))
        started = self.watch(repo, '--start', '--existing')
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertTrue(select.select([watcher_notification], [], [], 5)[0])
        watcher = pidfd_open(int(os.read(watcher_notification, 100)))
        self.addCleanup(os.close, watcher)
        self.assertTrue(select.select([notification], [], [], 5)[0], 'No delivery started')

        # Act: wait for the actual timeout and watcher cleanup, without releasing transport.
        began = time.monotonic()
        try:
            self.assertTrue(select.select([watcher], [], [], 15)[0], 'Watcher did not stop')
            self.assertGreater(time.monotonic() - began, 4)
            after = self.status(repo)

            # Assert: same live conversation, logged cause and no unsafe automatic retry.
            self.assertEqual(after['foreman'], 'ready')
            self.assertEqual(after['target'], original['target'])
            self.assertIn('uncertain', after['warning'])
            retry = self.watch(repo, '--start', '--existing')
            self.assertNotEqual(retry.returncode, 0)
            self.assertIn('delivery', retry.stderr)
            log = (repo / '.factory/runtime/foreman/owner.log').read_text()
            self.assertIn('send', log.lower())
            self.assertIn('uncertain', log)
            pane = subprocess.run([self.tmux, '-S', str(self.socket), 'display-message', '-p',
                                   '-t', original['target']['pane_id'], '#{pane_pid}'],
                                  env=self.env, capture_output=True, text=True, timeout=5)
            self.assertEqual(pane.returncode, 0, pane.stderr)
            self.assertEqual(int(pane.stdout), original['target']['pane_pid'])
        finally:
            os.write(release, b'continue\n')
        # Releasing transport and finalizing cannot turn a failed send into an acknowledgement.
        final = self.run_cli(repo, '--finalize', '--delegated-work-stopped')
        self.assertEqual(final.returncode, 0, final.stderr)
        retry = self.watch(repo, '--start', '--existing')
        self.assertNotEqual(retry.returncode, 0)
        self.assertIn('Inspect Foreman for the possible message', retry.stderr)
        self.assertIn('deliberately exit Foreman', retry.stderr)
        self.assertIn(f'foreman --workspace {shlex.quote(str(repo))}', retry.stderr)
        self.assertNotIn('after it resolves', retry.stderr)
        stopped = self.watch(repo, '--stop')
        self.assertEqual(stopped.returncode, 0, stopped.stderr)
        self.assertIn('deliberately exit Foreman', json.loads(stopped.stdout)['warning'])
        self.assertNotIn('in progress', self.status(repo)['warning'])
        self.send_and_wait_for_exit(repo, original['target'])

    def test_bad_interpreter_does_not_poison_setup_and_retry_succeeds(self):
        # Arrange / Act: the selected executable cannot run the controller, let alone Pi.
        repo = self.repo()
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted',
                              '--agentshell-python', '/bin/false', timeout=20)

        # Assert: no launch intent is saved for a failed preflight.
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('interpreter', failed.stderr)
        self.assertFalse((repo / '.factory/runtime/foreman/owner.json').exists())
        self.assertFalse((self.workspace / 'pi.jsonl').exists())
        final = self.run_cli(repo, '--finalize')
        self.assertEqual(final.returncode, 0, final.stderr)
        retry = self.foreman(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])

    def test_readiness_timeout_with_confirmed_cleanup_allows_retry(self):
        # Arrange: a real owned terminal opens, but fake Pi never sends readiness.
        repo = self.repo()
        self.env['FAKE_PI_NO_READY'] = '1'

        # Act
        failed = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=50)

        # Assert: successful owned cleanup is distinct from a lost controller.
        self.assertNotEqual(failed.returncode, 0)
        state = self.status(repo)
        self.assertEqual(state['foreman'], 'stopped')
        self.assertEqual(state['observation'], 'saved')
        self.env.pop('FAKE_PI_NO_READY')
        final = self.run_cli(repo, '--finalize')
        self.assertEqual(final.returncode, 0, final.stderr)
        retry = self.foreman(repo)
        self.assertEqual(retry.returncode, 0, retry.stderr)
        self.send_and_wait_for_exit(repo, self.status(repo)['target'])

    def test_actual_owner_loss_reports_saved_identity_without_authorizing_replacement(self):
        # Arrange: retain a pidfd for the actual live test owner, not a PID from saved state.
        repo = self.repo()
        setup = self.run_cli(repo, '--repo', '.', *INIT_SETTINGS, '--assisted', timeout=20)
        self.assertEqual(setup.returncode, 0, setup.stderr)
        original = self.status(repo)
        descriptor = self.owner_descriptors[original['owner_pid']]

        # Act: lose the owner before it can report controller cleanup.
        pidfd_send_signal(descriptor, signal.SIGKILL)
        self.assertTrue(select.select([descriptor], [], [], 5)[0], 'Test owner did not exit')
        status = self.watch(repo, '--status')
        retry = self.foreman(repo)

        # Assert: readable offline status, exact saved identity, and no unsafe replacement.
        self.assertEqual(status.returncode, 0, status.stderr)
        state = json.loads(status.stdout)
        self.assertEqual(state['foreman'], 'unknown')
        self.assertEqual(state['observation'], 'saved')
        self.assertEqual(state['target'], original['target'])
        self.assertIn('owner.json', state['recovery'])
        self.assertIn('uncertain', state['warning'])
        self.assertNotEqual(retry.returncode, 0)
