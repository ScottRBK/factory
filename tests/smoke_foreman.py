"""Opt-in public init/watch smoke with installed Pi 1.3 and AgentShell 0.5; no inference.

Requires existing Pi, tmux, Forgetful, uv 0.13.5, uv dependencies and FastEmbed model cache:
  PYTHONPATH=src .venv/bin/python tests/smoke_foreman.py --uv /path/to/audited/uv
    --forgetful /path/to/forgetful --model-cache /path/to/existing/fastembed/cache
The reviewed bundled 0.5 worker lock is installed offline into a disposable role venv.
Only the temporary agent.json selects the TEST-ONLY input interceptor. Normal launch
instructions load from the native role cwd. Synthetic model credentials target a loopback recorder;
every input is handled before inference and the recorder must receive ZERO requests.
Evidence and all settings stay under /tmp. An isolated tmux socket avoids existing user sessions.
"""
import argparse
import asyncio
import contextlib
import hashlib
import importlib.metadata
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from test_init import GH
from test_watch import GH as WATCH_GH

from forgetful_factory.configuration import load_configuration

MODEL = 'factory-smoke/no-inference'
ROLE_EXTENSIONS = ['../../resources/agentshell/extensions/agentshell.ts',
                   '../../resources/hide-tools/index.ts',
                   '../../resources/pi-forgetful/factory.ts']
# Test instrumentation only: never copied into production resources or selected automatically.
PROBE = r'''import fs from "node:fs";
export default function(pi) {
  let sequence = 0;
  pi.on("input", async (event, ctx) => {
    const result = {text: event.text, source: event.source};
    try {
      result.tools = pi.getAllTools();
      result.commands = pi.getCommands();
      result.prompt = ctx.getSystemPrompt();
      result.argv = process.argv;
      result.cwd = ctx.cwd;
      result.role = process.env.FACTORY_ROLE_DIR;
      result.home = process.env.PI_CODING_AGENT_DIR;
      result.xdg = process.env.XDG_CONFIG_HOME ?? null;
      result.rosterFile = process.env.PI_AGENTSHELL_ROSTER_FILE;
      result.roster = JSON.parse(fs.readFileSync(result.rosterFile, "utf8"));
      result.model = {provider: ctx.model?.provider, id: ctx.model?.id};
      // Execute the native CLI exactly as the role skill instructs, without a Factory wrapper.
      result.cli = await pi.exec("bash", ["-c", `(
        cd "$FACTORY_FORGETFUL_DIR" || exit
        XDG_CONFIG_HOME="$FACTORY_FORGETFUL_CONFIG_DIR" "$FACTORY_FORGETFUL_EXECUTABLE" \
          project list --local --json
      )`], {timeout: 30000});
    } catch (error) {
      result.error = String(error);
    }
    try {
      const path = `${process.env.FACTORY_SMOKE_EVIDENCE}/probe-${++sequence}.json`;
      fs.writeFileSync(path + ".tmp", JSON.stringify(result, null, 2));
      fs.renameSync(path + ".tmp", path);
      ctx.ui.notify("FACTORY_SMOKE_INPUT_HANDLED", "info");
    } finally {
      // Even a failed observation must never fall through to the provider.
      return {action: "handled"};
    }
  });
}
'''


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')


def command(path: Path, content: str) -> None:
    path.write_text(content)
    path.chmod(0o700)


def skill(path: Path, name: str, marker: str) -> None:
    path.mkdir(parents=True)
    (path / 'SKILL.md').write_text(f'---\nname: {name}\ndescription: {marker}\n---\nProbe.\n')


@contextlib.contextmanager
def provider_recorder(evidence: Path):
    """No provider implementation: record and reject any accidental HTTP request."""
    requests = []
    write_json(evidence / 'provider-requests.json', requests)

    class Recorder(BaseHTTPRequestHandler):
        def reject(self):
            requests.append({'method': self.command, 'path': self.path})
            write_json(evidence / 'provider-requests.json', requests)
            self.send_response(503)
            self.end_headers()

        do_GET = do_POST = do_PUT = do_DELETE = do_CONNECT = do_HEAD = do_OPTIONS = reject

        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), Recorder)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        if requests:
            raise AssertionError('Unexpected network requests; see provider-requests.json')


