from __future__ import annotations

import pytest

from gcdmc.model.types import TypedList


def test_init() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    assert l == [1, 2, 3]


def test_append() -> None:
    l: TypedList[int] = TypedList(int)
    l.append(1)
    l.append(2)
    l.append(3)
    assert l == [1, 2, 3]


def test_extend() -> None:
    l: TypedList[int] = TypedList(int)
    l.extend([1, 2, 3])
    assert l == [1, 2, 3]


def test_add_regular_list() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    result: TypedList[int] = l + [4, 5, 6]
    assert isinstance(result, TypedList)
    assert result == [1, 2, 3, 4, 5, 6]


def test_add_typed_list() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    result: TypedList[int] = l + TypedList(int, iterable=[4, 5, 6])
    assert isinstance(result, TypedList)
    assert result == [1, 2, 3, 4, 5, 6]


def test_iadd_regular_list() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    l += [4, 5, 6]
    assert l == [1, 2, 3, 4, 5, 6]


def test_iadd_typed_list() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    l += TypedList(int, iterable=[4, 5, 6])
    assert l == [1, 2, 3, 4, 5, 6]


def test_insert() -> None:
    l: TypedList[int] = TypedList(int)
    l.insert(0, 1)
    l.insert(1, 2)
    l.insert(2, 3)
    assert l == [1, 2, 3]


def test_copy_retains_type_and_values() -> None:
    l: TypedList[int] = TypedList(int, iterable=[1, 2, 3])
    copy: TypedList[int] = l.copy()
    assert isinstance(copy, TypedList)
    assert l is not copy
    assert l == copy


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: TypedList[int] = TypedList(int, iterable=[1, 'foo'])


def test_append_invalid_type() -> None:
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.append('foo')


def test_extend_invalid_type() -> None:
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.extend([1, 'foo'])


def test_add_invalid_type() -> None:
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        _: TypedList[int] = l + ['foo']


def test_iadd_invalid_type() -> None:
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l += [1, 'foo']


def test_insert_invalid_type() -> None:
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.insert(0, 'foo')


def test_init_invalid_value() -> None:
    with pytest.raises(ValueError):
        _: TypedList[int] = TypedList(int,
                                      validator=lambda x: x > 0,
                                      iterable=[1, -1])


def test_append_invalid_value() -> None:
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.append(-1)


def test_extend_invalid_value() -> None:
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.extend([1, -1])


def test_add_invalid_value() -> None:
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        _: TypedList[int] = l + [1, -1]


def test_iadd_invalid_value() -> None:
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l += [1, -1]


def test_insert_invalid_value() -> None:
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.insert(0, -1)
