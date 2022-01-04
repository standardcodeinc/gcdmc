from __future__ import annotations
from typing import Any

from model.properties.property import Property
from model.properties.string import StringProperty
from model.types import PhoneList
from model.types.utils import is_parseable_phone


class PhoneProperty(StringProperty):
    def validate(self, v: Any) -> str:
        super().validate(v)
        if v is not None and not is_parseable_phone(v):
            raise ValueError(f'value is not a parseable phone: {v!r}')
        return v


class PhoneListProperty(Property[PhoneList, PhoneList]):
    def validate(self, v: Any) -> PhoneList:
        if v is not None:
            if type(v) is list:
                return self.validate(PhoneList(v))
            if not isinstance(v, PhoneList):
                raise TypeError('invalid type for phone list property: '
                                f'{type(v).__name__}, expected a phone list')
        return super().validate(v)
