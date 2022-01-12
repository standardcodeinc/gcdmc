from __future__ import annotations
from typing import Iterable, List, Optional

import datetime

from google.cloud.datastore import Key, Entity

from gcdmc.model.types.typed_list import TypedList
from gcdmc.model.types.utils import (
    is_parseable_phone,
    is_valid_date,
    is_valid_email,
)


class BooleanList(TypedList[bool]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(bool, iterable=iterable)

    def copy(self) -> BooleanList:
        return BooleanList(list.copy(self))

    def __add__(self, other: List) -> BooleanList:
        return BooleanList(list.__add__(self, other))


class IntegerList(TypedList[int]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(int, iterable=iterable)

    def copy(self) -> IntegerList:
        return IntegerList(list.copy(self))

    def __add__(self, other: List) -> IntegerList:
        return IntegerList(list.__add__(self, other))


class FloatList(TypedList[float]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(float, iterable=iterable)

    def copy(self) -> FloatList:
        return FloatList(list.copy(self))

    def __add__(self, other: List) -> FloatList:
        return FloatList(list.__add__(self, other))


class StringList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, iterable=iterable)

    def copy(self) -> StringList:
        return StringList(list.copy(self))

    def __add__(self, other: List) -> StringList:
        return StringList(list.__add__(self, other))


class EmailList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, validator=is_valid_email, iterable=iterable)

    def copy(self) -> EmailList:
        return EmailList(list.copy(self))

    def __add__(self, other: List) -> EmailList:
        return EmailList(list.__add__(self, other))


class PhoneList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, validator=is_parseable_phone, iterable=iterable)

    def copy(self) -> PhoneList:
        return PhoneList(list.copy(self))

    def __add__(self, other: List) -> PhoneList:
        return PhoneList(list.__add__(self, other))


class DatetimeList(TypedList[datetime.datetime]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(datetime.datetime, iterable=iterable)

    def copy(self) -> DatetimeList:
        return DatetimeList(list.copy(self))

    def __add__(self, other: List) -> DatetimeList:
        return DatetimeList(list.__add__(self, other))


class DateList(TypedList[datetime.datetime]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(datetime.datetime,
                         validator=is_valid_date,
                         iterable=iterable)

    def copy(self) -> DateList:
        return DateList(list.copy(self))

    def __add__(self, other: List) -> DateList:
        return DateList(list.__add__(self, other))


class KeyList(TypedList[Key]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(Key, iterable=iterable)

    def copy(self) -> KeyList:
        return KeyList(list.copy(self))

    def __add__(self, other: List) -> KeyList:
        return KeyList(list.__add__(self, other))


class EntityList(TypedList[Entity]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(Entity, iterable=iterable)

    def copy(self) -> EntityList:
        return EntityList(list.copy(self))

    def __add__(self, other: List) -> EntityList:
        return EntityList(list.__add__(self, other))


__all__ = [
    'TypedList',
    'BooleanList',
    'IntegerList',
    'FloatList',
    'StringList',
    'EmailList',
    'PhoneList',
    'DatetimeList',
    'DateList',
    'KeyList',
    'EntityList',
]
