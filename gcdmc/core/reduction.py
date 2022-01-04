from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from core.subclient import Subclient

from google.api_core.retry import Retry
from google.cloud.datastore import Key, Batch, Transaction

from core.subentity import Subentity


class Reduction:
    """A data structure that groups together multiple puts of the same entity
    in order to reduce the number of writes to the Datastore in a single batch.
    """
    def __init__(self) -> None:
        self._keyed: Dict[Key, Subentity] = {}
        self._unkeyed: Dict[int, Subentity] = {}

    @property
    def entities(self) -> List[Subentity]:
        """Returns the unique entities that have been put as a list.
        """
        entities: list[Subentity] = list(self._keyed.values())
        entities.extend(self._unkeyed.values())
        return entities

    def put(self, entity: Subentity) -> None:
        """Adds an entity to the reduction. This method is called when a `put`
        call is made on an entity.

        :type entity: class:`core.subentity.Subentity`
        :param entity: The entity to add to the reduction.
        """
        if not entity.key.is_partial:
            self._keyed[entity.key] = entity
        else:
            self._unkeyed[id(entity)] = entity

    def put_multi(self, entities: List[Subentity]) -> None:
        """Adds multiple entities to the reduction. This method is called when
        a `put_multi` call is made on a list of entities.

        :type entities: list[class:`core.subentity.Subentity`]
        :param entities: The entities to add to the reduction.
        """
        entity: Subentity
        for entity in entities:
            self.put(entity)

    def clear(self) -> None:
        """Removes all the entities from the reduction.
        """
        self._keyed.clear()
        self._unkeyed.clear()


class ReducedBatch(Batch):
    """A `ReducedBatch` is a batch that uses a reduction to reduce the number
    of writes to the Datastore in a single commit.

    :type client: :class:`core.subclient.Subclient`
    :param client: The subclient used to connect to the Datastore.
    """
    def __init__(self, client: Subclient) -> None:
        super(ReducedBatch, self).__init__(client)
        self._reduction: Reduction = Reduction()

    def put(self, entity: Subentity) -> None:
        """Remembers an entity to be saved.

        This adds the entity to the batch's reduction, but does not call the
        base batch's `put` method.

        :type entity: class:`core.subentity.Subentity`
        :param entity: The entity to be saved.
        """
        self._reduction.put(entity)

    def commit(self,
               retry: Optional[Retry] = None,
               timeout: float = None) -> None:
        """Commits the batch.

        This method will iterate through all the entities in the batch's
        reduction and call the base batch's `put` method on each entity.
        Afterwards, the entites are committed.

        :type retry: :class:`google.api_core.retry.Retry`, optional
        :param retry: A retry object used to retry requests. If ``None`` is
            specified, requests will be retried using a default configuration.

        :type timeout: float, optional
        :param timeout: Time, in seconds, to wait for the request to complete.
            Note that if ``retry`` is specified, the timeout applies to each
            individual attempt.
        """
        entity: Subentity
        for entity in self._reduction.entities:
            super().put(entity)
        super().commit(retry=retry, timeout=timeout)


class ReducedTransaction(Transaction, ReducedBatch):
    """A `ReducedTransaction` is a transaction that also inherits behavior from
    the `ReducedBatch` type.

    The method resolution order for this class is: `ReducedTransaction`,
    `Transaction`, `ReducedBatch`, `Batch`, `object`.

    This means that when `put` or `commit` is called, the `Transaction`
    behavior will be executed first, which will result in a call to `super`.
    As a result of the call to `super`, the `ReducedBatch` behavior will be
    executed next. Thus, the entities that are to be put or committed will be
    properly stored in the reduction to minimize datastore write contention.

    See https://rhettinger.wordpress.com/2011/05/26/super-considered-super/ for
    a more detailed explanation of the method resolution order and `super`.
    """
    pass
