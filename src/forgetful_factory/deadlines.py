"""Explicit production deadlines for programmatic Factory composition."""
import math
from dataclasses import dataclass, field, fields


def _validate_duration(name: str, value: object) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be positive and finite.')


@dataclass(frozen=True)
class AgentShellLifecycleDeadlines:
    controller_ready: float = 30
    controller_send: float = 10
    controller_close: float = 8
    parent_ready: float = 35
    owner_watcher_start: float = 30
    owner_watcher_stop: float = 5
    owner_ready: float = 35
    owner_controller_close: float = 20
    owner_pre_adoption_cleanup: float = 45

    def __post_init__(self) -> None:
        for item in fields(self):
            _validate_duration(item.name, getattr(self, item.name))


@dataclass(frozen=True)
class DeadlinePolicy:
    external_command: float = 30
    owned_process_term_grace: float = 3
    agentshell: AgentShellLifecycleDeadlines = field(
        default_factory=AgentShellLifecycleDeadlines,
    )

    def __post_init__(self) -> None:
        if not isinstance(self.agentshell, AgentShellLifecycleDeadlines):
            raise ValueError('agentshell must be an AgentShellLifecycleDeadlines value.')
        _validate_duration('external_command', self.external_command)
        _validate_duration('owned_process_term_grace', self.owned_process_term_grace)
