"""Start the persistent Foreman, or reach the running one, and open a person's channel to it."""
import uuid
from collections.abc import Callable

from forgetful_factory.agents.ports import PersistentForeman
from forgetful_factory.channels.ports import Channel
from forgetful_factory.factory.ports import WatchLease
from forgetful_factory.shared.errors import FactoryError

# A new Foreman's memory notice (or None), role environment and launch data.
Launch = tuple[str | None, dict[str, str], dict]


class StartForeman:
    def __init__(self, lease: WatchLease, owner: PersistentForeman, channel: Channel,
                 prepare: Callable[[], Launch]):
        self.lease = lease
        self.owner = owner
        self.channel = channel
        self.prepare = prepare

    def run(self, *, attach: bool, notify: Callable[[str], None]) -> None:
        if attach:
            state = self.owner.status()
        else:
            with self.lease.hold():
                state = self.owner.saved()
                if state and state.get('foreman') != 'stopped':
                    raise FactoryError('Foreman already exists or is uncertain; use foreman '
                                       '--attach or watch --status. The existing owner was '
                                       'preserved.')
                notice, environment, launch = self.prepare()
                if notice is not None:
                    notify(notice)
                state = self.owner.start(environment, {
                    **launch, 'session_name': f'factory-foreman-{uuid.uuid4().hex[:12]}',
                    'prompt': None})
        if state['foreman'] != 'ready':
            raise FactoryError(state.get('warning', 'Foreman is not ready.') +
                               ' Foreman was preserved; inspect watch --status.')
        self.channel.open(state['target'])
