from dataclasses import dataclass

from forgetful_factory.factory.model.repositories import RepositoryReference
from forgetful_factory.planning.model import ForgetfulConnection, connection_from_mapping
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.validation import nonblank
from forgetful_factory.ticketing.model import TicketSource


@dataclass(frozen=True)
class FactoryConfiguration:
    watcher_label: tuple[str, ...]
    foreman_agent_file: str
    repository: tuple[RepositoryReference, ...]
    forgetful: ForgetfulConnection | None = None
    execution_enabled: bool = False


def validate(configuration: FactoryConfiguration) -> None:
    nonblank(configuration.foreman_agent_file, 'foreman_agent_file')
    if type(configuration.execution_enabled) is not bool:
        raise FactoryError('execution_enabled must be a boolean.')
    if configuration.forgetful is not None:
        configuration.forgetful.validate()
    if not configuration.watcher_label:
        raise FactoryError('watcher_label must contain at least one nonblank string.')
    for label in configuration.watcher_label:
        nonblank(label, 'watcher_label')
    if not configuration.repository:
        raise FactoryError('repository must contain at least one repository.')

    paths = set()
    for index, repository in enumerate(configuration.repository, 1):
        field = f'repository[{index}]'
        nonblank(repository.local_dir, f'{field}.local_dir')
        if repository.local_dir in paths:
            raise FactoryError(f'Duplicate repository local_dir: {repository.local_dir}')
        paths.add(repository.local_dir)
        nonblank(repository.remote, f'{field}.remote')
        nonblank(repository.work_source.provider, f'{field}.provider')
        nonblank(repository.work_source.reference, f'{field}.source')


def from_mapping(data: dict) -> FactoryConfiguration:
    if 'repositories' in data:
        raise FactoryError('Old repositories format is no longer supported. '
                           'Replace each [repositories."path"] header with [[repository]] '
                           'in .factory/factory.toml, keeping its fields, then rerun init.')
    allowed = {'watcher_label', 'foreman_agent_file', 'execution_enabled',
               'repository', 'forgetful'}
    if set(data) - allowed:
        raise FactoryError('Unknown Factory settings. Agent choices belong in agent.json, '
                           'not factory.toml; existing files were preserved.')
    labels = data.get('watcher_label')
    repositories = data.get('repository')
    if not isinstance(labels, list):
        raise FactoryError('watcher_label must be a list of nonblank strings.')
    if not isinstance(repositories, list):
        raise FactoryError('repository must be a TOML array of tables using [[repository]].')
    references = []
    for index, item in enumerate(repositories, 1):
        if not isinstance(item, dict):
            raise FactoryError(f'repository[{index}] must be a repository table.')
        references.append(RepositoryReference(
            item.get('local_dir'), item.get('remote'),
            TicketSource(item.get('provider'), item.get('source')),
        ))
    configuration = FactoryConfiguration(
        tuple(labels), data.get('foreman_agent_file'), tuple(references),
        connection_from_mapping(data.get('forgetful')), data.get('execution_enabled', False),
    )
    validate(configuration)
    return configuration


def unique_labels(labels: list[str]) -> tuple[str, ...]:
    result = {}
    for label in labels:
        nonblank(label, 'watcher_label')
        result.setdefault(label.casefold(), label)
    return tuple(result.values())
