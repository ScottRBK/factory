from dataclasses import dataclass

from forgetful_factory.domain.models import FactoryError, RepositoryReference, WorkSource


@dataclass(frozen=True)
class FactoryConfiguration:
    watcher_label: tuple[str, ...]
    foreman_agent_model: str
    foreman_agent_effort: str
    repositories: dict[str, RepositoryReference]


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
    if not configuration.repositories:
        raise FactoryError('repositories must contain at least one repository.')

    for key, repository in configuration.repositories.items():
        nonblank(key, 'repository key')
        nonblank(repository.local_dir, f'repositories.{key}.local_dir')
        nonblank(repository.remote, f'repositories.{key}.remote')
        nonblank(repository.work_source.provider, f'repositories.{key}.provider')
        nonblank(repository.work_source.reference, f'repositories.{key}.source')


def from_mapping(data: dict) -> FactoryConfiguration:
    labels = data.get('watcher_label')
    repositories = data.get('repositories')
    if not isinstance(labels, list):
        raise FactoryError('watcher_label must be a list of nonblank strings.')
    if not isinstance(repositories, dict):
        raise FactoryError('repositories must be a TOML dictionary of repository tables.')
    references = {}
    for key, item in repositories.items():
        if not isinstance(item, dict):
            raise FactoryError(f'repositories.{key} must be a repository table.')
        references[key] = RepositoryReference(
            item.get('local_dir'), item.get('remote'),
            WorkSource(item.get('provider'), item.get('source')),
        )
    configuration = FactoryConfiguration(
        tuple(labels), data.get('foreman_agent_model'), data.get('foreman_agent_effort'),
        references,
    )
    validate(configuration)
    return configuration


def unique_labels(labels: list[str]) -> tuple[str, ...]:
    result = {}
    for label in labels:
        nonblank(label, 'watcher_label')
        result.setdefault(label.casefold(), label)
    return tuple(result.values())