def prepare(evidence: Path, executable: str, model_cache: Path, uv: str,
            uv_cache: Path, endpoint: str) -> tuple[Path, dict[str, str]]:
    root = Path(__file__).resolve().parents[1]
    home, commands = evidence / 'home', evidence / 'commands'
    repo, pi_home = home / 'repo', home / '.pi/agent'
    for path in (repo, pi_home, commands):
        path.mkdir(parents=True)
    cache = evidence / 'model-cache'
    subprocess.run(['cp', '-a', '--reflink=auto', str(model_cache), str(cache)], check=True)
    command(commands / 'gh', GH)
    write_json(evidence / 'gh.json', {})
    # Use only selected executable directories, and never inherit credentials, TMUX or settings.
    path = os.pathsep.join(dict.fromkeys((str(commands), str(Path(shutil.which('pi')).parent),
                                         str(Path(sys.executable).parent), '/usr/bin', '/bin')))
    env = {'HOME': str(home), 'PATH': path, 'PYTHONPATH': str(root / 'src'),
           'PYTHONDONTWRITEBYTECODE': '1', 'GH_STATE': str(evidence / 'gh.json'),
           'PI_OFFLINE': '1', 'PI_CODING_AGENT_DIR': str(pi_home), 'TERM': 'xterm-256color',
           'HF_HUB_OFFLINE': '1', 'HF_HUB_DISABLE_TELEMETRY': '1',
           'FASTEMBED_LOCAL_FILES_ONLY': 'true', 'FASTEMBED_CACHE_DIR': str(cache),
           'UV_OFFLINE': '1', 'UV_PYTHON_DOWNLOADS': 'never', 'PIP_NO_INDEX': '1',
           'NPM_CONFIG_OFFLINE': 'true', 'GIT_CONFIG_NOSYSTEM': '1',
           'GIT_CONFIG_GLOBAL': '/dev/null', 'FACTORY_SMOKE_EVIDENCE': str(evidence),
           'HTTP_PROXY': endpoint, 'HTTPS_PROXY': endpoint, 'ALL_PROXY': endpoint,
           'NO_PROXY': '127.0.0.1,localhost', 'LANG': 'C.UTF-8', 'SHELL': '/bin/bash'}
    # CLI flags keep the installer offline even when production sanitizes package-manager env.
    command(commands / 'uv', '#!/bin/sh\n'
            f'printf "%s\\n" "$*" >> {shlex.quote(str(evidence / "uv-commands.log"))}\n'
            f'exec {shlex.quote(uv)} --offline --cache-dir {shlex.quote(str(uv_cache))} "$@"\n')
    # AgentShell invokes tmux itself; route *all* its operations to this disposable server.
    command(commands / 'tmux', '#!/bin/sh\n'
            f'exec {shlex.quote(shutil.which("tmux"))} '
            f'-S {shlex.quote(str(evidence / "tmux.sock"))} -f /dev/null "$@"\n')
    for name in ('npm', 'npx', 'uvx', 'pip', 'pip3'):
        command(commands / name, '#!/bin/sh\necho "Network/package install forbidden" >&2\n'
                'exit 97\n')
    for args in (['init', '-q'], ['remote', 'add', 'origin', 'git@github.com:team/app.git']):
        subprocess.run(['git', '-C', str(repo), *args], check=True, env=env)
    write_json(pi_home / 'settings.json', {'defaultProjectTrust': 'always'})
    # A made-up provider with a literal dummy key supports native listing without login/refresh.
    write_json(pi_home / 'models.json', {'providers': {'factory-smoke': {
        'baseUrl': endpoint + '/v1', 'api': 'openai-completions',
        'apiKey': 'synthetic-smoke-only', 'models': [{'id': 'no-inference'}],
    }}})
    write_json(pi_home / 'extensions/agentshell.json', {'max_sub_agent_depth': 1})
    grill = evidence / 'grill-me/SKILL.md'
    grill.parent.mkdir()
    grill.write_text('---\nname: grill-me\ndescription: Synthetic smoke interview source.\n'
                     'disable-model-invocation: true\n---\nAsk the user for clarification.\n')
    (repo / 'README.md').write_text('Disposable Factory smoke repository.\n')
    subprocess.run(['git', '-C', str(repo), 'add', 'README.md'], check=True, env=env)
    subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Factory smoke',
                    '-c', 'user.email=smoke@example.invalid', 'commit', '-qm', 'Initial'],
                   check=True, env=env)
    role = repo / '.factory/agents/foreman'
    role.mkdir(parents=True)
    database = repo / '.factory/data/forgetful.db'
    database.parent.mkdir()
    native_env = dict(env, XDG_CONFIG_HOME=str(repo / '.factory/cli-config'), DATABASE='SQLite',
                      SQLITE_PATH=str(database), SQLITE_MEMORY='false', PLANNING_ENABLED='true')
    project_command = [executable, 'call', 'create_project', '--args', json.dumps({
        'name': 'Disposable Factory smoke', 'description': 'Offline public init/watch validation',
        'project_type': 'development'}), '--local', '--json']
    write_json(evidence / 'project-command.json', project_command)
    project = subprocess.run(project_command, cwd=role, env=native_env, capture_output=True,
                             text=True, timeout=60)
    (evidence / 'project.log').write_text(project.stdout + project.stderr)
    project.check_returncode()
    project_id = json.loads(project.stdout)['id']
    write_json(evidence / 'project.json', json.loads(project.stdout))
    versions = {'agentshell': importlib.metadata.version('agent-shell-py')}
    for name, args in (('pi', ['pi', '--version']), ('uv', [uv, '--version']),
                       ('forgetful', [executable, '--version'])):
        versions[name] = subprocess.check_output(args, env=env, cwd=repo, text=True).strip()
    write_json(evidence / 'versions.json', versions)
    if (versions['agentshell'] != '0.5.0' or versions['pi'] != '1.3.0'
            or not versions['uv'].startswith('uv 0.13.5 ')
            or not re.search(r'\b0\.5\.5\b', versions['forgetful'])):
        raise AssertionError('Expected Pi 1.3.0, AgentShell 0.5.0, Forgetful 0.5.5 and uv 0.13.5')
    init_command = [sys.executable, '-m', 'forgetful_factory', 'init', '--planning-only',
         '--workspace', str(repo),
         '--repo', str(repo), '--label', 'factory', '--foreman-model', MODEL,
         '--foreman-effort', 'low', '--forgetful-instance', 'local',
         '--forgetful-executable', executable, '--install-role-runtime',
         '--forgetful-method', 'cli', '--share-pi-profile', '--pi-agent-dir', str(pi_home),
         '--forgetful-project', str(project_id), '--grill-me-skill', str(grill)]
    write_json(evidence / 'init-command.json', init_command)
    result = subprocess.run(init_command,
        cwd=repo, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=180)
    (evidence / 'init.log').write_text(result.stdout + result.stderr)
    if result.returncode:
        raise RuntimeError(f'Initialization failed; see {evidence}/init.log')
    if 'Forgetful: connected' not in result.stdout or MODEL not in result.stdout:
        raise AssertionError('Native model listing or local CLI initialization check failed')
    config = load_configuration(repo)
    definition = Path(config.foreman_agent_file)
    document = json.loads(definition.read_text())
    if config.forgetful.method != 'cli' or document['agent']['model'] != MODEL:
        raise AssertionError('Public configuration did not retain CLI/model selection')
    role = repo / '.factory/agents/foreman'
    resources = document['agent']['resources']
    if (resources['extensions'] != ROLE_EXTENSIONS
            or resources['skills'] != ['./skills']):
        raise AssertionError('Unexpected generated role resources')
    if (role / 'resources/factory-status.ts').exists():
        raise AssertionError('A production Factory status extension was generated')
    # Check installed runtime and unmodified reviewed inputs, without inventing setup receipts.
    worker = repo / '.factory/resources/agentshell/python'
    versions['worker_agentshell'] = subprocess.check_output(
        [str(worker / '.venv/bin/python'), '-I', '-B', '-c',
         'import importlib.metadata; print(importlib.metadata.version("agent-shell-py"))'],
        env=env, cwd=role, text=True).strip()
    manifest_path = root / 'src/forgetful_factory/resources/role-resources.json'
    manifest = json.loads(manifest_path.read_text())
    for name in ('pyproject.toml', 'uv.lock'):
        digest = hashlib.sha256((worker / name).read_bytes()).hexdigest()
        if digest != manifest['agentshell']['files'][f'python/{name}']:
            raise AssertionError('Bundled worker lock/project changed')
    write_json(evidence / 'versions.json', versions)
    if versions['worker_agentshell'] != '0.5.0':
        raise AssertionError('Expected audited worker AgentShell 0.5.0')
    add_test_resources(evidence, repo, resources)
    result = subprocess.run(init_command, cwd=repo, env=env, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, timeout=180)
    (evidence / 'reinit.log').write_text(result.stdout + result.stderr)
    result.check_returncode()
    add_excluded_resources(evidence, repo, pi_home)
    command(commands / 'gh', WATCH_GH)
    write_json(evidence / 'watch-gh.json', {'sources': {'team/app': [[[
        {'number': 1, 'state': 'open', 'title': 'Smoke feature',
         'body': 'Plan without model inference.',
         'html_url': 'https://github.com/team/app/issues/1',
         'updated_at': '2026-10-17T12:00:00Z', 'labels': [{'name': 'factory'}]}
    ]]]}})
    env['WATCH_GH_STATE'] = str(evidence / 'watch-gh.json')
    return repo, env


