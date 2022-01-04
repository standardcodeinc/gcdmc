from __future__ import annotations
from typing import Any

from model.properties.property import Property
from model.types import IntegerList


class IntegerProperty(Property[int, int]):
    def validate(self, v: Any) -> int:
        if v is not None and not isinstance(v, int):
            raise TypeError(
                f'invalid type for integer property: {type(v).__name__}, '
                'expected an integer')
        return super().validate(v)


class IntegerListProperty(Property[IntegerList, IntegerList]):
    def validate(self, v: Any) -> IntegerList:
        if v is not None:
            if type(v) is list:
                return self.validate(IntegerList(v))
            if not isinstance(v, IntegerList):
                raise TypeError('invalid type for integer list property: '
                                f'{type(v).__name__}, expected a integer list')
        return super().validate(v)
