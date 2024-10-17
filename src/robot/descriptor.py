"""Testing how mkdocstrings handles descriptors.

This module *is not* part of normal Robot Framework code.
"""

from typing import overload, Self


class PositiveInteger[T]:

    def __set_name__(self, owner: T, name: str):
        self.name = '_' + name

    @overload
    def __get__(self, instance: None, owner: type[T]) -> Self:
        ...

    @overload
    def __get__(self, instance: T, owner: type[T]) -> int:
        ...

    def __get__(self, instance, owner) -> int | Self:
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance: T, value: int):
        if value <= 0:
            raise ValueError(f'{value} is not positive')
        setattr(instance, self.name, value)


class Example:
    """Example using descriptor."""
    count = PositiveInteger()
    """Count as a positive integer."""

    def __init__(self, count: int = 1):
        self.count = count
