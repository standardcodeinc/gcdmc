from __future__ import annotations
from typing import Dict, Optional, Type

from core.subentity import Subentity


class RegistryError(Exception):
    """Raised when a registry cannot find a type for a given kind.
    """
    def __init__(self, kind: str) -> None:
        super().__init__(f'could not find a subentity type for {kind!r} and '
                         'no default was provided')


class Registry:
    def __init__(self, default: Optional[Type[Subentity]] = None) -> None:
        self._default: Optional[Type[Subentity]] = default
        self._types: Dict[str, Type[Subentity]] = {}

    def register_subentity_type(self, kind: str,
                                entity_type: Type[Subentity]) -> None:
        """Registers a subentity type associated with a given string kind.
        """
        self._types[kind] = entity_type

    def get_subentity_type(self, kind: str) -> Type[Subentity]:
        """Gets the subentity type associated with a given string kind.

        In cases where the kind has not been registered, this function will
        attempt to use the default type that was supplied at the time the
        registry was created. If no default exists, a key error is raised.
        """
        entity_type: Optional[Type[Subentity]] = self._types.get(kind)
        if entity_type is not None:
            return entity_type
        if self._default is None:
            raise RegistryError(kind)
        return self._default

    def has_subentity_type(self, kind: str) -> bool:
        """Returns whether or not a given string kind has been associated with
        a subentity type.
        """
        return kind in self._types
