from __future__ import annotations
from typing import Any, Callable, Generic, Iterable, List, Optional, TypeVar

T = TypeVar('T')
Validator = Callable[[T], bool]


class TypedList(Generic[T], List[T], list):
    """A list that only stores values of a certain type, used for properties
    that store lists.

    :type type_: type
    :param type_: The type of the values that are stored in the list. If a user
        tries to add a value which has a different type, a `TypeError` will be
        raised.

    :type validator: callable, optional
    :param validator: A function that takes a single argument of the list's
        type and returns a boolean indicating whether or not the value is
        valid. If a user tries to add an invalid value, a `ValueError` will be
        raised.

    :type iterable: iterable, optional
    :param iterable: An iterable of values to initialize the list with. Note
        that every value in the iterable will have its type and value checked.
    """

    def __init__(self,
                 type_: type,
                 validator: Optional[Validator] = None,
                 iterable: Optional[Iterable] = None) -> None:
        self._type: type = type_
        self._validator: Optional[Validator] = validator
        if iterable is not None:
            self._check_values(iterable)
            super().__init__(iterable)
        else:
            super().__init__()

    def append(self, v: Any) -> None:
        self._check_value(v)
        super().append(v)

    def extend(self, iterable: Iterable) -> None:
        self._check_values(iterable)
        super().extend(iterable)

    def insert(self, i: int, v: Any) -> None:
        self._check_value(v)
        super().insert(i, v)

    def copy(self) -> TypedList[T]:
        return TypedList(self._type,
                         validator=self._validator,
                         iterable=super().copy())

    def _check_value(self, v: Any) -> None:
        if not isinstance(v, self._type):
            raise TypeError(
                f'invalid type for {self.__class__.__name__}: '
                f'{type(v).__name__}, expected {self._type.__name__}')

        if self._validator is not None and not self._validator(v):
            raise ValueError(
                f'{self.__class__.__name__} validator failed for value: {v!r}')

    def _check_values(self, iterable: Iterable) -> None:
        for item in iterable:
            self._check_value(item)
