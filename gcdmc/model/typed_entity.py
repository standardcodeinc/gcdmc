from __future__ import annotations
from typing import (
    Any,
    Dict,
    Iterable,
    Optional,
    Type,
    Union,
    Tuple,
    List,
)

from google.cloud.datastore import Entity, Key

from core.subentity import Subentity, undelegated
from model.errors import UnassignedPropertyError, UndefinedPropertyError
from model.properties.property import Property


class TypedEntity(Subentity):
    """`TypedEntity` is a `Subentity` subclass which uses named properties to
    enforce data invairants on its values.

    When creating a new typed entity, you may pass in keyword arguments to set
    the properties on the entity. The constructor will iterate through each
    property, lookup the property's name in the keyword arguments and validate
    the found keyword argument value against the property. If the value is
    validated, then it is set on the entity. Otherwise, either a `TypeError` or
    `ValueError` is raised.
    """

    #: The kind of the entity. Must be set by subclass implementations if
    #  instances of the subclass are meant to be persisted into the Datastore.
    __kind__: Optional[str] = None

    #: The properties to be set on the entity. This is lazy intialized and is
    #  never accessed directly.
    __cached_properties__: Optional[Dict[str, Property]] = None

    #: The properties that should not be indexed. This is lazy initialized and
    #  never accessed directly.
    __unindexed_properties__: Optional[List[str]] = None

    def __init__(self,
                 key: Optional[Key] = None,
                 exclude_from_indexes: Union[Tuple, List] = (),
                 **kwargs: Any) -> None:
        cls: Type[TypedEntity] = type(self)
        if cls.__kind__ is not None:
            if key is None:
                raise ValueError(f'a key of kind {cls.__kind__!r} must be '
                                 f'provided when creating a {cls.__name__}')
            elif key.kind != cls.__kind__:
                raise TypeError(f'got unexpected key kind: {key.kind!r}, '
                                f'expected: {cls.__kind__!r}')

        if len(exclude_from_indexes) > 0:
            raise ValueError('exclude_from_indexes should not be explicitly '
                             'set on typed entities and is instead defined '
                             'by the properties on the entity')

        super().__init__(key=key,
                         exclude_from_indexes=self.unindexed_properties)

        for name, prop in self.properties.items():
            try:
                value: Any = (kwargs.pop(name)
                              if name in kwargs else prop.default)
                self[name] = value
            except (TypeError, ValueError, AttributeError) as e:
                msg: str = f'error setting property {name!r}: {str(e)!r}'
                raise type(e)(msg)

        # This should raise an `UndefinedPropertyError` if there are any extra
        # keyword arguments, mainly to signal improper initialization.
        for name, value in kwargs.items():
            self[name] = value

    def __getattribute__(self, name: str) -> Any:
        if name in ('properties', 'unindexed_properties'):
            return object.__getattribute__(self, name)
        if name in self.properties:
            return self[name]
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.properties:
            self[name] = value
        else:
            super().__setattr__(name, value)

    def __setitem__(self, key: Any, value: Any) -> None:
        if key not in self.properties:
            raise UndefinedPropertyError(key, self)
        prop: Property = self.properties[key]
        value = prop.validate(value)
        super().__setitem__(key, value)

    def __delitem__(self, key: Any) -> None:
        if key in self.properties:
            raise UnassignedPropertyError(key, self)
        super().__delitem__(key)

    def __ior__(self, other: Dict) -> TypedEntity:
        for key, value in other.items():
            self[key] = value
        return self

    @property
    def properties(self) -> Dict[str, Property]:
        """Returns the properties defined on the typed entity as a dictionary
        of name-property pairs.
        """
        return type(self)._properties()

    @classmethod
    def _properties(cls) -> Dict[str, Property]:
        """Lazy initializes the `__cached_properties__` dictionary and returns
        it.
        """
        if cls.__cached_properties__ is None:
            cls.__cached_properties__ = {}
            for name in dir(cls):
                attr: Any = getattr(cls, name)
                if isinstance(attr, Property):
                    cls.__cached_properties__[name] = attr

        return cls.__cached_properties__

    @property
    def unindexed_properties(self) -> List[str]:
        """Returns the properties that should not be indexed.
        """
        return type(self)._unindexed_properties()

    @classmethod
    def _unindexed_properties(cls) -> List[str]:
        """Lazy initializes the `__unindexed_properties__` list and returns it.
        """
        if cls.__unindexed_properties__ is None:
            cls.__unindexed_properties__ = []
            for name in dir(cls):
                attr: Any = getattr(cls, name)
                if isinstance(attr, Property):
                    if not attr.is_indexed:
                        cls.__unindexed_properties__.append(name)

        return cls.__unindexed_properties__

    @undelegated
    def clear(self) -> None:
        """Typed entites cannot be cleared, so this method raises an error.
        """
        raise NotImplementedError('clear is not supported on TypedEntity')

    @undelegated
    def pop(self, key: Any, *args: Any) -> Any:
        """Overrides the base dictionary `pop` method to raise an error if the
        user attempts to pop a property.

        This method is generally a no-op, due to the fact that only properties
        can be set on typed entities.
        """
        if key in self.properties:
            raise UnassignedPropertyError(key, self)
        return super().pop(key, *args)

    @undelegated
    def popitem(self) -> Any:
        """Typed entities cannot have properties removed, so this method raises
        an error.
        """
        raise NotImplementedError('popitem is not supported on TypedEntity')

    @undelegated
    def setdefault(self, key: Any, *args: Any) -> Any:
        """Overrides the base dictionary `setdefault` method to validate the
        value of the property before setting it.
        """
        if len(args) > 1:
            raise TypeError('setdefault expected at most 2 positional '
                            f'arguments, got {len(args)+1} arguments instead')

        if key not in self.properties:
            raise UndefinedPropertyError(key, self)

        prop: Property = self.properties[key]
        value: Any = prop.validate(args[0])
        return super().setdefault(key, value)

    @undelegated
    def update(self, *args: Union[Dict, List[Tuple]], **kwargs: Any) -> None:
        """Overrides the base dictionary `update` method to call `__setitem__`
        for every name-value pair to be set.

        This function will throw an error when a name is used that does not
        refer to a property, or when the value provided cannot be validated
        against the relevant property.
        """
        if len(args) > 1:
            raise TypeError('update expected at most 1 positional argument, '
                            f'got {len(args)} arguments instead')

        items: Iterable[Tuple]
        if len(args) == 1:
            items = args[0].items() if isinstance(args[0], dict) else args
            for name, value in items:
                self[name] = value

        for name, value in kwargs.items():
            self[name] = value

    @classmethod
    def kind(cls) -> Optional[str]:
        """Returns the value of the `__kind__` class attribute.
        """
        return cls.__kind__

    @classmethod
    def wrap(cls, entity: Entity) -> TypedEntity:
        """Wraps an existing entity and returns a `TypedEntity` object.

        This method will check the data types and values of the underlying
        entity and raise an error if it does not match the schema defined by
        the calling `TypedEntity` class.
        """
        return cls(key=entity.key,
                   exclude_from_indexes=list(entity.exclude_from_indexes),
                   **entity)
