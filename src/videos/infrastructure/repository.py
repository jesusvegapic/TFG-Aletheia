from src.shared.infrastructure.data_mapper import DataMapper, MapperEntity, MapperPersistenceModel
from src.shared.infrastructure.repositories import AsyncMotorGridFsGenericRepository, GridFsPersistenceModel
from src.videos.domain.entities import Video
from src.videos.domain.repository import VideoRepository


class VideoDataMapper(DataMapper):
    def persistence_model_to_entity(self, instance: MapperPersistenceModel) -> MapperEntity:
        raise NotImplementedError()

    def entity_to_persistence_model(self, entity: Video) -> GridFsPersistenceModel:
        return GridFsPersistenceModel(
            file_id=entity.id,
            filename=entity.name,
            content=entity.content,
            metadata={"content_type": entity.type}
        )


class AsyncMotorGridFsVideoRepository(AsyncMotorGridFsGenericRepository, VideoRepository):
    mapper_class = VideoDataMapper
