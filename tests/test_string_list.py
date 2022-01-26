from __future__ import annotations

import pytest

from gcdmc.model.types import StringList


def test_init() -> None:
    l: StringList = StringList(['a', 'b'])
    assert l == ['a', 'b']


def test_append() -> None:
    l: StringList = StringList()
    l.append('a')
    l.append('b')
    assert l == ['a', 'b']


def test_extend() -> None:
    l: StringList = StringList()
    l.extend(['a', 'b'])
    assert l == ['a', 'b']


def test_add_regular_list() -> None:
    l: StringList = StringList(['a', 'b'])
    result: StringList = l + ['c', 'd']
    assert isinstance(result, StringList)
    assert result == ['a', 'b', 'c', 'd']


def test_add_string_list() -> None:
    l: StringList = StringList(['a', 'b'])
    result: StringList = l + StringList(['c', 'd'])
    assert isinstance(result, StringList)
    assert result == ['a', 'b', 'c', 'd']


def test_iadd_regular_list() -> None:
    l: StringList = StringList(['a', 'b'])
    l += ['c', 'd']
    assert l == ['a', 'b', 'c', 'd']


def test_iadd_string_list() -> None:
    l: StringList = StringList(['a', 'b'])
    l += StringList(['c', 'd'])
    assert l == ['a', 'b', 'c', 'd']


def test_insert() -> None:
    l: StringList = StringList()
    l.insert(0, 'a')
    l.insert(1, 'b')
    assert l == ['a', 'b']


def test_copy_retains_type_and_values() -> None:
    l: StringList = StringList(['a', 'b'])
    copy: StringList = l.copy()
    assert isinstance(copy, StringList)
    assert l is not copy
    assert copy == ['a', 'b']


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: StringList = StringList(['a', 1])


def test_append_invalid_type() -> None:
    l: StringList = StringList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: StringList = StringList()
    with pytest.raises(TypeError):
        l.extend(['a', 1])


def test_add_invalid_type() -> None:
    l: StringList = StringList()
    with pytest.raises(TypeError):
        _: StringList = l + ['a', 1]


def test_iadd_invalid_type() -> None:
    l: StringList = StringList()
    with pytest.raises(TypeError):
        l += ['a', 1]


def test_insert_invalid_type() -> None:
    l: StringList = StringList()
    with pytest.raises(TypeError):
        l.insert(0, 1)
