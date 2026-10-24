import sys
from dataclasses import dataclass
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlsplit

from forgetful_factory.domain.models import FactoryError, RepositoryReference, WorkSource


@dataclass(frozen=True)
class ForgetfulConnection:
    method: str = 'cli'
    instance: str = 'local'
    executable: str = 'forgetful'
    database: str | None = None
    server: str | None = None
    project_id: int | None = None

    def validate(self) -> None:
        if self.project_id is not None and (
                type(self.project_id) is not int or self.project_id <= 0):
            raise FactoryError('forgetful.project_id must be a positive numeric project ID.')
        if self.method == 'mcp':
            raise FactoryError('Forgetful MCP configuration is unsupported in this slice. '
                               'For new setup select --forgetful-method cli. For saved setup, '
                               'explicitly set method = "cli" in .factory/factory.toml, then use '
                               'init --finalize if incomplete, or restart watch or foreman '
                               'if completed. Existing role files are preserved.')
        if self.method != 'cli' or self.instance not in ('local', 'server'):
            raise FactoryError('Forgetful requires method cli and instance local/server.')
        if sys.platform != 'linux':
            raise FactoryError('Forgetful CLI configuration requires Linux/WSL.')
        nonblank(self.executable, 'forgetful.executable')
        if self.executable.startswith('-') or any(c in self.executable for c in '\r\n'):
            raise FactoryError('forgetful.executable must identify one executable.')
        if self.instance == 'local':
            nonblank(self.database, 'forgetful.database')
            if not Path(self.database).is_absolute() or self.server is not None:
                raise FactoryError('Local Forgetful requires an absolute database path '
                                   'and no server.')
        else:
            self._validate_server()

    def _validate_server(self) -> None:
        nonblank(self.server, 'forgetful.server')
        try:
            url = urlsplit(self.server)
            valid = (url.scheme in ('http', 'https') and url.hostname and not url.username
                     and not url.password and not url.query and not url.fragment
                     and not any(c.isspace() for c in self.server))
            _ = url.port
        except ValueError:
            valid = False
        if not valid or self.database is not None:
            raise FactoryError('Forgetful server must be an HTTP(S) URL without credentials, '
                               'query, fragment, or local database.')
        if url.scheme == 'http' and not loopback_host(url.hostname):
            raise FactoryError('Remote Forgetful requires HTTPS; HTTP is allowed only '
                               'for localhost or a loopback address.')

def loopback_host(host: str) -> bool:
    if host.casefold().rstrip('.') == 'localhost':
        return True
    try:
        return ip_address(host).is_loopback
    except ValueError:
        return False


def connection_from_mapping(data: object) -> ForgetfulConnection | None:
    if data is None:
        return None
    allowed = {'method', 'instance', 'executable', 'database', 'server', 'project_id'}
    if not isinstance(data, dict) or set(data) - allowed:
        raise FactoryError('Invalid Forgetful settings; credentials belong in Pi/CLI storage.')
    connection = ForgetfulConnection(**data)
    connection.validate()
    return connection


@dataclass(frozen=True)
class FactoryConfiguration:
    watcher_label: tuple[str, ...]
    foreman_agent_file: str
    repository: tuple[RepositoryReference, ...]
    forgetful: ForgetfulConnection | None = None
    execution_enabled: bool = False


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
            WorkSource(item.get('provider'), item.get('source')),
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
