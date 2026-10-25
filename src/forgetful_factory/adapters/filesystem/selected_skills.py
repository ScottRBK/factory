"""Discover portable local skill files; metadata and ignore files remain native concerns."""
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


def _add_skill_file(path: Path, files: dict[Path, None]) -> None:
    if not path.is_file():
        raise FactoryError(f'Selected skill must be a readable regular file: {path}')
    # Opening is the availability check; the native harness owns content parsing.
    path.open('rb').close()
    files[path] = None


def _walk_skill_directory(
        directory: Path, ancestors: frozenset[tuple[int, int]],
        files: dict[Path, None]) -> None:
    identity = directory.stat()
    key = (identity.st_dev, identity.st_ino)
    if key in ancestors:
        raise FactoryError(f'Selected skill directory cycle: {directory}')
    skill = directory / 'SKILL.md'
    if skill.exists():
        _add_skill_file(skill, files)
        return
    for child in sorted(directory.iterdir()):
        if not child.name.startswith('.') and child.name != 'node_modules' and child.is_dir():
            _walk_skill_directory(child, ancestors | {key}, files)


def selected_skill_files(values: list[str]) -> list[Path]:
    files: dict[Path, None] = {}
    for value in values:
        path = Path(value)
        try:
            if path.is_dir():
                _walk_skill_directory(path, frozenset(), files)
            else:
                _add_skill_file(path, files)
        except OSError as error:
            raise FactoryError(f'Selected skills must be readable: {path}') from error
    return list(files)
