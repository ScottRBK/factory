import array
import fcntl
import json
import os
import selectors
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from deadline_support import programmatic_factory
from profile_support import install_commands, install_grill_skill
from test_init import GH as INIT_GH
from test_init import INIT_SETTINGS

from forgetful_factory.deadlines import AgentShellLifecycleDeadlines, DeadlinePolicy

ROOT = Path(__file__).resolve().parents[1]

GH = '''#!/usr/bin/env python3
import fcntl
import json
import os
from pathlib import Path
import sys

path = Path(os.environ['WATCH_GH_STATE'])
lock = path.with_suffix('.lock').open('a')
fcntl.flock(lock, fcntl.LOCK_EX)
state = json.loads(path.read_text())
args = sys.argv[1:]
source = '/'.join(args[1].split('/')[1:3])
count = state.setdefault('counts', {}).get(source, 0)
state['counts'][source] = count + 1
state.setdefault('calls', []).append(args)
replacement = path.with_suffix('.next')
replacement.write_text(json.dumps(state))
replacement.replace(path)
steps = state['sources'][source]
result = steps[min(count, len(steps) - 1)]
fcntl.flock(lock, fcntl.LOCK_UN)
if isinstance(result, dict) and 'gate' in result:
    import socket
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as gate:
        gate.settimeout(5)
        gate.connect(result['gate'])
        if gate.recv(1) != b'1':
            sys.exit('GitHub response gate closed without release')
    result = result['result']
if isinstance(result, str):
    sys.exit(result)
print(json.dumps(result))
'''

