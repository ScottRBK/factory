"""Read one normalized definition; delegation and child loading remain extension-owned."""
import json
import os
import re
from pathlib import Path

from forgetful_factory.application.configuration import nonblank
from forgetful_factory.domain.models import FactoryError

RESOURCE_FLAGS = ('inherit_personal_resources', 'inherit_project_resources',
                  'include_instruction_files', 'include_home_system_prompt')
PATH_RESOURCES = ('skills', 'extensions', 'plugins')
REQUIRED_AGENT_FIELDS = {'name', 'description', 'agent_type', 'model', 'effort'}
OPTIONAL_AGENT_FIELDS = {'cwd', 'resources'}
LOCAL_PATH_PREFIX = re.compile(r'(?i)^(?:[a-z]+:|~)')


def relative_path(directory: Path, value: str) -> Path:
    """Lexical resolution keeps references relative to the selected file, including symlinks."""
    nonblank(value, 'agent path')
    return Path(os.path.abspath(directory / value))


def _local_selection(value: object, field: str, message: str) -> str:
    selected = nonblank(value, field)
    if LOCAL_PATH_PREFIX.match(selected):
        raise ValueError(message)
    return selected


def _validate_agent(value: object) -> dict:
    if (not isinstance(value, dict) or not REQUIRED_AGENT_FIELDS <= set(value)
            or set(value) - REQUIRED_AGENT_FIELDS - OPTIONAL_AGENT_FIELDS):
        raise ValueError('Invalid agent fields')
    for key in REQUIRED_AGENT_FIELDS:
        nonblank(value[key], f'agent.{key}')
    if 'cwd' in value:
        _local_selection(value['cwd'], 'agent.cwd', 'Agent cwd must select a local path')
    return value


def _validate_roster(path: Path, value: object, agent_type: str) -> None:
    if (not isinstance(value, dict) or set(value) - {'enabled', 'roles'}
            or type(value.get('enabled', False)) is not bool
            or not isinstance(value.get('roles', []), list)):
        raise ValueError('Expected roster enabled and reference-only roles')
    for child in value.get('roles', []):
        if not isinstance(child, dict) or set(child) != {'agent_file'}:
            raise ValueError('Child entries contain only agent_file')
        selected = _local_selection(
            child['agent_file'], 'agent_file',
            'Child agent_file must select a local file')
        if not relative_path(path.parent, selected).is_file():
            raise ValueError('Child agent_file must select an existing regular file')
    if agent_type != 'pi' and (value.get('enabled', False) or value.get('roles', [])):
        raise ValueError('Non-Pi agents require a disabled empty roster')


def _validate_resources(value: object) -> None:
    allowed = {*PATH_RESOURCES, 'packages', 'mcp_servers', *RESOURCE_FLAGS}
    if not isinstance(value, dict) or set(value) - allowed:
        raise ValueError('Invalid native resources')
    for key in (*PATH_RESOURCES, 'packages'):
        if key in value and not isinstance(value[key], list):
            raise ValueError(f'Expected resource list: {key}')
    if value.get('mcp_servers') is not None and value['mcp_servers'] != []:
        raise ValueError('Resource mcp_servers supports only null or []')
    for key in RESOURCE_FLAGS:
        if key in value and type(value[key]) is not bool:
            raise ValueError(f'Resource {key} must be a boolean')


def read_definition(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(document, dict) or set(document) != {'agent', 'roster'}:
            raise ValueError('Expected exactly agent and roster')
        agent = _validate_agent(document['agent'])
        _validate_roster(path, document['roster'], agent['agent_type'])
        _validate_resources(agent.get('resources', {}))
        return document
    except (OSError, ValueError, TypeError, KeyError) as error:
        raise FactoryError(f'Invalid agent definition: {path}. {error}') from error


def foreman_launch(path: Path) -> dict:
    agent = read_definition(path)['agent']
    if agent['agent_type'] != 'pi':
        raise FactoryError('The root Foreman definition must select native Pi.')
    directory = relative_path(path.parent, agent['cwd']) if 'cwd' in agent else Path.cwd()
    if not directory.is_dir():
        raise FactoryError(f'Foreman cwd must be an existing directory: {directory}')
    resources = dict(agent.get('resources', {}))
    if resources.get('packages'):
        raise FactoryError('Foreman resources must select audited local paths, not packages.')
    for key in PATH_RESOURCES:
        values = resources.get(key, [])
        paths = []
        for value in values:
            nonblank(value, f'agent.resources.{key}')
            if value.startswith('!') or LOCAL_PATH_PREFIX.match(value):
                raise FactoryError('Foreman resources must select existing local paths.')
            selected = relative_path(path.parent, value)
            if not selected.is_file() and not selected.is_dir():
                raise FactoryError(f'Missing selected Foreman resource: {selected}')
            paths.append(str(selected))
        resources[key] = paths
    return {'cwd': str(directory), 'model': agent['model'], 'effort': agent['effort'],
            'resources': resources}
