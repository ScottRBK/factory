import json
import re

from forgetful_factory.adapters.command import run_command
from forgetful_factory.domain.models import FactoryError, Label, WorkSource


class GitHubWorkTracking:
    def source_from_remote(self, remote: str) -> WorkSource:
        match = re.fullmatch(
            r'(?:git@github\.com:|https://github\.com/)([A-Za-z0-9-]+/[A-Za-z0-9_.-]+)',
            remote,
        )
        reference = match.group(1).removesuffix('.git') if match else ''
        if not reference or reference.split('/')[-1] in ('', '.', '..'):
            raise FactoryError(f'Unsupported origin {remote!r}; use a github.com SSH or HTTPS URL.')
        return WorkSource('github', reference.casefold())

    def _api(self, source: WorkSource, suffix: str = '', *arguments: str) -> object:
        try:
            output = run_command(['gh', 'api', f'repos/{source.reference}{suffix}',
                                  '--hostname', 'github.com', *arguments])
            return json.loads(output)
        except (FactoryError, ValueError) as error:
            raise FactoryError(
                f'GitHub {source.reference}{suffix}: {error}. Check gh auth status and access.'
            ) from error

    def check_access(self, source: WorkSource) -> None:
        result = self._api(source)
        if not isinstance(result, dict) or not isinstance(result.get('full_name'), str):
            raise FactoryError(f'GitHub {source.reference}: malformed repository JSON response.')

    def list_labels(self, source: WorkSource) -> tuple[Label, ...]:
        pages = self._api(source, '/labels?per_page=100', '--paginate', '--slurp')
        if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
            raise FactoryError(f'GitHub {source.reference}: malformed label pages JSON.')
        result = [item for page in pages for item in page]
        if not isinstance(result, list) or any(
            not isinstance(item, dict) or not isinstance(item.get('name'), str)
            for item in result
        ):
            raise FactoryError(f'GitHub {source.reference}: malformed label JSON response.')
        return tuple(Label(item['name']) for item in result)

    def create_label(self, source: WorkSource, label: Label) -> None:
        result = self._api(source, '/labels', '--method', 'POST',
                  '-f', f'name={label.name}', '-f', 'color=ededed',
                  '-f', 'description=Factory work')
        if not isinstance(result, dict) or not isinstance(result.get('name'), str):
            raise FactoryError(
                f'GitHub {source.reference}: malformed label creation JSON response.'
            )
        if result['name'].casefold() != label.name.casefold():
            raise FactoryError(f'GitHub {source.reference}: unexpected created label name.')
