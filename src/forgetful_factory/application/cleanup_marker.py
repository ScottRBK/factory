"""Validate externally persisted worktree cleanup markers."""
import re
from typing import Literal

CleanupState = Literal['pending', 'removed']


class CleanupMarkerError(ValueError):
    """The persisted cleanup marker is not valid cleanup evidence."""


def validate_cleanup_marker(mapping: dict) -> CleanupState | None:
    """Return the semantic cleanup state from one persisted worktree mapping."""
    if 'cleanup' not in mapping:
        return None
    cleanup = mapping['cleanup']
    if not isinstance(cleanup, dict):
        raise CleanupMarkerError(
            'Invalid worktree cleanup record; reconcile it before continuing.')
    state = cleanup.get('state')
    url = cleanup.get('pull_request_url')
    commit = cleanup.get('merge_commit')
    repository = re.escape(mapping['repository'])
    expected = rf'https://github\.com/(?ai:{repository})/pull/[1-9][0-9]*'
    if (state not in ('pending', 'removed') or not isinstance(url, str)
            or re.fullmatch(expected, url) is None or not isinstance(commit, str)
            or re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', commit) is None):
        raise CleanupMarkerError(
            'Invalid worktree cleanup state or merge evidence; reconcile the matching canonical '
            'GitHub PR URL and full merge commit SHA.')
    return state
