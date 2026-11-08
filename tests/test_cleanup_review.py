"""Review regressions through public watch, external CLI fixtures and disposable native Git."""
import json
import shutil
from pathlib import Path

from test_completed_cleanup import CompletedCleanupFixture


class CleanupReviewTests(CompletedCleanupFixture):
    def control(self, value):
        path = self.workspace / 'review-control.json'
        path.write_text(json.dumps(value))
        self.env['PROFILE_PLANNING_CONTROL'] = str(path)
        return path

    def prepared(self):
        message, record = self.recorded()
        mapping = record['worktrees'][0]
        self.finish_mapping(mapping)
        self.save(message, record)
        return message, record, mapping

    def rival(self, record, mapping, *, project_id=13, external_ref='github:other/app#2',
              context='{}', status='active'):
        # A foreign active plan is not recoverable intake here, but its resource claim matters.
        other = self.planning_call('create_plan', project_id=project_id, status=status,
                                   external_ref=external_ref, context=context)
        task = self.planning_call('create_task', plan_id=other['id'], title='Feature ownership',
                                 description=json.dumps(dict(record, worktrees=[mapping],
                                                             external_ref=external_ref)))
        return other, task

    def assert_preserved(self, mapping):
        self.assertTrue(Path(mapping['path']).exists())
        self.assertTrue(self.branch_exists(mapping))
        self.assertTrue(self.branch_exists(mapping, remote=True))

    def test_invalid_competing_json_withholds_all_cleanup_but_allows_intake(self):
        # Arrange
        _, record, mapping = self.prepared()
        _, task = self.rival(record, mapping)
        self.planning_call('update_task', task_id=task['id'], description='{broken ownership')
        self.script({'team/app': [[[self.issue(3)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self._messages()))
        self.stop(process)
        # Assert
        self.assert_preserved(mapping)
        self.assertEqual(self._messages()[0]['number'], 3)
        self.assertTrue(any(a['scope'] == 'cleanup' for a in self.alerts()))

    def test_unreadable_competing_plan_withholds_cleanup_and_recovers(self):
        # Arrange
        _, record, mapping = self.prepared()
        other, _ = self.rival(record, mapping)
        control = self.control({'response_cases': [{'tool': 'get_plan',
            'arguments': {'plan_id': other['id']}, 'result': dict(other, id=999)}]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        # Assert
        self.assert_preserved(mapping)
        self.assertTrue(any(a.get('plan_id') == other['id'] for a in self.alerts()))
        # Removing unreadability alone exposes the real competing claim, not deletion authority.
        control.write_text('{}')
        before = self.polls()
        self.wait_until(process, lambda: self.polls() >= before + 2)
        self.stop(process)
        self.assert_preserved(mapping)

    def test_unknown_competing_target_withholds_disposal(self):
        # Arrange
        _, record, mapping = self.prepared()
        rival = dict(mapping, branch='factory/rival', path=str(self.workspace / 'other'))
        rival.pop('target_branch')
        self.rival(record, rival)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert: the unknown target may be the completed feature ref.
        self.assert_preserved(mapping)

    def test_unreadable_required_namespace_withholds_all_disposal(self):
        # Arrange: even a currently unclaimed configured root may share branch namespaces.
        self.configure(sources=('team/app', 'team/library'))
        second = self.workspace / 'repository-1'
        self.add_remote(second, 'team/library')
        _, _, mapping = self.prepared()
        native = shutil.which('git')
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\n'
                           f'if {str(second)!r} in sys.argv and "--git-common-dir" in sys.argv:\n'
                           '    sys.exit("fixture namespace unreadable")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        self.script({'team/app': [[[]]], 'team/library': [[[]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assert_preserved(mapping)
        self.assertTrue(any(str(second) in a.get('paths', []) for a in self.alerts()))

    def test_full_task_failure_withholds_competing_claims(self):
        # Arrange
        _, record, mapping = self.prepared()
        _, task = self.rival(record, mapping)
        self.control({'response_cases': [{'tool': 'get_task',
                      'arguments': {'task_id': task['id']}, 'result': dict(task, id=999)}]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assert_preserved(mapping)

    def test_task_inventory_failure_withholds_competing_claims(self):
        _, record, mapping = self.prepared()
        other, _ = self.rival(record, mapping)
        self.control({'fail': 'query_tasks', 'fail_arguments': {'plan_id': other['id']}})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        self.assert_preserved(mapping)

    def test_confirmed_cleanup_does_not_delete_new_human_work_in_the_same_run(self):
        # Arrange
        _, _, mapping = self.prepared()
        process = self.start('--new-only')
        self.wait_until(process, lambda: not self.branch_exists(mapping, remote=True))
        # Advance beyond the final absence checks and success report.
        before = self.polls()
        self.wait_until(process, lambda: self.polls() >= before + 2)
        root = mapping['local_dir']
        tree = self.git(root, 'rev-parse', 'HEAD^{tree}')
        head = self.git(root, 'rev-parse', 'HEAD')
        commit = self.git(root, '-c', 'user.name=Human', '-c', 'user.email=h@example.invalid',
                          'commit-tree', tree, '-p', head, '-m', 'New human work after cleanup')
        self.git(root, 'branch', mapping['branch'], commit)
        self.git(root, 'push', 'origin', f'{commit}:refs/heads/{mapping["branch"]}')
        # Act
        before = self.polls()
        self.wait_until(process, lambda: self.polls() >= before + 3)
        _, output, _ = self.stop(process)
        # Assert
        self.assertEqual(self.git(root, 'rev-parse', mapping['branch']), commit)
        self.assertIn(commit, self.git(root, 'ls-remote', '--heads', 'origin', mapping['branch']))
        self.assertEqual(output.count('Cleanup confirmed'), 1)

    def test_cleanup_inventory_outage_recovery_outage_alerts_and_intake_continues(self):
        # Arrange: unfinished startup inventory is already complete before the outages.
        control = self.control({})
        self.script({'team/app': [[[]]]})
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        failure = {'fail': 'list_plans', 'fail_arguments': {}}
        # Act / Assert: two distinct outage episodes must each notify; issue-specific lookups work.
        for number in (3, 4):
            control.write_text(json.dumps(failure))
            self.script({'team/app': [[[self.issue(number)]]]})
            self.wait_until(process, lambda: len(self._messages()) >= number - 2)
            self.assertEqual(sum(a['code'] == 'cleanup_inventory_read_failed'
                                 for a in self.alerts()), number - 2)
            self.assertTrue(all('Planning is paused' not in a['recovery']
                                for a in self.alerts() if a['scope'] == 'cleanup'))
            control.write_text('{}')
            before = self.polls()
            self.wait_until(process, lambda: self.polls() >= before + 2)
        self.stop(process)

    def test_preflight_target_is_carried_past_plan_creation_without_a_second_read(self):
        # Arrange: the first target read works; an unnecessary second read would fail.
        native = shutil.which('git')
        count = self.workspace / 'target-reads'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os, sys\nfrom pathlib import Path\n'
                           'if sys.argv[-2:] == ["symbolic-ref", "HEAD"]:\n'
                           f'    path = Path({str(count)!r})\n'
                           '    n = int(path.read_text()) + 1 if path.exists() else 1\n'
                           '    path.write_text(str(n))\n'
                           '    if n == 2: sys.exit("fixture second target read failed")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        self.script({'team/app': [[[self.issue(1)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: bool(self._messages() or self.alerts()))
        self.stop(process)
        # Assert: actual creation still performs its native root/path/branch checks.
        self.assertEqual(len(self._messages()), 1, self.alerts())
        self.assertEqual(int(count.read_text()), 1)
        self.assertTrue(Path(self._messages()[0]['worktrees'][0]['path']).is_dir())
        self.assertFalse(any(a['retry'] == 'manual_reconciliation' for a in self.alerts()))

    def log_git(self):
        native = shutil.which('git')
        log = self.workspace / 'review-git.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, sys\n'
                           'from pathlib import Path\n'
                           f'state = Path({str(self.state_path)!r})\n'
                           'counts = json.loads(state.read_text()).get("counts", {})\n'
                           'poll = counts.get("team/app", 0)\n'
                           f'with open({str(log)!r}, "a") as stream:\n'
                           '    stream.write(json.dumps([poll, sys.argv[1:]]) + "\\n")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        return log

    def test_default_network_query_is_once_per_root_cycle_and_finished_work_has_no_git_cost(self):
        # Arrange
        _, _, mapping = self.prepared()
        log = self.log_git()
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 3)
        first = [json.loads(line) for line in log.read_text().splitlines()]
        before = self.polls()
        self.wait_until(process, lambda: self.polls() >= before + 3)
        self.stop(process)
        last = [json.loads(line) for line in log.read_text().splitlines()]
        # Assert at native process boundary, not helper calls.
        defaults = [args for _, args in first if '--symref' in args]
        self.assertEqual(len(defaults), 1)
        self.assertEqual(last, first, 'Finished plans caused more Git processes')
        self.assert_disposed(mapping)

    def test_cleanup_network_ignores_inherited_interactive_auth_and_has_closed_stdin(self):
        # Arrange: unlike the general fixture, explicitly permit prompts in the parent environment.
        _, _, mapping = self.prepared()
        self.env['GIT_TERMINAL_PROMPT'] = '1'
        self.env['GIT_ASKPASS'] = '/fixture/must-not-run'
        native = shutil.which('git')
        log = self.workspace / 'network-input.jsonl'
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport json, os, select, sys\n'
                           'if "ls-remote" in sys.argv or "push" in sys.argv:\n'
                           '    ready = bool(select.select([sys.stdin], [], [], 0)[0])\n'
                           '    eof = ready and sys.stdin.read(1) == ""\n'
                           '    record = {"eof": eof, "prompt": os.getenv("GIT_TERMINAL_PROMPT"),\n'
                           '              "ssh": os.getenv("GIT_SSH_COMMAND"),\n'
                           '              "askpass": os.getenv("GIT_ASKPASS"),'
                           '              "ssh_askpass": os.getenv("SSH_ASKPASS"),'
                           '              "askpass_required": os.getenv("SSH_ASKPASS_REQUIRE")}\n'
                           f'    with open({str(log)!r}, "a") as stream:\n'
                           '        stream.write(json.dumps(record) + "\\n")\n'
                           '    if not eof: sys.exit("fixture attempted interactive input")\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        # Act: the public watch process has an open stdin pipe, deliberately kept open by fixture.
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        records = [json.loads(line) for line in log.read_text().splitlines()]
        self.assertTrue(records)
        self.assertTrue(all(r['eof'] for r in records))
        self.assertTrue(all(r['prompt'] == '0' for r in records))
        self.assertTrue(all('BatchMode=yes' in r['ssh'] for r in records))
        self.assertTrue(all(r['askpass'] != '/fixture/must-not-run' for r in records))
        self.assertTrue(all(r['ssh_askpass'] == '/bin/false' for r in records))
        self.assertTrue(all(r['askpass_required'] == 'force' for r in records))
        self.assert_disposed(mapping)

    def test_missing_git_link_blocks_cleanup_and_explains_targeted_approved_repair(self):
        # Arrange: filesystem-dependent partial-delete simulation, not a real signal/crash claim.
        _, _, mapping = self.prepared()
        (Path(mapping['path']) / '.git').unlink()
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert: no automated bypass, pruning or claim that this always recovers on its own.
        self.assert_preserved(mapping)
        alerts = [a for a in self.alerts() if a['code'] == 'worktree_mismatch']
        self.assertTrue(alerts)
        self.assertIn('git worktree repair', alerts[0]['recovery'])
        self.assertIn('user approval', alerts[0]['recovery'])
        self.assertIn('backlink', alerts[0]['recovery'])

    def test_cleanup_respects_configured_ssh_command_without_modifying_native_settings(self):
        # Arrange
        _, _, mapping = self.prepared()
        command = self.env.pop('GIT_SSH_COMMAND')
        self.env.pop('GIT_SSH_VARIANT')
        self.git(self.workspace, 'config', 'core.sshCommand', command)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.env['GIT_SSH_COMMAND'] = command  # Independent assertion transport, not production.
        self.assert_disposed(mapping)
        self.assertEqual(self.git(self.workspace, 'config', '--get', 'core.sshCommand'), command)

    def test_noninteractive_network_read_timeout_is_not_an_uncertain_write(self):
        # Arrange
        from forgetful_factory.deadlines import DeadlinePolicy

        _, _, mapping = self.prepared()
        native = shutil.which('git')
        wrapper = self.bin / 'git'
        wrapper.write_text('#!/usr/bin/env python3\nimport os, sys, time\n'
                           'if "ls-remote" in sys.argv: time.sleep(2)\n'
                           f'os.execv({native!r}, [{native!r}, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        self.script({'team/app': [[[self.issue(3)]]]})
        # Act
        process = self.start('--existing', deadlines=DeadlinePolicy(external_command=0.5))
        self.wait_until(process, lambda: bool(self._messages()))
        self.stop(process)
        # Assert: no tree/ref write preceded the failed default read; unrelated intake progressed.
        wrapper.unlink()
        self.assert_preserved(mapping)
        self.assertTrue(any(a['code'] == 'cleanup_network_read_failed' for a in self.alerts()))
        self.assertFalse(any(a['code'] == 'cleanup_operation_uncertain' for a in self.alerts()))

    def test_claim_read_failure_during_final_recheck_stops_other_plan_disposal_this_cycle(self):
        # Arrange: two independent native mappings; task 1 fails only after the initial claim read.
        message, record, mapping = self.prepared()
        other_mapping = dict(mapping, branch='factory/second',
                             path=str(self.workspace / '.factory/worktrees/second'))
        self.git(self.workspace, 'worktree', 'add', '-b', other_mapping['branch'],
                 other_mapping['path'], 'HEAD')
        self.finish_mapping(other_mapping)
        plan = self.planning_call('get_plan', plan_id=message['plan_id'])
        context = json.loads(plan['context'])
        context['issue']['number'] = 2
        self.rival(record, other_mapping, project_id=12, status='completed',
                   external_ref='github:team/app#2', context=json.dumps(context))
        command = self.bin / 'forgetful'
        source = command.read_text()
        point = "        state['calls'].append([tool, values])"
        source = source.replace(point, point + '\n'
            '        reads = sum(t == "get_task" and v.get("task_id") == 1\n'
            '                    for t, v in state["calls"])\n'
            '        if tool == "get_task" and values.get("task_id") == 1 and reads >= 3:\n'
            '            save_planning_state()\n'
            '            sys.exit("fixture final claim recheck unavailable")')
        # Ignore arrangement's native get_task reads when counting this watch invocation.
        source = source.replace('reads >= 3', 'reads >= ' + str(3 + sum(
            tool == 'get_task' and values.get('task_id') == 1
            for tool, values in json.loads((self.workspace / '.factory/fixture-plans.json')
                                           .read_text())['calls'])))
        command.write_text(source)
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: self.polls() >= 2)
        self.stop(process)
        # Assert
        self.assert_preserved(mapping)
        self.assert_preserved(other_mapping)
