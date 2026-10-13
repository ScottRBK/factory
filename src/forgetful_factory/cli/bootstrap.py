from pathlib import Path

from forgetful_factory.adapters.agentshell.terminal import AgentShellTerminal
from forgetful_factory.adapters.filesystem.git_repositories import GitRepositories
from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.adapters.filesystem.watch_lease import WorkspaceWatchLease
from forgetful_factory.adapters.github.work_tracking import GitHubWorkTracking
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.application.initialise_factory import InitialiseFactory
from forgetful_factory.application.watch_factory import WatchFactory
from forgetful_factory.domain.models import FactoryError


def build_initialiser(workspace: Path) -> InitialiseFactory:
    github = GitHubWorkTracking()
    return InitialiseFactory(github, TomlConfigurationStore(workspace),
                             GitRepositories(), github)


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
    return WatchFactory(github, AgentShellTerminal(python), WorkspaceWatchLease(workspace))
