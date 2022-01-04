from __future__ import annotations
from typing import Any

import datetime

from model.properties.property import Property
from model.types import DatetimeList


class DatetimeProperty(Property[datetime.datetime, datetime.datetime]):
    def validate(self, v: Any) -> datetime.datetime:
        if v is not None and not isinstance(v, datetime.datetime):
            raise TypeError(
                f'invalid type for datetime property: {type(v).__name__}, '
                'expected a datetime')
        return super().validate(v)


class DatetimeListProperty(Property[DatetimeList, DatetimeList]):
    def validate(self, v: Any) -> DatetimeList:
        if v is not None:
            if type(v) is list:
                return self.validate(DatetimeList(v))
            if not isinstance(v, DatetimeList):
                raise TypeError(
                    'invalid type for datetime list property: '
                    f'{type(v).__name__}, expected a datetime list')
        return super().validate(v)
