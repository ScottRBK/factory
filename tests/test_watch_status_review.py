"""Approved Opus findings exercised through public CLI and external observation boundaries."""
import json
import os
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

from test_watch import WatchFixture
from test_watch_status import OBSERVATION_SERVER, read_status

TARGET = {'socket_path': '/fixture-only', 'pane_id': '%1', 'server_pid': 10,
          'server_started': 11, 'pane_pid': 12}


def save_owner(fixture, foreman, watcher):
    path = fixture.workspace / '.factory/runtime/foreman/owner.json'
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_text(json.dumps({'workspace': str(fixture.workspace), 'run_id': 'saved-owner',
                               'foreman': foreman, 'watcher': watcher, 'target': TARGET,
                               'owner_pid': 4242}))
    path.chmod(0o600)
    return path


def finish_plain(fixture):
    process = fixture.start('--new-only')
    fixture.wait_until(process, lambda: any(e['kind'] == 'ready' for e in fixture.events()))
    fixture.stop(process)
    return fixture.workspace / '.factory/runtime/watch/status.json'


class NonliveStatusEvidenceTests(WatchFixture):
    def test_saved_plain_preserves_unreachable_managed_identity_and_recovery(self):
        # Arrange: both records are historical and the managed owner's transport is unavailable.
        plain = finish_plain(self)
        plain_before = plain.read_bytes()
        owner = save_owner(self, 'ready', 'running')
        owner_before = owner.read_bytes()
        events = self.events()

        # Act
        observed = read_status(self)

        # Assert: preserve managed reconciliation evidence without claiming a live session.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(observed['recorded_foreman'], 'ready')
        self.assertEqual(observed['recorded_watcher'], 'running')
        self.assertEqual(observed['target'], TARGET)
        self.assertEqual(observed['owner_pid'], 4242)
        self.assertTrue(observed['warning'])
        self.assertTrue(observed['recovery'])
        self.assertNotEqual(observed['observation'], 'live')
        self.assertEqual(observed['plain_watch']['source'], 'plain_watch')
        self.assertEqual(observed['plain_watch']['observation'], 'saved')
        self.assertEqual(observed['plain_watch']['recorded_phase'], 'stopped')
        self.assertEqual(plain.read_bytes(), plain_before)
        self.assertEqual(owner.read_bytes(), owner_before)
        self.assertEqual(self.events(), events)

    def test_saved_plain_and_stopped_owner_preserve_both_without_claiming_current_stop(self):
        # Arrange: neither stopped record observes what is currently running in the workspace.
        plain = finish_plain(self)
        owner = save_owner(self, 'stopped', 'stopped')
        before = {p: p.read_bytes() for p in (plain, owner)}

        # Act
        observed = read_status(self)

        # Assert: mixed historical records do not establish current presence or absence.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['recorded_foreman'], 'stopped')
        self.assertEqual(observed['recorded_watcher'], 'stopped')
        self.assertEqual(observed['target'], TARGET)
        self.assertEqual(observed['owner_pid'], 4242)
        self.assertEqual(observed['plain_watch']['recorded_phase'], 'stopped')
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_saved_plain_does_not_hide_malformed_managed_owner_warning(self):
        # Arrange: the plain record is valid historical data, but managed identity is unreadable.
        plain = finish_plain(self)
        owner = save_owner(self, 'ready', 'running')
        owner.write_text('{invalid')
        before = {p: p.read_bytes() for p in (plain, owner)}

        # Act
        observed = read_status(self)

        # Assert: the managed parse warning stays visible beside the separate plain evidence.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertTrue(observed['warning'])
        self.assertEqual(observed['plain_watch']['recorded_phase'], 'stopped')
        self.assertEqual({p: p.read_bytes() for p in before}, before)

    def test_timed_out_plain_and_stopped_owner_cannot_become_current_foreman_stop(self):
        # Arrange: the advertised plain process is alive but its observation transport stalls.
        path = self.workspace / '.factory/runtime/watch/status.json'
        server = subprocess.Popen(
            [sys.executable, '-c', OBSERVATION_SERVER, str(self.workspace), 'timeout'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.cleanup_process, server)
        self.wait_until(server, path.exists)
        owner = save_owner(self, 'stopped', 'stopped')
        before = {p: p.read_bytes() for p in (path, owner)}

        # Act
        observed = read_status(self)

        # Assert: blindly preferring an old stopped owner would lose plain uncertainty.
        self.assertIsNone(server.poll())
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['recorded_foreman'], 'stopped')
        self.assertEqual(observed['plain_watch']['recorded_foreman'], 'ready')
        self.assertEqual(observed['plain_watch']['observation'], 'saved')
        self.assertTrue(observed['plain_watch']['warning'])
        self.assertEqual({p: p.read_bytes() for p in before}, before)


