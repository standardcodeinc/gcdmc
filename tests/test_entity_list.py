from __future__ import annotations

import pytest

from google.cloud.datastore import Entity

from gcdmc.model.types import EntityList


def entity(s: str) -> Entity:
    e: Entity = Entity()
    e[s] = s
    return e


def test_init() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    assert l == [entity('a'), entity('b')]


def test_append() -> None:
    l: EntityList = EntityList()
    l.append(entity('a'))
    l.append(entity('b'))
    assert l == [entity('a'), entity('b')]


def test_extend() -> None:
    l: EntityList = EntityList()
    l.extend([entity('a'), entity('b')])
    assert l == [entity('a'), entity('b')]


def test_add_regular_list() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    result: EntityList = l + [entity('c'), entity('d')]
    assert isinstance(result, EntityList)
    assert result == [entity('a'), entity('b'), entity('c'), entity('d')]


def test_add_entity_list() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    result: EntityList = l + EntityList([entity('c'), entity('d')])
    assert isinstance(result, EntityList)
    assert result == [entity('a'), entity('b'), entity('c'), entity('d')]


def test_iadd_regular_list() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    l += [entity('c'), entity('d')]
    assert l == [entity('a'), entity('b'), entity('c'), entity('d')]


def test_iadd_entity_list() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    l += EntityList([entity('c'), entity('d')])
    assert l == [entity('a'), entity('b'), entity('c'), entity('d')]


def test_insert() -> None:
    l: EntityList = EntityList()
    l.insert(0, entity('a'))
    l.insert(1, entity('b'))
    assert l == [entity('a'), entity('b')]


def test_copy_retains_type_and_values() -> None:
    l: EntityList = EntityList([entity('a'), entity('b')])
    copy: EntityList = l.copy()
    assert isinstance(copy, EntityList)
    assert l is not copy
    assert copy == [entity('a'), entity('b')]


def test_init_invalid_type() -> None:
    with pytest.raises(TypeError):
        _: EntityList = EntityList([entity('a'), {'a': 'a'}])


def test_append_invalid_type() -> None:
    l: EntityList = EntityList()
    with pytest.raises(TypeError):
        l.append(1)


def test_extend_invalid_type() -> None:
    l: EntityList = EntityList()
    with pytest.raises(TypeError):
        l.extend([entity('a'), {'a': 'a'}])


def test_add_invalid_type() -> None:
    l: EntityList = EntityList()
    with pytest.raises(TypeError):
        _: EntityList = l + [entity('a'), {'a': 'a'}]


def test_iadd_invalid_type() -> None:
    l: EntityList = EntityList()
    with pytest.raises(TypeError):
        l += [entity('a'), {'a': 'a'}]


def test_insert_invalid_type() -> None:
    l: EntityList = EntityList()
    with pytest.raises(TypeError):
        l.insert(0, {'a': 'a'})
