"""Watch-local stop intent survives an exception discarded by a Python finalizer."""
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass


@dataclass
class WatchStop:
    requested: bool = False

    def interrupt(self, _signum, _frame) -> None:
        # Store intent first. CPython can discard the exception if it occurs inside __del__.
        self.requested = True
        raise KeyboardInterrupt


_active: ContextVar[WatchStop | None] = ContextVar('factory_watch_stop', default=None)


@contextmanager
def watch_stop_scope():
    stop = WatchStop()
    token = _active.set(stop)
    try:
        yield stop
    finally:
        _active.reset(token)


def check_watch_stop() -> None:
    stop = _active.get()
    if stop is not None and stop.requested:
        raise KeyboardInterrupt