class PlainWatchAdmissionTests(WatchFixture):
    def test_invalid_interval_preserves_prior_cleanup_uncertainty(self):
        # Arrange: an earlier invocation left meaningful uncertain cleanup evidence.
        self.env['WATCH_CLOSE_FAIL'] = '1'
        path = finish_plain(self)
        del self.env['WATCH_CLOSE_FAIL']
        self.assertEqual(read_status(self)['recorded_evidence'], 'cleanup_uncertain')
        before = path.read_bytes()
        events = self.events()

        # Act
        rejected = self.start('--new-only', '--interval', '0')
        _, errors = rejected.communicate(timeout=5)

        # Assert: rejected admission must not replace an earlier invocation's evidence.
        self.assertEqual(rejected.returncode, 1, errors)
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.events(), events)

    def test_unconfigured_workspace_is_not_created_by_a_refused_watch(self):
        # Arrange: the requested workspace has no Factory configuration or runtime data.
        with tempfile.TemporaryDirectory(prefix='factory-unconfigured-', dir='/tmp') as temporary:
            workspace = Path(temporary)

            # Act
            rejected = subprocess.run(
                [sys.executable, '-m', 'forgetful_factory', 'watch', '--new-only',
                 '--workspace', str(workspace)], cwd=workspace, env=self.env,
                capture_output=True, text=True, timeout=5)

            # Assert: configuration refusal leaves the directory byte-for-byte empty.
            self.assertEqual(rejected.returncode, 1, rejected.stderr)
            self.assertEqual(list(workspace.iterdir()), [])
            self.assertEqual(self.events(), [])

    def test_uncertain_owner_refusal_does_not_create_plain_discovery(self):
        # Arrange: this workspace has an uncertain managed owner but no plain invocation.
        owner = save_owner(self, 'unknown', 'stopped')
        before = owner.read_bytes()
        path = self.workspace / '.factory/runtime/watch'

        # Act
        rejected = self.start('--new-only')
        _, errors = rejected.communicate(timeout=5)

        # Assert: rejected watch adds neither an observer nor a new ownership claim.
        self.assertEqual(rejected.returncode, 1, errors)
        self.assertFalse(path.exists())
        self.assertEqual(owner.read_bytes(), before)
        self.assertEqual(self.events(), [])

    def test_uncertain_owner_refusal_preserves_prior_plain_discovery(self):
        # Arrange: plain history and managed uncertainty coexist before this refusal.
        plain = finish_plain(self)
        owner = save_owner(self, 'unknown', 'stopped')
        before = {p: p.read_bytes() for p in (plain, owner)}
        events = self.events()

        # Act
        rejected = self.start('--new-only')
        _, errors = rejected.communicate(timeout=5)

        # Assert: refusal cannot advertise a new dead plain run over the recorded one.
        self.assertEqual(rejected.returncode, 1, errors)
        self.assertEqual({p: p.read_bytes() for p in before}, before)
        self.assertEqual(self.events(), events)


class DeepObservationInputTests(WatchFixture):
    def test_maximum_size_deep_discovery_is_reported_as_unknown_without_traceback(self):
        # Arrange: malformed JSON is within the discovery byte limit but exceeds parser depth.
        path = self.workspace / '.factory/runtime/watch/status.json'
        path.parent.mkdir(parents=True, mode=0o700)
        path.write_bytes(b'[' * 16384)
        path.chmod(0o600)
        before = path.read_bytes()

        # Act
        observed = read_status(self)

        # Assert: untrusted JSON depth is a controlled unavailable observation.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.events(), [])

    def test_maximum_size_deep_request_cannot_kill_the_live_observer(self):
        # Arrange: only the external socket boundary is used to send the hostile request.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        original = read_status(self)

        # Act: EOF from this connection establishes that its malformed frame was processed.
        with socket.socket(socket.AF_UNIX) as connection:
            connection.settimeout(2)
            connection.connect(f'\0factory-watch-{os.getuid()}-{original["run_id"]}')
            connection.sendall(b'[' * 16383 + b'\n')
            connection.shutdown(socket.SHUT_WR)
            self.assertEqual(connection.recv(1), b'')
        observed = read_status(self)
        alive = process.poll() is None
        code, _, errors = self.stop(process)

        # Assert: a later ordinary caller still receives a live lifecycle observation.
        self.assertTrue(alive)
        self.assertEqual(code, 130, errors)
        self.assertEqual(observed['observation'], 'live')
        self.assertEqual(observed['process'], 'present')
        self.assertEqual(observed['run_id'], original['run_id'])

    def test_maximum_size_deep_discovery_cannot_replace_interrupt_exit_status(self):
        # Arrange: damage only this test's discovery after its owned session is ready.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        path = self.workspace / '.factory/runtime/watch/status.json'
        path.write_bytes(b'[' * 16384)

        # Act
        code, _, errors = self.stop(process)

        # Assert: invalid observation data cannot change cancellation or owned cleanup.
        self.assertEqual(code, 130, errors)
        self.assertEqual(path.read_bytes(), b'[' * 16384)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])


