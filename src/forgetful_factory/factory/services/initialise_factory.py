from collections.abc import Callable, Sequence
from pathlib import Path

from forgetful_factory.agents.ports import AgentTeam
from forgetful_factory.factory.model.configuration import (
    FactoryConfiguration,
    unique_labels,
    validate,
)
from forgetful_factory.factory.model.repositories import RepositoryReference
from forgetful_factory.factory.ports import ConfigurationStore, ToolInstaller
from forgetful_factory.forge.ports import Forge
from forgetful_factory.planning.model import ForgetfulConnection
from forgetful_factory.planning.ports import PlanningSetup
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.model import Label, TicketSource
from forgetful_factory.ticketing.ports import Ticketing
from forgetful_factory.workspace.ports import LocalRepositories


def missing_tools(tools: Sequence[ToolInstaller]) -> list[str]:
    """Every absent tool first, then every tool that is present but not ready."""
    return ([name for tool in tools for name in tool.absent()]
            + [name for tool in tools for name in tool.unready()])


def _reviewed_install(tools: Sequence[ToolInstaller],
                      name: str) -> tuple[ToolInstaller | None, str | None]:
    """The first tool with a reviewed recipe for name, and its consent question."""
    for tool in tools:
        recipe = tool.describe(name)
        if recipe is not None:
            return tool, recipe
    return None, None


