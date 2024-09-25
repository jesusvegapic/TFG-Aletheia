import abc
from typing import TypeVar, Generic, Optional
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.domain.entities import Entity as DomainEntity

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