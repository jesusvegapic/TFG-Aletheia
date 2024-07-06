from dataclasses import dataclass
from typing import Optional, Any, Mapping
from uuid import UUID
import bson
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket
from sqlalchemy.ext.asyncio import AsyncSession
from src.framework_ddd.core.domain.errors import EntityNotFoundError
from src.framework_ddd.core.domain.files import BinaryIOProtocol, AsyncBinaryIOProtocol
from src.framework_ddd.core.domain.repository import GenericRepository, Entity, EntityId
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.database import Base, GridOutWrapper, AsyncGridOutWrapper
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.errors import NullFilename


# a sentinel value for keeping track of entities removed from the repository
class Removed:
    def __repr__(self):
        return "<Removed entity>"

    def __str__(self):
        return "<Removed entity>"


class SqlAlchemyGenericRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[DataMapper[Entity, Base]]
    model_class: type[Base]
    removed: Removed

    def __init__(self, db_session: AsyncSession, identity_map=None):
        self._session = db_session
        self._identity_map = identity_map or dict()
        self.removed = Removed()

    @property
    def data_mapper(self):
        return self.mapper_class()

    async def add(self, entity: Entity):
        if entity.id not in self._identity_map.keys():
            self._identity_map[entity.id] = entity
            instance = self.map_entity_to_model(entity)
            self._session.add(instance)
        else:
            await self._merge(entity)

    async def _merge(self, entity: Entity):
        self._check_not_removed(entity.id)
        instance = self.map_entity_to_model(entity)
        merged = await self._session.merge(instance)
        self._session.add(merged)

    async def get(self, id: GenericUUID) -> Optional[Entity]:  # type: ignore
        instance = await self._session.get(self.get_model_class(), id)
        if instance is None:
            return None
        return self._get_entity(instance)

    async def remove(self, entity: Entity):
        self._check_not_removed(entity.id)
        self._identity_map[entity.id] = self.removed
        instance = await self._session.get(self.get_model_class(), id)
        await self._session.delete(instance)

    async def remove_by_id(self, entity_id: GenericUUID):
        self._check_not_removed(entity_id)
        self._identity_map[entity_id] = self.removed
        instance = await self._session.get(self.get_model_class(), id)
        if instance is None:
            raise EntityNotFoundError(entity_id.hex)
        await self._session.delete(instance)

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_model_to_entity(instance)
        self._check_not_removed(entity.id)

        if entity.id in self._identity_map:
            return self._identity_map[entity.id]

        self._identity_map[entity.id] = entity
        return entity

    def map_entity_to_model(self, entity: Entity):
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyDataMapper` in the Repository class."
        )

        return self.data_mapper.entity_to_model(entity)

    def map_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)

    def get_model_class(self):
        assert self.model_class is not None, (
            f"No model_class attribute in in {self.__class__.__name__}. "
            "Make sure to include `model_class = MyModel` in the class."
        )
        return self.model_class

    def _check_not_removed(self, entity_id):
        assert (
                self._identity_map.get(entity_id, None) is not self.removed
        ), f"Entity {entity_id} already removed"

    def collect_events(self):
        events = []
        for entity in self._identity_map.values():
            events.extend(entity.collect_events())
        return events


class AsyncMotorGridFsGenericRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[DataMapper[Entity, Base]]
    model_class: 'GridFsPersistenceModel'
    removed: Removed

    def __init__(self, bucket: AsyncIOMotorGridFSBucket, session: AsyncIOMotorClientSession, identity_map=None):
        self._session = session
        self._bucket = bucket
        self._identity_map = identity_map or dict()
        self.removed = Removed()

    @property
    def data_mapper(self):
        return self.mapper_class()

    async def add(self, entity: Entity):
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_model(entity)
        await self._bucket.upload_from_stream_with_id(
            file_id=bson.Binary.from_uuid(instance.file_id),
            filename=instance.filename,
            source=instance.content.sync_mode(),
            metadata=instance.metadata,
            session=self._session
        )

    def map_entity_to_model(self, entity: Entity) -> 'GridFsPersistenceModel':
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyDataMapper` in the Repository class."
        )

        return self.data_mapper.entity_to_model(entity)

    async def get(self, id: EntityId) -> Optional[Entity]:
        download = await self._bucket.open_download_stream(bson.Binary.from_uuid(id), self._session)
        filename = download.filename
        if filename:
            instance = GridFsPersistenceModel(
                file_id=id,
                filename=filename,
                content=AsyncGridOutWrapper(download),
                metadata=download.metadata
            )
            if instance is None:
                return None
            return self._get_entity(instance)
        else:
            raise NullFilename(id=id.hex)

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_model_to_entity(instance)
        self._check_not_removed(entity.id)

        if entity.id in self._identity_map:
            return self._identity_map[entity.id]

        self._identity_map[entity.id] = entity
        return entity

    def _check_not_removed(self, entity_id):
        assert (
                self._identity_map.get(entity_id, None) is not self.removed
        ), f"Entity {entity_id} already removed"

    def map_model_to_entity(self, instance) -> Entity:
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)

    async def remove(self, entity: Entity):
        raise NotImplementedError()

    async def remove_by_id(self, id: EntityId):
        raise NotImplementedError()

    def collect_events(self):
        raise NotImplementedError()


@dataclass(kw_only=True)
class GridFsPersistenceModel:
    file_id: UUID
    filename: str
    content: AsyncBinaryIOProtocol
    metadata: Optional[Mapping[str, Any]]
