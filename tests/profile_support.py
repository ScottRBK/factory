"""External Pi/Forgetful command doubles; never contact an account or install software."""
import json
import sys

from planning_support import PLANNING

COMMAND = '''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
name = Path(sys.argv[0]).name
args = sys.argv[1:]
if os.environ.get('PROFILE_LOG'):
    with open(os.environ['PROFILE_LOG'], 'a') as stream:
        stream.write(json.dumps({'name': name, 'args': args, 'cwd': os.getcwd(), 'pid': os.getpid(),
            'has_token': 'FORGETFUL_TOKEN' in os.environ,
            'pi_offline': os.environ.get('PI_OFFLINE'),
            'milo': os.environ.get('UNDICI_USE_MILO'),
            'models_offline': os.environ.get('HF_HUB_OFFLINE'),
            'agent_dir': os.environ.get('PI_CODING_AGENT_DIR'),
            'role_dir': os.environ.get('FACTORY_ROLE_DIR'),
            'config_home': os.environ.get('XDG_CONFIG_HOME'),
            'database': os.environ.get('SQLITE_PATH'),
            'server': os.environ.get('FORGETFUL_SERVER'),
            'configured_executable': os.environ.get('FACTORY_FORGETFUL_EXECUTABLE'),
            'database_type': os.environ.get('DATABASE')}) + '\\n')
if os.environ.get('PROFILE_INTERRUPT') == name:
    import signal, time
    os.kill(os.getppid(), signal.SIGINT)
    time.sleep(30)
if os.environ.get('PROFILE_FAIL') == name:
    print('TOP_SECRET failure', file=sys.stderr)
    sys.exit(1)
if name == 'pi' and args == ['--version']:
    print('1.4.0')
elif name == 'pi' and args == ['--no-approve', '--list-models']:
    print(os.environ.get('PROFILE_MODELS',
        'provider  model  context  max-out  thinking  images\\n'
        'provider  model  128000  8192  yes  yes'))
elif name == 'pi' and args == ['mcp', 'list', '--json']:
    print(os.environ.get('PROFILE_MCP_RESULT', json.dumps({'servers': [{
        'name': 'forgetful', 'enabled': True, 'state': 'connected',
        'tools': ['discover_forgetful_tools', 'execute_forgetful_tool',
                  'how_to_use_forgetful_tool']}], 'errors': []})))
elif name in ('forgetful', 'custom forgetful'):
    if args[:2] in (['auth', 'status'], ['auth', 'logout']) and len(args) != 2:
        sys.exit('unsupported auth arguments')
    failure = os.environ.get('PROFILE_PLANNING_FAILURE')
    if args[:2] == ['call', 'get_project'] and failure == 'login':
        sys.exit('TOP_SECRET login failed')
    if os.environ.get('PROFILE_PROJECTS_FILE'):
        projects_path = Path(os.environ['PROFILE_PROJECTS_FILE'])
        projects = json.loads(projects_path.read_text())
        if args[:2] == ['project', 'list']:
            print(json.dumps({'projects': projects, 'total_count': len(projects)}))
            sys.exit(0)
        if args[:2] == ['call', 'create_project']:
            if os.environ.get('PROFILE_CREATE_FAILURE') == 'denied':
                sys.exit('TOP_SECRET creation denied')
            fields = json.loads(args[args.index('--args') + 1])
            assert set(fields) == {'name', 'description', 'project_type'}
            assert fields['name'] and fields['description']
            assert fields['project_type'] == 'development'
            project = dict(fields, id=max([30, *[p['id'] for p in projects]]) + 1)
            projects_path.write_text(json.dumps([*projects, project]))
            if os.environ.get('PROFILE_CREATE_FAILURE') == 'interrupt':
                import signal
                os.kill(os.getppid(), signal.SIGINT)
                signal.pause()
            if os.environ.get('PROFILE_CREATE_FAILURE') == 'lost':
                sys.exit('TOP_SECRET response lost after commit')
            print(os.environ.get('PROFILE_CREATE_RESPONSE', json.dumps(project)))
            sys.exit(0)
        if args[:2] == ['call', 'get_project']:
            fields = json.loads(args[args.index('--args') + 1])
            project = next((p for p in projects if p['id'] == fields['project_id']), None)
            if project is None:
                sys.exit('TOP_SECRET project not found')
            print(json.dumps(project))
            sys.exit(0)
    if args[:2] == ['tools', 'list']:
        names = ('create_plan', 'list_plans', 'get_plan', 'update_plan', 'create_task',
                 'query_tasks', 'get_task', 'update_task', 'claim_task', 'transition_task',
                 'add_criterion', 'add_dependency', 'verify_criterion')
        tools = [{'name': tool, 'parameters': {
            ('old' if failure == 'external_ref' else 'external_ref'): {'type': 'string'}}}
            for tool in names if not (failure == 'permission' and tool == 'claim_task')
            and not (failure == 'verification' and tool == 'verify_criterion')]
        print(os.environ.get('PROFILE_TOOL_CATALOG', json.dumps({
            'tools_by_category': {'plan': tools[:4], 'task': tools[4:]}})))
        sys.exit(0)
    if args[:2] == ['tools', 'info'] and failure == 'permission':
        sys.exit('TOP_SECRET permission denied')
    if args[:2] == ['tools', 'info']:
        print(json.dumps({'name': args[2], 'json_schema': {'properties': {
            ('old' if failure == 'external_ref' else 'external_ref'): {'type': 'string'}}}}))
    elif args[:2] == ['call', 'get_current_user']:
        sys.exit('Unexpected user-profile request; project access is sufficient')
    elif args[:2] == ['call', 'get_project']:
        if os.environ.get('PROFILE_PROJECT_ACCESS') == 'denied':
            sys.exit('TOP_SECRET project not found for current user')
        print(json.dumps({'id': 99 if failure == 'project' else 12, 'name': 'Fixture project'}))
    else:
        print(json.dumps({'projects': [{'id': 12, 'name': 'Fixture project'}],
                          'total_count': 1, 'count': 1}))
'''

