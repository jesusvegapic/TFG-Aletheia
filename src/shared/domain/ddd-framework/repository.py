import abc
from typing import TypeVar, Generic, Optional

from src.shared.domain.ddd.entities import GenericUUID
from src.shared.domain.ddd.entities import Entity as DomainEntity

Entity = TypeVar("Entity", bound=DomainEntity)
EntityId = TypeVar("EntityId", bound=GenericUUID)


class GenericRepository(Generic[EntityId, Entity], metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: EntityId) -> Optional[Entity]:
        raise NotImplementedError

    @abc.abstractmethod
    async def remove(self, entity: Entity):
        raise NotImplementedError

    @abc.abstractmethod
    async def remove_by_id(self, id: EntityId):
        raise NotImplementedError

    @abc.abstractmethod
    def collect_events(self):
        raise NotImplementedError
    