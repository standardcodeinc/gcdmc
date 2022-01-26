from __future__ import annotations

import pytest

from google.cloud.datastore import Client, Key

from gcdmc.model.types import KeyList

c: Client = Client(project='test-project')


def key() -> Key:
    return c.key()


def test_init() -> None:
    l: KeyList = KeyList(['a', 'b'])
    assert l == ['a', 'b']


def test_append() -> None:
    l: KeyList = KeyList()
    l.append('a')
    l.append('b')
    assert l == ['a', 'b']


def test_extend() -> None:
    l: KeyList = KeyList()
    l.extend(['a', 'b'])
    assert l == ['a', 'b']


def test_add_regular_list() -> None:
    l: KeyList = KeyList(['a', 'b'])
    result: KeyList = l + ['c', 'd']
    assert isinstance(result, KeyList)
    assert result == ['a', 'b', 'c', 'd']


def test_add_key_list() -> None:
    l: KeyList = KeyList(['a', 'b'])
    result: KeyList = l + KeyList(['c', 'd'])
    assert isinstance(result, KeyList)
    assert result == ['a', 'b', 'c', 'd']


def test_iadd_regular_list() -> None:
    l: KeyList = KeyList(['a', 'b'])
    l += ['c', 'd']
    assert l == ['a', 'b', 'c', 'd']


def test_iadd_key_list() -> None:
    l: KeyList = KeyList(['a', 'b'])
    l += KeyList(['c', 'd'])
    assert l == ['a', 'b', 'c', 'd']


def test_insert() -> None:
    l: KeyList = KeyList()
    l.insert(0, 'a')
    l.insert(1, 'b')
    assert l == ['a', 'b']


def test_copy_retains_type_and_values() -> None:
    l: KeyList = KeyList(['a', 'b'])
    copy: KeyList = l.copy()
    assert isinstance(copy, KeyList)
    assert l is not copy
    assert copy == ['a', 'b']


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: KeyList = KeyList(['a', 1])


def test_append_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.extend(['a', 1])


def test_add_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        _: KeyList = l + ['a', 1]


def test_iadd_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l += ['a', 1]


def test_insert_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.insert(0, 1)
