from __future__ import annotations
from typing import Any

from google.cloud.datastore import Entity

from model.properties.property import Property
from model.types import EntityList


class EntityProperty(Property[Entity, Entity]):
    def validate(self, v: Any) -> Entity:
        if v is not None and not isinstance(v, Entity):
            raise TypeError(
                f'invalid type for entity property: {type(v).__name__}, '
                'expected an entity')
        return super().validate(v)


class EntityListProperty(Property[EntityList, EntityList]):
    def validate(self, v: Any) -> EntityList:
        if v is not None:
            if type(v) is list:
                return self.validate(EntityList(v))
            if not isinstance(v, EntityList):
                raise TypeError('invalid type for entity list property: '
                                f'{type(v).__name__}, expected an entity list')
        return super().validate(v)
