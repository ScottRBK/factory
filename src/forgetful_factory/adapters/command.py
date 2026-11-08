import subprocess

from forgetful_factory.application.watch_stop import check_watch_stop
from forgetful_factory.domain.models import FactoryError


def run_command(arguments: list[str], *, timeout: float = 30,
                env: dict[str, str] | None = None, stdin: int | None = None) -> str:
    check_watch_stop()
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=timeout,
                                env=env, stdin=stdin)
    except FileNotFoundError as error:
        raise FactoryError(f'{arguments[0]} is missing; install it and add it to PATH.') from error
    except OSError as error:
        raise FactoryError(f'Cannot run {arguments[0]}: {error}; check executable permissions '
                           'and installation.') from error
    except subprocess.TimeoutExpired as error:
        raise FactoryError(f'{arguments[0]} timed out after {timeout:g} seconds; '
                           'check access and retry.') from error
    check_watch_stop()
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or 'command failed'
        raise FactoryError(f'{arguments[0]} failed: {detail}')
    return result.stdout.removesuffix('\n')