def add_test_resources(evidence: Path, repo: Path, resources: dict) -> None:
    """Select test instrumentation directly in the root definition; init does not reconcile it."""
    (repo / 'AGENTS.md').write_text('REPOSITORY_INSTRUCTION_SENTINEL\n')
    selected = repo / '.pi/skills/selected-probe'
    skill(selected, 'selected-probe', 'EXPLICIT_REPOSITORY_SKILL_SENTINEL')
    role = repo / '.factory/agents/foreman'
    probe = evidence / 'input-probe.ts'
    probe.write_text(PROBE)
    resources['skills'].append(str(selected))
    resources['extensions'].append(str(probe))
    definition = role / 'agent.json'
    document = json.loads(definition.read_text())
    document['agent']['resources'] = resources
    write_json(definition, document)


def add_excluded_resources(evidence: Path, repo: Path, pi_home: Path) -> None:
    """Add automatic-discovery sentinels after the final native model listing."""
    (pi_home / 'SYSTEM.md').write_text('EXCLUDED_PERSONAL_SYSTEM_PROMPT\n')
    (pi_home / 'APPEND_SYSTEM.md').write_text('PERSONAL_APPEND_INSTRUCTION_SENTINEL\n')
    (pi_home / 'AGENTS.md').write_text('PERSONAL_AGENTS_INSTRUCTION_SENTINEL\n')
    # Both Pi-native and cross-agent automatic discovery locations must stay excluded.
    for base, name in ((pi_home, 'personal'), (repo / '.pi', 'project'),
                       (pi_home.parents[1] / '.agents', 'personal-shared'),
                       (repo / '.agents', 'project-shared')):
        skill(base / 'skills' / name, name, f'EXCLUDED_{name.upper()}_SKILL')
    for base, name in ((pi_home, 'personal'), (repo / '.pi', 'project')):
        extension = base / 'extensions' / f'{name}.ts'
        extension.parent.mkdir(parents=True, exist_ok=True)
        extension.write_text('import fs from "node:fs";\nexport default function(pi) {\n'
                             f'fs.writeFileSync({json.dumps(str(evidence / (name + "-leaked")))}, '
                             '"LOADED");\n'
                             f'pi.registerCommand("excluded-{name}", '
                             '{description: "Must not load", handler: async () => {}});\n}\n')
        # Local marker processes are harmless, but any launch proves --no-mcp was ineffective.
        marker = str(evidence / (name + '-mcp-leaked'))
        write_json(base / 'mcp.json', {'mcpServers': {name: {
            'command': sys.executable,
            'args': ['-I', '-B', '-c', f'from pathlib import Path; Path({marker!r}).touch()'],
        }}})


