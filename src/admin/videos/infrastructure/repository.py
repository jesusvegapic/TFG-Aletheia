from src.shared.infrastructure.persistence.data_mapper import DataMapper
from src.shared.infrastructure.persistence.sql_alchemy.repository import AsyncMotorGridFsGenericRepository, GridFsPersistenceModel
from src.videos.domain.entities import Video
from src.videos.domain.repository import VideoRepository


class VideoDataMapper(DataMapper):
    def persistence_model_to_entity(self, instance: GridFsPersistenceModel) -> Video:
        raise NotImplementedError()

    def entity_to_persistence_model(self, entity: Video) -> GridFsPersistenceModel:
        return GridFsPersistenceModel(
            file_id=entity.id,
            filename=entity.name.value,
            content=entity.content,
            metadata={"content_type": entity.type.value}
        )


class AsyncMotorGridFsVideoRepository(AsyncMotorGridFsGenericRepository, VideoRepository):
    mapper_class = VideoDataMapper
