from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from gcdmc.model.typed_entity import TypedEntity


class UndefinedPropertyError(Exception):
    """Raised when a user attempts to assign a value to a property that does
    not exist.
    """
    def __init__(self, name: Any, entity: TypedEntity) -> None:
        super().__init__(f'{entity.__class__.__name__} does not have property '
                         f'{name!r}')


class UnassignedPropertyError(Exception):
    """Raised when a user attempts to delete a property.
    """
    def __init__(self, name: Any, entity: TypedEntity) -> None:
        super().__init__(f'cannot delete {name!r} from an object of type '
                         f'{entity.__class__.__name__}')


class UnexposedPropertyError(Exception):
    """Raised when a user attempts to assign a value to an unexposed property.
    """
    def __init__(self, name: Any, entity: TypedEntity) -> None:
        super().__init__(f'cannot set {name!r} directly on an object of type '
                         f'{entity.__class__.__name__}')


class InvalidKeyError(Exception):
    """Raised when an entity has a key that does not conform to the expected
    ancestor hierarchy.
    """
    pass
