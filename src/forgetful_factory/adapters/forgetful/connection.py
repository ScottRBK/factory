"""Delegate authentication and connection checks to their owning CLI, never handle tokens."""
import json
import os
from pathlib import Path

from forgetful_factory.adapters.host_dependencies import executable_path
from forgetful_factory.adapters.sensitive_command import run_owned
from forgetful_factory.application.configuration import ForgetfulConnection
from forgetful_factory.domain.models import FactoryError


def role_environment(workspace: Path, connection: ForgetfulConnection,
                     pi_home: str | None = None) -> dict[str, str]:
    role = workspace / '.factory'
    env = dict(os.environ, FACTORY_ROLE_DIR=str(role),
               FACTORY_FORGETFUL_DIR=str(role),
               FACTORY_FORGETFUL_CONFIG_DIR=str(role / 'cli-config'),
               FACTORY_FORGETFUL_PROJECT_ID=str(connection.project_id or ''),
               FACTORY_FORGETFUL_METHOD=connection.method,
               FACTORY_FORGETFUL_INSTANCE=connection.instance,
               FACTORY_FORGETFUL_EXECUTABLE=connection.executable,
               FORGETFUL_SERVER=connection.server or '',
               PATH=executable_path(workspace))
    if pi_home is not None:
        env['PI_CODING_AGENT_DIR'] = pi_home
    env.setdefault('PI_OFFLINE', '1')
    if connection.instance == 'local':
        env.setdefault('HF_HUB_OFFLINE', '1')
    # Do not implicitly import a personal Forgetful target or bearer credential.
    env.pop('FORGETFUL_TOKEN', None)
    # The audited Pi runtime uses Undici's standard parser, not its experimental Milo backend.
    env.pop('UNDICI_USE_MILO', None)
    if connection.instance == 'local':
        env.update(DATABASE='SQLite', SQLITE_PATH=connection.database, SQLITE_MEMORY='false',
                   PLANNING_ENABLED='true')
    return env


def _catalog_tools(catalog: object) -> dict:
    if not isinstance(catalog, dict):
        raise ValueError('Invalid catalog')
    tools = {}
    for group in catalog.values():
        if not isinstance(group, list):
            raise ValueError('Invalid catalog group')
        for tool in group:
            if (not isinstance(tool, dict) or not isinstance(tool.get('name'), str)
                    or tool['name'] in tools):
                raise ValueError('Invalid catalog entry')
            tools[tool['name']] = tool
    return tools


class AgentForgetfulConnection:
    def __init__(self, workspace: Path, term_grace: float = 3):
        self.workspace = workspace
        self.role = workspace / '.factory'
        self.term_grace = term_grace

    def login(self, connection: ForgetfulConnection) -> None:
        if connection.instance != 'server':
            raise FactoryError('--login applies only to an existing HTTP server.')
        args = [connection.executable, 'auth', 'login', '--server', connection.server]
        run_owned(args, self.role, self._environment(connection), login=True,
                  term_grace=self.term_grace)

    def _environment(self, connection: ForgetfulConnection) -> dict[str, str]:
        env = role_environment(self.workspace, connection)
        env['XDG_CONFIG_HOME'] = str(self.role / 'cli-config')
        return env

    def command(self, connection: ForgetfulConnection, arguments: list[str]) -> dict:
        env = self._environment(connection)
        target = (['--local'] if connection.instance == 'local' else
                  ['--server', connection.server])
        args = [connection.executable, *arguments, *target, '--json']
        output = run_owned(args, self.role, env, term_grace=self.term_grace)
        try:
            data = json.loads(output)
            if not isinstance(data, dict) or 'error' in data:
                raise ValueError('Unavailable')
        except (ValueError, TypeError, KeyError) as error:
            raise FactoryError('Forgetful reply was invalid; the operation may have completed. '
                               'Inspect and reconcile backend state in Pi/CLI before any retry; '
                               'do not replay uncertain writes. After reconciliation, use '
                               'init --finalize for incomplete saved setup, or restart watch or '
                               'foreman for completed setup. If no configuration was saved, '
                               'retry first init only after reconciliation. '
                               'External diagnostics withheld.') from error
        return data

    def call(self, connection: ForgetfulConnection, tool: str, **arguments) -> dict:
        return self.command(connection, ['call', tool, '--args', json.dumps(arguments)])

    def projects(self, connection: ForgetfulConnection) -> list[dict]:
        data = self.command(connection, ['project', 'list'])
        projects = data.get('projects')
        if (not isinstance(projects, list) or any(
                not isinstance(project, dict) or type(project.get('id')) is not int
                or project['id'] <= 0 or not isinstance(project.get('name'), str)
                or not project['name'].strip() for project in projects)):
            raise FactoryError('Forgetful returned invalid projects; check the selected backend.')
        return projects

    def create_project(self, connection: ForgetfulConnection, name: str) -> int:
        try:
            project = self.call(connection, 'create_project', name=name,
                                description=f'Factory plans and knowledge for {name}.',
                                project_type='development')
            project_id = project.get('id')
            if type(project_id) is not int or project_id <= 0:
                raise ValueError('Invalid project ID')
        except (FactoryError, ValueError, KeyboardInterrupt) as error:
            message = ('Project creation could not be confirmed; it may already exist. '
                       'Rerun init and check the project list before creating another. '
                       'No automatic retry was made; setup is incomplete.')
            if isinstance(error, KeyboardInterrupt):
                raise KeyboardInterrupt(message) from error
            raise FactoryError(message) from error
        return project_id

    def check(self, connection: ForgetfulConnection, *, execution_enabled: bool) -> None:
        if connection.project_id is None:
            raise FactoryError('Select forgetful.project_id with init before planning.')
        try:
            # Project access already verifies the native connection and login.
            project = self.call(connection, 'get_project', project_id=connection.project_id)
            if project['id'] != connection.project_id:
                raise ValueError('Unexpected project')
            catalog = self.command(connection, ['tools', 'list'])['tools_by_category']
            tools = _catalog_tools(catalog)
            required = {'create_plan', 'list_plans', 'get_plan', 'update_plan', 'create_task',
                        'query_tasks', 'get_task', 'update_task', 'claim_task',
                        'transition_task', 'add_criterion', 'add_dependency'}
            if execution_enabled:
                required.add('verify_criterion')
            if not required.issubset(tools):
                raise ValueError('Missing permission')
            for name in ('create_plan', 'list_plans'):
                parameters = tools[name].get('parameters')
                if not isinstance(parameters, dict) or 'external_ref' not in parameters:
                    raise ValueError('Missing external_ref')
        except (FactoryError, KeyError, TypeError, ValueError) as error:
            raise FactoryError('Forgetful planning check failed: select an accessible project '
                               'under the current native login with plan/task permissions. '
                               'The selected backend must support external_ref (0.5.5+); '
                               'enable PLANNING_ENABLED on the server. After correction restart '
                               'foreman/watch, or use init --finalize for incomplete saved setup.'
                               ) from error
