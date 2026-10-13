import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]

GH = '''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

path = Path(os.environ['WATCH_GH_STATE'])
state = json.loads(path.read_text())
args = sys.argv[1:]
source = '/'.join(args[1].split('/')[1:3])
count = state.setdefault('counts', {}).get(source, 0)
state['counts'][source] = count + 1
state.setdefault('calls', []).append(args)
path.write_text(json.dumps(state))
steps = state['sources'][source]
result = steps[min(count, len(steps) - 1)]
if isinstance(result, str):
    sys.exit(result)
print(json.dumps(result))
'''

SHELL = '''import asyncio
import json
import os
from types import SimpleNamespace


def record(kind, **fields):
    with open(os.environ['WATCH_TERMINAL_LOG'], 'a') as log:
        log.write(json.dumps({'kind': kind, **fields}) + '\\n')


class Terminal:
    closed = False
    returncode = None

    async def send_text(self, text, *, submit=False):
        record('send', text=text, submit=submit)
        if os.environ.get('WATCH_SEND_HANG'):
            await asyncio.Event().wait()
        if os.environ.get('WATCH_SEND_FAIL'):
            raise RuntimeError('terminal delivery failed')

    async def wait(self):
        if os.environ.get('WATCH_EXIT_DELAY'):
            await asyncio.sleep(float(os.environ['WATCH_EXIT_DELAY']))
            return 7
        await asyncio.Event().wait()


class Session:
    def __init__(self):
        self.terminal = Terminal()

    async def events(self):
        if os.environ.get('WATCH_NO_READY'):
            await asyncio.Event().wait()
        await asyncio.sleep(0.05)
        record('ready')
        yield SimpleNamespace(type='system', session_id='pi-conversation')
        await asyncio.Event().wait()

    async def close(self):
        self.terminal.closed = True
        record('close')
        if os.environ.get('WATCH_CLOSE_FAIL'):
            raise RuntimeError('Pi cleanup failed')
        if os.environ.get('WATCH_CLOSE_HANG'):
            await asyncio.Event().wait()


class AgentShell:
    def __init__(self, agent_type, execution_host):
        self.agent_type = agent_type
        self.host = execution_host

    async def open_interactive(self, cwd, *, model=None, effort=None):
        print('library stdout banner', flush=True)
        os.write(1, b'native library stdout banner\\n')
        record('launch', cwd=cwd, model=model, effort=effort, agent_type=self.agent_type,
               placement=self.host.placement, controller_pid=os.getpid())
        if os.environ.get('WATCH_LAUNCH_DELAY'):
            await asyncio.sleep(float(os.environ['WATCH_LAUNCH_DELAY']))
        return Session()
'''

TMUX = '''class TmuxPlacement:
    @classmethod
    def new_session(cls, name=None):
        return {'kind': 'new-session', 'name': name}


class TmuxExecutionHost:
    def __init__(self, placement):
        self.placement = placement
'''


class WatchCliTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.bin = self.workspace / 'bin'
        self.bin.mkdir()
        (self.bin / 'gh').write_text(GH)
        (self.bin / 'gh').chmod(0o755)
        external = self.workspace / 'external'
        package = external / 'agent_shell'
        (package / 'models').mkdir(parents=True)
        (package / '__init__.py').write_text('')
        (package / 'shell.py').write_text(SHELL)
        (package / 'tmux.py').write_text(TMUX)
        (package / 'models' / '__init__.py').write_text('')
        (package / 'models' / 'agent.py').write_text('class AgentType:\n    PI = "pi"\n')
        self.state_path = self.workspace / 'gh.json'
        self.terminal_log = self.workspace / 'terminal.jsonl'
        self.state_path.write_text(json.dumps({'sources': {'team/app': [[[]]]}}))
        self.env = dict(os.environ,
                        PYTHONPATH=os.pathsep.join((str(external), str(ROOT / 'src'))),
                        PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        GH_HOST='wrong.example', WATCH_GH_STATE=str(self.state_path),
                        WATCH_TERMINAL_LOG=str(self.terminal_log))
        self.configure()

    def configure(self, labels=('factory',), sources=('team/app',), provider='github'):
        directory = self.workspace / '.factory'
        directory.mkdir(exist_ok=True)
        contents = (f'watcher_label = {json.dumps(labels)}\n'
                    'foreman_agent_model = "provider/model"\n'
                    'foreman_agent_effort = "high"\n')
        for index, source in enumerate(sources):
            contents += ('\n[[repository]]\n'
                         f'local_dir = {json.dumps(str(self.workspace / str(index)))}\n'
                         f'remote = "git@github.com:{source}.git"\n'
                         f'provider = {json.dumps(provider)}\nsource = {json.dumps(source)}\n')
        (directory / 'factory.toml').write_text(contents)

    def issue(self, number=1, title='Implement feature', labels=('factory',), **extra):
        return {'number': number, 'title': title, 'labels': [{'name': v} for v in labels],
                'html_url': f'https://github.com/team/app/issues/{number}',
                'state': 'open', 'body': 'BODY MUST NOT BE SENT', **extra}

    def script(self, sources):
        self.state_path.write_text(json.dumps({'sources': sources}))

    def events(self):
        if not self.terminal_log.exists():
            return []
        return [json.loads(line) for line in self.terminal_log.read_text().splitlines()]

    def start(self, *arguments, input=''):
        process = subprocess.Popen(
            [sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace',
             str(self.workspace), '--interval', '0.05',
             *arguments], cwd=self.workspace, env=self.env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        self.addCleanup(self.cleanup_process, process)
        if input:
            process.stdin.write(input)
            process.stdin.flush()
        return process

    def cleanup_process(self, process):
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=15)

    def wait_until(self, process, predicate, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                self.fail(f'Watch exited {process.returncode}: {stdout}\n{stderr}')
            time.sleep(0.02)
        self.fail(f'Watch did not reach expected state; terminal events: {self.events()}')

    def stop(self, process, sig=signal.SIGINT):
        process.send_signal(sig)
        stdout, stderr = process.communicate(timeout=15)
        return process.returncode, stdout, stderr

    def test_existing_issue_is_submitted_to_one_owned_ready_pi_session(self):
        # Arrange
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
        code, stdout, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        events = self.events()
        self.assertEqual([e['kind'] for e in events], ['launch', 'ready', 'send', 'close'])
        launch, _, sent, _ = events
        self.assertEqual((launch['cwd'], launch['model'], launch['effort'], launch['agent_type']),
                         (str(self.workspace), 'provider/model', 'high', 'pi'))
        self.assertEqual(launch['placement']['kind'], 'new-session')
        self.assertTrue(sent['submit'])
        self.assertIn('github:team/app#1', sent['text'])
        self.assertIn('Implement feature', sent['text'])
        self.assertIn('https://github.com/team/app/issues/1', sent['text'])
        self.assertNotIn('BODY MUST NOT BE SENT', sent['text'])
        self.assertIn('tmux attach', stdout)
        self.assertIn(launch['placement']['name'], stdout)
        self.assertIn('close', stdout.lower())
        self.assertIn('library stdout banner', stderr)
        self.assertNotIn('library stdout banner', stdout)
        calls = json.loads(self.state_path.read_text())['calls']
        self.assertEqual(calls[0], ['api', 'repos/team/app/issues?state=open&per_page=100',
                                    '--hostname', 'github.com', '--paginate', '--slurp'])

    def test_pagination_label_or_pr_filter_and_duplicate_sources(self):
        # Arrange
        self.configure(labels=('Factory', 'urgent'), sources=('team/app', 'TEAM/APP'))
        first = [[self.issue(1, labels=('FACTORY',)), self.issue(2, labels=('urgent',)),
                  self.issue(3, labels=('other',)), self.issue(4, pull_request={})],
                 [self.issue(5, labels=('factory',)), self.issue(6, state='closed')]]
        later = [[self.issue(1, title='Edited title'), self.issue(2, labels=('urgent',)),
                  self.issue(5), self.issue(7, labels=('URGENT',))]]
        self.script({'team/app': [first, later]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: sum(e['kind'] == 'send' for e in self.events()) >= 4)
        self.wait_until(process, lambda: json.loads(self.state_path.read_text())
                        .get('counts', {}).get('team/app', 0) >= 3)
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        events = self.events()
        sent = [e['text'] for e in events if e['kind'] == 'send']
        self.assertEqual(len(sent), 4)
        for text, expected in zip(sent, ('#1', '#2', '#5', '#7')):
            self.assertIn('github:team/app' + expected, text)
        self.assertNotIn('Edited title', ' '.join(sent))
        self.assertEqual(sum(e['kind'] == 'launch' for e in events), 1)
        self.assertEqual(sum(e['kind'] == 'close' for e in events), 1)
        self.assertTrue(all('repos/team/app/issues?' in call[1]
                            for call in json.loads(self.state_path.read_text())['calls']))

    def test_wildcard_matches_unlabelled_open_issues_and_empty_pages(self):
        # Arrange
        self.configure(labels=('*',))
        self.script({'team/app': [[[]], [[self.issue(8, labels=()),
                                        self.issue(9, pull_request={})]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        sent = [e['text'] for e in self.events() if e['kind'] == 'send']
        self.assertEqual(len(sent), 1)
        self.assertIn('github:team/app#8', sent[0])

    def test_startup_choice_new_only_baselines_then_sends_new_matches(self):
        for arguments, answer in ((('--new-only',), ''), ((), 'n\n'), ((), 'e\n')):
            with self.subTest(arguments=arguments, answer=answer):
                # Arrange
                self.terminal_log.unlink(missing_ok=True)
                self.script({'team/app': [[[self.issue(1)]],
                                         [[self.issue(1, title='Edited'), self.issue(2)]]]})
                # Act
                process = self.start(*arguments, input=answer)
                self.wait_until(process, lambda: any(e['kind'] == 'send' and '#2' in e['text']
                                                     for e in self.events()))
                code, stdout, stderr = self.stop(process)
                # Assert
                self.assertEqual(code, 130, stderr)
                sent = [e['text'] for e in self.events() if e['kind'] == 'send']
                self.assertEqual(len(sent), 2 if answer == 'e\n' else 1)
                self.assertIn('github:team/app#2', sent[-1])
                self.assertNotIn('Edited', ' '.join(sent))
                if not arguments:
                    self.assertIn('existing', stdout.lower())
                    self.assertIn('new', stdout.lower())

    def test_failed_reads_retry_per_source_and_baseline_first_success_only(self):
        # Arrange
        self.configure(sources=('team/app', 'team/healthy'))
        self.script({'team/app': ['HTTP 503 unavailable', [[self.issue(1)]],
                                  [[self.issue(1), self.issue(2)]]],
                     'team/healthy': [[[]], [[self.issue(3)]], [[self.issue(3)]]]})
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: sum(e['kind'] == 'send' for e in self.events()) >= 2)
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertIn('HTTP 503', stderr)
        self.assertIn('retry', stderr.lower())
        sent = [e['text'] for e in self.events() if e['kind'] == 'send']
        self.assertEqual(len(sent), 2)
        self.assertIn('github:team/healthy#3', sent[0])
        self.assertIn('github:team/app#2', sent[1])
        self.assertNotIn('github:team/app#1', ' '.join(sent))

    def test_malformed_reads_are_reported_and_retried_without_traceback(self):
        for malformed in ({'bad': 'pages'}, [[{'number': 'invalid'}]],
                          [[self.issue(labels=(), title=4)]]):
            with self.subTest(malformed=malformed):
                # Arrange
                self.terminal_log.unlink(missing_ok=True)
                self.script({'team/app': [malformed, [[self.issue(10)]]]})
                # Act
                process = self.start('--existing')
                self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
                code, _, stderr = self.stop(process)
                # Assert
                self.assertEqual(code, 130, stderr)
                self.assertIn('malformed', stderr.lower())
                self.assertNotIn('Traceback', stderr)
                self.assertEqual(sum(e['kind'] == 'send' for e in self.events()), 1)

    def test_invalid_watch_options_and_providers_fail_before_pi_or_github(self):
        for arguments, provider, expected in (
            (('--interval', '0'), 'github', 'positive'),
            (('--interval', '-2'), 'github', 'positive'),
            (('--interval', 'nan'), 'github', 'finite'),
            (('--interval', 'inf'), 'github', 'finite'),
            ((), 'linear', 'Unsupported'),
            ((), 'github', 'source'),
        ):
            with self.subTest(arguments=arguments, provider=provider, expected=expected):
                # Arrange
                source = 'team/app' if expected != 'source' else 'bad?query/source'
                self.configure(provider=provider, sources=(source,))
                # Act
                process = self.start('--existing', *arguments)
                try:
                    stdout, stderr = process.communicate(timeout=1)
                except subprocess.TimeoutExpired:
                    self.stop(process)
                    self.fail('Invalid configuration launched a watcher instead of failing.')
                # Assert
                self.assertNotEqual(process.returncode, 0, stdout)
                self.assertIn(expected, stderr)
                self.assertNotIn('Traceback', stderr)
                self.assertEqual(self.events(), [])
                self.assertEqual(json.loads(self.state_path.read_text()).get('calls', []), [])

    def test_delivery_failure_stops_without_success_or_replacement(self):
        # Arrange
        self.env['WATCH_SEND_FAIL'] = '1'
        self.script({'team/app': [[[self.issue(1), self.issue(2)]]]})
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('delivery failed', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'send', 'close'])

    def test_pi_exit_is_reported_while_waiting_without_matching_issues(self):
        # Arrange
        self.env['WATCH_EXIT_DELAY'] = '0.15'
        # Act
        process = self.start('--existing', '--interval', '30')
        try:
            stdout, stderr = process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            self.stop(process)
            self.fail('Dead Pi was not reported during the polling wait.')
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('Pi exited', stderr)
        self.assertIn('7', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual(sum(e['kind'] == 'launch' for e in self.events()), 1)
        self.assertEqual(self.events()[-1]['kind'], 'close')

    def test_pi_exit_during_poll_is_not_misreported_as_cleanup_failure(self):
        # Arrange
        gh = self.bin / 'gh'
        gh.write_text(gh.read_text().replace(
            'path.write_text(json.dumps(state))',
            'path.write_text(json.dumps(state))\nimport time; time.sleep(3)'))
        self.env['WATCH_EXIT_DELAY'] = '0.15'
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'close' for e in self.events()))
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertIn('Pi exited with status 7', stderr)
        self.assertNotIn('Pi cleanup:', stderr)
        self.assertNotIn('cleanup failed', stderr.lower())
        self.assertEqual(sum(e['kind'] == 'close' for e in self.events()), 1)

    def test_pi_exit_between_poll_and_send_preserves_the_actual_exit_reason(self):
        # Arrange
        gh = self.bin / 'gh'
        gh.write_text(gh.read_text().replace(
            'path.write_text(json.dumps(state))',
            'path.write_text(json.dumps(state))\n'
            'if count == 1:\n    import time; time.sleep(1)'))
        self.env['WATCH_EXIT_DELAY'] = '0.4'
        self.script({'team/app': [[[]], [[self.issue()]]]})
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('Pi exited with status 7', stderr)
        self.assertNotIn('Pi cleanup:', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual(sum(e['kind'] == 'close' for e in self.events()), 1)

    def test_parent_stdin_eof_closes_controller_while_waiting_for_pi_ready(self):
        # Arrange
        self.env['WATCH_NO_READY'] = '1'
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'launch' for e in self.events()))
        process.kill()  # Its private controller stdin reaches EOF; outer stdin is unrelated.
        try:
            process.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            controller = self.events()[0]['controller_pid']
            os.kill(controller, signal.SIGTERM)
            process.communicate(timeout=5)
            self.fail('Controller ignored stdin EOF during readiness.')
        # Assert
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'close'])

    def test_controller_signal_closes_pi_before_readiness(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            with self.subTest(signal=sig):
                # Arrange
                self.terminal_log.unlink(missing_ok=True)
                self.env['WATCH_NO_READY'] = '1'
                self.script({'team/app': [[[self.issue()]]]})
                # Act
                process = self.start('--existing')
                self.wait_until(process, lambda: any(e['kind'] == 'launch' for e in self.events()))
                os.kill(self.events()[0]['controller_pid'], sig)
                stdout, stderr = process.communicate(timeout=5)
                # Assert
                self.assertEqual(process.returncode, 1, stderr)
                self.assertEqual([e['kind'] for e in self.events()], ['launch', 'close'])
                self.assertNotIn('Submitted', stdout)
                self.assertEqual(json.loads(self.state_path.read_text()).get('calls', []), [])

    def test_readiness_timeout_gives_trust_dialog_help_and_closes_pi(self):
        # Arrange
        self.env['WATCH_NO_READY'] = '1'
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=40)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('ready', stderr.lower())
        self.assertIn('trust', stderr.lower())
        self.assertIn('new tmux attach-session', stderr)
        self.assertIn('restart watch', stderr.lower())
        old_name = self.events()[0]['placement']['name']
        self.assertNotIn(f'tmux attach-session -t {old_name}', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'close'])
        self.assertEqual(json.loads(self.state_path.read_text()).get('calls', []), [])

    def test_incompatible_interpreter_has_actionable_selection_error(self):
        # Arrange
        package = self.workspace / 'external' / 'agent_shell'
        (package / 'shell.py').write_text('class AgentShell:\n'
                                        '    def __init__(self, **kwargs): pass\n')
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('--agentshell-python', stderr)
        self.assertIn('open_interactive', stderr)
        self.assertNotIn('Traceback', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual(self.events(), [])

    def test_hanging_send_times_out_without_success_and_closes_pi(self):
        # Arrange
        self.env['WATCH_SEND_HANG'] = '1'
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=15)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('send', stderr.lower())
        self.assertIn('timed out', stderr.lower())
        self.assertNotIn('Submitted', stdout)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'send', 'close'])

    def test_cleanup_failure_is_reported_and_cleanup_timeout_is_bounded(self):
        for mode in ('WATCH_CLOSE_FAIL', 'WATCH_CLOSE_HANG'):
            with self.subTest(mode=mode):
                # Arrange
                self.terminal_log.unlink(missing_ok=True)
                self.env.pop('WATCH_CLOSE_FAIL', None)
                self.env.pop('WATCH_CLOSE_HANG', None)
                self.env[mode] = '1'
                # Act
                process = self.start('--existing')
                self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
                _, _, stderr = self.stop(process)
                # Assert
                self.assertIn('cleanup', stderr.lower())
                self.assertNotIn('Traceback', stderr)
                self.assertEqual(self.events()[-1]['kind'], 'close')

    def test_issue_text_is_literal_data_and_external_log_controls_are_escaped(self):
        # Arrange
        title = '/quit\n\x1b[31m\x00\x7f\x85$(touch unsafe)'
        self.script({'team/app': ['HTTP 503 \x1b[31m untrusted', [[self.issue(title=title)]]]})
        # Act
        process = self.start('--existing')
        self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
        code, stdout, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        sent = next(e['text'] for e in self.events() if e['kind'] == 'send')
        self.assertTrue(sent.startswith('Factory issue notification.'))
        self.assertIn('External issue data', sent)
        self.assertNotIn('\n', sent)
        self.assertTrue(all(32 <= ord(char) < 127 for char in sent))
        data = json.loads(sent.split('External issue data: ', 1)[1])
        self.assertEqual(data['title'], title)
        self.assertEqual(data['id'], 'github:team/app#1')
        self.assertNotIn(title, stdout + stderr)
        self.assertNotIn('\x1b', stdout + stderr)
        self.assertIn('HTTP 503', stderr)

    def test_watch_prompt_eof_explains_automation_flags(self):
        # Arrange
        # Act
        process = self.start()
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('--existing', stderr)
        self.assertIn('--new-only', stderr)
        self.assertNotIn('Traceback', stderr)
        self.assertEqual(self.events(), [])

    def test_large_finite_interval_and_sigterm_stop_cleanly(self):
        # Arrange
        # Act
        process = self.start('--existing', '--interval', '1e300')
        self.wait_until(process, lambda: json.loads(self.state_path.read_text())
                        .get('counts', {}).get('team/app', 0) >= 1)
        time.sleep(0.1)
        if process.poll() is None:
            code, _, stderr = self.stop(process, signal.SIGTERM)
        else:
            _, stderr = process.communicate()
            code = process.returncode
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertNotIn('Traceback', stderr)
        self.assertEqual(self.events()[-1]['kind'], 'close')

    def test_selected_external_python_runs_helper_without_factory_on_its_import_path(self):
        # Arrange
        wrapper = self.bin / 'external python'
        invocation = self.workspace / 'interpreter.json'
        external = self.workspace / 'external'
        wrapper.write_text(f'#!{sys.executable}\n'
                           'import json, os, sys\n'
                           'from pathlib import Path\n'
                           f'Path({str(invocation)!r}).write_text(json.dumps(sys.argv[1:]))\n'
                           f'os.environ["PYTHONPATH"] = {str(external)!r}\n'
                           'os.execv(sys.executable, [sys.executable, *sys.argv[1:]])\n')
        wrapper.chmod(0o755)
        self.script({'team/app': [[[self.issue()]]]})
        # Act
        process = self.start('--existing', '--agentshell-python', str(wrapper))
        self.wait_until(process, lambda: any(e['kind'] == 'send' for e in self.events()))
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        arguments = json.loads(invocation.read_text())
        self.assertEqual(arguments[0], '-u')
        self.assertTrue(Path(arguments[1]).is_absolute())
        self.assertEqual(Path(arguments[1]).name, 'controller.py')
        self.assertEqual(sum(e['kind'] == 'send' for e in self.events()), 1)
        self.assertEqual(self.events()[-1]['kind'], 'close')

    def test_startup_deadline_after_slow_launch_still_gives_trust_help(self):
        # Arrange
        self.env['WATCH_LAUNCH_DELAY'] = '6'
        self.env['WATCH_NO_READY'] = '1'
        # Act
        process = self.start('--existing')
        stdout, stderr = process.communicate(timeout=40)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('ready', stderr.lower())
        self.assertIn('trust', stderr.lower())
        old_name = self.events()[0]['placement']['name']
        self.assertIn(old_name, stderr)
        self.assertIn('new tmux attach-session', stderr)
        self.assertIn('restart watch', stderr.lower())
        self.assertNotIn(f'tmux attach-session -t {old_name}', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'close'])


if __name__ == '__main__':
    unittest.main()