class InitialiseFactory:
    def __init__(self, tracking: Ticketing, storage: ConfigurationStore,
                 repositories: LocalRepositories, forge: Forge, team: AgentTeam,
                 planning: PlanningSetup,
                 tools: Callable[[ForgetfulConnection], Sequence[ToolInstaller]]):
        self.tracking = tracking
        self.storage = storage
        self.repositories = repositories
        self.forge = forge
        self.team = team
        self.planning = planning
        self.tools = tools

    def prepare_foreman(self, connection: ForgetfulConnection,
                        install: Callable[[list[str]], None],
                        confirm: Callable[[str, str], bool]) -> None:
        self.team.prepare()
        self.planning.prepare(connection)
        tools = self.tools(connection)
        missing = missing_tools(tools)
        if missing:
            for command in missing:
                installer, recipe = _reviewed_install(tools, command)
                if recipe is None:
                    install([command])
                elif confirm(command, recipe):
                    installer.install(command)
                else:
                    raise FactoryError('Installation declined; executable missing. '
                                       'Setup is incomplete; rerun init to retry.')
            if missing_tools(tools):
                raise FactoryError('Required executable still missing; setup is incomplete. '
                                   'Complete the reviewed installation and rerun init.')

    def check_foreman(self, config: FactoryConfiguration, *, login: bool) -> str:
        if login:
            self.planning.login(config.forgetful)
        return self.planning.check(config.forgetful, execution_enabled=config.execution_enabled)

    def load_existing(self, paths: list[Path] | None,
                      labels: list[str] | None) -> FactoryConfiguration | None:
        config = self.storage.load()
        if config is None:
            return None
        conflicts = (
            paths is not None and {str(path) for path in paths} !=
            {repository.local_dir for repository in config.repository},
            labels is not None and {label.casefold() for label in unique_labels(labels)} !=
            {label.casefold() for label in config.watcher_label},
        )
        if config.forgetful is None:
            raise FactoryError('Existing testing factory lacks shared Forgetful settings. '
                               'Initialize a fresh factory; migration is not supported.')
        if config.forgetful.project_id is None:
            raise FactoryError('Existing .factory/factory.toml lacks forgetful.project_id. '
                               'Edit its [forgetful] section to add project_id = <existing '
                               'numeric project ID>. Use init --finalize for incomplete saved '
                               'setup, or restart watch or foreman for completed setup. '
                               'Init does not migrate '
                               'existing config or save project choices over it; edits are '
                               'preserved.')
        if any(conflicts):
            raise FactoryError('Arguments conflict with existing config; correct the arguments '
                               'or edit .factory/factory.toml explicitly. Use init --finalize '
                               'for incomplete saved setup, or restart watch or foreman '
                               'for completed setup.')
        return config

    def discover(self, workspace: Path) -> list[Path]:
        return self.repositories.discover(workspace)

    def inspect(self, paths: list[Path]) -> dict[str, RepositoryReference]:
        references = {}
        for path in paths:
            remote = self.repositories.origin(path)
            try:
                hosted = self.forge.repository(remote)
            except FactoryError as error:
                raise FactoryError(f'Repository {path}: {error}') from error
            # Default: the forge also tracks the work, so its repository is the ticket source.
            source = TicketSource(hosted.forge, hosted.reference)
            references[str(path)] = RepositoryReference(str(path), remote, source)
        return references

    def configure(self, paths: list[Path], labels: list[str],
                  agent_file: str) -> FactoryConfiguration:
        references = self.inspect(paths)
        return FactoryConfiguration(unique_labels(labels), agent_file, tuple(references.values()))

    def _preflight(self, config: FactoryConfiguration) -> dict[TicketSource, tuple[Label, ...]]:
        validate(config)
        for repository in config.repository:
            remote = self.repositories.origin(Path(repository.local_dir))
            hosted = self.forge.repository(remote)
            source = repository.work_source
            # The remote names the ticket source only when one service is both forge and ticketing.
            same_service = hosted.forge == source.provider
            changed = remote != repository.remote or (same_service and hosted.reference
                                                      != source.reference)
            try:
                self.tracking.validate_source(source)
            except FactoryError as error:
                # A source the forge derived from this origin is accepted, as before the
                # ticketing port; the check names the fault only for a source that differs.
                if changed or not same_service:
                    raise FactoryError(
                        f'{error} Correct .factory/factory.toml, then use init --finalize for '
                        'incomplete saved setup, or restart watch or foreman for completed setup.'
                    ) from error
            if changed:
                raise FactoryError(f'Origin/source changed for {repository.local_dir}; '
                                   'review the origin and correct .factory/factory.toml if saved. '
                                   'Use init --finalize for incomplete saved setup, or restart '
                                   'watch or foreman for completed setup. If no configuration '
                                   'was saved, retry first init with the corrected repository.')
        sources = dict.fromkeys(
            repository.work_source for repository in config.repository
        )
        for source in sources:
            self.tracking.check_access(source)
        return {source: self.tracking.list_labels(source) for source in sources}

    def _ensure_label(self, source: TicketSource, name: str, existing: set[str]) -> str:
        if name == '*':
            return f'Wildcard {source.reference}: watch all labels'
        if name.casefold() in existing:
            return f'Reused {source.reference}: {name}'
        self.tracking.create_label(source, Label(name))
        existing.add(name.casefold())
        return f'Created {source.reference}: {name}'

    def initialise(self, config: FactoryConfiguration, *,
                   before_writes: Callable[[], FactoryConfiguration | None],
                   save: bool = True) -> list[str]:
        labels_by_source = self._preflight(config)
        config = before_writes() or config
        messages = []
        operation = ''
        try:
            for source, labels in labels_by_source.items():
                existing = {label.name.casefold() for label in labels}
                for name in config.watcher_label:
                    operation = f'Creating {source.reference}: {name}'
                    messages.append(self._ensure_label(source, name, existing))
                    operation = ''
            if save:
                operation = 'Saving .factory/factory.toml'
                self.storage.save(config)
        except (FactoryError, OSError, KeyboardInterrupt) as error:
            detail = str(error) or 'Initialization interrupted'
            progress = '\n'.join(messages) or 'No completed label operations.'
            raise FactoryError(
                f'{operation} failed: {detail}\n{progress}\n'
                'Created labels are kept. The failed operation may have completed; '
                'check GitHub and the config file, then rerun init.'
            ) from error
        return messages
