from __future__ import annotations

import pytest

from gcdmc.model.types import IntegerList


def test_init() -> None:
    l: IntegerList = IntegerList([1, 2])
    assert l == [1, 2]


def test_append() -> None:
    l: IntegerList = IntegerList()
    l.append(1)
    l.append(2)
    assert l == [1, 2]


def test_extend() -> None:
    l: IntegerList = IntegerList()
    l.extend([1, 2])
    assert l == [1, 2]


def test_add_regular_list() -> None:
    l: IntegerList = IntegerList([1, 2])
    result: IntegerList = l + [3, 4]
    assert isinstance(result, IntegerList)
    assert result == [1, 2, 3, 4]


def test_add_boolean_list() -> None:
    l: IntegerList = IntegerList([1, 2])
    result: IntegerList = l + IntegerList([3, 4])
    assert isinstance(result, IntegerList)
    assert result == [1, 2, 3, 4]


def test_iadd_regular_list() -> None:
    l: IntegerList = IntegerList([1, 2])
    l += [3, 4]
    assert l == [1, 2, 3, 4]


def test_iadd_boolean_list() -> None:
    l: IntegerList = IntegerList([1, 2])
    l += IntegerList([3, 4])
    assert l == [1, 2, 3, 4]


def test_insert() -> None:
    l: IntegerList = IntegerList()
    l.insert(0, 1)
    l.insert(1, 2)
    assert l == [1, 2]


def test_copy_retains_type_and_values() -> None:
    l: IntegerList = IntegerList([1, 2])
    copy: IntegerList = l.copy()
    assert isinstance(copy, IntegerList)
    assert l is not copy
    assert copy == [1, 2]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: IntegerList = IntegerList([1, 'foo'])


def test_append_invlaid_type() -> None:
    l: IntegerList = IntegerList()
    with pytest.raises(TypeError):
        l.append('foo')


def test_extend_invalid_type() -> None:
    l: IntegerList = IntegerList()
    with pytest.raises(TypeError):
        l.extend([1, 'foo'])


def test_add_invalid_type() -> None:
    l: IntegerList = IntegerList()
    with pytest.raises(TypeError):
        _: IntegerList = l + [1, 'foo']


def test_iadd_invalid_type() -> None:
    l: IntegerList = IntegerList()
    with pytest.raises(TypeError):
        l += [1, 'foo']


def test_insert_invalid_type() -> None:
    l: IntegerList = IntegerList()
    with pytest.raises(TypeError):
        l.insert(0, 'foo')
