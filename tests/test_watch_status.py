"""Lifecycle observations through public watch commands; no native tmux or model calls."""
import json
import os
import signal
import subprocess
import sys
import time

from test_watch import INIT_GH, WatchFixture

OBSERVATION_SERVER = r'''
import json, os, socket, sys, time, uuid
from pathlib import Path
workspace, scenario = Path(sys.argv[1]), sys.argv[2]
run_id = uuid.uuid4().hex
record = dict(workspace=str(workspace), run_id=run_id, watcher_pid=os.getpid(),
              process_started='fixture-process', phase='watching', foreman='ready',
              watcher='running', target=None, evidence='session_ready')
if scenario == 'wrong_peer':
    record['watcher_pid'] = os.getpid() + 1
path = workspace / '.factory/runtime/watch/status.json'
path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
with socket.socket(socket.AF_UNIX) as listener:
    listener.bind(f'\0factory-watch-{os.getuid()}-{run_id}')
    listener.listen()
    path.write_text(json.dumps(record))
    path.chmod(0o600)
    with listener.accept()[0] as connection:
        connection.recv(4096)
        if scenario == 'timeout':
            time.sleep(10)
        elif scenario == 'oversized':
            connection.sendall(b'{' + b' ' * 20000)
        else:
            if scenario == 'wrong_run':
                record['run_id'] = '0' * 32
            elif scenario == 'changed_process':
                record['process_started'] = 'reused-process'
            elif scenario == 'changed_discovery':
                path.write_text(json.dumps({**record, 'run_id': '0' * 32}))
            elif scenario == 'updated_history':
                path.write_text(json.dumps({**record, 'phase': 'stopping',
                                            'watcher': 'stopping'}))
            connection.sendall((json.dumps(record) + '\n').encode())
    time.sleep(10)
'''


def read_status(fixture):
    process = fixture.start('--status')
    output, errors = process.communicate(timeout=5)
    fixture.assertEqual(process.returncode, 0, errors)
    return json.loads(output)


