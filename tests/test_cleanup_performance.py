"""Cleanup performance and safety observed through watch and disposable native CLIs."""
import array
import json
import os
import selectors
import shutil
import signal
import socket
import struct
from contextlib import contextmanager
from pathlib import Path

import test_watcher_cancellation as cancellation
from test_completed_cleanup import CompletedCleanupFixture

from forgetful_factory.cli.deadlines import DeadlinePolicy


class CleanupPerformanceFixture(CompletedCleanupFixture):
    def completed_sets(self, count):
        message, record = self.recorded(epic=True)
        mappings = []
        for number in range(count):
            branch = f'factory/batch-{number}'
            path = self.workspace / '.factory/worktrees' / f'batch-{number}'
            self.git(self.workspace, 'worktree', 'add', '-b', branch, str(path), 'HEAD')
            mapping = {'repository': 'team/app', 'local_dir': str(self.workspace),
                       'branch': branch, 'path': str(path)}
            self.finish_mapping(mapping)
            mappings.append(mapping)
        record['worktrees'] = mappings
        self.save(message, record)
        self.clear_calls()
        return message, record, mappings

    @contextmanager
    def intake_turn(self, *arguments):
        """Hold the first provider reply after cleanup, without racing the next cycle."""
        with socket.socket(socket.AF_UNIX) as listener:
            path = str(self.workspace / 'intake.sock')
            listener.bind(path)
            listener.listen()
            listener.settimeout(12)
            self.script({'team/app': [{'gate': path, 'result': [[]]}]})
            process = self.start(*arguments)
            try:
                with listener.accept()[0] as gate:
                    yield process
                    gate.sendall(b'1')
            finally:
                self.stop(process)
                self.workspace.joinpath('intake.sock').unlink()

    def clear_calls(self):
        # Only used with watch stopped. Runtime CLI updates use the fixture's flock/replace.
        path = self.workspace / '.factory/fixture-plans.json'
        state = json.loads(path.read_text())
        state['calls'] = []
        path.write_text(json.dumps(state))

    def read_replies(self, steps):
        """Change native replies by occurrence, under the CLI fixture's existing flock."""
        executable = self.bin / 'forgetful'
        source = executable.read_text()
        needle = "        if control.get('incomplete') == tool:"
        if 'CLEANUP_READ_STEPS' not in source:
            self.assertEqual(source.count(needle), 1)
            source = source.replace(needle, '''        # CLEANUP_READ_STEPS
        steps = json.loads(Path(os.environ['CLEANUP_READ_STEPS']).read_text())
        occurrence = sum(t == tool and a == values for t, a in state['calls'])
        for step in steps:
            if (step['tool'] == tool and step['arguments'] == values
                    and occurrence >= step.get('from_call', 1)
                    and occurrence <= step.get('through_call', occurrence)):
                if step.get('fail'):
                    sys.exit('controlled read failure')
                if step.get('malformed'):
                    print('{malformed reply')
                    sys.exit(0)
                result = dict(result, **step.get('fields', {}))
''' + needle)
            executable.write_text(source)
        path = self.workspace / 'read-steps.json'
        path.write_text(json.dumps(steps))
        self.env['CLEANUP_READ_STEPS'] = str(path)


