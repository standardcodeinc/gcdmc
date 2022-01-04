from __future__ import annotations
from typing import Any, Callable, Optional, Sequence, Tuple, Type

from google.api_core.page_iterator import Page
from google.api_core.retry import Retry
from google.cloud.datastore import Client, Entity, Key
from google.cloud.datastore.query import Iterator, Query
from google.protobuf.message import Message

from gcdmc.core.registry import Registry
from gcdmc.core.subentity import Subentity


class Subpage(Page):
    def __init__(self,
                 parent: Iterator,
                 items: Sequence[Entity],
                 item_to_value: Callable[[Iterator], Entity],
                 raw_page: Optional[Message] = None,
                 registry: Optional[Registry] = None):
        self._registry: Registry = registry
        super().__init__(parent, items, item_to_value, raw_page=raw_page)

    def __next__(self) -> Subentity:
        """Gets the next entity, and returns it as a subentity.

        If the subpage has a registry and the kind of the next entity is in its
        registry, then the registered subentity type is used to wrap the entity.
        Otherwise, the plain `Subentity` class is used to wrap the entity.
        """
        entity: Entity = super().next()
        if self._registry is None:
            return Subentity.wrap(entity)
        subentity_type: Type[Subentity] = self._registry.get_subentity_type(
            entity.key.kind)
        return subentity_type.wrap(entity)

    @classmethod
    def derive(cls,
               page: Page,
               registry: Optional[Registry] = None) -> Subpage:
        # We can't call the constructor here because we don't have an iterable
        # object to pass into it. So we allocate a new `Subpage` object and
        # then copy the members over instead.
        subpage: Subpage = object.__new__(Subpage)
        subpage._parent = page._parent
        subpage._num_items = page._num_items
        subpage._remaining = page._remaining
        subpage._item_iter = page._item_iter
        subpage._item_to_value = page._item_to_value
        subpage._raw_page = page.raw_page
        subpage._registry = registry
        return subpage


class Subiterator(Iterator):
    def __init__(self,
                 query: Query,
                 client: Client,
                 limit: Optional[int] = None,
                 offset: Optional[int] = None,
                 start_cursor: Optional[bytes] = None,
                 end_cursor: Optional[bytes] = None,
                 eventual: bool = False,
                 retry: Optional[Retry] = None,
                 timeout: float = None,
                 registry: Optional[Registry] = None):
        self._registry: Optional[Registry] = registry
        super().__init__(query,
                         client,
                         limit=limit,
                         offset=offset,
                         start_cursor=start_cursor,
                         end_cursor=end_cursor,
                         eventual=eventual,
                         retry=retry,
                         timeout=timeout)

    def _next_page(self) -> Optional[Subpage]:
        page: Optional[Page] = super()._next_page()
        if page is None:
            return None
        return Subpage.derive(page, registry=self._registry)

    @classmethod
    def derive(cls,
               iterator: Iterator,
               registry: Optional[Registry] = None) -> Subiterator:
        return Subiterator(iterator._query,
                           iterator.client,
                           limit=iterator.max_results,
                           offset=iterator._offset,
                           start_cursor=iterator.next_page_token,
                           end_cursor=iterator._end_cursor,
                           eventual=iterator._eventual,
                           retry=iterator._retry,
                           timeout=iterator._timeout,
                           registry=registry)


class Subquery(Query):
    def __init__(self,
                 client: Client,
                 kind: Optional[str] = None,
                 project: Optional[str] = None,
                 namespace: Optional[str] = None,
                 ancestor: Optional[Key] = None,
                 filters: Sequence[Tuple[str, str, str]] = (),
                 projection: Sequence[str] = (),
                 order: Sequence[str] = (),
                 distinct_on: Sequence[str] = (),
                 registry: Optional[Registry] = None):
        self._registry: Optional[Registry] = registry
        super().__init__(client,
                         kind=kind,
                         project=project,
                         namespace=namespace,
                         ancestor=ancestor,
                         filters=filters,
                         projection=projection,
                         order=order,
                         distinct_on=distinct_on)

    def fetch(self,
              limit: Optional[int] = None,
              offset: int = 0,
              start_cursor: Optional[bytes] = None,
              end_cursor: Optional[bytes] = None,
              client: Optional[Client] = None,
              eventual: bool = False,
              retry: Optional[Retry] = None,
              timeout: Optional[float] = None) -> Subiterator:
        iterator: Iterator = super().fetch(limit=limit,
                                           offset=offset,
                                           start_cursor=start_cursor,
                                           end_cursor=end_cursor,
                                           client=client,
                                           eventual=eventual,
                                           retry=retry,
                                           timeout=timeout)
        return Subiterator.derive(iterator, registry=self._registry)

    @classmethod
    def derive(cls,
               query: Query,
               registry: Optional[Registry] = None) -> Subquery:
        return Subquery(query._client,
                        kind=query._kind,
                        project=query._project,
                        namespace=query._namespace,
                        ancestor=query._ancestor,
                        filters=query._filters,
                        projection=query._projection,
                        order=query._order,
                        distinct_on=query._distinct_on,
                        registry=registry)
