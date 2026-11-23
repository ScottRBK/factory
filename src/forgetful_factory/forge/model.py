"""Repositories on a forge: where code is hosted, reviewed and merged."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RepositoryRef:
    forge: str
    reference: str