class CleanupSnapshotTests(CleanupPerformanceFixture):
    def test_discovery_reuses_full_tasks_for_claims_but_reads_fresh_before_disposal(self):
        # Arrange: summaries omit descriptions, including an ordinary task's potential claims.
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        task = self.planning_call('create_task', plan_id=message['plan_id'], title='Implement',
                                  description='Ordinary work')
        self.save(message, record)
        self.clear_calls()
        # Act: first public provider turn proves that cleanup has finished this cycle.
        with self.intake_turn('--new-only'):
            path = self.workspace / '.factory/fixture-plans.json'
            calls = json.loads(path.read_text())['calls']
            # Assert: one discovery inventory and one fresh pre-disposal inventory, not three.
            self.assert_disposed(mapping)
            self.assertEqual(sum(tool == 'query_tasks' for tool, _ in calls), 2, calls)
            for task_id in (task['id'], message['ownership_task_id']):
                self.assertEqual(sum(tool == 'get_task' and args['task_id'] == task_id
                                     for tool, args in calls), 2, calls)

    def test_incomplete_malformed_and_failed_discovery_withhold_the_entire_batch(self):
        # Arrange: incomplete inventories or full records must never yield partial deletion.
        message, _, mappings = self.completed_sets(2)
        faults = (
            {'tool': 'query_tasks', 'arguments': {'plan_id': message['plan_id']},
             'fields': {'total_count': 99}},
            {'tool': 'get_task', 'arguments': {'task_id': message['ownership_task_id']},
             'malformed': True},
            {'tool': 'get_task', 'arguments': {'task_id': message['ownership_task_id']},
             'fail': True},
        )
        for fault in faults:
            with self.subTest(fault=fault):
                self.clear_calls()
                self.read_replies([fault])
                # Act
                with self.intake_turn('--new-only'):
                    # Assert
                    for mapping in mappings:
                        self.assertTrue(Path(mapping['path']).is_dir())
                        self.assertTrue(self.branch_exists(mapping))
                        self.assertTrue(self.branch_exists(mapping, remote=True))
                    self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))
                self.terminal_log.unlink()

    def assert_fresh_check(self, change):
        # Arrange: change replies only after the first set has been durably confirmed.
        message, record, mappings = self.completed_sets(3)
        step = {'tool': 'get_plan', 'arguments': {'plan_id': message['plan_id']},
                'from_call': 3, 'fields': {'status': 'active'}}
        if change == 'association':
            step['fields'] = {'external_ref': 'github:team/app#99'}
        elif change in ('mapping', 'read-failed'):
            changed = json.loads(json.dumps(record))
            changed['worktrees'][1]['branch'] = 'factory/changed-identity'
            step.update(tool='get_task',
                        arguments={'task_id': message['ownership_task_id']},
                        fields={'description': json.dumps(changed)})
            if change == 'read-failed':
                step['fail'] = True
                step['through_call'] = 3
        self.read_replies([step])
        # Act
        with self.intake_turn('--new-only'):
            # Assert: first receipt survives; fresh evidence preserves the sibling.
            self.assert_disposed(mappings[0])
            for mapping in mappings[1:]:
                self.assertTrue(Path(mapping['path']).is_dir())
                self.assertTrue(self.branch_exists(mapping))
                self.assertTrue(self.branch_exists(mapping, remote=True))
            receipt = self.workspace / '.factory/cleanup-finished.json'
            self.assertEqual(len(json.loads(receipt.read_text())['finished']), 1)

    def test_second_set_rechecks_native_completed_status(self):
        self.assert_fresh_check('status')

    def test_second_set_rechecks_plan_association(self):
        self.assert_fresh_check('association')

    def test_second_set_rechecks_full_owner_mappings(self):
        self.assert_fresh_check('mapping')

    def test_failed_fresh_owner_read_stops_the_remaining_batch(self):
        self.assert_fresh_check('read-failed')


class CleanupBatchTests(CleanupPerformanceFixture):
    def test_three_distinct_attempts_per_cycle_rotate_and_leave_intake_a_turn(self):
        # Arrange: five sets, all rejected remotely, so no receipt can hide repeated attempts.
        _, _, mappings = self.completed_sets(5)
        remote = self.workspace / 'bare-team-app'
        hook = remote / 'hooks/update'
        hook.write_text('#!/bin/sh\ncase "$3" in 000000*) exit 1;; esac\n')
        hook.chmod(0o755)
        self.log_deletions()
        self.script({'team/app': [[[self.issue(9)]]]})
        # Act: a real new issue must reach Foreman while failing cleanup continues.
        process = self.start('--existing')
        self.wait_until(process, lambda: self.polls() >= 2 and bool(self._messages()), timeout=15)
        self.stop(process)
        attempts = self.deletions()
        # Assert: three distinct turns each cycle; rotation wraps rather than retrying the head.
        first = [ref for poll, ref in attempts if poll == 0]
        second = [ref for poll, ref in attempts if poll == 1]
        self.assertEqual(first, [':refs/heads/factory/batch-0', ':refs/heads/factory/batch-1',
                                 ':refs/heads/factory/batch-2'])
        self.assertEqual(second, [':refs/heads/factory/batch-3', ':refs/heads/factory/batch-4',
                                  ':refs/heads/factory/batch-0'])
        for poll in {poll for poll, _ in attempts}:
            refs = [ref for turn, ref in attempts if turn == poll]
            self.assertLessEqual(len(refs), 3, attempts)
            self.assertEqual(len(refs), len(set(refs)), attempts)
        self.assertEqual([m['key'] for m in self._messages()], ['9'])
        self.assertTrue(all(self.branch_exists(m, remote=True) for m in mappings))

    def log_deletions(self):
        native = shutil.which('git')
        self.deletion_log = self.workspace / 'deletions.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                           'from pathlib import Path\n'
                           'if "push" in sys.argv and any(a.startswith(":refs/heads/") '
                           'for a in sys.argv):\n'
                           f'    state = json.loads(Path({str(self.state_path)!r}).read_text())\n'
                           f'    fd = os.open({str(self.deletion_log)!r}, '
                           'os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)\n'
                           '    os.write(fd, (json.dumps([state.get("counts", {}).get('
                           '"team/app", 0), sys.argv[-1]]) + "\\n").encode())\n'
                           '    os.close(fd)\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)

    def deletions(self):
        return [json.loads(line) for line in self.deletion_log.read_text().splitlines()]

    def test_failed_receipt_storage_stops_the_remaining_batch(self):
        # Arrange: the first native deletion loses receipt storage before confirmation.
        _, _, mappings = self.completed_sets(2)
        receipt = self.workspace / '.factory/cleanup-finished.json'
        native = shutil.which('git')
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\nfrom pathlib import Path\n'
                           'if "push" in sys.argv and any(a.startswith(":refs/heads/") '
                           'for a in sys.argv):\n'
                           f'    Path({str(receipt)!r}).mkdir(exist_ok=True)\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        # Act
        with self.intake_turn('--new-only'):
            # Assert: the first set remains unconfirmed, the sibling keeps all its resources.
            self.assert_disposed(mappings[0])
            self.assertTrue(receipt.is_dir())
            self.assertTrue(self.branch_exists(mappings[1]))
            self.assertTrue(self.branch_exists(mappings[1], remote=True))
            self.assertTrue(any(a['code'] == 'cleanup_receipt_failed' for a in self.alerts()))


