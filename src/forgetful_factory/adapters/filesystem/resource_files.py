import json
import os
import stat
import uuid
from contextlib import contextmanager
from pathlib import Path

from forgetful_factory.domain.models import FactoryError


def check_real_path(path: Path) -> None:
    for parent in (path, *path.parents):
        if parent.is_symlink():
            raise FactoryError('Foreman resources require real files and directories; '
                               'symlinks are not supported.')


def write_new(path: Path, content: str) -> None:
    check_real_path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        with path.open('x', encoding='utf-8') as stream:
            stream.write(content)
        path.chmod(0o600)
    except FileExistsError:
        if not path.is_file():
            raise FactoryError('Foreman resource path must be a regular file.')


def write_json(path: Path, value: dict) -> None:
    write_new(path, json.dumps(value, indent=2) + '\n')


@contextmanager
def _generated_parent(path: Path):
    """Pin each directory without following symlinks during receipt operations (Linux/WSL)."""
    check_real_path(path)
    directory = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parent.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                            dir_fd=directory)
            os.close(directory)
            directory = child
        try:
            mode = os.stat(path.name, dir_fd=directory, follow_symlinks=False).st_mode
        except FileNotFoundError:
            pass
        else:
            if not stat.S_ISREG(mode):
                raise FactoryError('Generated setup receipt must be a regular file; no symlinks.')
        yield directory
    finally:
        os.close(directory)


def remove_generated(path: Path) -> None:
    try:
        with _generated_parent(path) as directory:
            os.unlink(path.name, dir_fd=directory)
            os.fsync(directory)
    except FileNotFoundError:
        pass


def replace_generated_json(path: Path, value: dict) -> None:
    """Replace the generated receipt atomically; never mutate a linked previous receipt."""
    with _generated_parent(path) as directory:
        temporary = f'.{path.name}.{uuid.uuid4().hex}.tmp'
        descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                             0o600, dir_fd=directory)
        try:
            with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
                stream.write(json.dumps(value, indent=2) + '\n')
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path.name, src_dir_fd=directory, dst_dir_fd=directory)
            os.fsync(directory)
        finally:
            try:
                os.unlink(temporary, dir_fd=directory)
            except FileNotFoundError:
                pass


def read_generated_json(path: Path) -> dict:
    with _generated_parent(path) as directory:
        descriptor = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                             dir_fd=directory)
        with os.fdopen(descriptor, encoding='utf-8') as stream:
            if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                raise FactoryError('Generated setup receipt must be a regular file.')
            return json.load(stream)


