"""Planning: where plans and tasks are stored, and how Factory reaches that store."""
import sys
from dataclasses import dataclass
from ipaddress import ip_address
from pathlib import Path
from urllib.parse import urlsplit

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.shared.validation import nonblank


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
