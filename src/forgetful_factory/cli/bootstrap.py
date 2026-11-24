import shlex
import sys
from functools import partial
from pathlib import Path

from forgetful_factory.agents.adapters.agentshell.owner_client import AgentShellOwner
from forgetful_factory.agents.adapters.agentshell.runtime_install import AgentShellRuntimeInstall
from forgetful_factory.agents.adapters.agentshell.terminal import AgentShellTerminal
from forgetful_factory.agents.adapters.pi.agent_team import PiAgentTeam
from forgetful_factory.agents.adapters.pi.runtime_install import PiInstall
from forgetful_factory.channels.adapters.terminal import TerminalChannel
from forgetful_factory.cli.deadlines import DeadlinePolicy
from forgetful_factory.configuration import load_configuration
from forgetful_factory.factory.adapters.cleanup_receipts import FileCleanupReceipts
from forgetful_factory.factory.adapters.toml_configuration import TomlConfigurationStore
from forgetful_factory.factory.adapters.watch_lease import WorkspaceWatchLease
from forgetful_factory.factory.adapters.watch_status import ObservedTerminal, plain_watch_status
from forgetful_factory.factory.model.configuration import FactoryConfiguration
from forgetful_factory.factory.services.cleanup_completed import CleanupCompleted
from forgetful_factory.factory.services.initialise_factory import InitialiseFactory, missing_tools
from forgetful_factory.factory.services.scaffold_issue import ScaffoldIssue
from forgetful_factory.factory.services.start_foreman import StartForeman
from forgetful_factory.factory.services.watch_factory import WatchFactory
from forgetful_factory.factory.services.watch_status import WatchStatus
from forgetful_factory.forge.adapters.github import GitHubForge
from forgetful_factory.planning.adapters.forgetful.connection import role_environment
from forgetful_factory.planning.adapters.forgetful.install import ForgetfulInstall
from forgetful_factory.planning.adapters.forgetful.plan_store import ForgetfulPlanStore
from forgetful_factory.planning.adapters.forgetful.setup import ForgetfulSetup
from forgetful_factory.planning.model import ForgetfulConnection
from forgetful_factory.runtime.adapters.tmux import TmuxHost, TmuxInstall
from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.adapters.github import GitHubTicketing
from forgetful_factory.ticketing.ports import Ticketing
from forgetful_factory.workspace.adapters.git.repositories import GitRepositories
from forgetful_factory.workspace.adapters.git.worktrees import GitWorktrees

# Ticketing adapters by the provider name saved in factory.toml.
TICKETING = {'github': GitHubTicketing}


def build_host() -> TmuxHost:
    """AgentShell supports interactive sessions on tmux only."""
    return TmuxHost()


def build_channel() -> TerminalChannel:
    """People reach the Foreman in their own terminal, through the session host."""
    return TerminalChannel(build_host())


def build_owner(workspace: Path, python: str,
                deadlines: DeadlinePolicy = DeadlinePolicy()) -> AgentShellOwner:
    """The persistent owner that keeps the Foreman open between commands."""
    return AgentShellOwner(workspace, python, deadlines.agentshell, host=build_host())


def build_tools(workspace: Path, connection: ForgetfulConnection, term_grace: float = 3):
    """The tools Factory installs. Init offers them in this order within each group."""
    return (PiInstall(workspace, term_grace), TmuxInstall(workspace, term_grace),
            ForgetfulInstall(workspace, connection, term_grace),
            AgentShellRuntimeInstall(workspace, term_grace))


def build_team(workspace: Path, term_grace: float = 3) -> PiAgentTeam:
    return PiAgentTeam(workspace, term_grace,
                       role_environment=partial(role_environment, workspace),
                       missing_tools=lambda connection: missing_tools(
                           build_tools(workspace, connection, term_grace)))


def build_initialiser(workspace: Path, deadlines: DeadlinePolicy = DeadlinePolicy()
                      ) -> InitialiseFactory:
    term_grace = deadlines.owned_process_term_grace
    return InitialiseFactory(GitHubTicketing(deadlines.external_command),
                             TomlConfigurationStore(workspace),
                             GitRepositories(deadlines.external_command), GitHubForge(),
                             build_team(workspace, term_grace),
                             ForgetfulSetup(workspace, term_grace),
                             partial(build_tools, workspace, term_grace=term_grace))


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
        python, environment, **launch, deadlines=deadlines.agentshell, host=build_host(),
        channel=build_channel())
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
    profile = build_team(workspace, term_grace)
    if config.forgetful is None:
        raise FactoryError('Shared Forgetful settings are missing; complete first setup.')
    if complete:
        profile.validate_completion()
    launch = profile.selected_launch(config.foreman_agent_file, config.forgetful)
    environment = role_environment(workspace, config.forgetful, profile.pi_home())
    environment['FACTORY_COMMAND'] = shlex.join([sys.executable, '-m', 'forgetful_factory'])
    environment['FACTORY_WORKSPACE'] = str(workspace)
    environment['PI_AGENTSHELL_ROSTER_FILE'] = config.foreman_agent_file
    environment['FACTORY_FOREMAN_AGENT_FILE'] = str(
        Path(config.foreman_agent_file).absolute())
    return profile, environment, launch


def build_watch_status(workspace: Path, python: str,
                       deadlines: DeadlinePolicy = DeadlinePolicy()) -> WatchStatus:
    return WatchStatus(partial(plain_watch_status, workspace),
                       build_owner(workspace, python, deadlines),
                       TomlConfigurationStore(workspace), build_team(workspace))


def build_start_foreman(workspace: Path, python: str,
                        deadlines: DeadlinePolicy = DeadlinePolicy()) -> StartForeman:
    def prepare():
        config = load_configuration(workspace)
        team, environment, launch = prepare_foreman_launch(
            config, workspace, term_grace=deadlines.owned_process_term_grace)
        return team.managed_memory_notice(), environment, launch

    return StartForeman(WorkspaceWatchLease(workspace), build_owner(workspace, python, deadlines),
                        build_channel(), prepare)
