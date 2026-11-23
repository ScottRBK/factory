import shlex
import sys
from pathlib import Path

from forgetful_factory.adapters.agentshell.terminal import AgentShellTerminal
from forgetful_factory.adapters.filesystem.cleanup_receipts import FileCleanupReceipts
from forgetful_factory.adapters.filesystem.foreman_profile import ForemanProfile
from forgetful_factory.adapters.filesystem.git_repositories import GitRepositories
from forgetful_factory.adapters.filesystem.git_worktrees import GitWorktrees
from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.adapters.watch_status import ObservedTerminal
from forgetful_factory.application.cleanup_completed import CleanupCompleted
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.application.scaffold_issue import ScaffoldIssue
from forgetful_factory.application.watch_factory import WatchFactory
from forgetful_factory.deadlines import DeadlinePolicy
from forgetful_factory.forge.adapters.github import GitHubForge
from forgetful_factory.planning.adapters.forgetful.connection import role_environment
from forgetful_factory.planning.adapters.forgetful.plan_store import ForgetfulPlanStore
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.adapters.github import GitHubTicketing
from forgetful_factory.ticketing.ports import Ticketing

# Ticketing adapters by the provider name saved in factory.toml.
TICKETING = {'github': GitHubTicketing}


def build_initialiser(workspace: Path, deadlines: DeadlinePolicy = DeadlinePolicy()
                      ) -> InitialiseFactory:
    return InitialiseFactory(GitHubTicketing(deadlines.external_command),
                             TomlConfigurationStore(workspace),
                             GitRepositories(deadlines.external_command), GitHubForge(),
                             ForemanProfile(workspace, deadlines.owned_process_term_grace))


def select_ticketing(config: FactoryConfiguration, command_timeout: float) -> Ticketing:
    """Choose the ticketing adapter for the configured sources, and check every source."""
    providers = [repository.work_source.provider for repository in config.repository]
    for provider in providers:
        if provider not in TICKETING:
            raise FactoryError(f'Unsupported work-tracking provider {provider!r}; '
                               f'watch supports {", ".join(sorted(TICKETING))} only.')
    if len(set(providers)) != 1:
        raise FactoryError('All repositories must use the same work-tracking provider.')
    ticketing = TICKETING[providers[0]](command_timeout)
    for repository in config.repository:
        ticketing.validate_source(repository.work_source)
    return ticketing


def build_watcher(python: str, config: FactoryConfiguration, workspace: Path,
                  terminal=None, deadlines: DeadlinePolicy = DeadlinePolicy(),
                  observation=None) -> WatchFactory:
    ticketing = select_ticketing(config, deadlines.external_command)
    if config.forgetful is None:
        raise FactoryError('Shared Forgetful settings are missing; run init in a fresh factory. '
                           'Migration of old testing factories is not supported.')
    ticketing.check_ready()
    profile, environment, launch = prepare_foreman_launch(
        config, workspace, term_grace=deadlines.owned_process_term_grace)
    notice = profile.managed_memory_notice()
    if notice is not None:
        print(notice, flush=True)
    terminal = terminal or AgentShellTerminal(
        python, environment, **launch, deadlines=deadlines.agentshell)
    if observation is not None:
        terminal = ObservedTerminal(terminal, observation)
    planning = ForgetfulPlanStore(workspace, config.forgetful,
                                 execution_enabled=config.execution_enabled,
                                 term_grace=deadlines.owned_process_term_grace)
    worktrees = GitWorktrees(deadlines.external_command)
    scaffold = ScaffoldIssue(planning, worktrees, workspace, config,
                             GitRepositories(deadlines.external_command), GitHubForge())
    return WatchFactory(ticketing, terminal, scaffold,
                        CleanupCompleted(scaffold.records, scaffold.worktrees,
                                         FileCleanupReceipts(workspace), ticketing))


def prepare_foreman_launch(config: FactoryConfiguration, workspace: Path, *, complete=True,
                           term_grace: float = 3):
    profile = ForemanProfile(workspace, term_grace)
    if config.forgetful is None:
        raise FactoryError('Shared Forgetful settings are missing; complete first setup.')
    if complete:
        profile.validate_completion(config)
    launch = profile.selected_launch(config)
    environment = role_environment(workspace, config.forgetful, profile.pi_home())
    environment['FACTORY_COMMAND'] = shlex.join([sys.executable, '-m', 'forgetful_factory'])
    environment['FACTORY_WORKSPACE'] = str(workspace)
    environment['PI_AGENTSHELL_ROSTER_FILE'] = config.foreman_agent_file
    environment['FACTORY_FOREMAN_AGENT_FILE'] = str(
        Path(config.foreman_agent_file).absolute())
    return profile, environment, launch
