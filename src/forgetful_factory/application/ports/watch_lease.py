from contextlib import AbstractContextManager
from typing import Protocol


class WatchLease(Protocol):
    def hold(self) -> AbstractContextManager[None]: ...
