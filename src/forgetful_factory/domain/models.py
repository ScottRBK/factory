from dataclasses import dataclass


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
    body: str = ''
    revision: str = ''
    epic: bool = False

    @property
    def id(self) -> str:
        return f'{self.source.provider}:{self.source.reference.casefold()}#{self.number}'
