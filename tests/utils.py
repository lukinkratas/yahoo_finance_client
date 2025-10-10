import warnings
from typing import Any


def assert_contains_keys(data: dict[str, Any], keys: list[str]) -> None:
    """Assert, that all of the keys exist in the data (dict).
    In case the key value is None, warning is raised.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    for key in keys:
        assert key in data, f'Key {key} not found.'
        if data[key]:
            warnings.warn(f'Key {key} is empty.')


def assert_keys_are_not_none(data: dict[str, Any], keys: list[str]) -> None:
    """Assert, that all of the keys axist in the data and are not None.

    Args:
        data: dict to be checked
        keys: keys to check in data (dict)
    """
    for key in keys:
        assert data[key], f'Key {key} is empty.'
