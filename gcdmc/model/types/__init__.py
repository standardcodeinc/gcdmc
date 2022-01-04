from __future__ import annotations
from typing import Iterable, Optional

import datetime

from google.cloud.datastore import Key, Entity

from model.types.typed_list import TypedList
from model.types.utils import is_parseable_phone, is_valid_date, is_valid_email


class BooleanList(TypedList[bool]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(bool, iterable=iterable)


class IntegerList(TypedList[int]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(int, iterable=iterable)


class FloatList(TypedList[float]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(float, iterable=iterable)


class StringList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, iterable=iterable)


class EmailList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, validator=is_valid_email, iterable=iterable)


class PhoneList(TypedList[str]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(str, validator=is_parseable_phone, iterable=iterable)


class DatetimeList(TypedList[datetime.datetime]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(datetime.datetime, iterable=iterable)


class DateList(TypedList[datetime.datetime]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(datetime.datetime,
                         validator=is_valid_date,
                         iterable=iterable)


class KeyList(TypedList[Key]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(Key, iterable=iterable)


class EntityList(TypedList[Entity]):
    def __init__(self, iterable: Optional[Iterable] = None) -> None:
        super().__init__(Entity, iterable=iterable)


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
