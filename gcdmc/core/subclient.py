from __future__ import annotations
from typing import Any, Callable, List, Optional, Union

from functools import update_wrapper
from google.cloud.datastore.entity import Entity
from google.cloud.datastore.key import Key
from google.cloud.datastore.transaction import Transaction
from requests import Session

from google.api_core.client_options import ClientOptions
from google.api_core.retry import Retry
from google.auth.credentials import Credentials
from google.cloud.datastore import Client

from gcdmc.core.reduction import ReducedBatch, ReducedTransaction
from gcdmc.core.registry import Registry
from gcdmc.core.subentity import Subentity
from gcdmc.core.subquery import Subquery


class Subclient(Client):
    def __init__(self,
                 project: Optional[str] = None,
                 namespace: Optional[str] = None,
                 credentials: Optional[Credentials] = None,
                 client_options: Optional[ClientOptions] = None,
                 registry: Optional[Registry] = None,
                 _http: Optional[Session] = None,
                 _use_grpc: Optional[bool] = None):
        self._registry: Optional[Registry] = registry
        super().__init__(project=project,
                         namespace=namespace,
                         credentials=credentials,
                         client_options=client_options,
                         _http=_http,
                         _use_grpc=_use_grpc)

    def get_multi(self,
                  keys: List[Key | str],
                  missing: Optional[List] = None,
                  deferred: Optional[List] = None,
                  transaction: Transaction = None,
                  eventual: bool = False,
                  retry: Optional[Retry] = None,
                  timeout: Optional[float] = None):
        """Retrieve entities and wrap them as subentities.

        Unlike the base client `get_multi` method, the subclient implementation
        also accpets a list of URL safe string representations of the keys. The
        input list of keys can be a mix of datastore keys and strings.
        """
        db_keys: List[Key] = [self._to_key(key) for key in keys]
        entities: List[Entity] = super().get_multi(db_keys,
                                                   missing=missing,
                                                   deferred=deferred,
                                                   transaction=transaction,
                                                   eventual=eventual,
                                                   retry=retry,
                                                   timeout=timeout)
        return [self._wrap(e) for e in entities]

    def batch(self) -> ReducedBatch:
        """Proxy to the `ReducedBatch` constructor.
        """
        return ReducedBatch(self)

    def transaction(self, **kwargs: Any) -> ReducedTransaction:
        """Proxy to the `ReducedTransaction` constructor.
        """
        return ReducedTransaction(self, **kwargs)

    def query(self, **kwargs: Any) -> Subquery:
        """Returns a subquery derived from a plain Datastore query.
        """
        return Subquery.derive(super().query(**kwargs),
                               registry=self._registry)

    def transactional(self,
                      allow_nesting: bool = False,
                      **kwargs: Any) -> Callable:
        """Decorates a method by wrapping it in a transaction.

        The `allow_nesting` argument allows you to specify whether or not a new
        transaction should be started if there is already an ongoing one. By
        default, `allow_nesting` is set to false since it seems that nested
        transactions can cause contention issues in certain situations.
        """
        def decorator(func: Callable) -> Callable:
            def wrapped(*a: Any, **kw: Any) -> Any:
                if not allow_nesting and self.current_transaction is not None:
                    return func(*a, **kw)
                with self.transaction(**kwargs):
                    return func(*a, **kw)

            return update_wrapper(wrapped, func)

        return decorator

    def _to_key(self, key: Union[Key, str]) -> Key:
        """Converts a datastore key or string into a datastore key.

        :type key: :class:`google.cloud.datastore.key.Key` | str
        :param key: The key to convert. If the key is a Datastore key, then it
            is simply returned unchanged.

        :rtype: :class:`google.cloud.datastore.key.Key`
        :returns: The converted key.
        """
        if isinstance(key, Key):
            return key
        return Key.from_legacy_urlsafe(key)

    def _wrap(self, entity: Entity) -> Subentity:
        """Wraps an entity in a subentity and returns the subentity.

        :type entity: :class:`google.cloud.datastore.entity.Entity`
        :param entity: The entity to wrap.

        :rtype: :class:`core.subentity.Subentity`
        :returns: The entity wrapped as a subentity.
        """
        if (self._registry is None
                or not self._registry.has_subentity_type(entity.key.kind)):
            return Subentity.wrap(entity)
        subtype: type[Subentity] = self._registry.get_subentity_type(
            entity.key.kind)
        return subtype.wrap(entity)
