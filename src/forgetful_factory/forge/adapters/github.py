"""GitHub as a forge: repositories from remote URLs, and pull request addresses."""
import re

from forgetful_factory.forge.model import RepositoryRef
from forgetful_factory.shared.errors import FactoryError


class GitHubForge:
    def repository(self, remote: str) -> RepositoryRef:
        match = re.fullmatch(
            r'(?:git@github\.com:|https://github\.com/)([A-Za-z0-9-]+/[A-Za-z0-9_.-]+)',
            remote,
        )
        reference = match.group(1).removesuffix('.git') if match else ''
        if not reference or reference.split('/')[-1] in ('', '.', '..'):
            raise FactoryError(f'Unsupported origin {remote!r}; use a github.com SSH or HTTPS URL.')
        return RepositoryRef('github', reference.casefold())

    def is_change_request(self, repository: RepositoryRef, url: str) -> bool:
        pattern = rf'https://github\.com/(?ai:{re.escape(repository.reference)})/pull/[1-9][0-9]*'
        return re.fullmatch(pattern, url) is not None
