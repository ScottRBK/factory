"""Editable role files; credentials are created only by Pi or the Forgetful CLI."""
import hashlib
import json
import os
import re
import shlex
import shutil
import sys
import zipfile
from dataclasses import asdict
from pathlib import Path

from forgetful_factory.adapters.filesystem.coordinator_profiles import CoordinatorProfiles
from forgetful_factory.adapters.filesystem.resource_files import (
    read_generated_json,
    remove_generated,
    replace_generated_json,
    write_json,
    write_new,
)
from forgetful_factory.adapters.forgetful.authentication import uses_browser_login
from forgetful_factory.adapters.forgetful.connection import (
    AgentForgetfulConnection,
    role_environment,
)
from forgetful_factory.adapters.host_dependencies import (
    FORGETFUL_PROBE,
    ROLE_PROBE,
    HostDependencies,
    executable_path,
    runtime_ready,
)
from forgetful_factory.adapters.sensitive_command import run_owned
from forgetful_factory.application.configuration import FactoryConfiguration, ForgetfulConnection
from forgetful_factory.domain.models import FactoryError

RESOURCES = Path(__file__).resolve().parents[2] / 'resources' / 'foreman'
FOREMAN_SKILL_PATH = 'skills/foreman/SKILL.md'
ROLE_GUIDANCE_FILE = 'APPEND_SYSTEM.md'
PI_PROFILE_FILE = 'pi-profile.json'
MODEL_SELECTION_FILE = 'model-selection.json'
ROLE_RESOURCES_FILE = 'role-resources.json'


