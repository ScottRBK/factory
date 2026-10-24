"""Bounded local control of the init-owned Foreman. No PID-based process control."""
import json
import os
import shlex
import socket
import stat
import struct
import subprocess
import sys
from pathlib import Path

from forgetful_factory.adapters.filesystem.foreman_runtime import runtime_directory
from forgetful_factory.adapters.filesystem.resource_files import read_generated_json
from forgetful_factory.domain.models import FactoryError


def _reply(stream) -> dict:
    try:
        line = stream.readline(65537)
        if len(line) > 65536 or not line.endswith(b'\n'):
            raise ValueError('Missing or oversized frame')
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError('Expected an object')
        if 'error' in value:
            if not isinstance(value['error'], str):
                raise ValueError('Expected an error message')
        elif (not isinstance(value.get('run_id'), str)
                or value.get('foreman') not in (
                    'starting', 'ready', 'stopping', 'stopped', 'unknown')
                or value.get('watcher') not in (
                    'starting', 'running', 'stopping', 'stopped', 'failed')
                or not isinstance(value.get('target'), (dict, type(None)))):
            raise ValueError('Invalid state fields')
        target = value.get('target')
        if target is not None and (
                not isinstance(target, dict) or not isinstance(target.get('socket_path'), str)
                or not target['socket_path'].startswith('/')
                or not isinstance(target.get('pane_id'), str)
                or not target['pane_id'].startswith('%') or not target['pane_id'][1:].isdigit()
                or any(type(target.get(key)) is not int or target[key] <= 0
                       for key in ('server_pid', 'server_started', 'pane_pid'))):
            raise ValueError('Invalid captured terminal identity')
        if value.get('foreman') == 'ready' and target is None:
            raise ValueError('Ready Foreman requires a captured target')
        return value
    except (ValueError, TypeError) as error:
        raise FactoryError('Invalid Foreman control reply; operation unconfirmed. '
                           'Preserve the recorded owner and terminal.') from error


def read_state(workspace: Path) -> dict | None:
    directory = runtime_directory(workspace)
    path = directory / 'owner.json'
    try:
        state = read_generated_json(path)
    except FileNotFoundError:
        if (directory / 'control.sock').exists():
            raise FactoryError('Unidentified Foreman socket; preserve it and reconcile manually.')
        return None
    except (ValueError, OSError) as error:
        raise FactoryError('Invalid owner state; preserve and reconcile manually.') from error
    if (not isinstance(state, dict) or state.get('workspace') != str(workspace)
            or not isinstance(state.get('run_id'), str) or not state['run_id']):
        raise FactoryError('Foreman owner identity mismatch; state was preserved.')
    return state


def request(workspace: Path, operation: str, **fields) -> dict:
    state = read_state(workspace)
    if state is None:
        raise FactoryError('No Foreman owner; complete first setup with init --finalize if needed, '
                           'then use foreman '
                           f'--workspace {shlex.quote(str(workspace))}. '
                           'Use foreman --attach for an existing owner.')
    path = runtime_directory(workspace) / 'control.sock'
    try:
        info = path.lstat()
        if (not stat.S_ISSOCK(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) & 0o077):
            raise FactoryError('Foreman control socket identity is invalid; preserved.')
        with socket.socket(socket.AF_UNIX) as connection:
            connection.settimeout(40 if operation == 'start' else 15 if operation == 'stop' else 5)
            connection.connect(str(path))
            _, uid, _ = struct.unpack('3i', connection.getsockopt(
                socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i')))
            if uid != os.getuid():
                raise FactoryError('Foreman control peer is not the current user.')
            connection.sendall((json.dumps({'operation': operation, 'run_id': state['run_id'],
                                           'workspace': str(workspace), **fields}) + '\n').encode())
            with connection.makefile('rb') as stream:
                result = _reply(stream)
    except (OSError, ValueError) as error:
        raise FactoryError('Foreman owner unavailable; terminal state is uncertain. '
                           'Do not replace it from saved PIDs. Inspect its terminal.') from error
    if result.get('run_id') != state['run_id']:
        raise FactoryError('Foreman owner changed; operation not confirmed.')
    if 'error' in result:
        raise FactoryError(result['error'])
    return result


def start_owner(workspace: Path, python: str, environment: dict, launch: dict) -> dict:
    try:
        checked = subprocess.run([python, '-u', str(Path(__file__).with_name('controller.py')),
                                  '--check'], env=environment, stdin=subprocess.DEVNULL,
                                 capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise FactoryError('AgentShell interpreter preflight failed; no Foreman launched. '
                           'Correct --agentshell-python and retry foreman; '
                           'use init --finalize for incomplete first setup.') from error
    if checked.returncode or checked.stdout.strip() != 'Factory AgentShell ready':
        raise FactoryError('AgentShell interpreter preflight failed; no Foreman launched. '
                           'Select an installed compatible --agentshell-python and retry.')
    directory = runtime_directory(workspace, create=True)
    log_path = directory / 'owner.log'
    descriptor = os.open(log_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    info = os.fstat(descriptor)
    if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
            or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) & 0o077):
        os.close(descriptor)
        raise FactoryError('Foreman log must be private with no additional hard links.')
    parent, child = socket.socketpair()
    process = None
    adopted = False
    try:
        with os.fdopen(descriptor, 'ab', buffering=0) as log:
            process = subprocess.Popen(
                [sys.executable, '-m', 'forgetful_factory.adapters.agentshell.owner',
                 str(workspace), python, str(child.fileno())], pass_fds=(child.fileno(),),
                stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True,
                env=environment)
        child.close()
        parent.settimeout(40)
        parent.sendall((json.dumps(launch) + '\n').encode())
        with parent.makefile('rb') as stream:
            result = _reply(stream)
            if 'error' in result:
                raise FactoryError(result['error'])
            parent.sendall(b'adopt\n')
            if stream.readline(100) != b'adopted\n':
                raise FactoryError('Foreman handover failed; check its private owner log.')
            adopted = True
        return result
    except (OSError, ValueError) as error:
        raise FactoryError('Foreman startup failed; inspect .factory/runtime/foreman/owner.log.') \
            from error
    finally:
        parent.close()
        child.close()
        if process is not None and not adopted:
            try:
                # Cover owner watcher-stop (up to 15s), controller-close (20s), and escalation
                # (5s), leaving room for scheduling and the final saved-state/socket cleanup.
                process.wait(timeout=45)
            except subprocess.TimeoutExpired:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    raise FactoryError('Foreman cleanup is uncertain; inspect owner.log. '
                                       'No replacement was started.') from None
        # Before adoption the owner treats handover EOF as cancellation, closing its controller.
        # After adoption it deliberately ignores init's descriptor/process lifetime.


def enter_terminal(target: dict) -> None:
    """Client navigation only. All delivery belongs to AgentShell."""
    command = ['tmux', '-S', target['socket_path'], 'attach-session', '-t', target['pane_id']]
    print('Enter Foreman: ' + shlex.join(command), flush=True)
    if not sys.stdin.isatty():
        return
    current = os.environ.get('TMUX', '').rsplit(',', 2)
    if len(current) == 3:
        if current[0] != target['socket_path']:
            print('Run that command from a terminal outside your current tmux server.')
            return
        command[3] = 'switch-client'
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise FactoryError('Could not enter Foreman; it remains alive. Use the printed command.')
