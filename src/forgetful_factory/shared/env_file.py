"""Read secrets by name from the environment or one KEY=value file. Never changes os.environ."""
import os
import re
from collections.abc import Mapping
from pathlib import Path

DEFAULT_ENV_FILE = Path('~/.config/forgetful-factory/.env')
_NAME = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')


def read_env_file(path: Path) -> dict[str, str]:
    """KEY=value lines. Blank lines and # comment lines are ignored. An `export ` prefix is
    accepted and one pair of matching quotes is removed. Values are not expanded."""
    values = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line.startswith('export '):
            line = line.removeprefix('export ').lstrip()
        name, separator, value = line.partition('=')
        name, value = name.strip(), value.strip()
        if not separator or not _NAME.fullmatch(name):
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '"\'':
            value = value[1:-1]
        values[name] = value
    return values


def find_secret(name: str, env_file: Path, *, explicit: bool,
                environment: Mapping[str, str] = os.environ) -> tuple[str | None, str | None]:
    """The value of `name`, first from the environment, then from env_file; else a warning.

    explicit is True when the settings name env_file. Only then is a missing file a problem
    of its own; the default file is just one of the places checked.
    """
    if environment.get(name):
        return environment[name], None
    note = ''
    try:
        value = read_env_file(env_file).get(name)
    except FileNotFoundError:
        value = None
        if explicit:
            note = f' The env_file {env_file} does not exist.'
    except (OSError, UnicodeError) as error:
        value = None
        note = f' Cannot read env_file {env_file}: {error}.'
    if value:
        return value, None
    return None, (f'{name} was not found in the environment or in {env_file}.{note}')
