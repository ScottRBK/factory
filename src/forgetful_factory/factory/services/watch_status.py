"""Report the watcher's lifecycle from live or saved records; never control a process."""
from collections.abc import Callable

from forgetful_factory.agents.model import unknown_status
from forgetful_factory.agents.ports import AgentTeam, PersistentForeman
from forgetful_factory.factory.ports import ConfigurationStore
from forgetful_factory.shared.errors import FactoryError


class WatchStatus:
    """A live plain watcher wins, then a live owner. Saved records stay historical evidence.

    plain() reads the plain watcher's report, or None when no plain watcher was recorded.
    """

    def __init__(self, plain: Callable[[], dict | None], owner: PersistentForeman,
                 storage: ConfigurationStore, team: AgentTeam):
        self.plain = plain
        self.owner = owner
        self.storage = storage
        self.team = team

    def report(self) -> dict:
        plain = self.plain()
        if plain and plain['observation'] == 'live':
            state = plain
        else:
            managed = self.owner.report()
            if managed and managed['observation'] == 'live':
                state = managed
            elif plain and managed:
                state = {**managed, 'source': 'combined', 'foreman': 'unknown',
                         'watcher': 'unknown', 'phase': 'unknown', 'process': 'unknown',
                         'health': 'not_checked',
                         'observation': ('saved' if 'saved' in (plain['observation'],
                                                              managed['observation'])
                                         else 'unavailable'),
                         'evidence': 'multiple_records', 'plain_watch': plain}
            else:
                state = plain or managed or unknown_status()
        try:
            # Setup counts as complete only when the configuration also loads.
            complete = self.storage.load() is not None
            if complete:
                self.team.validate_completion()
        except (FactoryError, OSError):
            complete = False
        state['setup'] = 'complete' if complete else 'incomplete'
        return state