SHELL = '''import array
import asyncio
import ctypes
import json
import os
import socket
from types import SimpleNamespace


def transfer_controller_handle():
    path = os.environ.get('WATCH_CONTROLLER_HANDLES')
    if not path:
        return
    function = ctypes.CDLL(None, use_errno=True).pidfd_open
    function.argtypes = [ctypes.c_int, ctypes.c_uint]
    function.restype = ctypes.c_int
    descriptor = function(os.getpid(), 0)
    if descriptor < 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error))
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as channel:
            channel.connect(path)
            channel.sendmsg([json.dumps({'pid': os.getpid()}).encode()],
                            [(socket.SOL_SOCKET, socket.SCM_RIGHTS,
                              array.array('i', [descriptor]))])
    finally:
        os.close(descriptor)


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
        yield SimpleNamespace(type='system', session_id=None)
        if os.environ.get('WATCH_NO_READY'):
            await asyncio.Event().wait()
        if os.environ.get('WATCH_READY_GATE'):
            from pathlib import Path
            while not Path(os.environ['WATCH_READY_GATE']).exists():
                await asyncio.sleep(0.01)
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
    def __init__(self, agent_type, execution_host=None):
        self.agent_type = agent_type
        self.host = execution_host

    async def list_models(self, cwd, timeout=30):
        return ['provider/model']

    async def open_interactive(self, cwd, *, model=None, effort=None, resources=None, prompt=None):
        transfer_controller_handle()
        print('library stdout banner', flush=True)
        os.write(1, b'native library stdout banner\\n')
        record('launch', cwd=cwd, model=model, effort=effort, agent_type=self.agent_type,
               resources=resources.__dict__,
               roster=os.environ.get('PI_AGENTSHELL_ROSTER_FILE'), prompt=prompt,
               forgetful_dir=os.environ.get('FACTORY_FORGETFUL_DIR'),
               forgetful_config=os.environ.get('FACTORY_FORGETFUL_CONFIG_DIR'),
               project=os.environ.get('FACTORY_FORGETFUL_PROJECT_ID'),
               placement=self.host.placement, controller_pid=os.getpid(),
               agent_dir=os.environ.get('PI_CODING_AGENT_DIR'),
               config_home=os.environ.get('XDG_CONFIG_HOME'),
               target=os.environ.get('FACTORY_FORGETFUL_METHOD'))
        if os.environ.get('WATCH_SKILL_COMMANDS'):
            import subprocess
            for command in json.loads(os.environ['WATCH_SKILL_COMMANDS']):
                result = subprocess.run(['bash', '-c', command], cwd=cwd,
                                        capture_output=True, text=True, timeout=5)
                record('skill-command', code=result.returncode, stdout=result.stdout)
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


class WatchFixture(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.grill_skill = install_grill_skill(self.workspace)
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
        (package / 'models/resources.py').write_text(
            'class SessionResources:\n'
            '    def __init__(self, **kwargs): self.__dict__.update(kwargs)\n')
        (package / 'models' / 'agent.py').write_text(
            'from enum import Enum\nclass AgentType(str, Enum):\n    PI = "pi"\n')
        self.state_path = self.workspace / 'gh.json'
        self.terminal_log = self.workspace / 'terminal.jsonl'
        self.state_path.write_text(json.dumps({'sources': {'team/app': [[[]]]}}))
        self.controller_handles = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        controller_handle_path = self.workspace / 'controller-handles.sock'
        self.controller_handles.bind(str(controller_handle_path))
        self.controller_handles.listen()
        self.controller_handles.setblocking(False)
        self.controller_descriptors: list[int] = []
        self.addCleanup(self._close_controller_handles)
        self.env = dict(os.environ,
                        PYTHONPATH=os.pathsep.join((str(external), str(ROOT / 'src'))),
                        PATH=str(self.bin) + os.pathsep + os.environ['PATH'],
                        PI_CODING_AGENT_DIR=str(self.workspace / 'native pi'),
                        XDG_STATE_HOME=str(self.workspace / 'state'),
                        GH_HOST='wrong.example', WATCH_GH_STATE=str(self.state_path),
                        WATCH_TERMINAL_LOG=str(self.terminal_log),
                        WATCH_CONTROLLER_HANDLES=str(controller_handle_path))
        # The external program fixture models a standalone root, not this test runner's ancestry.
        for key in ('PI_AGENT_SHELL_CHILD', 'PI_AGENT_SHELL_DEPTH', 'PI_AGENT_SHELL_MAX_DEPTH'):
            self.env.pop(key, None)
        (self.workspace / 'native pi/extensions').mkdir(parents=True)
        (self.workspace / 'native pi/extensions/agentshell.json').write_text(
            '{"max_sub_agent_depth": 1}')
        self.initialize_profile()
        self.configure()

    def initialize_profile(self):
        # A custom endpoint skips optional HTTP policy discovery; native access stays doubled.
        install_commands(self.bin)
        subprocess.run(['git', 'init', '-q', str(self.workspace)], check=True)
        subprocess.run(['git', '-C', str(self.workspace), 'remote', 'add', 'origin',
                        'git@github.com:team/app.git'], check=True)
        subprocess.run(['git', '-C', str(self.workspace), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.invalid', 'commit', '--allow-empty',
                        '-qm', 'fixture'], check=True)
        state = self.workspace / 'init-gh.json'
        state.write_text('{}')
        (self.bin / 'gh').write_text(INIT_GH)
        result = subprocess.run(
            [sys.executable, '-m', 'forgetful_factory', 'init', '--planning-only',
             '--repo', '.', *INIT_SETTINGS,
             '--forgetful-instance', 'server', '--forgetful-server',
             'https://memory.example/custom-endpoint',
             '--install-role-runtime', '--share-pi-profile', '--check-connection',
             '--forgetful-project', '12', '--grill-me-skill', str(self.grill_skill)],
            cwd=self.workspace,
            env=dict(self.env, GH_STATE=str(state)), input='', capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        (self.bin / 'gh').write_text(GH)

    def configure(self, labels=('factory',), sources=('team/app',), provider='github'):
        directory = self.workspace / '.factory'
        directory.mkdir(exist_ok=True)
        contents = (f'watcher_label = {json.dumps(labels)}\n'
                    'foreman_agent_file = "agents/foreman/agent.json"\n'
                    'execution_enabled = false\n')
        for index, source in enumerate(sources):
            local = self.workspace if index == 0 else self.workspace / f'repository-{index}'
            if not local.exists():
                subprocess.run(['git', 'init', '-q', str(local)], check=True)
                subprocess.run(['git', '-C', str(local), 'remote', 'add', 'origin',
                                f'git@github.com:{source}.git'], check=True)
                subprocess.run(['git', '-C', str(local), '-c', 'user.name=Fixture',
                                '-c', 'user.email=fixture@example.invalid', 'commit',
                                '--allow-empty', '-qm', 'fixture'], check=True)
            contents += ('\n[[repository]]\n'
                         f'local_dir = {json.dumps(str(local))}\n'
                         f'remote = "git@github.com:{source}.git"\n'
                         f'provider = {json.dumps(provider)}\nsource = {json.dumps(source)}\n')
        contents += ('\n[forgetful]\ninstance = "server"\nproject_id = 12\n'
                     'server = "https://memory.example/custom-endpoint"\n')
        (directory / 'factory.toml').write_text(contents)

    def issue(self, number=1, title='Implement feature', labels=('factory',), **extra):
        return {'number': number, 'title': title, 'labels': [{'name': v} for v in labels],
                'html_url': f'https://github.com/team/app/issues/{number}',
                'state': 'open', 'body': 'Issue requirements', **extra}

    def script(self, sources):
        with self.state_path.with_suffix('.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            replacement = self.state_path.with_suffix('.next')
            replacement.write_text(json.dumps({'sources': sources}))
            replacement.replace(self.state_path)

    def events(self):
        if not self.terminal_log.exists():
            return []
        return [json.loads(line) for line in self.terminal_log.read_text().splitlines()]

    def _issue_events(self):
        return [e for e in self.events() if e['kind'] == 'send'
                and e['text'].startswith('Factory issue notification.')]

    def start(self, *arguments, input='', stdout=subprocess.PIPE, cwd=None, deadlines=None):
        entrypoint = (['-m', 'forgetful_factory'] if deadlines is None
                      else programmatic_factory(deadlines))
        process = subprocess.Popen(
            [sys.executable, *entrypoint, 'watch', '--workspace',
             str(self.workspace), '--interval', '0.05', *arguments],
            cwd=cwd or self.workspace, env=self.env, stdin=subprocess.PIPE,
            stdout=stdout, stderr=subprocess.PIPE, text=True,
        )
        self.addCleanup(self.cleanup_process, process)
        if input:
            process.stdin.write(input)
            process.stdin.flush()
        return process

    def cleanup_process(self, process):
        if process.poll() is None:
            process.kill()
        timeout_error = None
        diagnostic = None
        stream_cleanup_errors = []
        owned_cleanup_error = None
        try:
            process.communicate(timeout=15)
        except subprocess.TimeoutExpired as error:
            timeout_error = error
            try:
                diagnostic = self._shutdown_diagnostic(process, error)
            except Exception as diagnostic_error:
                diagnostic = {'diagnostic_error': repr(diagnostic_error)}
        finally:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except Exception as error:
                        stream_cleanup_errors.append(error)
            if timeout_error is not None:
                try:
                    self._close_controller_handles()
                except Exception as error:
                    owned_cleanup_error = repr(error)
        if timeout_error is not None:
            raise AssertionError(
                'Watcher fixture cleanup could not drain pipes: '
                f'{diagnostic}; stream_cleanup_errors={stream_cleanup_errors!r}; '
                f'owned_cleanup_error={owned_cleanup_error}') from timeout_error
        if stream_cleanup_errors:
            raise AssertionError('Watcher fixture stream cleanup failed') \
                from stream_cleanup_errors[0]

    def _collect_controller_handles(self):
        if self.controller_handles is None:
            return
        while True:
            try:
                connection, _ = self.controller_handles.accept()
            except BlockingIOError:
                return
            descriptors = array.array('i')
            retained = None
            try:
                with connection:
                    connection.settimeout(5)
                    credentials = connection.getsockopt(
                        socket.SOL_SOCKET, socket.SO_PEERCRED, 12)
                    peer_pid, peer_uid, _ = struct.unpack('3i', credentials)
                    data, controls, flags, _ = connection.recvmsg(
                        1024, socket.CMSG_SPACE(4))
                for level, kind, payload in controls:
                    if level == socket.SOL_SOCKET and kind == socket.SCM_RIGHTS:
                        descriptors.frombytes(payload[:len(payload) - len(payload) % 4])
                self.assertFalse(flags & socket.MSG_CTRUNC)
                self.assertEqual(len(descriptors), 1)
                self.assertEqual(peer_uid, os.getuid())
                self.assertEqual(json.loads(data)['pid'], peer_pid)
                descriptor = descriptors[0]
                self.assertEqual(
                    os.readlink(f'/proc/self/fd/{descriptor}'), 'anon_inode:[pidfd]')
                with open(f'/proc/self/fdinfo/{descriptor}') as stream:
                    identity = dict(line.split(':', 1) for line in stream if ':' in line)
                pidfd_pid = int(identity['Pid'])
                if pidfd_pid == -1:
                    with selectors.DefaultSelector() as selector:
                        selector.register(descriptor, selectors.EVENT_READ)
                        self.assertTrue(selector.select(0), 'Exited pidfd was not readable')
                else:
                    self.assertEqual(pidfd_pid, peer_pid)
                    self.controller_descriptors.append(descriptor)
                    retained = descriptor
            finally:
                active_error = sys.exception()
                close_errors = []
                for descriptor in descriptors:
                    if descriptor != retained:
                        try:
                            os.close(descriptor)
                        except OSError as error:
                            close_errors.append(error)
                if close_errors:
                    message = 'Could not close rejected controller handles: ' + '; '.join(
                        repr(error) for error in close_errors)
                    if active_error is not None:
                        active_error.add_note(message)
                    else:
                        raise AssertionError(message) from close_errors[0]

    def _close_controller_handles(self):
        from lifecycle_support import pidfd_send_signal

        failures = []
        try:
            self._collect_controller_handles()
        except Exception as error:
            failures.append(error)
        for descriptor in self.controller_descriptors:
            try:
                with selectors.DefaultSelector() as selector:
                    selector.register(descriptor, selectors.EVENT_READ)
                    if not selector.select(0):
                        pidfd_send_signal(descriptor, signal.SIGKILL)
                        if not selector.select(5):
                            failures.append(AssertionError(
                                'Diagnostic controller survived cleanup'))
            except Exception as error:
                failures.append(error)
            finally:
                try:
                    os.close(descriptor)
                except OSError as error:
                    failures.append(error)
        self.controller_descriptors.clear()
        if self.controller_handles is not None:
            try:
                self.controller_handles.close()
            except Exception as error:
                failures.append(error)
            self.controller_handles = None
        if failures:
            raise AssertionError(
                'Controller handle cleanup failed: '
                + '; '.join(repr(error) for error in failures)) from failures[0]

    def wait_until(self, process, predicate, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            self._collect_controller_handles()
            if predicate():
                self._collect_controller_handles()
                return
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                self.fail(f'Watch exited {process.returncode}: {stdout}\n{stderr}')
            time.sleep(0.02)
        self.fail(f'Watch did not reach expected state; terminal events: {self.events()}')

    def _shutdown_diagnostic(self, process, error):
        self._collect_controller_handles()
        with selectors.DefaultSelector() as selector:
            for descriptor in self.controller_descriptors:
                selector.register(descriptor, selectors.EVENT_READ)
            ready = {key.fd for key, _ in selector.select(0)}
        return {
            'root_poll': process.poll(),
            'partial_stdout': str(error.stdout),
            'partial_stderr': str(error.stderr),
            'events': self.events(),
            'controller_exited': [descriptor in ready
                                  for descriptor in self.controller_descriptors],
        }

    def stop(self, process, sig=signal.SIGINT):
        process.send_signal(sig)
        try:
            stdout, stderr = process.communicate(timeout=15)
        except subprocess.TimeoutExpired as error:
            diagnostic = self._shutdown_diagnostic(process, error)
            raise AssertionError(
                f'Watcher shutdown timed out before fixture cleanup: {diagnostic}') from error
        return process.returncode, stdout, stderr


class WatchCliTests(WatchFixture):
    def test_missing_connection_does_not_fall_back_to_personal_pi(self):
        # Arrange
        path = self.workspace / '.factory/factory.toml'
        path.write_text(path.read_text().split('[forgetful]')[0])
        # Act
        process = self.start('--new-only')
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertNotEqual(process.returncode, 0)
        self.assertIn('Forgetful', stderr)
        self.assertEqual(self.events(), [])

    def test_foreman_profile_reaches_agentshell_through_inherited_environment(self):
        # Arrange
        self.env['XDG_CONFIG_HOME'] = str(self.workspace / 'personal-config')
        path = self.workspace / '.factory/factory.toml'
        path.write_text(path.read_text().replace('[forgetful]', '[forgetful]\nmethod = "cli"'))
        (self.workspace / '.factory/agents/foreman/mcp.json').write_text('{"mcpServers": {}}')
        # Act
        process = self.start('--new-only')
        self.wait_until(process, lambda: any(e['kind'] == 'ready' for e in self.events()))
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        launch = self.events()[0]
        self.assertEqual(launch['agent_dir'], str(self.workspace / 'native pi'))
        self.assertEqual(launch['config_home'],
                         str(self.workspace / 'personal-config'))
        self.assertEqual(launch['target'], 'cli')

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
                         (str(self.workspace / '.factory/agents/foreman'),
                          'provider/model', 'high', 'pi'))
        self.assertEqual(launch['placement']['kind'], 'new-session')
        self.assertTrue(sent['submit'])
        self.assertIn('github:team/app#1', sent['text'])
        self.assertIn('Implement feature', sent['text'])
        self.assertIn('https://github.com/team/app/issues/1', sent['text'])
        self.assertIn('Issue requirements', sent['text'])
        self.assertIn('tmux attach', stdout)
        self.assertIn(launch['placement']['name'], stdout)
        self.assertIn('close', stdout.lower())
        self.assertIn('library stdout banner', stderr)
        self.assertNotIn('library stdout banner', stdout)
        calls = json.loads(self.state_path.read_text())['calls']
        self.assertEqual(calls[0], ['api', 'repos/team/app/issues?state=open&per_page=100',
                                    '--hostname', 'github.com', '--paginate', '--slurp'])

    def test_startup_checks_planning_and_waits_for_native_session_readiness(self):
        # Arrange
        gate = self.workspace / 'ready-gate'
        output = self.workspace / 'watch-output'
        commands = self.workspace / 'commands.jsonl'
        self.env.update(WATCH_READY_GATE=str(gate), PROFILE_LOG=str(commands))
        # Act
        with output.open('w') as stream:
            process = self.start('--new-only', stdout=stream)
            self.wait_until(process, lambda: any(e['kind'] == 'launch' for e in self.events()))
            # Assert: launch and unrelated system events are not session readiness.
            self.assertIn('tmux attach-session', output.read_text())
            self.assertNotIn('Foreman session ready', output.read_text())
            # Act
            gate.touch()
            self.wait_until(process, lambda: 'Baseline' in output.read_text())
            code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        text = output.read_text()
        self.assertIn('Foreman session ready; model access unverified.', text)
        self.assertIn('Forgetful planning access checked', text)
        self.assertNotIn('Forgetful: connected', text)
        self.assertLess(text.index('Foreman session ready'), text.index('Baseline'))
        self.assertEqual([e['kind'] for e in self.events()], ['launch', 'ready', 'close'])
        calls = [json.loads(line)['args'] for line in commands.read_text().splitlines()]
        self.assertEqual([c[:2] for c in calls[:2]],
                         [['call', 'get_project'], ['tools', 'list']])
        self.assertFalse(any(c[:2] == ['call', 'get_current_user'] for c in calls))
        self.assertFalse(any(c[:2] == ['auth', 'login'] for c in calls))

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
                (self.workspace / '.factory/fixture-plans.json').unlink(
                    missing_ok=True)
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
        self.wait_until(process, lambda: len(self._issue_events()) == 2)
        code, _, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        self.assertIn('HTTP 503', stderr)
        self.assertIn('retry', stderr.lower())
        sent = [e['text'] for e in self._issue_events()]
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
                (self.workspace / '.factory/fixture-plans.json').unlink(
                    missing_ok=True)
                self.script({'team/app': [malformed, [[self.issue(10)]]]})
                # Act
                process = self.start('--existing')
                self.wait_until(process, lambda: len(self._issue_events()) == 1)
                code, _, stderr = self.stop(process)
                # Assert
                self.assertEqual(code, 130, stderr)
                self.assertIn('malformed', stderr.lower())
                self.assertNotIn('Traceback', stderr)
                self.assertEqual(len(self._issue_events()), 1)
                self.assertEqual(sum(e['kind'] == 'send' for e in self.events()), 2)

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
        script = gh.read_text()
        self.assertEqual(script.count('replacement.replace(path)'), 1)
        gh.write_text(script.replace(
            'replacement.replace(path)',
            'replacement.replace(path)\nimport time; time.sleep(3)'))
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
        script = gh.read_text()
        self.assertEqual(script.count('replacement.replace(path)'), 1)
        gh.write_text(script.replace(
            'replacement.replace(path)',
            'replacement.replace(path)\n'
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
                self.assertNotIn('Foreman session ready', stdout)
                self.assertEqual(json.loads(self.state_path.read_text()).get('calls', []), [])

    def test_readiness_timeout_gives_trust_dialog_help_and_closes_pi(self):
        # Arrange
        self.env['WATCH_NO_READY'] = '1'
        self.script({'team/app': [[[self.issue()]]]})
        deadlines = DeadlinePolicy(agentshell=AgentShellLifecycleDeadlines(
            controller_ready=0.2,
        ))
        # Act
        process = self.start('--existing', deadlines=deadlines)
        stdout, stderr = process.communicate(timeout=5)
        # Assert
        self.assertEqual(process.returncode, 1, stderr)
        self.assertIn('ready', stderr.lower())
        self.assertIn('0.2 seconds', stderr)
        self.assertIn('trust', stderr.lower())
        self.assertIn('new tmux attach-session', stderr)
        self.assertIn('restart watch', stderr.lower())
        old_name = self.events()[0]['placement']['name']
        self.assertNotIn(f'tmux attach-session -t {old_name}', stderr)
        self.assertNotIn('Submitted', stdout)
        self.assertNotIn('Foreman session ready', stdout)
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
        deadlines = DeadlinePolicy(agentshell=AgentShellLifecycleDeadlines(
            controller_send=0.2,
        ))
        # Act
        process = self.start('--existing', deadlines=deadlines)
        stdout, stderr = process.communicate(timeout=5)
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
                deadlines = DeadlinePolicy(agentshell=AgentShellLifecycleDeadlines(
                    controller_close=0.2,
                ))
                # Act
                process = self.start('--existing', deadlines=deadlines)
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
        self.wait_until(process, lambda: len(self._issue_events()) == 1)
        code, stdout, stderr = self.stop(process)
        # Assert
        self.assertEqual(code, 130, stderr)
        sent = self._issue_events()[0]['text']
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
        self.env['WATCH_LAUNCH_DELAY'] = '0.2'
        self.env['WATCH_NO_READY'] = '1'
        deadlines = DeadlinePolicy(agentshell=AgentShellLifecycleDeadlines(
            controller_ready=1,
            parent_ready=1,
        ))
        # Act
        process = self.start('--existing', deadlines=deadlines)
        stdout, stderr = process.communicate(timeout=5)
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
