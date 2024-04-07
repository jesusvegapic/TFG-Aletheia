from abc import ABC, abstractmethod
from typing import TypeVar, Any, Generic

from src.shared.domain.entities import Entity
from src.shared.domain.value_objects import GenericUUID

MapperEntity = TypeVar("MapperEntity", bound=Entity)
MapperPersistenceModel = TypeVar("MapperPersistenceModel", bound=Any)


class DataMapper(Generic[MapperEntity, MapperPersistenceModel], ABC):
    entity_class: type[MapperEntity]
    model_class: type[MapperPersistenceModel]

    @abstractmethod
    def persistence_model_to_entity(self, instance: MapperPersistenceModel) -> MapperEntity:
        raise NotImplementedError()

    @abstractmethod
    def entity_to_persistence_model(self, entity: MapperEntity) -> MapperPersistenceModel:
        raise NotImplementedError()
