from __future__ import annotations

import pytest

from gcdmc.model.types import EmailList


def test_init() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    assert l == ['foo@gmail.com', 'bar@gmail.com']


def test_append() -> None:
    l: EmailList = EmailList()
    l.append('foo@gmail.com')
    l.append('bar@gmail.com')
    assert l == ['foo@gmail.com', 'bar@gmail.com']


def test_extend() -> None:
    l: EmailList = EmailList()
    l.extend(['foo@gmail.com', 'bar@gmail.com'])
    assert l == ['foo@gmail.com', 'bar@gmail.com']


def test_add_regular_list() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    result: EmailList = l + ['baz@gmail.com', 'qux@gmail.com']
    assert isinstance(result, EmailList)
    assert result == [
        'foo@gmail.com', 'bar@gmail.com', 'baz@gmail.com', 'qux@gmail.com'
    ]


def test_add_email_list() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    result: EmailList = l + EmailList(['baz@gmail.com', 'qux@gmail.com'])
    assert isinstance(result, EmailList)
    assert result == [
        'foo@gmail.com', 'bar@gmail.com', 'baz@gmail.com', 'qux@gmail.com'
    ]


def test_iadd_regular_list() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    l += ['baz@gmail.com', 'qux@gmail.com']
    assert l == [
        'foo@gmail.com', 'bar@gmail.com', 'baz@gmail.com', 'qux@gmail.com'
    ]


def test_iadd_email_list() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    l += EmailList(['baz@gmail.com', 'qux@gmail.com'])
    assert l == [
        'foo@gmail.com', 'bar@gmail.com', 'baz@gmail.com', 'qux@gmail.com'
    ]


def test_insert() -> None:
    l: EmailList = EmailList()
    l.insert(0, 'foo@gmail.com')
    l.insert(1, 'bar@gmail.com')
    assert l == ['foo@gmail.com', 'bar@gmail.com']


def test_copy_retains_type_and_values() -> None:
    l: EmailList = EmailList(['foo@gmail.com', 'bar@gmail.com'])
    copy: EmailList = l.copy()
    assert isinstance(copy, EmailList)
    assert l is not copy
    assert copy == ['foo@gmail.com', 'bar@gmail.com']


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: EmailList = EmailList(['foo@gmail.com', 1])


def test_append_invalid_type() -> None:
    l: EmailList = EmailList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: EmailList = EmailList()
    with pytest.raises(TypeError):
        l.extend(['foo@gmail.com', 1])


def test_add_invalid_type() -> None:
    l: EmailList = EmailList()
    with pytest.raises(TypeError):
        _: EmailList = l + ['foo@gmail.com', 1]


def test_iadd_invalid_type() -> None:
    l: EmailList = EmailList()
    with pytest.raises(TypeError):
        l += ['foo@gmail.com', 1]


def test_insert_invalid_type() -> None:
    l: EmailList = EmailList()
    with pytest.raises(TypeError):
        l.insert(0, 1)


def test_init_invalid_value() -> None:
    with pytest.raises(ValueError):
        _: EmailList = EmailList(['foo@gmail.com', 'a'])


def test_append_invalid_value() -> None:
    l: EmailList = EmailList()
    with pytest.raises(ValueError):
        l.append('a')


def test_extend_invalid_value() -> None:
    l: EmailList = EmailList()
    with pytest.raises(ValueError):
        l.extend(['foo@gmail.com', 'a'])


def test_add_invalid_value() -> None:
    l: EmailList = EmailList()
    with pytest.raises(ValueError):
        _: EmailList = l + ['foo@gmail.com', 'a']


def test_iadd_invalid_value() -> None:
    l: EmailList = EmailList()
    with pytest.raises(ValueError):
        l += ['foo@gmail.com', 'a']


def test_insert_invalid_value() -> None:
    l: EmailList = EmailList()
    with pytest.raises(ValueError):
        l.insert(0, 'a')
