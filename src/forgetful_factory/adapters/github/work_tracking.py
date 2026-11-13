import hashlib
import json
import re

from forgetful_factory.adapters.command import run_command
from forgetful_factory.domain.models import FactoryError, Issue, Label, WorkSource


class GitHubWorkTracking:
    def __init__(self, command_timeout: float = 30):
        self.command_timeout = command_timeout

    def check_cli(self) -> None:
        """Check local pagination support without authentication or an API request."""
        try:
            help_text = run_command(['gh', 'api', '--help'], timeout=self.command_timeout)
        except FactoryError as error:
            raise FactoryError(f'GitHub CLI readiness check failed: {error}') from error
        if re.search(r'(?m)^[ \t]+--slurp(?:[ \t]|$)', help_text) is None:
            raise FactoryError('GitHub CLI must support gh api --paginate --slurp. '
                               'Install or upgrade gh on PATH, then restart watch.')

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
                                  '--hostname', 'github.com', *arguments],
                                 timeout=self.command_timeout)
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

    def list_issues(self, source: WorkSource, labels: tuple[str, ...]) -> tuple[Issue, ...]:
        pages = self._api(source, '/issues?state=open&per_page=100', '--paginate', '--slurp')
        if not isinstance(pages, list) or any(not isinstance(page, list) for page in pages):
            raise FactoryError(f'GitHub {source.reference}: malformed issue pages JSON.')
        watched = {name.casefold() for name in labels}
        eligible = []
        items = [item for page in pages for item in page]
        for item in items:
            if not isinstance(item, dict):
                raise FactoryError(f'GitHub {source.reference}: malformed issue JSON.')
            if 'pull_request' in item:
                continue
            self._validate_issue(source, item)
            matches = '*' in watched or any(label['name'].casefold() in watched
                                            for label in item['labels'])
            if item['state'] == 'open' and matches:
                eligible.append(item)
        if not eligible:
            return ()
        issues = []
        for item in eligible:
            fields = {
                'title': item['title'], 'body': item.get('body') or '',
                'state': item['state'], 'state_reason': item.get('state_reason'),
                'labels': sorted(label['name'] for label in item['labels']),
                'assignees': sorted(assignee['login'] for assignee in item.get('assignees', [])),
                'milestone': self._milestone(item.get('milestone')),
                'type': (item.get('type') or {}).get('name'),
                'comments': self._comments(source, item['number']),
            }
            data = json.dumps(fields, sort_keys=True, ensure_ascii=True, separators=(',', ':'))
            revision = hashlib.sha256(data.encode()).hexdigest()
            issues.append(Issue(source, item['number'], item['title'], item['html_url'],
                                item.get('body') or '', revision,
                                any(label['name'].casefold() == 'epic'
                                    for label in item['labels'])))
        return tuple(issues)

    def _comments(self, source: WorkSource, number: int) -> list[tuple[int, str, str]]:
        pages = self._api(source, f'/issues/{number}/comments?per_page=100',
                          '--paginate', '--slurp')
        if not isinstance(pages, list) or not pages or any(
            not isinstance(page, list) for page in pages
        ):
            raise FactoryError(f'GitHub {source.reference}: malformed comment pages JSON.')
        result: list[tuple[int, str, str]] = []
        seen: set[int] = set()
        expected_url = f'https://api.github.com/repos/{source.reference}/issues/{number}'
        for page in pages:
            for item in page:
                if not isinstance(item, dict):
                    raise FactoryError(f'GitHub {source.reference}: malformed comment JSON.')
                url = item.get('issue_url')
                if (not isinstance(url, str) or url.casefold() != expected_url.casefold()
                        or type(item.get('id')) is not int or item['id'] < 1
                        or item['id'] in seen or not isinstance(item.get('body'), str)
                        or not isinstance(item.get('updated_at'), str)
                        or not item['updated_at']):
                    raise FactoryError(f'GitHub {source.reference}: malformed comment JSON.')
                seen.add(item['id'])
                result.append((item['id'], item['body'], item['updated_at']))
        result.sort()
        return result

    @staticmethod
    def _milestone(item: object) -> object:
        if item is None:
            return None
        return {key: item.get(key) for key in ('number', 'title', 'description', 'due_on', 'state')}

    @staticmethod
    def _validate_issue(source: WorkSource, item: dict) -> None:
        valid = (type(item.get('number')) is int and item['number'] > 0
                 and isinstance(item.get('title'), str)
                 and isinstance(item.get('html_url'), str)
                 and item.get('state') in ('open', 'closed')
                 and isinstance(item.get('labels'), list)
                 and (item.get('body') is None or isinstance(item.get('body'), str))
                 and isinstance(item.get('assignees', []), list)
                 and all(isinstance(assignee, dict) and isinstance(assignee.get('login'), str)
                         for assignee in item.get('assignees', []))
                 and (item.get('milestone') is None or isinstance(item['milestone'], dict))
                 and (item.get('type') is None or isinstance(item['type'], dict))
                 and all(isinstance(label, dict) and isinstance(label.get('name'), str)
                         for label in item['labels']))
        if not valid:
            raise FactoryError(f'GitHub {source.reference}: malformed issue JSON.')
