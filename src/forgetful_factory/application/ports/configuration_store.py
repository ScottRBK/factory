from typing import Protocol

from forgetful_factory.application.configuration import FactoryConfiguration


class ConfigurationStore(Protocol):
    def load(self) -> FactoryConfiguration | None: ...

    def save(self, configuration: FactoryConfiguration) -> None: ...
