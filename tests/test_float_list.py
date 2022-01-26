from __future__ import annotations

import pytest

from gcdmc.model.types import FloatList


def test_init() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    assert l == [1.0, 2.0]


def test_append() -> None:
    l: FloatList = FloatList()
    l.append(1.0)
    l.append(2.0)
    assert l == [1.0, 2.0]


def test_extend() -> None:
    l: FloatList = FloatList()
    l.extend([1.0, 2.0])
    assert l == [1.0, 2.0]


def test_add_regular_list() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    result: FloatList = l + [3.0, 4.0]
    assert isinstance(result, FloatList)
    assert result == [1.0, 2.0, 3.0, 4.0]


def test_add_float_list() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    result: FloatList = l + FloatList([3.0, 4.0])
    assert isinstance(result, FloatList)
    assert result == [1.0, 2.0, 3.0, 4.0]


def test_iadd_regular_list() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    l += [3.0, 4.0]
    assert l == [1.0, 2.0, 3.0, 4.0]


def test_iadd_float_list() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    l += FloatList([3.0, 4.0])
    assert l == [1.0, 2.0, 3.0, 4.0]


def test_insert() -> None:
    l: FloatList = FloatList()
    l.insert(0, 1.0)
    l.insert(1, 2.0)
    assert l == [1.0, 2.0]


def test_copy_retains_type_and_values() -> None:
    l: FloatList = FloatList([1.0, 2.0])
    copy: FloatList = l.copy()
    assert isinstance(copy, FloatList)
    assert l is not copy
    assert copy == [1.0, 2.0]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: FloatList = FloatList([1.0, 'foo'])


def test_append_invalid_type() -> None:
    l: FloatList = FloatList()
    with pytest.raises(TypeError):
        l.append('foo')


def test_extend_invalid_type() -> None:
    l: FloatList = FloatList()
    with pytest.raises(TypeError):
        l.extend([1.0, 'foo'])


def test_add_invalid_type() -> None:
    l: FloatList = FloatList()
    with pytest.raises(TypeError):
        _: FloatList = l + [1.0, 'foo']


def test_iadd_invalid_type() -> None:
    l: FloatList = FloatList()
    with pytest.raises(TypeError):
        l += [1.0, 'foo']


def test_insert_invalid_type() -> None:
    l: FloatList = FloatList()
    with pytest.raises(TypeError):
        l.insert(0, 'foo')
