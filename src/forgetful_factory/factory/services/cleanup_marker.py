"""Validate externally persisted worktree cleanup markers."""
import re
from typing import Literal

from forgetful_factory.forge.model import RepositoryRef
from forgetful_factory.forge.ports import Forge

CleanupState = Literal['pending', 'removed']


class CleanupMarkerError(ValueError):
    """The persisted cleanup marker is not valid cleanup evidence."""


def validate_cleanup_marker(mapping: dict, forge: Forge,
                            repository: RepositoryRef) -> CleanupState | None:
    """Return the semantic cleanup state from one persisted worktree mapping.

    The change-request URL must belong to the repository of the configured remote.
    """
    if 'cleanup' not in mapping:
        return None
    cleanup = mapping['cleanup']
    if not isinstance(cleanup, dict):
        raise CleanupMarkerError(
            'Invalid worktree cleanup record; reconcile it before continuing.')
    state = cleanup.get('state')
    url = cleanup.get('pull_request_url')
    commit = cleanup.get('merge_commit')
    if (state not in ('pending', 'removed') or not isinstance(url, str)
            or not forge.is_change_request(repository, url) or not isinstance(commit, str)
            or re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', commit) is None):
        raise CleanupMarkerError(
            'Invalid worktree cleanup state or merge evidence; reconcile the matching canonical '
            'change request URL and full merge commit SHA.')
    return state