COMMAND = COMMAND.replace("    failure = os.environ.get('PROFILE_PLANNING_FAILURE')",
                          PLANNING + "    failure = os.environ.get('PROFILE_PLANNING_FAILURE')")

# Optional external-command fault controls. Tests can repair service replies while watch runs.
COMMAND = COMMAND.replace("name = Path(sys.argv[0]).name", """
control_path = os.environ.get('PROFILE_PLANNING_CONTROL')
control = json.loads(Path(control_path).read_text()) if control_path else {}
name = Path(sys.argv[0]).name
""").replace("        state['calls'].append([tool, values])", """
        state['calls'].append([tool, values])
        if (control.get('fail') == tool
                and control.get('fail_arguments', values) == values):
            save_planning_state()
            sys.exit('TOP_SECRET controlled native failure')
""").replace("        print(json.dumps(result))\n        sys.exit(0)", """
        if control.get('incomplete') == tool:
            result['total_count'] += 1
        result = control.get('responses', {}).get(tool, result)
        for case in control.get('response_cases', []):
            if case['tool'] == tool and case['arguments'] == values:
                result = case['result']
        print(json.dumps(result))
        sys.exit(0)
""").replace("    failure = os.environ.get('PROFILE_PLANNING_FAILURE')", """
    if args[:2] == ['call', 'get_project'] and control.get('fail') == 'get_project':
        sys.exit('TOP_SECRET planning preflight unavailable')
    failure = os.environ.get('PROFILE_PLANNING_FAILURE')
""")


def install_commands(directory):
    for name in ('pi', 'tmux', 'forgetful'):
        path = directory / name
        path.write_text(COMMAND)
        path.chmod(0o755)
    (directory / 'uv').write_text(INSTALLER)
    (directory / 'uv').chmod(0o755)
    python = directory / 'installed python3.12'
    python.write_text(INSTALLED_PYTHON)
    python.chmod(0o755)


def events(path):
    return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

RUNTIME_PYTHON = '''#!/usr/bin/env python3
import os
import sys
from pathlib import Path
if '-c' in sys.argv:
    sys.exit(0 if (Path(sys.argv[0]).parent / '.fixture-package').exists() else 1)
os.execv(%r, [%r, *sys.argv[1:]])
'''

