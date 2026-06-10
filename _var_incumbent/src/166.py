"""Core implementation for df-166.

The filename is intended to be ``166.py``.
"""

from __future__ import annotations


def digital_root(value: int) -> int:
    """Return the digital root of a non-negative integer."""
    if not isinstance(value, int):
        raise TypeError("value must be an int")
    if value < 0:
        raise ValueError("value must be non-negative")
    while value >= 10:
        value = sum(int(ch) for ch in str(value))
    return value


def is_dark_factory_code(value: int) -> bool:
    """A code is valid when its digital root matches df-166's root."""
    return digital_root(value) == digital_root(166)


def classify_codes(values: list[int]) -> list[bool]:
    """Classify each value as matching or not matching df-166."""
    return [is_dark_factory_code(value) for value in values]
# [CRUX-MK]
