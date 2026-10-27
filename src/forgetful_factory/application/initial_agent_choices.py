"""One-time choices for the starter team; not saved Factory configuration."""
from dataclasses import dataclass

from forgetful_factory.application.configuration import nonblank
from forgetful_factory.domain.models import FactoryError


@dataclass(frozen=True)
class InitialAgentChoices:
    foreman_agent_model: str
    foreman_agent_effort: str
    foreman_memory_enabled: bool = False
    foreman_memory_model: str | None = None
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
    research_agent_model: str | None = None
    research_agent_harness: str | None = None
    research_agent_effort: str | None = None

    @property
    def execution_enabled(self) -> bool:
        return self.implementation_agent_model is not None


WORKER_FIELDS = ('implementation_agent_model', 'implementation_agent_harness',
                 'implementation_agent_effort', 'review_agent_model', 'review_agent_harness',
                 'review_agent_effort')
RESEARCH_FIELDS = ('research_agent_model', 'research_agent_harness', 'research_agent_effort')
WORKER_EFFORTS = {
    'pi': ('off', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max'),
    'codex': ('none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'max', 'ultra', 'persistent'),
    'claude_code': ('low', 'medium', 'high', 'xhigh', 'max'),
}
# AgentShell 0.5 AgentType values. Launch support alone does not imply skill support.
DOWNSTREAM_APPS = (*WORKER_EFFORTS, 'opencode', 'copilot_cli', 'cursor', 'grok')


def validate_role_app(harness: str, role: str) -> None:
    if harness not in DOWNSTREAM_APPS:
        raise FactoryError(f'{role} harness must be one of: ' + ', '.join(DOWNSTREAM_APPS))
    if harness in ('opencode', 'cursor'):
        raise FactoryError(f'{role}: AgentShell supports {harness}, but the bundled roster '
                           'requires effort and this app needs optional effort. Upstream roster '
                           'support is required; Factory will not invent an effort value. '
                           'Native selected skills also require validation before use.')
    if harness in ('copilot_cli', 'grok') or (
            role == 'research' and harness in ('codex', 'claude_code')):
        raise FactoryError(f'{role}: AgentShell 0.5 supports {harness} launches but not native '
                           'selected skills for this role. Upstream adapter support is required. '
                           'Existing Codex/Claude worker prompt compatibility is unchanged.')


def validate_workers(configuration: InitialAgentChoices) -> None:
    values = [getattr(configuration, field) for field in WORKER_FIELDS]
    if not any(value is not None for value in values) and not (
            configuration.tdd_skill is not None or configuration.implementation_skills
            or configuration.review_skills):
        return
    if any(value is None for value in values):
        raise FactoryError('Incomplete worker setup: configure both workers model/harness/effort, '
                           'or omit all worker settings for planning only.')
    for field in WORKER_FIELDS:
        nonblank(getattr(configuration, field), field)
    if configuration.tdd_skill is not None:
        nonblank(configuration.tdd_skill, 'tdd_skill')
    for role in ('implementation', 'review'):
        harness = getattr(configuration, f'{role}_agent_harness')
        validate_role_app(harness, role)
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


def _validate_foreman_memory(configuration: InitialAgentChoices) -> None:
    if configuration.foreman_memory_enabled and configuration.foreman_memory_model is None:
        raise FactoryError('Foreman automatic recall and capture requires a memory model.')
    if configuration.foreman_memory_model is not None:
        model = nonblank(configuration.foreman_memory_model, 'foreman_memory_model')
        if model.startswith('-') or any(ord(char) < 32 or ord(char) == 127 for char in model):
            raise FactoryError('Foreman memory model must be an exact native selector without '
                               'control characters.')


def validate_initial_agents(configuration: InitialAgentChoices) -> None:
    validate_workers(configuration)
    _validate_foreman_memory(configuration)
    research = [getattr(configuration, field) for field in RESEARCH_FIELDS]
    if any(value is not None for value in research):
        for field in RESEARCH_FIELDS:
            nonblank(getattr(configuration, field), field)
        validate_role_app(configuration.research_agent_harness, 'research')
        if configuration.research_agent_effort not in WORKER_EFFORTS['pi']:
            raise FactoryError('Research effort for pi must be one of: '
                               + ', '.join(WORKER_EFFORTS['pi']))
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
