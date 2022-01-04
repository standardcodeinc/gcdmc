from __future__ import annotations
from typing import Any

from google.cloud.datastore import Key

from model.properties.property import Property
from model.types import KeyList


class KeyProperty(Property[Key, Key]):
    def validate(self, v: Any) -> Key:
        if v is not None and not isinstance(v, Key):
            raise TypeError(
                f'invalid type for key property: {type(v).__name__}, '
                'expected a Datastore key')
        return super().validate(v)


class KeyListProperty(Property[KeyList, KeyList]):
    def validate(self, v: Any) -> KeyList:
        if v is not None:
            if type(v) is list:
                return self.validate(KeyList(v))
            if not isinstance(v, KeyList):
                raise TypeError('invalid type for key list property: '
                                f'{type(v).__name__}, expected a key list')
        return super().validate(v)