class ObservationPublicationTests(WatchFixture):
    def test_abrupt_loss_retains_last_ready_phase_as_historical_evidence(self):
        # Arrange: readiness is acknowledged before this fixture's owned process is killed.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        live = read_status(self)
        self.assertEqual(live['phase'], 'watching')

        # Act: use the fixture's original Popen handle, never a PID from saved metadata.
        process.kill()
        process.communicate(timeout=5)
        observed = read_status(self)

        # Assert: current state is unknown but the last persisted readiness is not erased.
        self.assertEqual(observed['observation'], 'saved')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['recorded_phase'], 'watching')
        self.assertEqual(observed['recorded_foreman'], 'ready')
        self.assertEqual(observed['recorded_evidence'], 'session_ready')
        self.assertEqual(observed['run_id'], live['run_id'])

    def test_native_preflight_failure_records_exit_before_session_start(self):
        # Arrange: admission succeeds but an external native prerequisite refuses startup.
        self.env['WATCH_GH_HELP_EXIT'] = '1'

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)
        observed = read_status(self)

        # Assert: no terminal started, and historical startup is no longer reported in progress.
        self.assertEqual(process.returncode, 1, errors)
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['recorded_phase'], 'stopped')
        self.assertEqual(observed['recorded_watcher'], 'stopped')
        self.assertEqual(observed['recorded_evidence'], 'exited_before_session')
        self.assertEqual(self.events(), [])

    def test_same_run_history_update_during_query_does_not_invalidate_live_identity(self):
        # Arrange: the external responder publishes a newer phase before returning its snapshot.
        path = self.workspace / '.factory/runtime/watch/status.json'
        server = subprocess.Popen(
            [sys.executable, '-c', OBSERVATION_SERVER, str(self.workspace), 'updated_history'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.cleanup_process, server)
        self.wait_until(server, path.exists)

        # Act
        observed = read_status(self)

        # Assert: a same-identity lifecycle update is distinct from discovery replacement.
        self.assertEqual(observed['observation'], 'live')
        self.assertEqual(observed['process'], 'present')
        self.assertEqual(observed['phase'], 'watching')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(json.loads(path.read_text())['phase'], 'stopping')

    def test_history_publication_permission_failure_preserves_interrupt_exit(self):
        # Arrange: make only the fixture's observation directory unwritable after readiness.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        directory = self.workspace / '.factory/runtime/watch'
        self.addCleanup(directory.chmod, 0o700)
        directory.chmod(0o500)

        # Act
        try:
            code, _, errors = self.stop(process)
        finally:
            directory.chmod(0o700)

        # Assert: optional history failure cannot change cancellation or owned cleanup.
        self.assertEqual(code, 130, errors)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])

    def test_history_publication_permission_failure_preserves_native_failure_diagnostic(self):
        # Arrange: gate an external native exit until the observation directory is unwritable.
        shell = self.workspace / 'external/agent_shell/shell.py'
        gate = self.workspace / 'exit-native'
        shell.write_text(shell.read_text().replace(
            '    async def wait(self):\n',
            '    async def wait(self):\n'
            '        from pathlib import Path\n'
            f'        while not Path({str(gate)!r}).exists(): await asyncio.sleep(0.01)\n'
            '        return 7\n'))
        self.addCleanup(gate.touch)
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        directory = self.workspace / '.factory/runtime/watch'
        self.addCleanup(directory.chmod, 0o700)
        directory.chmod(0o500)

        # Act
        try:
            gate.touch()
            _, errors = process.communicate(timeout=10)
        finally:
            directory.chmod(0o700)

        # Assert: preserve the underlying native exit result instead of a publication error.
        self.assertEqual(process.returncode, 1)
        self.assertRegex(errors, r'\bstatus\s+7\b')
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])