class WatchStatusTests(WatchFixture):
    def test_plain_watch_is_observed_while_running_without_changing_its_lifetime(self):
        # Arrange: a foreground watch owns one ready external Pi fixture.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        configuration = self.workspace / '.factory/factory.toml'
        before = configuration.read_bytes()

        # Act: another caller observes the same running invocation repeatedly.
        first = read_status(self)
        second = read_status(self)

        # Assert: observing never launches, delivers, stops or changes configuration.
        self.assertEqual(first['watcher'], 'running')
        self.assertEqual(first['foreman'], 'ready')
        self.assertEqual(first['source'], 'plain_watch')
        self.assertEqual(first['observation'], 'live')
        self.assertEqual(first['process'], 'present')
        self.assertEqual(first['phase'], 'watching')
        self.assertEqual(first['health'], 'not_checked')
        self.assertEqual(first['run_id'], second['run_id'])
        self.assertIsNone(process.poll())
        self.assertEqual(configuration.read_bytes(), before)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready'])
        self.stop(process)

    def test_plain_startup_and_exit_cannot_be_masked_by_a_previous_managed_stop(self):
        # Arrange: an earlier persistent owner stopped, and this invocation is not ready yet.
        owner = self.workspace / '.factory/runtime/foreman/owner.json'
        owner.parent.mkdir(parents=True, mode=0o700)
        owner.write_text(json.dumps(dict(workspace=str(self.workspace), run_id='old-owner',
                                        foreman='stopped', watcher='stopped', target=None)))
        before = owner.read_bytes()
        gate = self.workspace / 'ready-gate'
        self.env['WATCH_READY_GATE'] = str(gate)
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'launch' for e in self.events()))

        # Act / Assert: responsive startup is not Foreman readiness or functional health.
        starting = read_status(self)
        self.assertEqual(starting['source'], 'plain_watch')
        self.assertEqual(starting['process'], 'present')
        self.assertEqual(starting['phase'], 'starting')
        self.assertEqual(starting['foreman'], 'starting')
        self.assertEqual(starting['watcher'], 'starting')
        self.assertEqual(starting['health'], 'not_checked')
        gate.touch()
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        self.assertEqual(read_status(self)['foreman'], 'ready')
        self.stop(process)

        # Historical cleanup evidence must not become a current process observation.
        stopped = read_status(self)
        self.assertEqual(stopped['source'], 'combined')
        self.assertEqual(stopped['observation'], 'saved')
        self.assertEqual(stopped['process'], 'unknown')
        self.assertEqual(stopped['watcher'], 'unknown')
        self.assertEqual(stopped['recorded_foreman'], 'stopped')
        self.assertEqual(stopped['plain_watch']['recorded_phase'], 'stopped')
        self.assertEqual(owner.read_bytes(), before)

    def test_missing_discovery_does_not_claim_absence_even_with_a_setup_lease(self):
        # Arrange: hold a real public init inside its external native validation command.
        command = self.bin / 'forgetful'
        (self.bin / 'gh').write_text(INIT_GH)
        self.env['GH_STATE'] = str(self.workspace / 'init-gh.json')
        gate = self.workspace / 'release-setup'
        marker = self.workspace / 'setup-checking'
        command.write_text(command.read_text().replace(
            'import sys', 'import sys\nimport time\nfrom pathlib import Path\n'
            f'Path({str(marker)!r}).touch()\n'
            f'while not Path({str(gate)!r}).exists(): time.sleep(0.01)', 1))
        setup = subprocess.Popen(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--finalize',
             '--workspace', str(self.workspace)], env=self.env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(self.cleanup_process, setup)
        self.wait_until(setup, marker.exists)

        # Act
        before = {p: p.read_bytes() for p in (self.workspace / '.factory').rglob('*')
                  if p.is_file()}
        observed = read_status(self)
        gate.touch()
        output, errors = setup.communicate(timeout=5)

        # Assert: lock ownership supplies no watcher or Foreman presence evidence.
        self.assertEqual(setup.returncode, 0, output + errors)
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['source'], 'none')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertFalse((self.workspace / '.factory/runtime/watch').exists())
        self.assertEqual(self.events(), [])
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)

    def test_malformed_and_stale_discovery_remain_unknown_and_are_preserved(self):
        # Arrange: discovery is observation data, including potentially broken old records.
        path = self.workspace / '.factory/runtime/watch/status.json'
        path.parent.mkdir(parents=True, mode=0o700)
        stale = dict(workspace=str(self.workspace), run_id='a' * 32, watcher_pid=os.getpid(),
                     process_started='old-process', foreman='ready', watcher='running')
        for content in ('{invalid', '[]', ' ' * 17000, '[' * 1500 + ']' * 1500,
                        json.dumps(stale)):
            with self.subTest(content=content[:30]):
                path.write_text(content)
                path.chmod(0o600)

                # Act
                observed = read_status(self)

                # Assert
                self.assertEqual(observed['source'], 'plain_watch')
                self.assertEqual(observed['watcher'], 'unknown')
                self.assertEqual(observed['foreman'], 'unknown')
                self.assertEqual(observed['process'], 'unknown')
                self.assertEqual(observed['health'], 'not_checked')
                self.assertEqual(path.read_text(), content)
                self.assertEqual(self.events(), [])

    def test_transport_failure_and_identity_changes_never_establish_presence(self):
        for scenario in ('timeout', 'oversized', 'wrong_run', 'changed_process',
                         'changed_discovery'):
            with self.subTest(scenario=scenario):
                # Arrange: a controlled external endpoint advertises a plausible live record.
                path = self.workspace / '.factory/runtime/watch/status.json'
                path.unlink(missing_ok=True)
                server = subprocess.Popen(
                    [sys.executable, '-c', OBSERVATION_SERVER, str(self.workspace), scenario],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                self.addCleanup(self.cleanup_process, server)
                self.wait_until(server, path.exists)

                # Act
                started = time.monotonic()
                observed = read_status(self)
                elapsed = time.monotonic() - started
                self.cleanup_process(server)

                # Assert: timeout, stale replies and changing discovery all retain uncertainty.
                self.assertLess(elapsed, 2)
                self.assertEqual(observed['watcher'], 'unknown')
                self.assertEqual(observed['foreman'], 'unknown')
                self.assertEqual(observed['process'], 'unknown')
                self.assertEqual(observed['health'], 'not_checked')
                self.assertEqual(self.events(), [])

    def test_discovery_replacement_is_preserved_during_status_and_original_exit(self):
        # Arrange: only this fixture's watcher and files can be affected.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        path = self.workspace / '.factory/runtime/watch/status.json'
        replacement = json.loads(path.read_text())
        replacement['run_id'] = 'b' * 32
        path.write_text(json.dumps(replacement))
        before = path.read_bytes()

        # Act
        observed = read_status(self)
        self.stop(process)

        # Assert: the original invocation cannot overwrite another run's discovery on exit.
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(path.read_bytes(), before)

    def test_live_plain_status_does_not_consult_broken_managed_owner_records(self):
        # Arrange: an unrelated damaged/stale managed record appears after plain watch is ready.
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        owner = self.workspace / '.factory/runtime/foreman/owner.json'
        owner.parent.mkdir(parents=True, mode=0o700)

        # Act / Assert: live plain evidence wins without changing either record or lifetime.
        for content in ('{invalid', json.dumps(dict(workspace=str(self.workspace),
                             run_id='stale-owner', foreman='unknown', watcher='running'))):
            with self.subTest(content=content):
                owner.write_text(content)
                observed = read_status(self)
                self.assertEqual(observed['source'], 'plain_watch')
                self.assertEqual(observed['process'], 'present')
                self.assertEqual(observed['watcher'], 'running')
                self.assertEqual(owner.read_text(), content)
                self.assertIsNone(process.poll())
        self.stop(process)

    def test_interrupted_startup_never_turns_into_foreman_readiness_or_health(self):
        # Arrange: the external session exists but has not emitted its ready event.
        self.env['WATCH_NO_READY'] = '1'
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'launch' for e in self.events()))

        # Act
        before = read_status(self)
        code, _, errors = self.stop(process)
        after = read_status(self)

        # Assert: normal owned cancellation still closes the external session.
        self.assertEqual(code, 130, errors)
        self.assertEqual(before['foreman'], 'starting')
        self.assertEqual(before['phase'], 'starting')
        self.assertEqual(after['foreman'], 'unknown')
        self.assertEqual(after['process'], 'unknown')
        self.assertEqual(after['recorded_foreman'], 'unknown')
        self.assertEqual(after['recorded_phase'], 'stopped')
        self.assertEqual(after['health'], 'not_checked')
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'close'])

    def test_cleanup_failure_is_preserved_as_uncertain_foreman_evidence(self):
        # Arrange: owned session cleanup reports failure at the external AgentShell boundary.
        self.env['WATCH_CLOSE_FAIL'] = '1'
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))

        # Act
        self.stop(process)
        observed = read_status(self)

        # Assert: an ended watcher is not proof that its Foreman was successfully closed.
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['recorded_foreman'], 'unknown')
        self.assertEqual(observed['recorded_evidence'], 'cleanup_uncertain')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')

    def test_status_during_owned_cleanup_stays_observational_and_stop_is_managed_only(self):
        # Arrange: gate only the external session close after cleanup has begun.
        shell = self.workspace / 'external/agent_shell/shell.py'
        gate = self.workspace / 'finish-close'
        marker = self.workspace / 'closing'
        shell.write_text(shell.read_text().replace(
            "        record('close')", "        record('close')\n"
            "        from pathlib import Path\n"
            f"        Path({str(marker)!r}).touch()\n"
            f"        while not Path({str(gate)!r}).exists(): await asyncio.sleep(0.01)"))
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        refused = self.start('--stop')
        _, errors = refused.communicate(timeout=5)
        self.assertNotEqual(refused.returncode, 0, errors)
        self.assertIsNone(process.poll())
        process.send_signal(signal.SIGTERM)
        self.wait_until(process, marker.exists)

        # Act
        observed = read_status(self)
        repeated = read_status(self)
        gate.touch()
        _, errors = process.communicate(timeout=10)
        saved = read_status(self)

        # Assert: a live cleanup observation and historical final snapshot stay distinct.
        self.assertEqual(process.returncode, 130, errors)
        self.assertEqual(observed['process'], 'present')
        self.assertEqual(observed['phase'], 'stopping')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(observed['run_id'], repeated['run_id'])
        self.assertEqual(saved['observation'], 'saved')
        self.assertEqual(saved['process'], 'unknown')
        self.assertEqual(saved['recorded_phase'], 'stopped')
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])

    def test_saved_running_watcher_is_historical_even_when_foreman_recorded_stopped(self):
        # Arrange: model the snapshot left between Foreman exit and watcher cleanup.
        path = self.workspace / '.factory/runtime/foreman/owner.json'
        path.parent.mkdir(parents=True, mode=0o700)
        path.write_text(json.dumps(dict(workspace=str(self.workspace), run_id='old-owner',
                                       foreman='stopped', watcher='running', target=None)))
        before = path.read_bytes()

        # Act
        observed = read_status(self)

        # Assert: even a known historical Foreman stop cannot establish current watcher state.
        self.assertEqual(observed['source'], 'managed_owner')
        self.assertEqual(observed['observation'], 'saved')
        self.assertEqual(observed['process'], 'unknown')
        self.assertEqual(observed['phase'], 'unknown')
        self.assertEqual(observed['watcher'], 'unknown')
        self.assertEqual(observed['recorded_foreman'], 'stopped')
        self.assertEqual(observed['foreman'], 'unknown')
        self.assertEqual(observed['recorded_watcher'], 'running')
        self.assertEqual(observed['health'], 'not_checked')
        self.assertEqual(path.read_bytes(), before)


