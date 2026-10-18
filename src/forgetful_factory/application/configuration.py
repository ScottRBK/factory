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
                               'Explicitly set method = "cli" in .factory/factory.toml and '
                               'rerun init; existing role files are preserved.')
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
    foreman_agent_model: str
    foreman_agent_effort: str
    repository: tuple[RepositoryReference, ...]
    forgetful: ForgetfulConnection | None = None
    feature_owner_agent_model: str | None = None
    feature_owner_agent_effort: str | None = None
    feature_owner_agent_harness: str = 'pi'
    grill_me_skill: str | None = None
    implementation_agent_model: str | None = None
    implementation_agent_harness: str | None = None
    implementation_agent_effort: str | None = None
    review_agent_model: str | None = None
    review_agent_harness: str | None = None
    review_agent_effort: str | None = None
    tdd_skill: str | None = None
    implementation_skills: tuple[str, ...] = ()
    review_skills: tuple[str, ...] = ()

    @property
    def execution_enabled(self) -> bool:
        return self.implementation_agent_model is not None


WORKER_FIELDS = ('implementation_agent_model', 'implementation_agent_harness',
                 'implementation_agent_effort', 'review_agent_model', 'review_agent_harness',
                 'review_agent_effort', 'tdd_skill')
WORKER_EFFORTS = {
    'pi': ('off', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max'),
    'codex': ('none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra', 'persistent'),
    'claude_code': ('low', 'medium', 'high', 'xhigh', 'max'),
}


def validate_workers(configuration: FactoryConfiguration) -> None:
    values = [getattr(configuration, field) for field in WORKER_FIELDS]
    if not any(value is not None for value in values) and not (
            configuration.implementation_skills or configuration.review_skills):
        return
    if any(value is None for value in values):
        raise FactoryError('Incomplete worker setup: configure both workers model/harness/effort '
                           'and tdd_skill, or omit all worker settings for planning only.')
    for field in WORKER_FIELDS:
        nonblank(getattr(configuration, field), field)
    for role in ('implementation', 'review'):
        harness = getattr(configuration, f'{role}_agent_harness')
        if harness not in WORKER_EFFORTS:
            raise FactoryError(f'{role} harness must be pi, codex or claude_code.')
        effort = getattr(configuration, f'{role}_agent_effort')
        if effort not in WORKER_EFFORTS[harness]:
            raise FactoryError(f'{role} effort for {harness} must be one of: '
                               + ', '.join(WORKER_EFFORTS[harness]))
        model = getattr(configuration, f'{role}_agent_model')
        if model.startswith('-') or any(ord(c) < 32 or ord(c) == 127 for c in model):
            raise FactoryError(f'{role} model must be a native selector '
                               'without control characters.')


def skill_paths(data: dict, field: str) -> tuple[str, ...]:
    paths = data.get(field, [])
    if not isinstance(paths, list):
        raise FactoryError(f'{field} must be a list of local skill paths.')
    return tuple(nonblank(path, field) for path in paths)


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
    validate_workers(configuration)
    if configuration.forgetful is not None:
        configuration.forgetful.validate()
    nonblank(configuration.foreman_agent_model, 'foreman_agent_model')
    nonblank(configuration.foreman_agent_effort, 'foreman_agent_effort')
    efforts = ('off', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max')
    for effort in (configuration.foreman_agent_effort, configuration.feature_owner_agent_effort):
        if effort is not None and effort not in efforts:
            raise FactoryError('Pi effort must be one of: ' + ', '.join(efforts))
    if configuration.feature_owner_agent_harness != 'pi':
        raise FactoryError('The feature-owner harness must be pi for native session tracking.')
    if configuration.feature_owner_agent_model is not None:
        nonblank(configuration.feature_owner_agent_model, 'feature_owner_agent_model')
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
        tuple(references), connection_from_mapping(data.get('forgetful')),
        data.get('feature_owner_agent_model'), data.get('feature_owner_agent_effort'),
        data.get('feature_owner_agent_harness', 'pi'), data.get('grill_me_skill'),
        data.get('implementation_agent_model'), data.get('implementation_agent_harness'),
        data.get('implementation_agent_effort'), data.get('review_agent_model'),
        data.get('review_agent_harness'), data.get('review_agent_effort'), data.get('tdd_skill'),
        skill_paths(data, 'implementation_skills'), skill_paths(data, 'review_skills'),
    )
    validate(configuration)
    return configuration


def unique_labels(labels: list[str]) -> tuple[str, ...]:
    result = {}
    for label in labels:
        nonblank(label, 'watcher_label')
        result.setdefault(label.casefold(), label)
    return tuple(result.values())
