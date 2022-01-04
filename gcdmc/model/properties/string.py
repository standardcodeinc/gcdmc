from __future__ import annotations
from typing import Any

from gcdmc.model.properties.property import Property
from gcdmc.model.types import StringList


class StringProperty(Property[str, str]):
    def validate(self, v: Any) -> str:
        if v is not None and not isinstance(v, str):
            raise TypeError(
                f'invalid type for string property: {type(v).__name__}, '
                'expected a string')
        return super().validate(v)


class StringListProperty(Property[StringList, StringList]):
    def validate(self, v: Any) -> StringList:
        if v is not None:
            if type(v) is list:
                return self.validate(StringList(v))
            if not isinstance(v, StringList):
                raise TypeError('invalid type for string list property: '
                                f'{type(v).__name__}, expected a string list')
        return super().validate(v)
