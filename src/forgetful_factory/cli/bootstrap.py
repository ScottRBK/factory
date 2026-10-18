from pathlib import Path

from forgetful_factory.adapters.agentshell.terminal import AgentShellTerminal
from forgetful_factory.adapters.filesystem.foreman_profile import ForemanProfile
from forgetful_factory.adapters.filesystem.git_repositories import GitRepositories
from forgetful_factory.adapters.filesystem.git_worktrees import GitWorktrees
from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease
from forgetful_factory.adapters.forgetful.connection import role_environment
from forgetful_factory.adapters.forgetful.planning import ForgetfulPlanning
from forgetful_factory.adapters.github.work_tracking import GitHubWorkTracking
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.application.scaffold_issue import ScaffoldIssue
from forgetful_factory.application.watch_factory import WatchFactory
from forgetful_factory.domain.models import FactoryError


def build_initialiser(workspace: Path) -> InitialiseFactory:
    github = GitHubWorkTracking()
    return InitialiseFactory(github, TomlConfigurationStore(workspace),
                             GitRepositories(), github, ForemanProfile(workspace))


def build_watcher(python: str, config: FactoryConfiguration, workspace: Path) -> WatchFactory:
    github = GitHubWorkTracking()
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
    profile = ForemanProfile(workspace)
    profile.validate_guidance()
    profile.launch_resources()
    profile.validate_completion(config)
    profile.validate_setup(config.forgetful)
    environment = role_environment(workspace, config.forgetful, profile.pi_home())
    environment['PI_AGENTSHELL_ROSTER_FILE'] = str(profile.directory / 'roster.json')
    return WatchFactory(github, AgentShellTerminal(python, environment, profile.launch_resources(),
                                                  cwd=str(profile.directory)),
                        WorkspaceWatchLease(workspace),
                        ScaffoldIssue(ForgetfulPlanning(
                            workspace, config.forgetful,
                            execution_enabled=config.execution_enabled),
                                      GitWorktrees(), workspace, config))
