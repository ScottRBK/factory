"""Provision native role instructions and explicit child rosters; no launch/auth wrapper."""
import json
import os
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_skill_file,
    read_generated_json,
    write_definition,
    write_json,
    write_new,
)
from forgetful_factory.adapters.filesystem.worker_profiles import WorkerProfiles
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.domain.models import FactoryError

TEMPLATES = Path(__file__).resolve().parents[2] / 'resources'
ROLE_INSTRUCTIONS_FILE = 'AGENTS.md'
LOCAL_SKILLS_DIRECTORY = './skills'


def selected_resources(skills: list[str], extensions: list[str]) -> dict:
    return {'skills': skills, 'extensions': extensions, 'plugins': [], 'packages': [],
            'mcp_servers': [], 'inherit_personal_resources': False,
            'inherit_project_resources': False, 'include_instruction_files': True,
            'include_home_system_prompt': False}


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

    def prepare(self, config: FactoryConfiguration, choices) -> None:
        """Write the starter tree once, descendants before their parents."""
        self.validate_guidance(config)
        if not choices.grill_me_skill:
            raise FactoryError('Owner setup needs an existing unchanged grill-me SKILL.md.')
        check_skill_file(Path(choices.grill_me_skill))
        for role in ('foreman', 'feature-owner', 'research'):
            paths = (ROLE_INSTRUCTIONS_FILE,) if role == 'foreman' else (
                ROLE_INSTRUCTIONS_FILE, f'skills/{role}/SKILL.md')
            for relative in paths:
                content = (TEMPLATES / role / relative).read_text()
                content = content.replace('@GRILL_ME@', json.dumps(choices.grill_me_skill))
                write_new(self.directory / role / relative, content)
        children = ['research']
        self._write_agent('research', choices.research_agent_model or
                          choices.feature_owner_agent_model,
                          choices.research_agent_effort or choices.feature_owner_agent_effort,
                          'Gather facts and return context', [],
                          selected_resources([LOCAL_SKILLS_DIRECTORY], []))
        if config.execution_enabled:
            self.workers.prepare(choices)
            children.extend(('implementation', 'review'))
        extension = '../../resources/agentshell/extensions/agentshell.ts'
        self._write_agent('feature-owner', choices.feature_owner_agent_model,
                          choices.feature_owner_agent_effort, 'Plan and own a feature', children,
                          selected_resources([LOCAL_SKILLS_DIRECTORY, choices.grill_me_skill],
                                             [extension]))
        foreman_extensions = [
            '../../resources/agentshell/extensions/agentshell.ts',
            '../../resources/hide-tools/index.ts',
            '../../resources/pi-forgetful/factory.ts',
        ]
        self._write_agent('foreman', choices.foreman_agent_model, choices.foreman_agent_effort,
                          'Coordinate the factory and its feature owners', ['feature-owner'],
                          selected_resources([LOCAL_SKILLS_DIRECTORY], foreman_extensions))
        self._write_foreman_memory(choices)

    def _write_foreman_memory(self, choices) -> None:
        path = self.directory / 'foreman/forgetful.json'
        value = {
            'enabled': choices.foreman_memory_enabled,
            'capture_mode': 'auto' if choices.foreman_memory_enabled else 'off',
            'model': choices.foreman_memory_model,
        }
        write_json(path, value)
        try:
            saved = read_generated_json(path)
            if json.dumps(saved, sort_keys=True) == json.dumps(value, sort_keys=True):
                return
        except (OSError, ValueError, UnicodeError):
            pass
        raise FactoryError(f'Existing Foreman memory preferences differ or are invalid: {path}. '
                           'The file is preserved. Review it and retry first setup with matching '
                           'choices, or explicitly move the conflicting file aside.')

    def _write_agent(self, name, model, effort, description, children, resources):
        write_definition(self.directory / name / 'agent.json', {
            'agent': {'name': name, 'description': description, 'agent_type': 'pi',
                      'model': model, 'effort': effort, 'cwd': '.', 'resources': resources},
            'roster': {'enabled': bool(children),
                       'roles': [{'agent_file': f'../{child}/agent.json'} for child in children]},
        })

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
