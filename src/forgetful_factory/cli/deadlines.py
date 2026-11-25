"""Explicit production deadlines for programmatic Factory composition."""
from dataclasses import dataclass, field

from forgetful_factory.agents.model import AgentShellLifecycleDeadlines
from forgetful_factory.shared.validation import positive_duration


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
        positive_duration('external_command', self.external_command)
        positive_duration('owned_process_term_grace', self.owned_process_term_grace)
