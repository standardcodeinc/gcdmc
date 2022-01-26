from __future__ import annotations

import pytest

from gcdmc.model.types import PhoneList


def test_init() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    assert l == ['+15555551234', '+447700900077']


def test_append() -> None:
    l: PhoneList = PhoneList()
    l.append('+15555551234')
    l.append('+447700900077')
    assert l == ['+15555551234', '+447700900077']


def test_extend() -> None:
    l: PhoneList = PhoneList()
    l.extend(['+15555551234', '+447700900077'])
    assert l == ['+15555551234', '+447700900077']


def test_add_regular_list() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    result: PhoneList = l + ['+61770101111', '+913858210056']
    assert isinstance(result, PhoneList)
    assert result == [
        '+15555551234', '+447700900077', '+61770101111', '+913858210056'
    ]


def test_add_phone_list() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    result: PhoneList = l + PhoneList(['+61770101111', '+913858210056'])
    assert isinstance(result, PhoneList)
    assert result == [
        '+15555551234', '+447700900077', '+61770101111', '+913858210056'
    ]


def test_iadd_regular_list() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    l += ['+61770101111', '+913858210056']
    assert l == [
        '+15555551234', '+447700900077', '+61770101111', '+913858210056'
    ]


def test_iadd_phone_list() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    l += PhoneList(['+61770101111', '+913858210056'])
    assert l == [
        '+15555551234', '+447700900077', '+61770101111', '+913858210056'
    ]


def test_insert() -> None:
    l: PhoneList = PhoneList()
    l.insert(0, '+15555551234')
    l.insert(1, '+447700900077')
    assert l == ['+15555551234', '+447700900077']


def test_copy_retains_type_and_values() -> None:
    l: PhoneList = PhoneList(['+15555551234', '+447700900077'])
    copy: PhoneList = l.copy()
    assert isinstance(copy, PhoneList)
    assert l is not copy
    assert copy == ['+15555551234', '+447700900077']


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: PhoneList = PhoneList(['+15555551234', 1])


def test_append_invalid_type() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(TypeError):
        l.extend(['+15555551234', 1])


def test_add_invalid_type() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(TypeError):
        _: PhoneList = l + ['+15555551234', 1]


def test_iadd_invalid_type() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(TypeError):
        l += ['+15555551234', 1]


def test_insert_invalid_type() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(TypeError):
        l.insert(0, 1)


def test_init_invalid_value() -> None:
    with pytest.raises(ValueError):
        _: PhoneList = PhoneList(['+15555551234', '5555551234'])


def test_append_invalid_value() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(ValueError):
        l.append('5555551234')


def test_extend_invalid_value() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(ValueError):
        l.extend(['+15555551234', '5555551234'])


def test_add_invalid_value() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(ValueError):
        _: PhoneList = l + ['+15555551234', '5555551234']


def test_iadd_invalid_value() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(ValueError):
        l += ['+15555551234', '5555551234']


def test_insert_invalid_value() -> None:
    l: PhoneList = PhoneList()
    with pytest.raises(ValueError):
        l.insert(0, '5555551234')
