import json
import os
import stat
from pathlib import Path
import tomllib
from uuid import uuid4

from forgetful_factory.application.configuration import FactoryConfiguration, from_mapping
from forgetful_factory.domain.models import FactoryError


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False).replace('\x7f', '\\u007f')


class TomlConfigurationStore:
    def __init__(self, workspace: Path):
        self.path = workspace / '.factory' / 'factory.toml'

    def load(self) -> FactoryConfiguration | None:
        try:
            directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        except FileNotFoundError:
            return None
        except OSError as error:
            raise FactoryError(f'Cannot open {self.path.parent}; use a real directory: {error}') \
                from error
        try:
            try:
                descriptor = os.open(self.path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                     dir_fd=directory)
            except FileNotFoundError:
                return None
            with os.fdopen(descriptor, 'rb') as file:
                if not stat.S_ISREG(os.fstat(file.fileno()).st_mode):
                    raise FactoryError(f'Configuration must be a regular file: {self.path}')
                data = tomllib.load(file)
            return from_mapping(data)
        except (OSError, ValueError) as error:
            raise FactoryError(f'Cannot load {self.path}: {error}') from error
        finally:
            os.close(directory)

    def save(self, configuration: FactoryConfiguration) -> None:
        lines = [
            'watcher_label = [' + ', '.join(map(quote, configuration.watcher_label)) + ']',
            'foreman_agent_model = ' + quote(configuration.foreman_agent_model),
            'foreman_agent_effort = ' + quote(configuration.foreman_agent_effort),
        ]
        for repository in configuration.repository:
            lines.extend(['', '[[repository]]',
                          'local_dir = ' + quote(repository.local_dir),
                          'remote = ' + quote(repository.remote),
                          'provider = ' + quote(repository.work_source.provider),
                          'source = ' + quote(repository.work_source.reference)])
        self.path.parent.mkdir(exist_ok=True)
        directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        temporary = f'.factory-{uuid4().hex}.tmp'
        created = False
        try:
            descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                                 0o600, dir_fd=directory)
            created = True
            with os.fdopen(descriptor, 'w', encoding='utf-8') as file:
                file.write('\n'.join(lines) + '\n')
                file.flush()
                os.fsync(file.fileno())
            # Linking a complete file is atomic and fails if another init saved first.
            os.link(temporary, self.path.name, src_dir_fd=directory, dst_dir_fd=directory,
                    follow_symlinks=False)
        except FileExistsError as error:
            raise FactoryError(f'Configuration appeared concurrently at {self.path}; '
                               'it was preserved. Inspect it and rerun init.') from error
        except OSError as error:
            raise FactoryError(f'Cannot save {self.path}: {error}') from error
        finally:
            if created:
                os.unlink(temporary, dir_fd=directory)
            os.close(directory)
