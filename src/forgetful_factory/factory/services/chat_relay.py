"""The rules between the Foreman and a chat room. A chat problem never stops watch."""
import contextvars
import threading
import time

from forgetful_factory.agents.model import ForemanReply
from forgetful_factory.agents.ports import ForemanTerminal
from forgetful_factory.channels.model import ChatMessage, Delivery
from forgetful_factory.channels.ports import ChatChannel
from forgetful_factory.shared.errors import FactoryError

# Seconds between chat checks unless watch --chat-interval says otherwise.
CHAT_INTERVAL = 1.0
# Seconds the chat thread reads Foreman replies for each check, holding the terminal.
READ = 0.05


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

    With a chat, a thread does this all the time, also while watch polls. Watch's own terminal
    use goes through `foreman`, which shares a lock with that thread. Without a chat there is no
    thread, and watch waits on the terminal as before.
    """

    def __init__(self, terminal: ForemanTerminal, chat: ChatChannel | None, *,
                 interval: float = CHAT_INTERVAL):
        self.terminal = terminal
        self.chat = chat
        # Seconds between chat checks; each check sends new messages and posts new replies.
        self.interval = interval
        self.lock = threading.Lock()
        # Watch holds this while it waits for the lock, so the thread sends at most one message
        # before watch's send: a plain lock is not fair.
        self.turn = threading.Lock()
        self.foreman = _SharedTerminal(self)
        self.thread: threading.Thread | None = None
        self.stopping = threading.Event()
        self.failed = threading.Event()
        self.failure: BaseException | None = None

    def start(self) -> None:
        if self.chat is not None:
            self.chat.start()

    def online(self) -> None:
        """Say the Foreman is ready and start the chat thread. The terminal must be started."""
        if self.chat is None:
            return
        self.chat.online()
        # A copy of the context, so the thread sees watch's stop request (Ctrl-C).
        context = contextvars.copy_context()
        thread = threading.Thread(target=context.run, args=(self._run,), name='factory-chat',
                                  daemon=True)
        thread.start()
        self.thread = thread

    def wait(self, interval: float) -> None:
        if self.thread is None:
            self.terminal.wait(interval)
            return
        self.check()
        deadline = time.monotonic() + interval
        while (remaining := deadline - time.monotonic()) > 0:
            # Steps of at most a minute: threading refuses very long timeouts.
            if self.failed.wait(min(remaining, 60)):
                break
        self.check()

    def check(self) -> None:
        """Raise the chat thread's failure, so watch stops as for its own failed send."""
        if self.failure is not None:
            raise self.failure

    def halt(self) -> None:
        """End the chat thread. Watch calls this before it closes the terminal and the chat.

        The thread finishes the terminal use in progress, which has its own deadline, and then
        uses neither again.
        """
        if self.thread is None:
            return
        self.stopping.set()
        while self.thread.is_alive():
            try:
                self.thread.join()
            except KeyboardInterrupt:
                # A second Ctrl-C: still let the send in progress end before watch closes.
                continue

    def stop(self, error: BaseException | None) -> None:
        if self.chat is not None:
            self.chat.close(stop_reason(error))

    def use_terminal(self, action, *arguments):
        """One terminal use; the caller holds the lock. A failure is kept before the lock is
        released, so neither thread uses the terminal after it."""
        self.check()
        try:
            return action(*arguments)
        except BaseException as error:
            self._fail(error)
            raise

    def _fail(self, error: BaseException) -> None:
        if self.failure is None:
            self.failure = error
        self.failed.set()

    def _run(self) -> None:
        try:
            while not self.stopping.is_set():
                self._exchange()
                self.stopping.wait(self.interval)
        except (Exception, KeyboardInterrupt) as error:
            # Handed to watch, which raises it. KeyboardInterrupt comes from the Ctrl-C check.
            self._fail(error)

    def _exchange(self) -> None:
        for message in self.chat.receive():
            with self.turn:
                pass  # Let a waiting watch send go first.
            with self.lock:
                if self.stopping.is_set():
                    return  # Left unmarked: the relay marks it 💤 when watch stops.
                self.use_terminal(self._deliver, message)
        with self.lock:
            if self.stopping.is_set():
                return
            replies = self.use_terminal(self.terminal.wait, READ)
        for reply in replies:
            self._post(reply)

    def _post(self, reply: ForemanReply) -> None:
        if reply.text:
            self.chat.post(reply.text)
        if reply.error:
            self.chat.post(f'⚠️ {reply.error}')

    def _deliver(self, message: ChatMessage) -> None:
        try:
            self.terminal.send(f'[{self.chat.name}] {message.author}: {message.text}')
        except BaseException:
            # The send may or may not have reached Pi; watch stops as for any failed send.
            self.chat.mark(message.id, Delivery.UNCERTAIN)
            raise
        self.chat.mark(message.id, Delivery.SENT)


class _SharedTerminal:
    """The Foreman terminal for watch itself. Sends wait while the chat thread uses it."""

    def __init__(self, relay: ChatRelay):
        self.relay = relay
        self.terminal = relay.terminal

    def startup_hint(self) -> str:
        return self.terminal.startup_hint()

    def start(self) -> None:
        self.terminal.start()

    def send(self, message: str) -> None:
        with self.relay.turn, self.relay.lock:
            self.relay.use_terminal(self.terminal.send, message)

    def wait(self, interval: float) -> list[ForemanReply]:
        with self.relay.lock:
            return self.relay.use_terminal(self.terminal.wait, interval)

    def close(self) -> None:
        self.terminal.close()