class ForemanProfile:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.directory = workspace / '.factory/agents/foreman'
        self.resources_path = self.directory / 'resources.json'
        self._pi_choice: dict | None = None

    def missing_executables(self, connection: ForgetfulConnection) -> list[str]:
        required = ['pi', 'tmux']
        if connection.method == 'cli' or connection.instance == 'local':
            required.append(connection.executable)
        path = executable_path(self.workspace)
        missing = [command for command in required if shutil.which(command, path=path) is None]
        managed_pi = self.workspace / '.factory/runtime/pi/node_modules/.bin/pi'
        if (shutil.which('pi', path=path) == str(managed_pi)
                and Path(self.pi_home()).is_dir()
                and not HostDependencies(self.workspace).pi_ready(self.pi_home())):
            missing.append('pi')
        managed = self.workspace / '.factory/runtime/forgetful'
        selected = shutil.which(connection.executable, path=path)
        if (connection.executable in required
                and selected == str(managed / 'bin/forgetful')
                and connection.executable not in missing
                and not runtime_ready(managed, (managed / 'forgetful-requirements.txt',),
                                      FORGETFUL_PROBE)):
            missing.append('forgetful')
        project = self.directory / 'resources/agentshell/python'
        if not runtime_ready(project / '.venv', (project / 'pyproject.toml', project / 'uv.lock'),
                             ROLE_PROBE):
            missing.append('agentshell-runtime')
        return missing

    def validate_setup(self, connection: ForgetfulConnection) -> None:
        """Read-only preflight. Connection/authentication readiness belongs to Pi/CLI."""
        self.validate_guidance()
        self.require_pi_home(self.pi_home())
        manifest = json.loads((RESOURCES.parent / ROLE_RESOURCES_FILE).read_text())
        required = ['resources.json', ROLE_GUIDANCE_FILE, FOREMAN_SKILL_PATH]
        required.extend(f'resources/{name}/{relative}'
                        for name, source in manifest.items() for relative in source['files'])
        if (any(not (self.directory / name).is_file() for name in required)
                or self.missing_executables(connection)):
            raise FactoryError('Foreman profile/runtime is incomplete; rerun init before watch.')
        CoordinatorProfiles(self.workspace).validate_depth(self.pi_home())
        self.validate_bundled_resources()
        self.launch_resources()

    def validate_bundled_resources(self) -> None:
        manifest = json.loads((RESOURCES.parent / ROLE_RESOURCES_FILE).read_text())
        for name, source in manifest.items():
            for relative, digest in source['files'].items():
                path = self.directory / 'resources' / name / relative
                if (path.is_symlink() or not path.is_file() or
                        hashlib.sha256(path.read_bytes()).hexdigest() != digest):
                    raise FactoryError(f'Stale or edited role resource: {path}; explicitly '
                                       'reconcile it with the audited bundle and rerun init. '
                                       'Existing files are preserved.')

    def installation(self, command: str) -> str | None:
        return HostDependencies(self.workspace).description(command)

    def install(self, command: str) -> None:
        HostDependencies(self.workspace).install(command)

    def _install_resources(self) -> None:
        manifest = json.loads((RESOURCES.parent / ROLE_RESOURCES_FILE).read_text())
        with zipfile.ZipFile(RESOURCES.parent / 'role-resources.zip') as archive:
            for name, source in manifest.items():
                for relative, digest in source['files'].items():
                    member = f'{name}/{relative}'
                    data = archive.read(member)
                    if hashlib.sha256(data).hexdigest() != digest:
                        raise FactoryError('Bundled role resource checksum failed; '
                                           'reinstall factory.')
                    path = self.directory / 'resources' / member
                    if path.exists() and (path.is_symlink() or
                            hashlib.sha256(path.read_bytes()).hexdigest() != digest):
                        raise FactoryError(f'Stale or edited role resource: {path}. Explicitly '
                                           'reconcile with the audited bundle, or initialize a '
                                           'fresh factory. User edits are preserved.')
                    write_new(path, data.decode())
    def uses_browser_login(self, connection: ForgetfulConnection) -> bool:
        return uses_browser_login(connection)

    def login(self, connection: ForgetfulConnection) -> None:
        AgentForgetfulConnection(self.workspace).login(connection)

    def check(self, connection: ForgetfulConnection) -> str:
        AgentForgetfulConnection(self.workspace).check(connection)
        return 'Forgetful: connected; selected project and planning permissions verified.'

    def projects(self, connection: ForgetfulConnection) -> list[dict]:
        return AgentForgetfulConnection(self.workspace).projects(connection)

    def create_project(self, connection: ForgetfulConnection, name: str) -> int:
        return AgentForgetfulConnection(self.workspace).create_project(connection, name)

    def _protect_runtime(self) -> None:
        path = self.workspace / '.factory/.gitignore'
        # Positive exclusions never undo a user's stricter ignore policy.
        block = ('# Factory credential/runtime exclusions\n'
                 '/runtime/\n/data/\n/worktrees/\n/agents/*/*auth*.json\n/agents/*/models.json\n'
                 '/agents/*/models-store.json\n/agents/*/*.log\n/agents/*/.env*\n'
                 '/agents/*/trust.json\n/agents/*/crashes.json\n/agents/*/tmp/\n'
                 '/agents/*/tools/\n/agents/*/npm/\n/agents/*/git/\n'
                 '/agents/*/sessions/\n'
                 '/agents/*/pi-profile.json\n/agents/*/model-selection.json\n'
                 '/agents/*/.model-selection.json.*.tmp\n'
                 '/agents/*/cli-config/\n/agents/*/bin/\n/agents/*/cache/\n'
                 '/agents/*/mcp-cache/\n/agents/*/resources/**/.venv/\n')
        write_new(path, block)
        if block not in path.read_text():
            with path.open('a', encoding='utf-8') as stream:
                stream.write('\n' + block)

    def prepare(self, connection: ForgetfulConnection) -> None:
        self.validate_guidance()
        if self._pi_choice is not None:
            write_json(self.directory / PI_PROFILE_FILE, self._pi_choice)
        self._protect_runtime()
        write_json(self.resources_path, {
            'skills': ['skills/foreman'],
            'extensions': ['resources/agentshell/extensions/agentshell.ts',
                           'resources/hide-tools/index.ts'],
        })
        self._install_resources()
        for relative in (ROLE_GUIDANCE_FILE, FOREMAN_SKILL_PATH):
            write_new(self.directory / relative, (RESOURCES / relative).read_text())
        self.launch_resources()
        if connection.instance == 'local':
            Path(connection.database).parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    def prepare_roles(self, config) -> None:
        profiles = CoordinatorProfiles(self.workspace)
        profiles.validate_depth(self.pi_home())
        try:
            profiles.prepare(config)
            profiles.selection(config)
        except (ValueError, TypeError, KeyError) as error:
            raise FactoryError('Invalid owner resources/roster; explicitly reconcile the '
                               'preserved files and rerun init.') from error

    def choose_pi_home(self, requested: str | None, confirm) -> str:
        path = self.directory / PI_PROFILE_FILE
        if path.exists():
            directory = self.pi_home()
            if requested is not None and str(Path(requested).expanduser().absolute()) != directory:
                raise FactoryError('Pi directory conflicts with saved consent. Explicitly review '
                                   'pi-profile.json and model-selection.json before rerunning init.'
                                   )
            if requested is not None:
                self.require_pi_home(directory)
            return directory
        directory = str(Path(requested or os.environ.get('PI_CODING_AGENT_DIR')
                             or Path.home() / '.pi/agent').expanduser().absolute())
        if Path(directory).is_relative_to(self.workspace / '.factory'):
            raise FactoryError('Select your normal native Pi agent directory, outside .factory.')
        if requested is not None:
            self.require_pi_home(directory)
        if not confirm(directory):
            raise FactoryError('Shared Pi profile consent declined; '
                               'setup stopped before invoking Pi.')
        self._pi_choice = {'agent_directory': directory, 'shared_profile_consent': True}
        return directory

    def require_pi_home(self, directory: str) -> None:
        if not Path(directory).is_dir():
            executable = shutil.which('pi', path=executable_path(self.workspace)) or 'pi'
            raise FactoryError(f'Chosen native Pi home does not exist: {directory}. '
                               'Setup is incomplete. Initialize your normal native Pi home '
                               f'in another terminal with PI_CODING_AGENT_DIR='
                               f'{shlex.quote(directory)} {shlex.quote(executable)}, '
                               'then /login, and rerun init. '
                               'If the path is a typo, correct --pi-agent-dir or '
                               'PI_CODING_AGENT_DIR. If saved consent already exists, review or '
                               'remove .factory/agents/foreman/pi-profile.json before rerunning '
                               'init to approve the corrected home.')

    def pi_home(self) -> str:
        try:
            data = json.loads((self.directory / PI_PROFILE_FILE).read_text())
            directory = data['agent_directory']
            if (data['shared_profile_consent'] is not True or not isinstance(directory, str)
                    or not Path(directory).is_absolute() or '\x00' in directory
                    or Path(directory).is_relative_to(self.workspace / '.factory')):
                raise ValueError('Invalid consent')
            return directory
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise FactoryError('Shared Pi profile consent is missing or invalid; rerun init. '
                               'Review .factory/agents/foreman/pi-profile.json if it exists.'
                               ) from error

    def list_models(self, connection: ForgetfulConnection) -> list[str]:
        self.require_pi_home(self.pi_home())
        helper = Path(__file__).parents[1] / 'agentshell/model_catalog.py'
        environment = role_environment(self.workspace, connection, self.pi_home())
        try:
            output = run_owned([sys.executable, str(helper)], self.workspace, environment)
            models = json.loads(output)
            if not isinstance(models, list) or any(not isinstance(m, str) for m in models):
                raise ValueError('Invalid catalog')
        except (FactoryError, ValueError) as error:
            raise FactoryError('Pi model listing failed; setup is incomplete. Use native Pi /login '
                               'in the chosen home and rerun init. External diagnostics withheld.'
                               ) from error
        return sorted(set(models))

    def _selection(self, config: FactoryConfiguration) -> dict:
        return {'agent_directory': self.pi_home(), 'model': config.foreman_agent_model,
                'foreman_effort': config.foreman_agent_effort,
                'owner_model': config.feature_owner_agent_model,
                'owner_effort': config.feature_owner_agent_effort,
                'owner_harness': config.feature_owner_agent_harness,
                'forgetful': asdict(config.forgetful),
                'profiles': CoordinatorProfiles(self.workspace).selection(config)}

    def record_completion(self, config: FactoryConfiguration) -> None:
        expected = self._selection(config)
        replace_generated_json(self.directory / MODEL_SELECTION_FILE, expected)
        self.validate_completion(config)

    def begin_setup(self) -> None:
        remove_generated(self.directory / MODEL_SELECTION_FILE)

    def validate_completion(self, config: FactoryConfiguration) -> None:
        try:
            data = read_generated_json(self.directory / MODEL_SELECTION_FILE)
            if data != self._selection(config):
                raise ValueError('Selection changed')
        except (OSError, ValueError) as error:
            raise FactoryError('Pi model setup is incomplete or changed; rerun init. '
                               'model-selection.json binds models/efforts, role selections, '
                               'grill-me source, Pi home and Forgetful target.') from error

    def launch_resources(self) -> dict:
        try:
            settings = json.loads(self.resources_path.read_text())
            if not isinstance(settings, dict) or settings.keys() - {'skills', 'extensions'}:
                raise ValueError('Unsupported selection')
            resources = {}
            for key in ('skills', 'extensions'):
                values = settings.get(key, [])
                if not isinstance(values, list):
                    raise ValueError('Invalid paths')
                resources[key] = [self._local_resource_path(value) for value in values]
            skill = (self.directory / FOREMAN_SKILL_PATH).resolve()
            extension = (self.directory / 'resources/agentshell/extensions/agentshell.ts').resolve()
            if (not {skill, skill.parent}.intersection(Path(p).resolve()
                                                       for p in resources['skills'])
                    or extension not in {Path(p).resolve() for p in resources['extensions']}):
                raise FactoryError('Incomplete Foreman resources.json: select skills/foreman '
                                   '(or skills/foreman/SKILL.md) under skills and '
                                   'resources/agentshell/extensions/agentshell.ts under '
                                   'extensions. Edits are preserved; reconcile the selections '
                                   'and rerun init.')
            return resources
        except (OSError, ValueError, TypeError) as error:
            raise FactoryError('Invalid Foreman resources.json: select only existing local '
                               'skills/extensions paths, relative to the role or absolute. '
                               'No packages, URLs or inheritance overrides are supported; '
                               'Edits are preserved. Correct the file and rerun init.') from error

    def _local_resource_path(self, value: object) -> str:
        if (not isinstance(value, str) or not value or '\x00' in value
                or value.startswith(('!', 'npm:', 'git:', 'http:', 'https:', 'github:'))):
            raise ValueError('Expected a provisioned local path')
        path = Path(value).expanduser()
        if not path.is_absolute():
            path = self.directory / path
        if not path.is_file() and not path.is_dir():
            raise ValueError('Missing resource')
        return str(path.absolute())

    def _read_guidance(self, relative: str) -> str:
        try:
            return (self.directory / relative).read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            raise FactoryError(f'Foreman {relative} must be readable valid UTF-8. '
                               'The file is preserved; correct it and rerun init.') from error

    def validate_guidance(self) -> None:
        if (self.directory / '.pi/SYSTEM.md').exists():
            raise FactoryError('The Foreman launch directory has .pi/SYSTEM.md. '
                               'AgentShell cannot keep that '
                               'file while excluding your personal SYSTEM.md in interactive Pi. '
                               'Setup is incomplete; instructions were not changed. Review moving '
                               'project guidance to AGENTS.md, or wait for upstream support.')
        pi_variable = r'\$(?:PI_CODING_AGENT_DIR\b|\{PI_CODING_AGENT_DIR\})'
        obsolete = (
            pi_variable + r'''["']?/cli-config\b''',
            r'''\bcd\s+(?:--\s+)?["']?''' + pi_variable + r'''["']?(?:\s|$)''',
            r'(?:/mcp|\bpi\s+mcp)\s+login\s+forgetful\b',
        )
        for relative in (FOREMAN_SKILL_PATH, ROLE_GUIDANCE_FILE):
            path = self.directory / relative
            if not path.exists():
                continue
            content = self._read_guidance(relative)
            if ('Do not start implementation or dispatch feature owners.' in content
                    or 'Do not dispatch agents, create plans or tasks,' in content):
                raise FactoryError(f'Foreman {relative} is from the discussion-only slice; '
                                   'manual reconciliation with current instructions is needed. '
                                   'Your guidance is preserved; rerun init after review.')
            if any(re.search(pattern, content) for pattern in obsolete):
                raise FactoryError(f'Foreman {relative} needs manual reconciliation: obsolete '
                                   'Pi-home Forgetful commands or MCP sign-in instructions. '
                                   'Use FACTORY_ROLE_DIR for native Forgetful CLI cwd and '
                                   'cli-config; MCP is unsupported. Files are preserved; edit '
                                   'the instructions explicitly and rerun init.')
