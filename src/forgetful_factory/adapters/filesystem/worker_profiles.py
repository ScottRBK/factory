"""Provision worker definitions; Factory never launches workers."""
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_skill_file,
    write_definition,
    write_new,
)
from forgetful_factory.application.initial_agent_choices import InitialAgentChoices

TEMPLATES = Path(__file__).resolve().parents[2] / 'resources'
WORKERS = ('implementation', 'review')


class WorkerProfiles:
    def __init__(self, workspace: Path):
        self.directory = workspace / '.factory/agents'

    def prepare(self, choices: InitialAgentChoices) -> None:
        for role in WORKERS:
            directory = self.directory / role
            skills = list(getattr(choices, f'{role}_skills'))
            if role == 'implementation' and choices.tdd_skill:
                skills.insert(0, choices.tdd_skill)
            for value in skills:
                check_skill_file(Path(value))
            relative = f'skills/{role}/SKILL.md'
            write_new(directory / relative, (TEMPLATES / role / relative).read_text())
            resources = {'skills': ['./skills', *skills]}
            harness = getattr(choices, f'{role}_agent_harness')
            if harness == 'pi':
                resources.update(extensions=[], plugins=[], packages=[], mcp_servers=[],
                                 inherit_personal_resources=False, inherit_project_resources=False,
                                 include_instruction_files=True, include_home_system_prompt=False)
            write_definition(directory / 'agent.json', {
                'agent': {'name': role, 'description': f'{role.capitalize()} assigned tasks',
                          'agent_type': harness, 'model': getattr(choices, f'{role}_agent_model'),
                          'effort': getattr(choices, f'{role}_agent_effort'),
                          'resources': resources},
                'roster': {'enabled': False, 'roles': []},
            })
