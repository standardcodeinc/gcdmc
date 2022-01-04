from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from google.cloud.datastore import Client, Entity, Key


class undelegated:
    """Decorator to mark a method as undelegated.

    If you wish to override a dictionary method such as `get`, you should
    decorate it as undelegated. Otherwise, the subentity will resolve the name
    by looking up the attribute on the underlying raw `Entity` object.
    """
    def __init__(self, func: Callable) -> None:
        self.func: Callable = func

    def __set_name__(self, owner: Subentity, name: str) -> None:
        owner.__undelegated_attrs__.add(name)
        setattr(owner, name, self.func)


class Subentity(Entity):
    """`Subentity` is an `Entity` subclass that delegates all entity-specific
    behavior to an underlying `Entity` object while also providing additional
    behavior.

    This class is meant to be used as a base type for other classes that want
    to inherit and extend entity behavior.

    To preserve the entity-specific behavior, this class stores an underlying
    `Entity` object as a class member and also overrides the `__getattribute__`
    method to delegate attribute access to the underlying entity. This allows
    subentities to be created from base entities without needing to copy over
    property values. A `wrap` class method is provided that allows the caller
    to wrap an existing entity to create a new subentity.
    """

    #: The attributes which should not be delegated to the underlying entity.
    #  Method names can be added to this set by decorating methods with the
    # `undelegated` decorator.
    __undelegated_attrs__: Set[str] = set()

    def __init__(self,
                 key: Optional[Key] = None,
                 exclude_from_indexes: Union[Tuple, List] = ()):
        self._entity: Entity = Entity(
            key=key,
            exclude_from_indexes=exclude_from_indexes,
        )
        super().__init__(key=key, exclude_from_indexes=exclude_from_indexes)

    def __getattribute__(self, name: str) -> Any:
        is_delegated: bool = name not in type(self).__undelegated_attrs__
        if name.startswith('__') and name.endswith('__'):
            return object.__getattribute__(self, name)
        if name == '_entity':
            return object.__getattribute__(self, name)
        if is_delegated and hasattr(self._entity, name):
            return getattr(self._entity, name)
        return object.__getattribute__(self, name)

    def __getitem__(self, key: Any) -> Any:
        return self._entity[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._entity[key] = value

    def __delitem__(self, key: Any) -> None:
        del self._entity[key]

    def __contains__(self, key: Any) -> bool:
        return key in self._entity

    def __eq__(self, other: Entity) -> bool:
        return self._entity == other

    def __ne__(self, other: Entity) -> bool:
        return self._entity != other

    def __or__(self, other: Dict) -> Dict:
        # Note that the return type is a dict, not a subentity. This behavior
        # is consistent with that of the raw `Entity` class.
        return self._entity | other

    def __ior__(self, other: Dict) -> Subentity:
        self._entity |= other
        return self

    def __repr__(self) -> str:
        return self._entity.__repr__()

    @classmethod
    def kind(cls) -> Optional[str]:
        """Returns the key kind that should be used for keys corresponding to
        subentities of this type.
        """
        return None

    @classmethod
    def create_key(cls,
                   client: Client,
                   parent: Optional[Key] = None,
                   id_or_name: Union[int, str] = None) -> Optional[Key]:
        """Creates a key for this subentity type.

        :type client: :class:`google.cloud.datastore.client.Client`
        :param client: The client to use to create the key.

        :type parent: :class:`google.cloud.datastore.key.Key`, optional
        :param parent: A key representing the parent of the subentity.

        :type id_or_name: int | str, optional
        :param id_or_name: The ID or name of the subentity.

        :rtype: :class:`google.cloud.datastore.key.Key`
        :returns: A key with a kind that corresponds to this subentity type.
        """
        if cls.kind() is None:
            return None
        return (client.key(cls.kind(), parent=parent) if id_or_name is None
                else client.key(cls.kind(), id_or_name, parent=parent))

    @classmethod
    def create(cls,
               client: Client,
               parent: Optional[Key] = None,
               id_or_name: Union[int, str] = None,
               exclude_from_indexes: Union[Tuple, List] = (),
               **kwargs: Any) -> Subentity:
        """Creates a subentity of this type.

        :type client: :class:`google.cloud.datastore.client.Client`
        :param client: The client to use to create the subentity.

        :type parent: :class:`google.cloud.datastore.key.Key`, optional
        :param parent: A key representing the parent of the subentity.

        :type id_or_name: int | str, optional
        :param id_or_name: The ID or name of the subentity.

        :type exclude_from_indexes: tuple | list, optional
        :param exclude_from_indexes: Names of fields whose values are not to be
            indexed for this subentity.

        :rtype: :class:`Subentity`
        :returns: A subentity of this type.
        """
        key: Optional[Key] = cls.create_key(client,
                                            parent=parent,
                                            id_or_name=id_or_name)
        return cls(key=key,
                   exclude_from_indexes=exclude_from_indexes,
                   **kwargs)

    @classmethod
    def wrap(cls, entity: Entity) -> Subentity:
        """Wraps an exisitng entity and returns a `Subentity` object.

        This function is meant to be called when raw entities are fetched from
        the datastore, allowing the caller to interact with the raw data via
        a potentially richer `Subentity` interface.

        :type entity: :class:`google.cloud.datastore.entity.Entity`
        :param entity: The entity to wrap.

        :rtype: :class:`core.subentity.Subentity`
        :returns: A subentity which wraps the input entity.
        """
        wrapped: Subentity = Subentity(
            key=entity.key,
            exclude_from_indexes=list(entity.exclude_from_indexes),
        )
        wrapped._entity = entity
        return wrapped
