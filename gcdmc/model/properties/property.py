from __future__ import annotations
from typing import Any, Callable, Generic, Optional, Tuple, TypeVar, Union

# The type of the property's value
T = TypeVar('T')
Generator = Callable[[], T]
Validator = [[T], bool]

# The type of the property's serialized value.
S = TypeVar('S')


class Property(Generic[T, S]):
    """A property is a definition for a single value that is stored on a typed
    entity.

    While the generic property base class does not place any restrictions on
    the type of the value, its subclasses can and generally should enforce type
    requirements. If a user tries to assign a value to a property that has an
    invalid type, a `TypeError` will be raised.

    :type nullable: bool, optional
    :param nullable: Whether or not the property can be assigned a null value.
        Defaults to `true`, meaning that properties are nullable by default.

    :type choices: tuple, optional
    :param choices: A tuple of values that are valid for the property. If the
        user tries to assign a value that is not a choice, then a `ValueError`
        will be raised.

    :type autoupdater: callable, optional
    :param autoupdater: A function that will be called to update the value of
        the property whenever the entity is updated. This could be useful e.g.
        to implement a timestamp that is updated anytime the entity is changed.

    :type validator: callable, optional
    :param validator: A function that will be called to validate a value before
        it is assigned to the property. If the value cannot be validated, then
        a `ValueError` will be raised.

    :type serialize: bool, optional
    :param serialize: Whether or not the property should included when the
        entity is serialized. Defaults to `true`, meaning that properties are
        serialized by default.

    :type default: Any, optional
    :param default: The default value for the property if no value is assigned.
        Note that `default` could be a callable, in which case the return value
        of the callable will be used as the default value. Defaults to `None`,
        meaning that properties have no default value by default.
    """
    def __init__(self,
                 nullable: bool = True,
                 choices: Optional[Tuple[T, ...]] = None,
                 autoupdater: Optional[Generator] = None,
                 validator: Optional[Validator] = None,
                 indexed: bool = True,
                 serialized: bool = True,
                 **kwargs: Any) -> None:
        self._nullable: bool = nullable
        self._choices: Optional[Tuple[T, ...]] = choices
        self._autoupdater: Optional[Generator] = autoupdater
        self._validator: Optional[Validator] = validator
        self._indexed: bool = indexed
        self._serialized: bool = serialized
        self._has_set_default: bool = 'default' in kwargs
        self._set_default: Union[None, T, Generator] = kwargs.get('default')
        if self._has_set_default:
            self.validate(self.default)
        if self.is_autoupdated:
            self.validate(self._autoupdater())

    @property
    def has_default(self) -> bool:
        """Returns whether or not this property has a default value that can
        be used if there is no user-provided value.

        Note that both the set default and the return value of the autoupdater
        function can be used for the default value.
        """
        return self._has_set_default or self.is_autoupdated

    @property
    def default(self) -> T:
        """Returns the default value of the property.

        Note that both the set default and the return value of the autoupdater
        function can be used for the default value, with the set default taking
        precedence.
        """
        if not self.has_default:
            raise AttributeError('property has no default')
        if self._has_set_default:
            if callable(self._set_default):
                return self._set_default()
            return self._set_default
        return self.generate_update()

    @property
    def is_autoupdated(self) -> bool:
        """Returns whether or not this property should be updated when the
        entity to which it belongs is modified.
        """
        return self._autoupdater is not None

    def generate_update(self) -> Optional[Generator]:
        """Calls the autoupdater function and returns the generated value.

        This will raise a `TypeError` if the property does not have an assigned
        autoupdater function.
        """
        return self._autoupdater()

    def validate(self, v: Any) -> T:
        """Validates that a value can be used for a property, and then returns
        it. If the input value is not validated, then an error will be thrown.

        If validation fails, then either a `ValueError` or `TypeError` will be
        thrown.

        Subclasses of the base property type can override this behavior to
        return a transformed value if necessary.
        """
        if not self._nullable and v is None:
            raise ValueError('property value cannot be None')
        if self._choices is not None and v not in self._choices:
            choices: str = ', '.join(repr(c) for c in self._choices)
            raise ValueError(f'got invalid property value: {v!r}, '
                             f'expected one of {choices}')
        if self._validator is not None and not self._validator(v):
            raise ValueError(f'could not validate property value: {v!r}')
        return v

    @property
    def is_indexed(self) -> bool:
        """Returns whether or not this property should be indexed.
        """
        return self._indexed

    @property
    def is_serialized(self) -> bool:
        """Returns whether or not this property should be serialized.
        """
        return self._serialized

    def serialize_value(self, v: T) -> S:
        """Returns a value stored for a property for serialization purposes.

        The default behavior is to just return the value itself, but derived
        classes can change this behavior if values need to be processed before
        being serialized.
        """
        return v
