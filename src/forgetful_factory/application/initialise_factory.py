from pathlib import Path

from forgetful_factory.application.configuration import (
    FactoryConfiguration, unique_labels, validate,
)
from forgetful_factory.application.ports.configuration_store import ConfigurationStore
from forgetful_factory.application.ports.local_repositories import LocalRepositories
from forgetful_factory.application.ports.work_source_resolver import WorkSourceResolver
from forgetful_factory.domain.models import FactoryError, Label, RepositoryReference, WorkSource
from forgetful_factory.domain.services.work_tracking import WorkTrackingService


class InitialiseFactory:
    def __init__(self, tracking: WorkTrackingService, storage: ConfigurationStore,
                 repositories: LocalRepositories, sources: WorkSourceResolver):
        self.tracking = tracking
        self.storage = storage
        self.repositories = repositories
        self.sources = sources

    def load_existing(self, paths: list[Path] | None, labels: list[str] | None,
                      model: str | None, effort: str | None) -> FactoryConfiguration | None:
        config = self.storage.load()
        if config is None:
            return None
        conflicts = (
            paths is not None and {str(path) for path in paths} !=
            {repository.local_dir for repository in config.repositories.values()},
            labels is not None and {label.casefold() for label in unique_labels(labels)} !=
            {label.casefold() for label in config.watcher_label},
            model is not None and model != config.foreman_agent_model,
            effort is not None and effort != config.foreman_agent_effort,
        )
        if any(conflicts):
            raise FactoryError('Arguments conflict with existing config; edit '
                               '.factory/factory.toml explicitly, then rerun init.')
        return config

    def discover(self, workspace: Path) -> list[Path]:
        return self.repositories.discover(workspace)

    def inspect(self, paths: list[Path]) -> dict[str, RepositoryReference]:
        references = {}
        for path in paths:
            remote = self.repositories.origin(path)
            try:
                source = self.sources.source_from_remote(remote)
            except FactoryError as error:
                raise FactoryError(f'Repository {path}: {error}') from error
            references[str(path)] = RepositoryReference(str(path), remote, source)
        return references

    def configure(self, paths: list[Path], labels: list[str], model: str,
                  effort: str) -> FactoryConfiguration:
        references = self.inspect(paths)
        return FactoryConfiguration(unique_labels(labels), model, effort, references)

    def _preflight(self, config: FactoryConfiguration) -> dict[WorkSource, tuple[Label, ...]]:
        validate(config)
        for repository in config.repositories.values():
            remote = self.repositories.origin(Path(repository.local_dir))
            source = self.sources.source_from_remote(remote)
            if repository.work_source.provider != source.provider:
                raise FactoryError(
                    f'Unsupported work-tracking provider {repository.work_source.provider!r}; '
                    f'this integration supports {source.provider!r}. '
                    'Edit .factory/factory.toml and rerun init.'
                )
            if remote != repository.remote or source != repository.work_source:
                raise FactoryError(f'Origin/source changed for {repository.local_dir}; '
                                   'edit .factory/factory.toml and rerun init.')
        sources = dict.fromkeys(
            repository.work_source for repository in config.repositories.values()
        )
        for source in sources:
            self.tracking.check_access(source)
        return {source: self.tracking.list_labels(source) for source in sources}

    def _ensure_label(self, source: WorkSource, name: str, existing: set[str]) -> str:
        if name == '*':
            return f'Wildcard {source.reference}: watch all labels'
        if name.casefold() in existing:
            return f'Reused {source.reference}: {name}'
        self.tracking.create_label(source, Label(name))
        existing.add(name.casefold())
        return f'Created {source.reference}: {name}'

    def initialise(self, config: FactoryConfiguration, *, save: bool = True) -> list[str]:
        labels_by_source = self._preflight(config)
        messages = []
        operation = ''
        try:
            for source, labels in labels_by_source.items():
                existing = {label.name.casefold() for label in labels}
                for name in config.watcher_label:
                    operation = f'Creating {source.reference}: {name}'
                    messages.append(self._ensure_label(source, name, existing))
                    operation = ''
            if save:
                operation = 'Saving .factory/factory.toml'
                self.storage.save(config)
        except (FactoryError, OSError, KeyboardInterrupt) as error:
            detail = str(error) or 'Initialization interrupted'
            progress = '\n'.join(messages) or 'No completed label operations.'
            raise FactoryError(
                f'{operation} failed: {detail}\n{progress}\n'
                'Created labels are kept. The failed operation may have completed; '
                'check GitHub and the config file, then rerun init.'
            ) from error
        return messages
