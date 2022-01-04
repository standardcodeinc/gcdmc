from __future__ import annotations

import pytest

from model.types import *


def test_init_invalid_type():
    with pytest.raises(TypeError):
        _: TypedList[int] = TypedList(int, iterable=[1, 'foo'])


def test_append_invalid_type():
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.append('foo')


def test_extend_invalid_type():
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.extend([1, 'foo'])


def test_insert_invalid_type():
    l: TypedList[int] = TypedList(int)
    with pytest.raises(TypeError):
        l.insert(0, 'foo')


def test_init_invalid_value():
    with pytest.raises(ValueError):
        _: TypedList[int] = TypedList(int,
                                      validator=lambda x: x > 0,
                                      iterable=[1, -1])


def test_append_invalid_value():
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.append(-1)


def test_extend_invalid_value():
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.extend([1, -1])


def test_insert_invalid_value():
    l: TypedList[int] = TypedList(int, validator=lambda x: x > 0)
    with pytest.raises(ValueError):
        l.insert(0, -1)
