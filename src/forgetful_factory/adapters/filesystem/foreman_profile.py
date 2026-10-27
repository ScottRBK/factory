"""Editable role files; credentials are created only by Pi or the Forgetful CLI."""
import hashlib
import json
import os
import re
import shlex
import shutil
import sys
import zipfile
from pathlib import Path

from forgetful_factory.adapters.filesystem.agent_definitions import foreman_launch
from forgetful_factory.adapters.filesystem.coordinator_profiles import CoordinatorProfiles
from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    read_generated_json,
    remove_generated,
    replace_generated_json,
    write_json,
    write_new,
)
from forgetful_factory.adapters.filesystem.selected_skills import selected_skill_files
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
MAINTENANCE_SKILL_PATH = 'skills/factory-maintenance/SKILL.md'
ROLE_GUIDANCE_FILE = 'APPEND_SYSTEM.md'
PI_PROFILE_FILE = 'pi-profile.json'
COMPLETION_FILE = 'setup-complete.json'
ROLE_RESOURCES_FILE = 'role-resources.json'
FACTORY_DIRECTORY = '.factory'
MANAGED_MEMORY_RESOURCE = 'pi-forgetful'


class ForemanProfile:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.directory = workspace / '.factory/agents/foreman'
        self.foreman_skill = self.directory / FOREMAN_SKILL_PATH
        self.bundle_directory = workspace / '.factory/resources'
        self._pi_choice: dict | None = None
        self._model_catalogs: dict[tuple[str, Path], list[str]] = {}
        self._managed_memory_selected: bool | None = None

    def prepare_setup_guidance(self) -> None:
        template = (RESOURCES / 'AGENTS.md').read_text()
        path = self.directory / 'AGENTS.md'
        write_new(path, template)
        # The first paragraph is the current setup contract; other guidance stays editable.
        setup_guidance = template.split('\n\n')[1]
        if setup_guidance not in path.read_text():
            raise FactoryError(f'Stale testing guidance: {path} lacks current setup guidance. '
                               'Reconcile its setup paragraph with the installed Foreman '
                               'AGENTS.md before assisted launch. Custom instructions and '
                               'existing files were preserved; no Foreman was launched.')

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
        project = self.bundle_directory / 'agentshell/python'
        if not runtime_ready(project / '.venv', (project / 'pyproject.toml', project / 'uv.lock'),
                             ROLE_PROBE):
            missing.append('agentshell-runtime')
        return missing

    def validate_setup(self, connection: ForgetfulConnection, *,
                       include_home_system_prompt: bool = False,
                       include_memory_extension: bool = False) -> None:
        """Read-only preflight. Connection/authentication readiness belongs to Pi/CLI."""
        self.validate_guidance(include_home_system_prompt=include_home_system_prompt)
        self.require_pi_home(self.pi_home())
        if self.missing_executables(connection):
            raise FactoryError('Foreman profile/runtime is incomplete; complete first setup.')
        CoordinatorProfiles(self.workspace).validate_depth(self.pi_home())
        self.validate_bundled_resources(include_memory_extension=include_memory_extension)

    def validate_bundled_resources(self, *, include_memory_extension: bool = False) -> None:
        manifest = json.loads((RESOURCES.parent / ROLE_RESOURCES_FILE).read_text())
        for name, source in manifest.items():
            if name == MANAGED_MEMORY_RESOURCE and not include_memory_extension:
                continue
            for relative, digest in source['files'].items():
                path = self.bundle_directory / name / relative
                check_real_path(path)
                if (path.is_symlink() or not path.is_file() or
                        hashlib.sha256(path.read_bytes()).hexdigest() != digest):
                    raise FactoryError(f'Stale or edited role resource: {path}; explicitly '
                                       'reconcile it with the audited bundle before a restart '
                                       'with foreman/watch, or init --finalize for incomplete '
                                       'first setup. Existing files are preserved.')

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
                    path = self.bundle_directory / member
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

    def check(self, connection: ForgetfulConnection, *, execution_enabled: bool) -> str:
        AgentForgetfulConnection(self.workspace).check(
            connection, execution_enabled=execution_enabled)
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
                 '/pi-profile.json\n/setup-complete.json\n/cli-config/\n'
                 '/.setup-complete.json.*.tmp\n'
                 '/agents/*/cli-config/\n/agents/*/bin/\n/agents/*/cache/\n'
                 '/agents/*/mcp-cache/\n/resources/**/.venv/\n')
        write_new(path, block)
        if block not in path.read_text():
            with path.open('a', encoding='utf-8') as stream:
                stream.write('\n' + block)

    def prepare(self, connection: ForgetfulConnection) -> None:
        self.validate_guidance()
        self.save_pi_choice()
        self._protect_runtime()
        self._install_resources()
        for relative in (ROLE_GUIDANCE_FILE, FOREMAN_SKILL_PATH, MAINTENANCE_SKILL_PATH):
            write_new(self.directory / relative, (RESOURCES / relative).read_text())
        if connection.instance == 'local':
            Path(connection.database).parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    def save_pi_choice(self) -> None:
        if self._pi_choice is not None:
            write_json(self.workspace / FACTORY_DIRECTORY / PI_PROFILE_FILE, self._pi_choice)

    def prepare_roles(self, config, choices) -> None:
        profiles = CoordinatorProfiles(self.workspace)
        profiles.validate_depth(self.pi_home())
        if config.execution_enabled:
            self.validate_worker_models(config, choices)
        if choices.foreman_memory_model is not None:
            models = self.list_models(config.forgetful)
            if choices.foreman_memory_model not in models:
                raise FactoryError('Foreman memory model is not selectable in the native Pi '
                                   'catalog; choose an exact provider/model and rerun init.')
        if choices.research_agent_model is not None:
            directory = self.workspace / '.factory/agents/research'
            check_real_path(directory)
            directory.mkdir(parents=True, exist_ok=True, mode=0o700)
            models = self.list_models(config.forgetful, harness=choices.research_agent_harness,
                                      cwd=directory)
            if choices.research_agent_model not in models:
                raise FactoryError('Research model is not selectable in the native catalog; '
                                   'choose an exact selector and rerun init.')
        profiles.prepare(config, choices)

    def validate_worker_models(self, config: FactoryConfiguration, choices) -> None:
        for role in ('implementation', 'review'):
            harness = getattr(choices, f'{role}_agent_harness')
            model = getattr(choices, f'{role}_agent_model')
            for repository in config.repository:
                try:
                    models = self.list_models(config.forgetful, harness=harness,
                                              cwd=Path(repository.local_dir))
                    if model not in models:
                        raise ValueError('Unlisted selector')
                except (FactoryError, ValueError) as error:
                    raise FactoryError(f'{role} model {model!r} is not selectable through '
                                       f'native {harness} in {repository.local_dir}. Use an exact '
                                       'native catalog selector; access and model-specific effort '
                                       'support remain unverified. Diagnostics withheld.'
                                       ) from error

    def choose_pi_home(self, requested: str | None, confirm) -> str:
        path = self.workspace / FACTORY_DIRECTORY / PI_PROFILE_FILE
        if path.exists():
            directory = self.pi_home()
            if requested is not None and str(Path(requested).expanduser().absolute()) != directory:
                raise FactoryError('Pi directory conflicts with saved consent. Explicitly review '
                                   'the factory pi-profile.json before using init --finalize.'
                                   )
            if requested is not None:
                self.require_pi_home(directory)
            return directory
        directory = str(Path(requested or os.environ.get('PI_CODING_AGENT_DIR')
                             or Path.home() / '.pi/agent').expanduser().absolute())
        if Path(directory).is_relative_to(self.workspace / FACTORY_DIRECTORY):
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
                               'then /login. Retry first init if no configuration exists; '
                               'otherwise use init --finalize for incomplete setup, or restart '
                               'foreman/watch for completed setup. '
                               'If the path is a typo, correct --pi-agent-dir or '
                               'PI_CODING_AGENT_DIR. If saved consent already exists, review or '
                               'remove .factory/pi-profile.json before using '
                               'init --finalize to approve the corrected home.')

    def pi_home(self) -> str:
        try:
            data = read_generated_json(
                self.workspace / FACTORY_DIRECTORY / PI_PROFILE_FILE)
            directory = data['agent_directory']
            if (data['shared_profile_consent'] is not True or not isinstance(directory, str)
                    or not Path(directory).is_absolute() or '\x00' in directory
                    or Path(directory).is_relative_to(
                        self.workspace / FACTORY_DIRECTORY)):
                raise ValueError('Invalid consent')
            return directory
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise FactoryError('Shared Pi profile consent is missing or invalid. '
                               'Review .factory/pi-profile.json if it exists; '
                               'use init --finalize to approve missing consent for saved setup.'
                               ) from error

    def list_models(self, connection: ForgetfulConnection, *, harness: str = 'pi',
                    cwd: Path | None = None) -> list[str]:
        cwd = cwd or self.workspace
        key = (harness, cwd)
        if key in self._model_catalogs:
            return self._model_catalogs[key].copy()
        self.require_pi_home(self.pi_home())
        helper = Path(__file__).parents[1] / 'agentshell/model_catalog.py'
        environment = role_environment(self.workspace, connection, self.pi_home())
        try:
            output = run_owned([sys.executable, str(helper), harness],
                               cwd, environment)
            models = json.loads(output)
            if not isinstance(models, list) or any(not isinstance(m, str) for m in models):
                raise ValueError('Invalid catalog')
        except (FactoryError, ValueError) as error:
            raise FactoryError(f'{harness} model listing failed; native catalog unavailable. '
                               'Setup is incomplete; check the native login and rerun init. '
                               'External diagnostics withheld.'
                               ) from error
        models = sorted(set(models))
        if models:
            self._model_catalogs[key] = models
        return models.copy()

    def selected_launch(self, config: FactoryConfiguration) -> dict:
        launch = foreman_launch(Path(config.foreman_agent_file))
        self.directory = Path(launch['cwd'])
        skills = selected_skill_files(launch['resources']['skills'])
        required = {}
        for name in ('foreman', 'factory-maintenance'):
            candidates = [skill for skill in skills
                          if skill.name == 'SKILL.md' and skill.parent.name == name]
            if len(candidates) > 1:
                raise FactoryError(f'Ambiguous required Foreman guidance: {name}. '
                                   'Select one workflow skill; agent files were preserved.')
            required[name] = next(iter(candidates), None)
        if not all(required.values()):
            raise FactoryError('Required Foreman guidance must be selected: skills/foreman and '
                               'skills/factory-maintenance. Agent files were preserved.')
        self.foreman_skill = required['foreman']
        extension = self.bundle_directory / 'agentshell/extensions/agentshell.ts'
        if str(extension) not in launch['resources']['extensions']:
            raise FactoryError('Foreman must select the audited AgentShell extension. '
                               'Agent files were preserved.')
        memory_extension = self.bundle_directory / 'pi-forgetful/factory.ts'
        self._managed_memory_selected = str(memory_extension.absolute()) in (
            launch['resources']['extensions'])
        self.validate_setup(config.forgetful, include_home_system_prompt=
                            launch['resources'].get('include_home_system_prompt', True),
                            include_memory_extension=self._managed_memory_selected)
        return launch

    def managed_memory_notice(self) -> str | None:
        if self._managed_memory_selected is not False:
            return None
        return ('The managed Foreman extension is not selected; saved automatic-memory '
                'preferences are inactive. Native Factory CLI planning remains available; '
                'no REST target was guessed.')

    def record_completion(self, config: FactoryConfiguration) -> bool:
        self.selected_launch(config)
        replace_generated_json(
            self.workspace / FACTORY_DIRECTORY / COMPLETION_FILE, {'complete': True})
        return self._managed_memory_selected is True

    def begin_setup(self) -> None:
        remove_generated(self.workspace / FACTORY_DIRECTORY / COMPLETION_FILE)

    def validate_completion(self, _config: FactoryConfiguration) -> None:
        """Validate the receipt; completion is independent of editable configuration."""
        try:
            data = read_generated_json(
                self.workspace / FACTORY_DIRECTORY / COMPLETION_FILE)
            if data != {'complete': True}:
                raise ValueError('Incomplete initial setup')
        except (OSError, ValueError) as error:
            raise FactoryError('Initial factory setup is incomplete; use init --finalize '
                               'to validate the first setup.') from error

    def _read_guidance(self, path: Path) -> str:
        try:
            return path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            raise FactoryError(f'Foreman {path} must be readable valid UTF-8. '
                               'The file is preserved; correct it before restarting foreman/watch '
                               'or validating incomplete first setup with init --finalize.'
                               ) from error

    def validate_guidance(self, *, include_home_system_prompt: bool = False) -> None:
        if not include_home_system_prompt and (self.directory / '.pi/SYSTEM.md').exists():
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
        for path in (self.foreman_skill, self.directory / ROLE_GUIDANCE_FILE):
            if not path.exists():
                continue
            content = self._read_guidance(path)
            if ('Do not start implementation or dispatch feature owners.' in content
                    or 'Do not dispatch agents, create plans or tasks,' in content):
                raise FactoryError(f'Foreman {path} is from the discussion-only slice; '
                                   'manual reconciliation with current instructions is needed. '
                                   'Your guidance is preserved; after review restart foreman/watch '
                                   'or validate incomplete first setup with init --finalize.')
            if any(re.search(pattern, content) for pattern in obsolete):
                raise FactoryError(f'Foreman {path} needs manual reconciliation: obsolete '
                                   'Pi-home Forgetful commands or MCP sign-in instructions. '
                                   'Use FACTORY_ROLE_DIR for native Forgetful CLI cwd and '
                                   'cli-config; MCP is unsupported. Files are preserved; edit '
                                   'the instructions explicitly before restarting foreman/watch '
                                   'or validating incomplete first setup with init --finalize.')
