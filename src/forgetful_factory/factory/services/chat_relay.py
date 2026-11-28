"""The rules between the Foreman and a chat room. A chat problem never stops watch."""
import time
from collections.abc import Callable

from forgetful_factory.agents.ports import ForemanTerminal
from forgetful_factory.channels.model import ChatMessage, Delivery
from forgetful_factory.channels.ports import ChatChannel
from forgetful_factory.shared.errors import FactoryError


def stop_reason(error: BaseException | None) -> str:
    """The reason watch prints when it stops."""
    if error is None:
        return 'Watch stopped.'
    if isinstance(error, KeyboardInterrupt):
        return 'Watch was stopped with Ctrl-C or a stop signal.'
    if isinstance(error, FactoryError):
        return str(error)
    return f'Watch stopped after an unexpected error: {type(error).__name__}: {error}'


class ChatRelay:
    """Posts Foreman replies and status; sends chat messages to the Foreman.

    Without a chat, it only waits on the terminal, as watch did before.
    """

    def __init__(self, terminal: ForemanTerminal, chat: ChatChannel | None, *,
                 tick: float = 1.0, clock: Callable[[], float] = time.monotonic):
        self.terminal = terminal
        self.chat = chat
        # Chat messages are checked at least this often (seconds) while watch waits.
        self.tick = tick
        self.clock = clock

    def start(self) -> None:
        if self.chat is not None:
            self.chat.start()

    def online(self) -> None:
        if self.chat is not None:
            self.chat.online()

    def wait(self, interval: float) -> None:
        if self.chat is None:
            self.terminal.wait(interval)
            return
        deadline = self.clock() + interval
        while True:
            for message in self.chat.receive():
                self._deliver(message)
            remaining = deadline - self.clock()
            if remaining <= 0:
                return
            for reply in self.terminal.wait(min(remaining, self.tick)):
                if reply.text:
                    self.chat.post(reply.text)
                if reply.error:
                    self.chat.post(f'⚠️ {reply.error}')

    def stop(self, error: BaseException | None) -> None:
        if self.chat is not None:
            self.chat.close(stop_reason(error))

    def _deliver(self, message: ChatMessage) -> None:
        try:
            self.terminal.send(f'[{self.chat.name}] {message.author}: {message.text}')
        except BaseException:
            # The send may or may not have reached Pi; watch stops as for any failed send.
            self.chat.mark(message.id, Delivery.UNCERTAIN)
            raise
        self.chat.mark(message.id, Delivery.SENT)