async def wait_json(path: Path) -> dict:
    async with asyncio.timeout(40):
        while not path.exists():
            await asyncio.sleep(.1)
    return json.loads(path.read_text())


def check_scaffold(evidence: Path, repo: Path, env: dict, message: dict) -> None:
    """Observe durable records through the real public CLI after native input interception."""
    config = load_configuration(repo)
    role = repo / '.factory/agents/foreman'
    native_env = dict(env, XDG_CONFIG_HOME=str(repo / '.factory/cli-config'), DATABASE='SQLite',
                      SQLITE_PATH=config.forgetful.database, SQLITE_MEMORY='false',
                      PLANNING_ENABLED='true')
    records = {}
    for tool, arguments in (
        ('get_plan', {'plan_id': message['plan_id']}),
        ('query_tasks', {'plan_id': message['plan_id']}),
        ('get_task', {'task_id': message['ownership_task_id']}),
    ):
        args = [config.forgetful.executable, 'call', tool, '--args', json.dumps(arguments),
                '--local', '--json']
        result = subprocess.run(args, cwd=role, env=native_env, capture_output=True,
                                text=True, timeout=45)
        (evidence / f'{tool}.log').write_text(result.stdout + result.stderr)
        result.check_returncode()
        records[tool] = json.loads(result.stdout)
    plan, task = records['get_plan'], records['get_task']
    if (plan['external_ref'] != 'github:team/app#1'
            or plan['project_id'] != config.forgetful.project_id
            or task['plan_id'] != plan['id']
            or [row['id'] for row in records['query_tasks']['tasks']] != [task['id']]):
        raise AssertionError('Notification does not identify the real plan and ownership task')
    mapping, = message['worktrees']
    if json.loads(task['description'])['worktrees'] != [mapping]:
        raise AssertionError('Ownership mapping was not durable before notification')
    actual_branch = subprocess.check_output(
        ['git', '-C', mapping['path'], 'branch', '--show-current'], env=env, text=True).strip()
    tree_list = subprocess.check_output(
        ['git', '-C', str(repo), 'worktree', 'list', '--porcelain', '-z'], env=env)
    (evidence / 'worktrees.porcelain').write_bytes(tree_list)
    if (actual_branch != 'factory/team-app-1' or actual_branch != mapping['branch']
            or f'worktree {mapping["path"]}\0'.encode() not in tree_list):
        raise AssertionError('Native Git worktree does not match the durable ownership mapping')
    write_json(evidence / 'scaffold.json', records | {'actual_branch': actual_branch})


