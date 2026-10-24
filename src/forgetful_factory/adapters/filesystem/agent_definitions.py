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


def relative_path(directory: Path, value: str) -> Path:
    """Lexical resolution keeps references relative to the selected file, including symlinks."""
    nonblank(value, 'agent path')
    return Path(os.path.abspath(directory / value))


def read_definition(path: Path) -> dict:
    try:
        document = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(document, dict) or set(document) != {'agent', 'roster'}:
            raise ValueError('Expected exactly agent and roster')
        agent = document['agent']
        required = {'name', 'description', 'agent_type', 'model', 'effort'}
        if (not isinstance(agent, dict) or not required <= set(agent)
                or set(agent) - required - {'cwd', 'resources'}):
            raise ValueError('Invalid agent fields')
        for key in required:
            nonblank(agent[key], f'agent.{key}')
        if 'cwd' in agent:
            nonblank(agent['cwd'], 'agent.cwd')
            if re.match(r'(?i)^(?:[a-z]+:|~)', agent['cwd']):
                raise ValueError('Agent cwd must select a local path')
        roster = document['roster']
        if (not isinstance(roster, dict) or set(roster) - {'enabled', 'roles'}
                or type(roster.get('enabled', False)) is not bool
                or not isinstance(roster.get('roles', []), list)):
            raise ValueError('Expected roster enabled and reference-only roles')
        for child in roster.get('roles', []):
            if not isinstance(child, dict) or set(child) != {'agent_file'}:
                raise ValueError('Child entries contain only agent_file')
            nonblank(child['agent_file'], 'agent_file')
            if re.match(r'(?i)^(?:[a-z]+:|~)', child['agent_file']):
                raise ValueError('Child agent_file must select a local file')
            if not relative_path(path.parent, child['agent_file']).is_file():
                raise ValueError('Child agent_file must select an existing regular file')
        if agent['agent_type'] != 'pi' and (roster.get('enabled', False)
                                          or roster.get('roles', [])):
            raise ValueError('Non-Pi agents require a disabled empty roster')
        resources = agent.get('resources', {})
        if not isinstance(resources, dict) or set(resources) - {
                *PATH_RESOURCES, 'packages', 'mcp_servers', *RESOURCE_FLAGS}:
            raise ValueError('Invalid native resources')
        for key in (*PATH_RESOURCES, 'packages'):
            if key in resources and not isinstance(resources[key], list):
                raise ValueError(f'Expected resource list: {key}')
        if resources.get('mcp_servers') is not None and resources['mcp_servers'] != []:
            raise ValueError('Resource mcp_servers supports only null or []')
        for key in RESOURCE_FLAGS:
            if key in resources and type(resources[key]) is not bool:
                raise ValueError(f'Resource {key} must be a boolean')
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
            if value.startswith('!') or re.match(r'(?i)^(?:[a-z]+:|~)', value):
                raise FactoryError('Foreman resources must select existing local paths.')
            selected = relative_path(path.parent, value)
            if not selected.is_file() and not selected.is_dir():
                raise FactoryError(f'Missing selected Foreman resource: {selected}')
            paths.append(str(selected))
        resources[key] = paths
    return {'cwd': str(directory), 'model': agent['model'], 'effort': agent['effort'],
            'resources': resources}
