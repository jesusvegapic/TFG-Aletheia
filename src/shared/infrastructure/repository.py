from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.shared.domain.errors import EntityNotFoundError
from src.shared.domain.repositories import GenericRepository, Entity
from src.shared.domain.value_objects import GenericUUID
from src.shared.infrastructure.data_mapper import DataMapper
from src.shared.infrastructure.database import Base


# a sentinel value for keeping track of entities removed from the repository
class Removed:
    def __repr__(self):
        return "<Removed entity>"

    def __str__(self):
        return "<Removed entity>"


REMOVED = Removed()


class SqlAlchemyGenericRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[DataMapper[Entity, Base]]
    persistence_model_class: type[Entity]

    def __init__(self, db_session: AsyncSession, identity_map=None):
        self._session = db_session
        self._identity_map = identity_map or dict()

    @property
    def data_mapper(self):
        return self.mapper_class()

    def add(self, entity: Entity):
        if entity.id not in self._identity_map:
            self._identity_map[entity.id] = entity
            instance = self.map_entity_to_persistence_model(entity)
            self._session.add(instance)
        else:
            self._merge(entity)

    def _merge(self, entity: Entity):
        self._check_not_removed(entity.id)
        instance = self.map_entity_to_persistence_model(entity)
        merged = self._session.merge(instance)
        self._session.add(merged)

    async def get(self, id: GenericUUID) -> Optional[Entity]:  # type: ignore
        instance = await self._session.get(self.get_persistence_model_class(), id)
        if instance is None:
            return None
        return self._get_entity(instance)

    async def remove(self, entity: Entity):
        self._check_not_removed(entity.id)
        self._identity_map[entity.id] = REMOVED
        instance = await self._session.get(self.get_persistence_model_class(), id)
        await self._session.delete(instance)

    async def remove_by_id(self, entity_id: GenericUUID):
        self._check_not_removed(entity_id)
        self._identity_map[entity_id] = REMOVED
        instance = await self._session.get(self.get_persistence_model_class(), id)
        if instance is None:
            raise EntityNotFoundError(repository=self, entity_id=entity_id)
        await self._session.delete(instance)

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_persistence_model_to_entity(instance)
        self._check_not_removed(entity.id)

        if entity.id in self._identity_map:
            return self._identity_map[entity.id]

        self._identity_map[entity.id] = entity
        return entity

    def map_entity_to_persistence_model(self, entity: Entity):
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyDataMapper` in the Repository class."
        )

        return self.data_mapper.entity_to_persistence_model(entity)

    def map_persistence_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.persistence_model_to_entity(instance)

    def get_persistence_model_class(self):
        assert self.persistence_model_class is not None, (
            f"No model_class attribute in in {self.__class__.__name__}. "
            "Make sure to include `model_class = MyModel` in the class."
        )
        return self.persistence_model_class

    def _check_not_removed(self, entity_id):
        assert (
                self._identity_map.get(entity_id, None) is not REMOVED
        ), f"Entity {entity_id} already removed"

    def collect_events(self):
        events = []
        for entity in self._identity_map.values():
            events.extend(entity.collect_events())
        return events
