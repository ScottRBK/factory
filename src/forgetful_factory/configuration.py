"""Public workspace configuration loading API."""
from pathlib import Path

from forgetful_factory.adapters.filesystem.toml_configuration import TomlConfigurationStore
from forgetful_factory.application.configuration import FactoryConfiguration
from forgetful_factory.domain.models import FactoryError


def load_configuration(workspace: str | Path) -> FactoryConfiguration:
    configuration = TomlConfigurationStore(Path(workspace)).load()
    if configuration is None:
        raise FactoryError(f'No .factory/factory.toml in {workspace}; run init first.')
    return configuration