class ObservationPeerIdentityTests(WatchFixture):
    def test_different_advertised_pid_cannot_establish_a_live_observation(self):
        # Arrange: a real external listener advertises the identity of a different process.
        path = self.workspace / '.factory/runtime/watch/status.json'
        server = subprocess.Popen(
            [sys.executable, '-c', OBSERVATION_SERVER, str(self.workspace), 'wrong_peer'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.cleanup_process, server)
        self.wait_until(server, path.exists)
        before = path.read_bytes()

        # Act
        observed = read_status(self)

        # Assert: a matching run ID and reply body cannot replace kernel peer-PID evidence.
        self.assertEqual(observed['observation'], 'saved')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(self.events(), [])


class ApprovedSavedStopPolicyTests(WatchFixture):
    def test_clean_saved_owner_stop_is_unknown_current_state_without_invented_recovery(self):
        # Arrange: only a clean stopped managed record exists, with no live control endpoint.
        owner = save_owner(self, 'stopped', 'stopped')
        before = owner.read_bytes()

        # Act
        observed = read_status(self)

        # Assert: keep clean stop history without pretending it observes current liveness.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['recorded_foreman'], 'stopped')
        self.assertEqual(observed['recorded_watcher'], 'stopped')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['observation'], 'saved')
        self.assertEqual(observed['target'], TARGET)
        self.assertEqual(observed['health'], 'not_checked')
        self.assertNotIn('recovery', observed)
        self.assertNotIn('warning', observed)
        self.assertEqual(owner.read_bytes(), before)
        self.assertEqual(self.events(), [])


class OptionalObserverStartupTests(WatchFixture):
    def test_nonprivate_observation_directory_warns_and_preserves_owned_watch_lifetime(self):
        # Arrange: observation is unavailable, but configuration and actual watch admission pass.
        directory = self.workspace / '.factory/runtime/watch'
        directory.mkdir(parents=True, mode=0o700)
        directory.chmod(0o755)
        self.addCleanup(directory.chmod, 0o700)

        # Act: a real owned watcher must still reach readiness and close on interruption.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        observed = read_status(self)
        code, _, errors = self.stop(process)

        # Assert: distinguish warning severity from a failed watcher or falsely live observation.
        self.assertEqual(code, 130, errors)
        self.assertRegex(errors, r'(?m)^Warning:.*observation')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertNotEqual(observed['observation'], 'live')
        self.assertFalse((directory / 'status.json').exists())
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])

    def test_partial_listener_startup_failure_closes_resources_and_keeps_discovery_unknown(self):
        # Arrange: bind/listen can succeed, but initial discovery publication cannot write.
        directory = self.workspace / '.factory/runtime/watch'
        directory.mkdir(parents=True, mode=0o700)
        directory.chmod(0o500)
        self.addCleanup(directory.chmod, 0o700)
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))

        # Act: inspect only the owned fixture process's external file-descriptor boundary.
        sockets = []
        for descriptor in Path(f'/proc/{process.pid}/fd').iterdir():
            try:
                target = os.readlink(descriptor)
            except FileNotFoundError:
                continue
            if target.startswith('socket:'):
                sockets.append(target)
        observed = read_status(self)
        try:
            code, _, errors = self.stop(process)
        finally:
            directory.chmod(0o700)

        # Assert: no failed observer listener remains owned by this running/closing watch.
        self.assertEqual(sockets, [])
        self.assertEqual(code, 130, errors)
        self.assertRegex(errors, r'(?m)^Warning:.*observation')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertFalse((directory / 'status.json').exists())
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])

    def test_optional_observer_failure_does_not_replace_actual_native_preflight_failure(self):
        # Arrange: observation refusal and an independent external native failure coexist.
        directory = self.workspace / '.factory/runtime/watch'
        directory.mkdir(parents=True, mode=0o700)
        directory.chmod(0o755)
        self.addCleanup(directory.chmod, 0o700)
        self.env['WATCH_GH_HELP_EXIT'] = '1'

        # Act
        process = self.start('--new-only')
        _, errors = process.communicate(timeout=5)

        # Assert: native preflight still executes and its failure determines the command result.
        self.assertEqual(process.returncode, 1, errors)
        self.assertRegex(errors, r'(?m)^Warning:.*observation')
        self.assertRegex(errors, r'(?m)^Error:')
        self.assertEqual(json.loads(self.state_path.read_text())['help_calls'], [['api', '--help']])
        self.assertEqual(self.events(), [])

    def test_fallback_does_not_replace_previous_discovery_with_a_dead_or_false_live_run(self):
        # Arrange: previous valid history is retained when this observer cannot initialize.
        path = finish_plain(self)
        before = path.read_bytes()
        directory = path.parent
        directory.chmod(0o755)
        self.addCleanup(directory.chmod, 0o700)
        count = sum(e['kind'] == 'ready' for e in self.events())

        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: sum(e['kind'] == 'ready' for e in self.events()) > count)
        observed = read_status(self)
        code, _, errors = self.stop(process)

        # Assert: fallback runs normal ownership while keeping old evidence explicitly saved.
        self.assertEqual(code, 130, errors)
        self.assertRegex(errors, r'(?m)^Warning:.*observation')
        self.assertEqual(observed['observation'], 'saved')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(sum(e['kind'] == 'launch' for e in self.events()), 2)
        self.assertEqual(sum(e['kind'] == 'close' for e in self.events()), 2)
