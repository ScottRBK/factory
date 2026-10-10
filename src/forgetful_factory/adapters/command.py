import subprocess

from forgetful_factory.domain.models import FactoryError


def run_command(arguments: list[str]) -> str:
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=30)
    except FileNotFoundError as error:
        raise FactoryError(f'{arguments[0]} is missing; install it and add it to PATH.') from error
    except OSError as error:
        raise FactoryError(f'Cannot run {arguments[0]}: {error}; check executable permissions '
                           'and installation.') from error
    except subprocess.TimeoutExpired as error:
        raise FactoryError(f'{arguments[0]} timed out after 30 seconds; check access and retry.') \
            from error
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or 'command failed'
        raise FactoryError(f'{arguments[0]} failed: {detail}')
    return result.stdout.removesuffix('\n')
