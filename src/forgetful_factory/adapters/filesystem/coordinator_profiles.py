"""Provision native role instructions and explicit child rosters; no launch/auth wrapper."""
import json
import os
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    write_json,
    write_new,
)
from forgetful_factory.adapters.filesystem.worker_profiles import WorkerProfiles
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.domain.models import FactoryError

TEMPLATES = Path(__file__).resolve().parents[2] / 'resources'
ROLE_INSTRUCTIONS_FILE = 'AGENTS.md'
RESOURCE_SELECTION_FILE = 'resources.json'
ROSTER_FILE = 'roster.json'


def _selection_conflict(path: Path) -> FactoryError:
    return FactoryError('Pi model setup has an invalid or conflicting preserved selection: '
                        f'{path}. '
                        'Back up your edits, reconcile this file with the configured role '
                        'and local skills, then rerun init. Existing files are preserved.')


def _read_selection(path: Path) -> dict:
    try:
        check_real_path(path)
        return json.loads(path.read_text())
    except (OSError, ValueError, FactoryError) as error:
        raise _selection_conflict(path) from error


def selected_resources(skills: list[str], extensions: list[str]) -> dict:
    return {'skills': skills, 'extensions': extensions, 'plugins': [], 'packages': [],
            'mcp_servers': [], 'inherit_personal_resources': False,
            'inherit_project_resources': False, 'include_instruction_files': True,
            'include_home_system_prompt': False}


def _local_resource_paths(directory: Path, paths: object) -> list[str]:
    if not isinstance(paths, list):
        raise ValueError('Resource paths must be a list')
    resolved = []
    for value in paths:
        if (not isinstance(value, str) or not value or '\x00' in value
                or value.startswith(('!', 'npm:', 'git:', 'http:', 'https:', 'github:'))):
            raise ValueError('Expected a provisioned local path')
        path = Path(value)
        path = path if path.is_absolute() else directory / path
        if not path.is_file() and not path.is_dir():
            raise ValueError('Missing selected resource')
        resolved.append(str(path.absolute()))
    return resolved


