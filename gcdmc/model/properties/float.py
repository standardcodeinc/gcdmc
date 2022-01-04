from __future__ import annotations
from typing import Any

from model.properties.property import Property
from model.types import FloatList


class FloatProperty(Property[float, float]):
    def validate(self, v: Any) -> float:
        if v is not None and not isinstance(v, float):
            raise TypeError(
                f'invalid type for float property: {type(v).__name__}, '
                'expected a float')
        return super().validate(v)


class FloatListProperty(Property[FloatList, FloatList]):
    def validate(self, v: Any) -> FloatList:
        if v is not None:
            if type(v) is list:
                return self.validate(FloatList(v))
            if not isinstance(v, FloatList):
                raise TypeError('invalid type for float list property: '
                                f'{type(v).__name__}, expected a float list')
        return super().validate(v)
