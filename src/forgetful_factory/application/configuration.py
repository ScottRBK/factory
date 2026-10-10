from dataclasses import dataclass

from forgetful_factory.domain.models import FactoryError, RepositoryReference, WorkSource


@dataclass(frozen=True)
class FactoryConfiguration:
    watcher_label: tuple[str, ...]
    foreman_agent_model: str
    foreman_agent_effort: str
    repository: tuple[RepositoryReference, ...]


def nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FactoryError(f'{field} must be a nonblank string.')
    if '\x00' in value:
        raise FactoryError(f'{field} must not contain NUL characters.')
    try:
        value.encode('utf-8')
    except UnicodeError as error:
        raise FactoryError(f'{field} must contain valid Unicode text.') from error
    return value


def validate(configuration: FactoryConfiguration) -> None:
    nonblank(configuration.foreman_agent_model, 'foreman_agent_model')
    nonblank(configuration.foreman_agent_effort, 'foreman_agent_effort')
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
            WorkSource(item.get('provider'), item.get('source')),
        ))
    configuration = FactoryConfiguration(
        tuple(labels), data.get('foreman_agent_model'), data.get('foreman_agent_effort'),
        tuple(references),
    )
    validate(configuration)
    return configuration


def unique_labels(labels: list[str]) -> tuple[str, ...]:
    result = {}
    for label in labels:
        nonblank(label, 'watcher_label')
        result.setdefault(label.casefold(), label)
    return tuple(result.values())