INSTALLED_PYTHON = '''#!/usr/bin/env python3
import json
import os
import sys
if os.environ.get('PROFILE_PREFLIGHT_LOG'):
    with open(os.environ['PROFILE_PREFLIGHT_LOG'], 'a') as stream:
        stream.write(json.dumps({'name': 'python', 'args': sys.argv[1:]}) + '\\n')
if os.environ.get('PROFILE_PYTHON_PROBE_FAIL'):
    sys.exit('TOP_SECRET Python probe failed')
print(os.environ.get('PROFILE_PYTHON_PROBE_OUTPUT', 'cpython 3 12'))
'''

INSTALLER = '''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
args = sys.argv[1:]
if (args == ['--version'] or args[:2] == ['python', 'find']):
    if os.environ.get('PROFILE_PREFLIGHT_LOG'):
        with open(os.environ['PROFILE_PREFLIGHT_LOG'], 'a') as stream:
            stream.write(json.dumps({'name': 'uv', 'args': args,
                'config_env': sorted(k for k in os.environ
                    if k.upper().startswith(('UV_', 'PIP_', 'NPM_CONFIG_'))),
                'virtual_env': 'VIRTUAL_ENV' in os.environ or 'CONDA_PREFIX' in os.environ,
                'node_options': 'NODE_OPTIONS' in os.environ}) + '\\n')
if args == ['--version']:
    print(os.environ.get('PROFILE_UV_VERSION', 'uv 0.13.5'))
    if os.environ.get('PROFILE_UV_VERSION_FAIL'):
        sys.exit('TOP_SECRET uv failure')
    sys.exit(0)
if args[:2] == ['python', 'find']:
    if os.environ.get('PROFILE_PYTHON_FIND_FAIL'):
        sys.exit('TOP_SECRET interpreter discovery failed')
    if not Path(sys.argv[0]).with_name('installed python3.12').exists():
        sys.exit('No Python 3.12 installation found')
    print(os.environ.get('PROFILE_PYTHON_FIND_RESULT',
                         str(Path(sys.argv[0]).with_name('installed python3.12'))))
    sys.exit(0)
if os.environ.get('PROFILE_INSTALL_LOG'):
    with open(os.environ['PROFILE_INSTALL_LOG'], 'a') as stream:
        stream.write(json.dumps({'name': Path(sys.argv[0]).name, 'args': args,
            'config_env': sorted(k for k in os.environ
                if k.upper().startswith(('UV_', 'PIP_', 'NPM_CONFIG_'))),
            'node_options': 'NODE_OPTIONS' in os.environ,
            'project_metadata': (Path(args[args.index('--project') + 1])
                                 / 'pyproject.toml').read_text()
                if args[0] == 'sync' else None}) + '\\n')
if Path(sys.argv[0]).name == 'npm':
    target = Path.cwd() / 'node_modules/.bin/pi'
elif args[:1] == ['sync']:
    target = Path(os.environ['UV_PROJECT_ENVIRONMENT']) / 'bin/python'
    target.parent.mkdir(parents=True, exist_ok=True)
    (target.parent.parent / 'pyvenv.cfg').write_text('home = test-fixture')
elif args[:1] == ['venv']:
    target = Path(args[-1]) / 'bin/python'
    target.parent.mkdir(parents=True, exist_ok=True)
    (target.parent.parent / 'pyvenv.cfg').write_text('home = test-fixture')
else:
    target = Path(args[args.index('--python') + 1]).with_name('forgetful')
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(%r)
target.chmod(0o755)
if os.environ.get('PROFILE_INSTALL_FAIL') == args[0]:
    sys.exit(1)
if Path(sys.argv[0]).name == 'uv':
    python = target if target.name == 'python' else target.with_name('python')
    python.write_text(%r)
    python.chmod(0o755)
    if args[0] != 'venv':
        (python.parent / '.fixture-package').touch()
''' % (COMMAND, RUNTIME_PYTHON % (sys.executable, sys.executable))


def install_grill_skill(workspace):
    path = workspace / 'grill-me/SKILL.md'
    path.parent.mkdir(exist_ok=True)
    path.write_text('---\nname: grill-me\ndescription: Interview fixture.\n'
                    'disable-model-invocation: true\n---\n'
                    'Ask frontier questions; delegate fact gathering to research.\n')
    return path