TARGET_DOUBLE = '''
import os
from dataclasses import dataclass

@dataclass
class TmuxTarget:
    socket_path: str
    pane_id: str
    server_pid: int
    server_started: int
    pane_pid: int

    @classmethod
    async def capture(cls, pane_id, socket_path):
        return cls(socket_path, pane_id, os.getpid(), 1, os.getpid())
'''


class ManagedWatchStatusTests(WatchFixture):
    def launch_foreman(self):
        # External AgentShell double supplies a stable target and a gate for real owned cleanup.
        package = self.workspace / 'external/agent_shell'
        target = package / 'tmux.py'
        target.write_text(target.read_text() + TARGET_DOUBLE)
        shell = package / 'shell.py'
        shell.write_text(shell.read_text() + '''
from pathlib import Path
from agent_shell.tmux import TmuxTarget
Terminal.target = property(lambda self: TmuxTarget('/fixture-only', '%1',
                                                 os.getpid(), 1, os.getpid()))
async def gated_exit(self):
    while not Path(os.environ['WATCH_EXIT_GATE']).exists():
        await asyncio.sleep(0.02)
    return 7
Terminal.wait = gated_exit
''')
        gate = self.workspace / 'exit-foreman'
        self.env['WATCH_EXIT_GATE'] = str(gate)
        self.addCleanup(gate.touch)
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'foreman',
             '--workspace', str(self.workspace)], env=self.env, input='',
            capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        original = read_status(self)

        # Retain only this test's live owner handle; never recover a handle from saved state.
        from lifecycle_support import pidfd_open
        descriptor = pidfd_open(original['owner_pid'])

        def finish():
            import select
            gate.touch()
            try:
                self.assertTrue(select.select([descriptor], [], [], 10)[0],
                                'Isolated owner did not finish after fake Pi exit')
            finally:
                os.close(descriptor)
        self.addCleanup(finish)
        return original

    def test_live_managed_owner_wins_over_stale_missing_or_malformed_plain_discovery(self):
        # Arrange: leave an earlier plain invocation's discovery before persistent root launch.
        plain = self.start('--new-only')
        self.wait_until(plain, lambda: any(e['kind'] == 'ready' for e in self.events()))
        self.stop(plain)
        original = self.launch_foreman()
        path = self.workspace / '.factory/runtime/watch/status.json'
        configurations = {p: p.read_bytes() for p in (self.workspace / '.factory').rglob('*')
                          if p.is_file() and '/runtime/' not in str(p)}

        # Act / Assert: owner presence is distinct from watcher presence and model health.
        for content in (path.read_text(), '{invalid', None):
            with self.subTest(content=content):
                if content is None:
                    path.unlink()
                else:
                    path.write_text(content)
                observed = read_status(self)
                self.assertEqual(observed['source'], 'managed_owner')
                self.assertEqual(observed['observation'], 'live')
                self.assertEqual(observed['process'], 'present')
                self.assertEqual(observed['process_role'], 'foreman_owner')
                self.assertEqual(observed['foreman'], 'ready')
                self.assertEqual(observed['watcher'], 'stopped')
                self.assertEqual(observed['health'], 'not_checked')
                self.assertEqual(observed['target'], original['target'])

        # Public managed start/stop still borrows the same owner; status does neither.
        started = self.start('--start', '--new-only')
        output, errors = started.communicate(timeout=10)
        self.assertEqual(started.returncode, 0, output + errors)
        during = read_status(self)
        self.assertEqual(during['watcher'], 'running')
        self.assertEqual(during['phase'], 'watching')
        self.assertEqual(during['health'], 'not_checked')
        stopped = self.start('--stop')
        output, errors = stopped.communicate(timeout=10)
        self.assertEqual(stopped.returncode, 0, output + errors)
        self.assertEqual(read_status(self)['target'], original['target'])
        self.assertEqual({p: p.read_bytes() for p in configurations}, configurations)
        self.assertEqual(sum(e['kind'] == 'launch' for e in self.events()), 2)
        self.assertFalse(any(e['kind'] == 'send' for e in self.events()))
