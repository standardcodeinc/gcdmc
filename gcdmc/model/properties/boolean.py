from __future__ import annotations
from typing import Any

from model.properties.property import Property
from model.types import BooleanList


class BooleanProperty(Property[bool, bool]):
    def validate(self, v: Any) -> bool:
        if v is not None and not isinstance(v, bool):
            raise TypeError(
                f'invalid type for boolean property: {type(v).__name__}, '
                'expected a boolean')
        return super().validate(v)


class BooleanListProperty(Property[BooleanList, BooleanList]):
    def validate(self, v: Any) -> BooleanList:
        if v is not None:
            if type(v) is list:
                return self.validate(BooleanList(v))
            if not isinstance(v, BooleanList):
                raise TypeError('invalid type for boolean list property: '
                                f'{type(v).__name__}, expected a boolean list')
        return super().validate(v)
