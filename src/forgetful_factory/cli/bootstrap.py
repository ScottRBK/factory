import shlex
import sys
from pathlib import Path

from forgetful_factory.adapters.agentshell.terminal import AgentShellTerminal
from forgetful_factory.adapters.filesystem.foreman_profile import ForemanProfile
from forgetful_factory.adapters.filesystem.git_repositories import GitRepositories
from forgetful_factory.adapters.filesystem.git_worktrees import GitWorktrees
from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.adapters.forgetful.connection import role_environment
from forgetful_factory.adapters.forgetful.planning import ForgetfulPlanning
from forgetful_factory.adapters.github.work_tracking import GitHubWorkTracking
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.application.scaffold_issue import ScaffoldIssue
from forgetful_factory.application.watch_factory import WatchFactory
from forgetful_factory.deadlines import DeadlinePolicy
from forgetful_factory.domain.models import FactoryError


def build_initialiser(workspace: Path, deadlines: DeadlinePolicy = DeadlinePolicy()
                      ) -> InitialiseFactory:
    github = GitHubWorkTracking(deadlines.external_command)
    return InitialiseFactory(github, TomlConfigurationStore(workspace),
                             GitRepositories(deadlines.external_command), github,
                             ForemanProfile(workspace, deadlines.owned_process_term_grace))


def build_watcher(python: str, config: FactoryConfiguration, workspace: Path,
                  terminal=None, deadlines: DeadlinePolicy = DeadlinePolicy()) -> WatchFactory:
    github = GitHubWorkTracking(deadlines.external_command)
    for repository in config.repository:
        source = repository.work_source
        if source.provider != 'github':
            raise FactoryError(f'Unsupported work-tracking provider {source.provider!r}; '
                               'watch supports github only.')
        try:
            resolved = github.source_from_remote(f'https://github.com/{source.reference}')
        except FactoryError as error:
            raise FactoryError(f'Invalid GitHub work source {source.reference!r}.') from error
        if resolved.reference != source.reference.casefold():
            raise FactoryError(f'Invalid GitHub work source {source.reference!r}.')
    if config.forgetful is None:
        raise FactoryError('Shared Forgetful settings are missing; run init in a fresh factory. '
                           'Migration of old testing factories is not supported.')
    profile, environment, launch = prepare_foreman_launch(
        config, workspace, term_grace=deadlines.owned_process_term_grace)
    notice = profile.managed_memory_notice()
    if notice is not None:
        print(notice, flush=True)
    return WatchFactory(
        github,
        terminal or AgentShellTerminal(
            python, environment, **launch, deadlines=deadlines.agentshell),
        ScaffoldIssue(ForgetfulPlanning(
                            workspace, config.forgetful,
                            execution_enabled=config.execution_enabled,
                            term_grace=deadlines.owned_process_term_grace),
                      GitWorktrees(deadlines.external_command), workspace, config,
                      GitRepositories(deadlines.external_command), github))


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
