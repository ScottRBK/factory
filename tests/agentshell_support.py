"""External tmux/Pi doubles; AgentShell and its worker/lifecycle run unchanged."""
import contextlib
import os
import signal
import time


def stop_terminal_fixture(root):
    """Reap the detached test PTY before TemporaryDirectory removes its log directory."""
    pid_file = root / 'native-pid'
    if not pid_file.exists():
        return
    with contextlib.suppress(ProcessLookupError):
        os.killpg(int(pid_file.read_text()), signal.SIGTERM)
    deadline = time.monotonic() + 5
    while not (root / 'host-exited').exists():
        if time.monotonic() >= deadline:
            raise AssertionError('External test PTY did not finish cleanup')
        time.sleep(0.02)


TMUX = r'''#!/usr/bin/env python3
import json
import os
from pathlib import Path
import pty
import select
import shlex
import subprocess
import sys
import time

root = Path(os.environ['TERMINAL_FIXTURE'])
root.mkdir(exist_ok=True)
args = sys.argv[1:]
if args[:1] == ['fixture-host']:
    pid, master = pty.fork()
    if pid == 0:
        os.environ.update(TMUX=str(root / 'socket') + ',1,0', TMUX_PANE='%1')
        os.execv(args[1], args[1:])
    (root / 'native-pid').write_text(str(pid))
    offset = 0
    try:
        while True:
            if select.select([master], [], [], 0.02)[0]:
                try:
                    if not os.read(master, 65536):
                        break
                except OSError:
                    break
            incoming = root / 'input'
            if incoming.exists():
                data = incoming.read_bytes()
                if len(data) > offset:
                    os.write(master, data[offset:])
                    offset = len(data)
    finally:
        os.close(master)
        os.waitpid(pid, 0)
        (root / 'host-exited').touch()
    sys.exit(0)
while args and args[0] in ('-f', '-S'):
    args = args[2:]
with (root / 'commands.jsonl').open('a') as log:
    log.write(json.dumps(args) + '\n')
if args[0] == 'new-session':
    subprocess.Popen([sys.executable, __file__, 'fixture-host',
                      *args[args.index('--') + 1:]],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, start_new_session=True)
    print('$1\t@1\t%1\t' + str(root / 'socket'))
elif args[0] == 'display-message':
    print(str(root / 'socket') + '\t%1\t1\t1\t1\t0'
          if 'socket_path' in args[-1] else '%1')
elif args[0] == 'load-buffer':
    (root / args[args.index('-b') + 1]).write_bytes(sys.stdin.buffer.read())
elif args[0] == 'delete-buffer':
    (root / args[args.index('-b') + 1]).unlink(missing_ok=True)
elif args[0] == 'if-shell':
    command = shlex.split(args[-1])
    if command[0] == 'paste-buffer':
        with (root / 'input').open('ab') as stream:
            stream.write((root / command[command.index('-b') + 1]).read_bytes())
    if command[0] == 'send-keys':
        with (root / 'input').open('ab') as stream:
            stream.write(b'\n')
    if 'display-message' in command:
        print(command[-1])
else:
    sys.exit('Unsupported fixture tmux operation')
'''

PI_INTERACTIVE = r'''
elif name == 'pi' and '--extension' in args:
    import time
    observer = next(Path(args[i + 1]) for i, arg in enumerate(args)
                    if arg == '--extension' and args[i + 1].endswith('pi-events.mjs'))
    with observer.with_name('events.jsonl').open('a') as stream:
        stream.write(json.dumps({'type': 'session_start', 'session_id': 'fixture-pi'}) + '\n')
    while True:
        time.sleep(0.1)
'''
