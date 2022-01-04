from __future__ import annotations
from typing import Any

from gcdmc.model.properties.property import Property
from gcdmc.model.properties.string import StringProperty
from gcdmc.model.types import EmailList
from gcdmc.model.types.utils import is_valid_email


class EmailProperty(StringProperty):
    def validate(self, v: Any) -> str:
        super().validate(v)
        if v is not None and not is_valid_email(v):
            raise ValueError(f'value is not a valid email: {v!r}')
        return v


class EmailListProperty(Property[EmailList, EmailList]):
    def validate(self, v: Any) -> EmailList:
        if v is not None:
            if type(v) is list:
                return self.validate(EmailList(v))
            if not isinstance(v, EmailList):
                raise TypeError('invalid type for email list property: '
                                f'{type(v).__name__}, expected an email list')
        return super().validate(v)
