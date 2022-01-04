from __future__ import annotations
from typing import (
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from google.cloud.datastore import Client, Entity, Key

from gcdmc.core.subentity import Subentity, undelegated
from gcdmc.model.errors import InvalidKeyError, UnexposedPropertyError
from gcdmc.model.typed_entity import TypedEntity

E = TypeVar('E', bound=TypedEntity)


class IEntity(Subentity, Generic[E]):
    """An `IEntity` (or "interfaced entity") is a wrapper over a typed entity
    that controls how the underlying data can be changed.

    By default, all properties on the typed entity can be accessed via an
    attribute expression, but none of them can be modified.

    For example, one could write: `prop = entity.prop`.

    But one could not set `prop` like so: `entity.prop = 'new value'`

    However, subclasses can specify in the `__exposed_properties__` class
    attribute which properties can be modified via an attribute expression.
    Subclasses should also implement the methods necessary to change the
    underlying data based on application specific logic.

    :type entity: :class:`model.typed_entity.TypedEntity`
    :param entity: The typed entity to wrap.
    """

    #: The typed entity to provide an interface to.
    __type__: Optional[E] = None

    #: The properties that can be set directly via an attribute expression.
    __exposed_properties__: Sequence[str] = ()

    def __init__(self, entity: E) -> None:
        valid, err_msg = self.__class__.is_key_valid(entity.key)
        if not valid:
            raise InvalidKeyError(err_msg)
        self._entity: E = entity

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_entity':
            return super().__setattr__(name, value)
        elif name in self._entity.properties:
            self[name] = value
        else:
            return super().__setattr__(name, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if (key in self._entity.properties
                and key not in self.__exposed_properties__):
            raise UnexposedPropertyError(key, self)
        try:
            return super().__setitem__(key, value)
        except (TypeError, ValueError) as e:
            msg: str = f'error setting property {key!r}: {str(e)!r}'
            raise type(e)(msg)

    def __ior__(self, other: Dict) -> IEntity:
        return TypedEntity.__ior__(self, other)

    @undelegated
    def clear(self) -> None:
        """The underlying typed entity cannot be cleared, so this will raise
        an error.
        """
        TypedEntity.clear(self)

    @undelegated
    def pop(self, key: Any, *args: Any) -> Any:
        """Delegates `pop` to the underlying typed entity.
        """
        return TypedEntity.pop(self, key, *args)

    @undelegated
    def popitem(self) -> Any:
        """Properties cannot be removed from the underlying typed entity, so
        this will raise an error.
        """
        return TypedEntity.popitem(self)

    @undelegated
    def setdefault(self, key: Any, *args: Any) -> Any:
        """Delegates `setdefault` to the underlying typed entity, while also
        raising an error if the user attempts to set a property that is
        unexposed.
        """
        return TypedEntity.setdefault(self, key, *args)

    @undelegated
    def update(self, *args: Union[Dict, List[Tuple]], **kwargs: Any) -> None:
        """Delegates `updates` to the underlying typed entity, while also
        raising an error if the user attempts to set a property that is
        unexposed.
        """
        TypedEntity.update(self, *args, **kwargs)

    @classmethod
    def create(cls,
               client: Client,
               parent: Optional[Key] = None,
               id_or_name: Union[int, str] = None,
               exclude_from_indexes: Union[Tuple, List] = (),
               **kwargs: Any) -> IEntity:
        """Creates a typed entity with the type specified by the interfaced
        entity class, and then returns an interface to it.
        """
        entity: E = cls.__type__.create(
            client,
            parent=parent,
            id_or_name=id_or_name,
            exclude_from_indexes=exclude_from_indexes,
            **kwargs)
        return cls(entity)

    @classmethod
    def kind(cls) -> Optional[str]:
        """Returns the key kind of the underlying typed entity.
        """
        return cls.__type__.kind()

    @classmethod
    def is_key_valid(cls, key: Key) -> Tuple[bool, Optional[str]]:
        """Returns whether or not a key is valid, along with an error message
        if the key is not valid.

        By default, all keys are valid. However, subclasses can override this
        method to enforce ancestor relationships.

        When an interfaced entity is created, the constructor will check if
        the key on the supplied typed entity is valid. If the key is not valid,
        then an `InvalidKeyError` will be raised.
        """
        return True, None

    @classmethod
    def wrap(cls, entity: Entity) -> IEntity:
        """Wraps an entity with the typed entity specified by the interfaced
        entity class, and then returns an interface to it.
        """
        typed_entity: TypedEntity = cls.__type__.wrap(entity)
        return cls(typed_entity)