class CleanupCancellationTests(CleanupPerformanceFixture):
    def assert_cancelled_read(self, sig):
        # Arrange: block the fresh full-owner CLI read, after discovery has completed.
        message, _, mappings = self.completed_sets(2)
        executable = self.bin / 'forgetful'
        needle = "        if control.get('incomplete') == tool:"
        source = executable.read_text()
        self.assertEqual(source.count(needle), 1)
        address = str(self.workspace / 'read.sock')
        source = source.replace(needle, '''        if (tool == 'get_task' and
                sum(t == tool and a == values for t, a in state['calls']) == 2):
            import array, signal, socket
            sys.path.insert(0, TEST_SUPPORT)
            from lifecycle_support import pidfd_open
            descriptor = pidfd_open(os.getpid())
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            with socket.socket(socket.AF_UNIX) as channel:
                channel.connect(READ_ADDRESS)
                channel.sendmsg([json.dumps({'pid': os.getpid()}).encode()],
                                [(socket.SOL_SOCKET, socket.SCM_RIGHTS,
                                  array.array('i', [descriptor]))])
            os.close(descriptor)
            while True:
                signal.pause()
'''.replace('TEST_SUPPORT', repr(str(Path(__file__).resolve().parent)))
            .replace('READ_ADDRESS', repr(address)) + needle)
        executable.write_text(source)
        with socket.socket(socket.AF_UNIX) as listener:
            listener.bind(address)
            listener.listen()
            listener.settimeout(10)
            process = self.start('--new-only',
                                 deadlines=DeadlinePolicy(owned_process_term_grace=0.2))
            with listener.accept()[0] as channel:
                channel.settimeout(5)
                peer, uid, _ = struct.unpack('3i', channel.getsockopt(socket.SOL_SOCKET,
                                                                   socket.SO_PEERCRED, 12))
                data, controls, flags, _ = channel.recvmsg(1024, socket.CMSG_SPACE(4))
                descriptors = array.array('i')
                for level, kind, payload in controls:
                    if level == socket.SOL_SOCKET and kind == socket.SCM_RIGHTS:
                        descriptors.frombytes(payload)
                for descriptor in descriptors:
                    self.addCleanup(cancellation.WatcherCancellationTests.close_owned_check,
                                    descriptor)
                self.assertFalse(flags & socket.MSG_CTRUNC)
                self.assertEqual(len(descriptors), 1)
                self.assertEqual((peer, uid), (json.loads(data)['pid'], os.getuid()))
                # Act: one signal must stop the whole watcher and reap the stubborn CLI child.
                process.send_signal(sig)
            output, errors = process.communicate(timeout=5)
        # Assert: no set was touched and owned Foreman shutdown still ran.
        self.assertEqual(process.returncode, 130, errors)
        self.assertNotIn('Cleanup confirmed', output)
        self.assertNotIn('Traceback', errors)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])
        with selectors.DefaultSelector() as selector:
            selector.register(descriptors[0], selectors.EVENT_READ)
            self.assertTrue(selector.select(1), 'Cleanup CLI survived watcher cancellation')
        for mapping in mappings:
            self.assertTrue(Path(mapping['path']).is_dir())
            self.assertTrue(self.branch_exists(mapping))
            self.assertTrue(self.branch_exists(mapping, remote=True))
        path = self.workspace / '.factory/fixture-plans.json'
        calls = json.loads(path.read_text())['calls']
        self.assertEqual(sum(tool == 'get_task' and args['task_id'] ==
                             message['ownership_task_id'] for tool, args in calls), 2)

    def test_sigint_during_fresh_cleanup_read_reaps_native_child(self):
        self.assert_cancelled_read(signal.SIGINT)

    def test_sigterm_during_fresh_cleanup_read_reaps_native_child(self):
        self.assert_cancelled_read(signal.SIGTERM)
