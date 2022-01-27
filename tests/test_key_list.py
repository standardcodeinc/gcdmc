from __future__ import annotations

import mock
import pytest

from google.api_core.client_options import ClientOptions
from google.auth.credentials import Credentials
from google.cloud.datastore import Client, Key

from gcdmc.model.types import KeyList

c: Client = Client(project='test-project',
                   namespace='test-namespace',
                   credentials=mock.Mock(spec=Credentials))


def key(name: str) -> Key:
    return c.key('test-kind', name)


def test_init() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    assert l == [key('a'), key('b')]


def test_append() -> None:
    l: KeyList = KeyList()
    l.append(key('a'))
    l.append(key('b'))
    assert l == [key('a'), key('b')]


def test_extend() -> None:
    l: KeyList = KeyList()
    l.extend([key('a'), key('b')])
    assert l == [key('a'), key('b')]


def test_add_regular_list() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    result: KeyList = l + [key('c'), key('d')]
    assert isinstance(result, KeyList)
    assert result == [key('a'), key('b'), key('c'), key('d')]


def test_add_key_list() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    result: KeyList = l + KeyList([key('c'), key('d')])
    assert isinstance(result, KeyList)
    assert result == [key('a'), key('b'), key('c'), key('d')]


def test_iadd_regular_list() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    l += [key('c'), key('d')]
    assert l == [key('a'), key('b'), key('c'), key('d')]


def test_iadd_key_list() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    l += KeyList([key('c'), key('d')])
    assert l == [key('a'), key('b'), key('c'), key('d')]


def test_insert() -> None:
    l: KeyList = KeyList()
    l.insert(0, key('a'))
    l.insert(1, key('b'))
    assert l == [key('a'), key('b')]


def test_copy_retains_type_and_values() -> None:
    l: KeyList = KeyList([key('a'), key('b')])
    copy: KeyList = l.copy()
    assert isinstance(copy, KeyList)
    assert l is not copy
    assert copy == [key('a'), key('b')]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: KeyList = KeyList([key('a'), 1])


def test_append_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.extend([key('a'), 1])


def test_add_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        _: KeyList = l + [key('a'), 1]


def test_iadd_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l += [key('a'), 1]


def test_insert_invalid_type() -> None:
    l: KeyList = KeyList()
    with pytest.raises(TypeError):
        l.insert(0, 1)
