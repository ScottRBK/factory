"""Parse numbered menu answers without performing terminal input or output."""

from forgetful_factory.domain.models import FactoryError


def parse_numbered_selection(label: str, answer: str, choice_count: int) -> int:
    """Return the selected one-based position or raise a user-facing selection error."""
    try:
        index = int(answer)
    except ValueError as error:
        raise FactoryError(f'{label}: select a number from 1 to {choice_count}.') from error
    if index < 1 or index > choice_count:
        raise FactoryError(f'{label} selection is out of range; '
                           f'select a number from 1 to {choice_count}.')
    return index
