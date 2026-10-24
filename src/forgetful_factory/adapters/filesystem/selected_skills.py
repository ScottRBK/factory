"""Discover portable local skill files; metadata and ignore files remain native concerns."""
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


def selected_skill_files(values: list[str]) -> list[Path]:
    files: dict[Path, None] = {}

    def add_file(path: Path) -> None:
        if not path.is_file():
            raise FactoryError(f'Selected skill must be a readable regular file: {path}')
        with path.open('rb'):
            pass
        files[path] = None

    def walk(directory: Path, ancestors: frozenset) -> None:
        identity = directory.stat()
        key = (identity.st_dev, identity.st_ino)
        if key in ancestors:
            raise FactoryError(f'Selected skill directory cycle: {directory}')
        skill = directory / 'SKILL.md'
        if skill.exists():
            add_file(skill)
            return
        for child in sorted(directory.iterdir()):
            if not child.name.startswith('.') and child.name != 'node_modules' and child.is_dir():
                walk(child, ancestors | {key})

    for value in values:
        path = Path(value)
        try:
            if path.is_dir():
                walk(path, frozenset())
            else:
                add_file(path)
        except OSError as error:
            raise FactoryError(f'Selected skills must be readable: {path}') from error
    return list(files)
