from __future__ import annotations
from typing import Any, List

import datetime

from model.properties.property import Property
from model.types import DateList
from model.types.utils import is_valid_date


class DateProperty(Property[datetime.datetime, datetime.date]):
    def validate(self, v: Any) -> datetime.datetime:
        super().validate(v)
        if v is not None and not is_valid_date(v):
            raise ValueError(f'value is not a valid date: {v!r}')
        return v

    def serialize_value(self, v: datetime.datetime) -> datetime.date:
        return datetime.date(v.year, v.month, v.day)


class DateListProperty(Property[DateList, List[datetime.date]]):
    def validate(self, v: Any) -> DateList:
        if v is not None:
            if type(v) is list:
                return self.validate(DateList(v))
            if not isinstance(v, DateList):
                raise TypeError('invalid type for date list property: '
                                f'{type(v).__name__}, expected a date list')
        return super().validate(v)

    def serialize_value(self, v: DateList) -> List[datetime.date]:
        return [datetime.date(d.year, d.month, d.day) for d in v]