class CoordinatorProfiles:
    def __init__(self, workspace: Path):
        self.workers = WorkerProfiles(workspace)
        self.directory = workspace / '.factory/agents'

    def validate_depth(self, pi_home: str) -> None:
        if any(key in os.environ for key in ('PI_AGENT_SHELL_CHILD', 'PI_AGENT_SHELL_DEPTH',
                                            'PI_AGENT_SHELL_MAX_DEPTH')):
            raise FactoryError('Start Factory outside a Pi subagent; inherited ancestry and '
                               'depth policy cannot be reset by Factory.')
        path = Path(pi_home) / 'extensions/agentshell.json'
        try:
            preferences = json.loads(path.read_text()) if path.exists() else {}
            depth = preferences.get('max_sub_agent_depth', 0)
            if type(depth) is not int or depth < 1:
                raise ValueError('Insufficient depth')
        except (OSError, ValueError, AttributeError) as error:
            raise FactoryError('Native Pi max_sub_agent_depth must be at least 1 for owner '
                               'research delegation. Review extensions/agentshell.json in the '
                               'shared Pi home; Factory preserves those preferences.') from error

    def prepare(self, config: FactoryConfiguration) -> None:
        self.validate_guidance(config)
        if (not config.feature_owner_agent_model or not config.feature_owner_agent_effort
                or not config.grill_me_skill or not Path(config.grill_me_skill).is_file()):
            raise FactoryError('Owner setup is incomplete. Select a native Pi model/effort and '
                               'an existing unchanged grill-me SKILL.md; rerun init.')
        for role in ('foreman', 'feature-owner', 'research'):
            paths = (ROLE_INSTRUCTIONS_FILE,) if role == 'foreman' else (
                ROLE_INSTRUCTIONS_FILE, f'skills/{role}/SKILL.md')
            for relative in paths:
                content = (TEMPLATES / role / relative).read_text()
                content = content.replace('@GRILL_ME@', json.dumps(config.grill_me_skill))
                write_new(self.directory / role / relative, content)
        extension = str(self.directory / 'foreman/resources/agentshell/extensions/agentshell.ts')
        owner = self.directory / 'feature-owner'
        research = self.directory / 'research'
        write_json(owner / RESOURCE_SELECTION_FILE, {
            'skills': [str(owner / 'skills/feature-owner'), config.grill_me_skill],
            'extensions': [extension],
        })
        write_json(research / RESOURCE_SELECTION_FILE, {
            'skills': [str(research / 'skills/research')], 'extensions': [],
        })
        write_json(research / ROSTER_FILE, {'roster': {'enabled': False}})
        children = [self._role('research', config)]
        if config.execution_enabled:
            self.workers.prepare(config)
            children.extend(self._worker_role(role, config)
                            for role in ('implementation', 'review'))
        write_json(owner / ROSTER_FILE, {'roster': {'enabled': True, 'roles': children}})
        write_json(self.directory / 'foreman' / ROSTER_FILE, {'roster': {
            'enabled': True, 'roles': [self._role('feature-owner', config)]}})

    def _worker_role(self, role: str, config: FactoryConfiguration) -> dict:
        entry = {'name': role, 'description': f'{role.capitalize()} assigned repository tasks',
                 'agent_type': getattr(config, f'{role}_agent_harness'),
                 'model': getattr(config, f'{role}_agent_model'),
                 'effort': getattr(config, f'{role}_agent_effort')}
        if entry['agent_type'] == 'pi':
            directory = self.directory / role
            selected = self.workers.resources(role, config)
            entry['resources'] = selected_resources(
                _local_resource_paths(directory, selected['skills']), [])
            entry['roster_file'] = str(directory / ROSTER_FILE)
        return entry

    def _role(self, name: str, config: FactoryConfiguration) -> dict:
        directory = self.directory / name
        path = directory / RESOURCE_SELECTION_FILE
        resources = _read_selection(path)
        try:
            if not isinstance(resources, dict) or set(resources) != {'skills', 'extensions'}:
                raise ValueError('Only explicit local skills/extensions are supported')
            for key, paths in resources.items():
                resources[key] = _local_resource_paths(directory, paths)
        except (ValueError, TypeError) as error:
            raise _selection_conflict(path) from error
        return {'name': name, 'description': ('Plan and own a feature' if name == 'feature-owner'
                                              else 'Gather facts and return context'),
                'agent_type': 'pi', 'model': config.feature_owner_agent_model,
                'effort': config.feature_owner_agent_effort, 'cwd': str(directory),
                'roster_file': str(directory / ROSTER_FILE),
                'resources': selected_resources(**resources)}

    def _selection_files(self) -> dict:
        files = {}
        for role in ('foreman', 'feature-owner', 'research'):
            for relative in (ROLE_INSTRUCTIONS_FILE, f'skills/{role}/SKILL.md'):
                if not (self.directory / role / relative).is_file():
                    raise ValueError('Missing role instructions')
            for relative in (RESOURCE_SELECTION_FILE, ROSTER_FILE):
                path = self.directory / role / relative
                files[f'{role}/{relative}'] = _read_selection(path)
        return files

    def selection(self, config: FactoryConfiguration) -> dict:
        """Validate selected child contracts and bind selectors to successful setup."""
        self.validate_guidance(config)
        try:
            if (not config.feature_owner_agent_model or not config.feature_owner_agent_effort
                    or not config.grill_me_skill):
                raise ValueError('Missing owner configuration')
            files = self._selection_files()
            for parent, child in (('foreman', 'feature-owner'), ('feature-owner', 'research')):
                children = [self._role(child, config)]
                if parent == 'feature-owner' and config.execution_enabled:
                    children.extend(self._worker_role(role, config)
                                    for role in ('implementation', 'review'))
                expected = {'roster': {'enabled': True, 'roles': children}}
                if files[f'{parent}/{ROSTER_FILE}'] != expected:
                    raise _selection_conflict(self.directory / parent / ROSTER_FILE)
            if files[f'research/{ROSTER_FILE}'] != {'roster': {'enabled': False}}:
                raise _selection_conflict(self.directory / 'research' / ROSTER_FILE)
            owner = self._role('feature-owner', config)['resources']
            research = self._role('research', config)['resources']
            required = [str(self.directory / 'feature-owner/skills/feature-owner'),
                        config.grill_me_skill]
            extension = str(self.directory / 'foreman/resources/agentshell'
                            / 'extensions/agentshell.ts')
            if not set(required) <= set(owner['skills']) or extension not in owner['extensions']:
                raise _selection_conflict(
                    self.directory / 'feature-owner' / RESOURCE_SELECTION_FILE)
            if research['extensions']:
                raise _selection_conflict(self.directory / 'research' / RESOURCE_SELECTION_FILE)
            import hashlib
            files['grill_me_source'] = {
                'path': config.grill_me_skill,
                'sha256': hashlib.sha256(Path(config.grill_me_skill).read_bytes()).hexdigest()}
            if config.execution_enabled:
                files['workers'] = self.workers.selection(config)
            return files
        except (OSError, ValueError, TypeError, KeyError) as error:
            raise FactoryError('Pi model setup is incomplete or conflicting; explicitly '
                               'reconcile resources.json/roster.json with configured models '
                               'and local skills, then rerun init. Edits are preserved.') from error

    def validate_guidance(self, config: FactoryConfiguration) -> None:
        if not config.execution_enabled:
            return
        obsolete = ('this slice stops at a reviewable plan',
                    'are not available in this slice',
                    'implementation/review execution, commits, pr creation',
                    'execution remain for slice 6')
        for role, names in (
                ('foreman', (ROLE_INSTRUCTIONS_FILE, 'APPEND_SYSTEM.md',
                             'skills/foreman/SKILL.md')),
                ('feature-owner', (ROLE_INSTRUCTIONS_FILE, 'skills/feature-owner/SKILL.md'))):
            for name in names:
                path = self.directory / role / name
                try:
                    content = ' '.join(path.read_text().lower().split()) if path.exists() else ''
                except (OSError, UnicodeError) as error:
                    raise FactoryError(f'Worker guidance needs manual reconciliation: {path}; '
                                       'preserved file must be readable UTF-8.') from error
                if any(phrase in content for phrase in obsolete):
                    raise FactoryError(f'Execution needs manual reconciliation of planning-only '
                                       f'guidance: {path}. Compare current Factory role templates, '
                                       'preserve team edits, then rerun init. Files are preserved.')