def tmux(env: dict, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(['tmux', *args], env=env, check=check, capture_output=True,
                          text=True, timeout=5)


def check_probe(data: dict, evidence: Path, repo: Path, env: dict) -> None:
    if 'error' in data:
        raise AssertionError(f'Native probe failed: {data["error"]}')
    tools = {tool['name'] for tool in data['tools']}
    required = {'read', 'bash', 'edit', 'write', 'subagent', 'subagent_status', 'subagent_roster'}
    if not required <= tools:
        raise AssertionError('Missing native tools or actual AgentShell role extension')
    if (any(name.startswith('mcp__') for name in tools)
            or tools & {'list_mcp_resources', 'list_mcp_resource_templates', 'read_mcp_resource'}):
        raise AssertionError('Native MCP tools leaked into the session')
    commands = {entry['name'] for entry in data['commands']}
    if not {'hide-tools', 'skill:foreman', 'skill:factory-maintenance',
            'skill:selected-probe'} <= commands:
        raise AssertionError('Explicit role extensions/skills or repository skill did not load')
    if 'mcp' in commands:
        raise AssertionError('Native /mcp unexpectedly available')
    if any('excluded' in name or name.startswith(('skill:personal', 'skill:project'))
           for name in commands):
        raise AssertionError('Automatic personal/project resources leaked')
    for marker in ('REPOSITORY_INSTRUCTION_SENTINEL', 'EXPLICIT_REPOSITORY_SKILL_SENTINEL',
                   'PERSONAL_APPEND_INSTRUCTION_SENTINEL', 'PERSONAL_AGENTS_INSTRUCTION_SENTINEL'):
        if marker not in data['prompt']:
            raise AssertionError(f'Missing prompt content: {marker}')
    if 'EXCLUDED_' in data['prompt'] or list(evidence.glob('*-leaked')):
        raise AssertionError('Excluded automatic skill/extension/MCP loaded')
    role = repo / '.factory/agents/foreman'
    command_paths = {entry['name']: entry['sourceInfo']['path'] for entry in data['commands']}
    expected = {'agentshell-jobs': (role / ROLE_EXTENSIONS[0]).resolve(),
                'hide-tools': (role / ROLE_EXTENSIONS[1]).resolve(),
                'skill:foreman': role / 'skills/foreman/SKILL.md',
                'skill:factory-maintenance': role / 'skills/factory-maintenance/SKILL.md',
                'skill:selected-probe': repo / '.pi/skills/selected-probe/SKILL.md'}
    if any(command_paths.get(name) != str(path) for name, path in expected.items()):
        raise AssertionError('Native commands did not come from the selected local resources')
    if not {'--no-extensions', '--no-skills', '--no-mcp', '--system-prompt'} <= set(data['argv']):
        raise AssertionError('Public watcher launch did not apply native resource exclusions')
    if data['argv'][data['argv'].index('--system-prompt') + 1] != '':
        raise AssertionError('Personal SYSTEM.md discovery was not disabled')
    if (data['role'] != str(repo / '.factory') or data['home'] != env['PI_CODING_AGENT_DIR']
            or data['role'] == data['home'] or data['cwd'] != str(role) or data['xdg'] is not None):
        raise AssertionError('Role cwd/XDG configuration was conflated with the shared Pi home')
    if data['model'] != {'provider': 'factory-smoke', 'id': 'no-inference'}:
        raise AssertionError('Session did not select the loopback dummy model')
    result = data['cli']
    if result['code'] or result['killed']:
        raise AssertionError('Native role CLI failed; see probe CLI output')
    projects = json.loads(result['stdout'])['projects']
    expected_project = json.loads((evidence / 'project.json').read_text())['id']
    if [project['id'] for project in projects] != [expected_project]:
        raise AssertionError('Native role CLI did not share the provisioned project')
    if '# Factory Foreman' not in data['prompt']:
        raise AssertionError('Native Foreman AGENTS.md was not loaded')
    if data['rosterFile'] != str(role / 'agent.json'):
        raise AssertionError('Native child roster selector was not forwarded')
    reference, = data['roster']['roster']['roles']
    if reference != {'agent_file': '../feature-owner/agent.json'}:
        raise AssertionError('Unexpected normalized owner reference')
    owner_file = role / reference['agent_file']
    owner_document = json.loads(owner_file.read_text())
    owner = owner_document['agent']
    if owner['name'] != 'feature-owner' or owner['cwd'] != '.':
        raise AssertionError('Foreman did not select the owner role directory')
    resources = owner['resources']
    for flag in ('inherit_personal_resources', 'inherit_project_resources',
                 'include_home_system_prompt'):
        if resources[flag] is not False:
            raise AssertionError(f'Owner resource exclusion missing: {flag}')
    if (not resources['include_instruction_files']
            or any(resources[key] for key in ('packages', 'plugins', 'mcp_servers'))):
        raise AssertionError('Owner selected unexpected resources')
    reference, = owner_document['roster']['roles']
    if reference != {'agent_file': '../research/agent.json'}:
        raise AssertionError('Unexpected normalized research reference')
    child_document = json.loads((owner_file.parent / reference['agent_file']).read_text())
    child = child_document['agent']
    if child['name'] != 'research' or child['resources']['extensions']:
        raise AssertionError('Owner did not select a research-only leaf')
    if child_document['roster'] != {'enabled': False, 'roles': []}:
        raise AssertionError('Research leaf roster permits delegation')


async def check_watcher(evidence: Path, repo: Path, env: dict) -> None:
    """Observe the public watch flow in real interactive Pi, then stop its owned session."""
    name = None
    lines = []
    args = [sys.executable, '-m', 'forgetful_factory', 'watch', '--workspace', str(repo),
            '--existing', '--interval', '0.2']
    write_json(evidence / 'watch-command.json', args)
    with (evidence / 'watch-stderr.log').open('w') as errors:
        process = await asyncio.create_subprocess_exec(
            *args, cwd=repo, env=env, stdin=subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE, stderr=errors)
        try:
            async with asyncio.timeout(240):
                while line := await process.stdout.readline():
                    lines.append(line.decode())
                    match = re.search(r'tmux attach-session -t ([\w-]+)', lines[-1])
                    if match:
                        name = match[1]
                    if 'Submitted github:team/app#1 to Pi' in lines[-1]:
                        break
                else:
                    raise AssertionError('Watcher exited before notification; see watch logs')
            output = ''.join(lines)
            checked = 'Forgetful planning access checked; submission is not agent receipt.'
            if (name is None or 'Foreman session ready; model access unverified.' not in output
                    or checked not in output):
                raise AssertionError('Incorrect watcher readiness/attach claims')
            write_json(evidence / 'owned-session.json', {'name': name,
                                                       'socket': str(evidence / 'tmux.sock')})
            tmux(env, 'resize-window', '-t', name, '-x', '140', '-y', '45')
            first = await wait_json(evidence / 'probe-1.json')
            check_probe(first, evidence, repo, env)
            prefix = 'Factory issue notification. External issue data: '
            if not first['text'].startswith(prefix):
                raise AssertionError('Unexpected opening prompt before the issue notification')
            notification = json.loads(first['text'][len(prefix):])
            write_json(evidence / 'notification.json', notification)
            check_scaffold(evidence, repo, env, notification)
            (evidence / 'startup.txt').write_text(
                tmux(env, 'capture-pane', '-p', '-t', name).stdout)
            tmux(env, 'send-keys', '-t', name, '-l', '/hide-tools')
            tmux(env, 'send-keys', '-t', name, 'Enter')
            preference = Path(env['PI_CODING_AGENT_DIR']) / 'pi-hide-tools.json'
            if (await wait_json(preference))['hidden'] is not True:
                raise AssertionError('Actual hide-tools extension failed to persist preference')
            tmux(env, 'send-keys', '-t', name, '-l', 'FACTORY_SMOKE_EXPLICIT_INPUT')
            tmux(env, 'send-keys', '-t', name, 'Enter')
            second = await wait_json(evidence / 'probe-2.json')
            check_probe(second, evidence, repo, env)
            if second['text'] != 'FACTORY_SMOKE_EXPLICIT_INPUT':
                raise AssertionError('Interactive input was not intercepted')
            screen = tmux(env, 'capture-pane', '-p', '-t', name).stdout
            (evidence / 'final-screen.txt').write_text(screen)
            if 'FACTORY_SMOKE_INPUT_HANDLED' not in screen:
                raise AssertionError('Native input-handler acknowledgement missing from TUI')
        finally:
            if name is not None:
                # A failed capture must not prevent watcher/session cleanup.
                with contextlib.suppress(OSError, subprocess.TimeoutExpired):
                    capture = tmux(env, 'capture-pane', '-p', '-t', name, check=False)
                    (evidence / 'cleanup-screen.txt').write_text(capture.stdout + capture.stderr)
            if process.returncode is None:
                process.send_signal(signal.SIGINT)
            try:
                remaining, _ = await asyncio.wait_for(process.communicate(), timeout=15)
                (evidence / 'watch-stdout.log').write_text(''.join(lines) + remaining.decode())
            finally:
                if process.returncode is None:
                    process.kill()
                    await process.wait()
                if name is not None and tmux(env, 'has-session', '-t', name,
                                             check=False).returncode == 0:
                    tmux(env, 'kill-session', '-t', name)
                    raise AssertionError('Watcher leaked its session; '
                                         'smoke removed only that session')
        if process.returncode != 130:
            raise AssertionError('Watcher did not shut down cleanly; see watch logs')
    sessions = tmux(env, 'list-sessions', check=False)
    if sessions.returncode == 0:
        raise AssertionError('Unexpected sessions remain on the disposable socket')
    write_json(evidence / 'cleanup.json', {'watch_exit': process.returncode,
                                         'owned_session_removed': True})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--forgetful', required=True, help='Existing real Forgetful executable')
    parser.add_argument('--model-cache', required=True, type=Path,
                        help='Existing FastEmbed cache; downloads are disabled')
    parser.add_argument('--uv', required=True, help='Existing audited uv 0.13.5 executable')
    parser.add_argument('--uv-cache', type=Path,
                        help='Existing dependency cache (default: uv cache)')
    parser.add_argument('--method', choices=('cli',), default='cli',
                        help='CLI is the only access mode')
    args = parser.parse_args()
    uv, executable = shutil.which(args.uv), shutil.which(args.forgetful)
    if not uv or not executable or any(shutil.which(tool) is None for tool in ('pi', 'tmux')):
        parser.error('Existing Pi, tmux, Forgetful and uv required; no host tools are installed')
    uv_cache = args.uv_cache or Path(subprocess.check_output(
        [uv, '--offline', 'cache', 'dir'], text=True).strip())
    if not args.model_cache.is_dir() or not uv_cache.is_dir():
        parser.error('FastEmbed and uv dependency caches must already exist')
    evidence = Path(tempfile.mkdtemp(prefix='factory-shared-pi-smoke-', dir='/tmp'))
    print(f'Evidence: {evidence}', flush=True)
    write_json(evidence / 'invocation.json', [sys.executable, *sys.argv])
    if not uv_cache.resolve().is_relative_to(Path('/tmp')):
        disposable_cache = evidence / 'uv-cache'
        subprocess.run(['cp', '-a', '--reflink=auto', str(uv_cache), str(disposable_cache)],
                       check=True)
        uv_cache = disposable_cache
    with provider_recorder(evidence) as endpoint:
        repo, env = prepare(evidence, str(Path(executable).resolve()), args.model_cache.resolve(),
                            str(Path(uv).resolve()), uv_cache.resolve(), endpoint)
        try:
            asyncio.run(check_watcher(evidence, repo, env))
        finally:
            # This wrapper always names the private socket, never the user's server.
            tmux(env, 'kill-server', check=False)
    print('PASS: native init/re-init/watch, durable plan/task/worktree, role cwd/resources,')
    print('automatic personal/project resources and MCP excluded; native role CLI project list.')
    print('PASS: input intercepted, ZERO provider requests, owned tmux session removed.')
    write_json(evidence / 'result.json', {
        'status': 'passed', 'provider_requests': 0, 'public_init_reinit_watch': True,
        'real_plan_task_worktree': True, 'real_pi_input_intercepted': True,
        'limits': 'No child dispatch, model inference, autonomous planning or resume exercised.'})


if __name__ == '__main__':
    main()
