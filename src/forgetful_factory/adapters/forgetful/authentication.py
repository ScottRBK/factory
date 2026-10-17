"""Read public server policy for guidance only; native Forgetful still owns authentication."""
import json
from contextlib import closing
from http.client import HTTPConnection, HTTPException, HTTPSConnection
from urllib.parse import urlsplit

from forgetful_factory.application.configuration import ForgetfulConnection


def uses_browser_login(connection: ForgetfulConnection) -> bool:
    if connection.instance != 'server':
        return False
    server = urlsplit(connection.server)
    path = server.path.rstrip('/')
    if path.endswith('/mcp'):
        path = path[:-4]
    elif path:
        # The application prefix of an arbitrary custom MCP route is unknown.
        return False
    client = HTTPSConnection if server.scheme == 'https' else HTTPConnection
    try:
        # No credentials, proxy environment, redirect following or loginUrl navigation.
        with closing(client(server.hostname, server.port, timeout=2)) as request:
            request.request('GET', path + '/api/v1/auth/info',
                            headers={'Accept': 'application/json'})
            response = request.getresponse()
            if response.status != 200:
                return False
            data = response.read(8193)
            if len(data) > 8192:
                return False
            policy = json.loads(data)
        return (isinstance(policy, dict) and policy.get('authEnabled') is True
                and policy.get('authMode') == 'oauth')
    except (OSError, HTTPException, ValueError):
        # Metadata is optional. An unavailable policy must not bypass the real access check.
        return False
