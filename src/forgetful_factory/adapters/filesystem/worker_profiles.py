"""Local worker selections and completion evidence, without launching a worker."""
import hashlib
import json
import shutil
from pathlib import Path

from forgetful_factory.adapters.filesystem.resource_files import (
    check_real_path,
    write_json,
    write_new,
)
from forgetful_factory.adapters.host_dependencies import executable_path
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.domain.models import FactoryError

TEMPLATES = Path(__file__).resolve().parents[2] / 'resources'
WORKERS = ('implementation', 'review')
EXECUTABLES = {'pi': 'pi', 'codex': 'codex', 'claude_code': 'claude'}


class WorkerProfiles:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.directory = workspace / '.factory/agents'

    def skills(self, role: str, config: FactoryConfiguration) -> list[str]:
        paths = [str(self.directory / role / f'skills/{role}/SKILL.md')]
        if role == 'implementation':
            paths.append(config.tdd_skill)
        return [*paths, *getattr(config, f'{role}_skills')]

    @staticmethod
    def _skill_digest(value: str) -> str:
        source = Path(value)
        try:
            if not source.is_absolute() or not source.is_file():
                raise ValueError('Not an absolute regular file')
            return hashlib.sha256(source.read_bytes()).hexdigest()
        except (OSError, ValueError) as error:
            raise FactoryError(f'Worker skill must be an absolute readable regular file: {value}. '
                               'Correct the selected path and rerun init; files are preserved.'
                               ) from error

    def _validate_skill_sources(self, config: FactoryConfiguration) -> None:
        for role in WORKERS:
            selected = self.skills(role, config)
            # New role instructions come from our template; preserve and validate existing edits.
            source = Path(selected[0])
            if source.exists() or source.is_symlink():
                self._skill_digest(selected[0])
            for value in selected[1:]:
                self._skill_digest(value)

    def prepare(self, config: FactoryConfiguration) -> None:
        self._validate_skill_sources(config)
        for role in WORKERS:
            directory = self.directory / role
            relative = f'skills/{role}/SKILL.md'
            write_new(directory / relative, (TEMPLATES / role / relative).read_text())
            write_json(directory / 'resources.json', {
                'skills': self.skills(role, config), 'extensions': []})
            if getattr(config, f'{role}_agent_harness') == 'pi':
                write_json(directory / 'roster.json', {'roster': {'enabled': False}})

    def resources(self, role: str, config: FactoryConfiguration) -> dict:
        path = self.directory / role / 'resources.json'
        check_real_path(path)
        selected = json.loads(path.read_text())
        if (not isinstance(selected, dict) or set(selected) != {'skills', 'extensions'}
                or not isinstance(selected['skills'], list) or selected['extensions'] != []
                or not set(self.skills(role, config)) <= set(selected['skills'])):
            raise ValueError(f'Reconcile {role}/resources.json with configured skills')
        return selected

    def _role_selection(self, role: str, config: FactoryConfiguration) -> dict:
        harness = getattr(config, f'{role}_agent_harness')
        executable = shutil.which(EXECUTABLES[harness], path=executable_path(self.workspace))
        if executable is None:
            raise ValueError(f'Missing executable for {role}: {harness}')
        selected = self.resources(role, config)
        sources = {value: self._skill_digest(value) for value in selected['skills']}
        if harness == 'pi':
            roster = self.directory / role / 'roster.json'
            check_real_path(roster)
            if json.loads(roster.read_text()) != {'roster': {'enabled': False}}:
                raise ValueError(f'{role} child roster must be disabled')
        return {'harness': harness, 'executable': executable,
                'model': getattr(config, f'{role}_agent_model'),
                'effort': getattr(config, f'{role}_agent_effort'),
                'resources': selected, 'sources': sources}

    def selection(self, config: FactoryConfiguration) -> dict:
        try:
            return {role: self._role_selection(role, config) for role in WORKERS}
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise FactoryError('Incomplete worker setup; reconcile configured local skills, '
                               'resources.json and required executable, then rerun init. '
                               'Existing files are preserved. ' + str(error)) from error
