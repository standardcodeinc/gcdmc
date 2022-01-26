from __future__ import annotations

import datetime
import pytest

from gcdmc.model.types import DateList

a: datetime.datetime = datetime.datetime(2022, 1, 1)
a = a.replace(tzinfo=datetime.timezone.utc)
b: datetime.datetime = datetime.datetime(2022, 1, 2)
b = b.replace(tzinfo=datetime.timezone.utc)
c: datetime.datetime = datetime.datetime(2022, 1, 3)
c = c.replace(tzinfo=datetime.timezone.utc)
d: datetime.datetime = datetime.datetime(2022, 1, 4)
d = d.replace(tzinfo=datetime.timezone.utc)


def test_init() -> None:
    l: DateList = DateList([a, b])
    assert l == [a, b]


def test_append() -> None:
    l: DateList = DateList()
    l.append(a)
    l.append(b)
    assert l == [a, b]


def test_extend() -> None:
    l: DateList = DateList()
    l.extend([a, b])
    assert l == [a, b]


def test_add_regular_list() -> None:
    l: DateList = DateList([a, b])
    result: DateList = l + [c, d]
    assert isinstance(result, DateList)
    assert result == [a, b, c, d]


def test_add_date_list() -> None:
    l: DateList = DateList([a, b])
    result: DateList = l + DateList([c, d])
    assert isinstance(result, DateList)
    assert result == [a, b, c, d]


def test_iadd_regular_list() -> None:
    l: DateList = DateList([a, b])
    l += [c, d]
    assert l == [a, b, c, d]


def test_iadd_date_list() -> None:
    l: DateList = DateList([a, b])
    l += DateList([c, d])
    assert l == [a, b, c, d]


def test_insert() -> None:
    l: DateList = DateList()
    l.insert(0, a)
    l.insert(1, b)
    assert l == [a, b]


def test_copy_retains_type_and_values() -> None:
    l: DateList = DateList([a, b])
    copy: DateList = l.copy()
    assert isinstance(copy, DateList)
    assert l is not copy
    assert copy == [a, b]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: DateList = DateList([a, 1])


def test_append_invalid_type() -> None:
    l: DateList = DateList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: DateList = DateList()
    with pytest.raises(TypeError):
        l.extend([a, 1])


def test_add_invalid_type() -> None:
    l: DateList = DateList()
    with pytest.raises(TypeError):
        _: DateList = l + [a, 1]


def test_iadd_invalid_type() -> None:
    l: DateList = DateList()
    with pytest.raises(TypeError):
        l += [a, 1]


def test_insert_invalid_type() -> None:
    l: DateList = DateList()
    with pytest.raises(TypeError):
        l.insert(0, 1)


def test_init_invalid_value() -> None:
    with pytest.raises(ValueError):
        _: DateList = DateList([a, datetime.datetime.now()])


def test_append_invalid_value() -> None:
    l: DateList = DateList()
    with pytest.raises(ValueError):
        l.append(datetime.datetime.now())


def test_extend_invalid_value() -> None:
    l: DateList = DateList()
    with pytest.raises(ValueError):
        l.extend([a, datetime.datetime.now()])


def test_add_invalid_value() -> None:
    l: DateList = DateList()
    with pytest.raises(ValueError):
        _: DateList = l + [a, datetime.datetime.now()]


def test_iadd_invalid_value() -> None:
    l: DateList = DateList()
    with pytest.raises(ValueError):
        l += [a, datetime.datetime.now()]


def test_insert_invalid_value() -> None:
    l: DateList = DateList()
    with pytest.raises(ValueError):
        l.insert(0, datetime.datetime.now())
