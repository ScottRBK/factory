from pathlib import Path

from forgetful_factory.adapters.filesystem.git_repositories import GitRepositories
from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.adapters.github.work_tracking import GitHubWorkTracking
from forgetful_factory.application.initialise_factory import InitialiseFactory


def build_initialiser(workspace: Path) -> InitialiseFactory:
    github = GitHubWorkTracking()
    return InitialiseFactory(github, TomlConfigurationStore(workspace),
                             GitRepositories(), github)
