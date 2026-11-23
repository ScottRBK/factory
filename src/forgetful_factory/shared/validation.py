import math

from forgetful_factory.shared.errors import FactoryError


def nonblank(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FactoryError(f'{field} must be a nonblank string.')
    if '\x00' in value:
        raise FactoryError(f'{field} must not contain NUL characters.')
    try:
        value.encode('utf-8')
    except UnicodeError as error:
        raise FactoryError(f'{field} must contain valid Unicode text.') from error
    return value


def positive_duration(name: str, value: object) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be positive and finite.')
