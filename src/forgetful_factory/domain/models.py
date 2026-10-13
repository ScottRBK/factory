from dataclasses import dataclass


class FactoryError(Exception):
    """An actionable failure that can be displayed without a traceback."""


@dataclass(frozen=True)
class WorkSource:
    provider: str
    reference: str


@dataclass(frozen=True)
class RepositoryReference:
    local_dir: str
    remote: str
    work_source: WorkSource


@dataclass(frozen=True)
class Label:
    name: str


@dataclass(frozen=True)
class Issue:
    source: WorkSource
    number: int
    title: str
    url: str

    @property
    def id(self) -> str:
        return f'{self.source.provider}:{self.source.reference}#{self.number}'
