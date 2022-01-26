from __future__ import annotations

import datetime
import pytest

from gcdmc.model.types import DatetimeList

a: datetime.datetime = datetime.datetime.now()
b: datetime.datetime = datetime.datetime.now()
c: datetime.datetime = datetime.datetime.now()
d: datetime.datetime = datetime.datetime.now()


def test_init() -> None:
    l: DatetimeList = DatetimeList([a, b])
    assert l == [a, b]


def test_append() -> None:
    l: DatetimeList = DatetimeList()
    l.append(a)
    l.append(b)
    assert l == [a, b]


def test_extend() -> None:
    l: DatetimeList = DatetimeList()
    l.extend([a, b])
    assert l == [a, b]


def test_add_regular_list() -> None:
    l: DatetimeList = DatetimeList([a, b])
    result: DatetimeList = l + [c, d]
    assert isinstance(result, DatetimeList)
    assert result == [a, b, c, d]


def test_add_datetime_list() -> None:
    l: DatetimeList = DatetimeList([a, b])
    result: DatetimeList = l + DatetimeList([c, d])
    assert isinstance(result, DatetimeList)
    assert result == [a, b, c, d]


def test_iadd_regular_list() -> None:
    l: DatetimeList = DatetimeList([a, b])
    l += [c, d]
    assert l == [a, b, c, d]


def test_iadd_datetime_list() -> None:
    l: DatetimeList = DatetimeList([a, b])
    l += DatetimeList([c, d])
    assert l == [a, b, c, d]


def test_insert() -> None:
    l: DatetimeList = DatetimeList()
    l.insert(0, a)
    l.insert(1, b)
    assert l == [a, b]


def test_copy_retains_type_and_values() -> None:
    l: DatetimeList = DatetimeList([a, b])
    copy: DatetimeList = l.copy()
    assert isinstance(copy, DatetimeList)
    assert l is not copy
    assert copy == [a, b]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: DatetimeList = DatetimeList([a, 1])


def test_append_invalid_type() -> None:
    l: DatetimeList = DatetimeList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: DatetimeList = DatetimeList()
    with pytest.raises(TypeError):
        l.extend([a, 1])


def test_add_invalid_type() -> None:
    l: DatetimeList = DatetimeList()
    with pytest.raises(TypeError):
        _: DatetimeList = l + [a, 1]


def test_iadd_invalid_type() -> None:
    l: DatetimeList = DatetimeList()
    with pytest.raises(TypeError):
        l += [a, 1]


def test_insert_invalid_type() -> None:
    l: DatetimeList = DatetimeList()
    with pytest.raises(TypeError):
        l.insert(0, 1)
