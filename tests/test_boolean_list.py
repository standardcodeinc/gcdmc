from __future__ import annotations

import pytest

from gcdmc.model.types import BooleanList


def test_init() -> None:
    l: BooleanList = BooleanList([True, False])
    assert l == [True, False]


def test_append() -> None:
    l: BooleanList = BooleanList()
    l.append(True)
    l.append(False)
    assert l == [True, False]


def test_extend() -> None:
    l: BooleanList = BooleanList()
    l.extend([True, False])
    assert l == [True, False]


def test_add_regular_list() -> None:
    l: BooleanList = BooleanList([True, False])
    result: BooleanList = l + [True, False]
    assert isinstance(result, BooleanList)
    assert result == [True, False, True, False]


def test_add_boolean_list() -> None:
    l: BooleanList = BooleanList([True, False])
    result: BooleanList = l + BooleanList([True, False])
    assert isinstance(result, BooleanList)
    assert result == [True, False, True, False]


def test_iadd_regular_list() -> None:
    l: BooleanList = BooleanList([True, False])
    l += [True, False]
    assert l == [True, False, True, False]


def test_iadd_boolean_list() -> None:
    l: BooleanList = BooleanList([True, False])
    l += BooleanList([True, False])
    assert l == [True, False, True, False]


def test_insert() -> None:
    l: BooleanList = BooleanList()
    l.insert(0, True)
    l.insert(1, False)
    assert l == [True, False]


def test_copy_retains_type_and_values() -> None:
    l: BooleanList = BooleanList([True, False])
    copy: BooleanList = l.copy()
    assert isinstance(copy, BooleanList)
    assert l is not copy
    assert copy == [True, False]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: BooleanList = BooleanList([True, 1])


def test_append_invlaid_type() -> None:
    l: BooleanList = BooleanList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: BooleanList = BooleanList()
    with pytest.raises(TypeError):
        l.extend([True, 1])


def test_add_invalid_type() -> None:
    l: BooleanList = BooleanList()
    with pytest.raises(TypeError):
        _: BooleanList = l + [True, 1]


def test_iadd_invalid_type() -> None:
    l: BooleanList = BooleanList()
    with pytest.raises(TypeError):
        l += [True, 1]


def test_insert_invalid_type() -> None:
    l: BooleanList = BooleanList()
    with pytest.raises(TypeError):
        l.insert(0, 1)
