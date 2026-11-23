"""Map a GitHub remote URL to its ticket source. Slice 2 replaces this with the forge."""
import re

from forgetful_factory.shared.errors import FactoryError
from forgetful_factory.ticketing.model import TicketSource


class GitHubSourceResolver:
    def source_from_remote(self, remote: str) -> TicketSource:
        match = re.fullmatch(
            r'(?:git@github\.com:|https://github\.com/)([A-Za-z0-9-]+/[A-Za-z0-9_.-]+)',
            remote,
        )
        reference = match.group(1).removesuffix('.git') if match else ''
        if not reference or reference.split('/')[-1] in ('', '.', '..'):
            raise FactoryError(f'Unsupported origin {remote!r}; use a github.com SSH or HTTPS URL.')
        return TicketSource('github', reference.casefold())
