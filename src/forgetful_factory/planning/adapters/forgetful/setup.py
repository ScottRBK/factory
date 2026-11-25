"""First setup of Forgetful planning through the native CLI: project, sign-in and checks."""
from pathlib import Path

from forgetful_factory.planning.adapters.forgetful.authentication import uses_browser_login
from forgetful_factory.planning.adapters.forgetful.connection import AgentForgetfulConnection
from forgetful_factory.planning.model import ForgetfulConnection


class ForgetfulSetup:
    def __init__(self, workspace: Path, term_grace: float = 3):
        self.workspace = workspace
        self.term_grace = term_grace

    def _native(self) -> AgentForgetfulConnection:
        return AgentForgetfulConnection(self.workspace, self.term_grace)

    def projects(self, connection: ForgetfulConnection) -> list[dict]:
        return self._native().projects(connection)

    def create_project(self, connection: ForgetfulConnection, name: str) -> int:
        return self._native().create_project(connection, name)

    def prepare(self, connection: ForgetfulConnection) -> None:
        if connection.instance == 'local':
            Path(connection.database).parent.mkdir(parents=True, exist_ok=True, mode=0o700)

    def uses_browser_login(self, connection: ForgetfulConnection) -> bool:
        return uses_browser_login(connection)

    def login(self, connection: ForgetfulConnection) -> None:
        self._native().login(connection)

    def check(self, connection: ForgetfulConnection, *, execution_enabled: bool) -> str:
        self._native().check(connection, execution_enabled=execution_enabled)
        return 'Forgetful: connected; selected project and planning permissions verified.'
