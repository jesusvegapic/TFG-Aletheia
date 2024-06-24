from src.akademos.videos.domain.entities import Video
from src.akademos.videos.domain.repository import VideoRepository
from src.framework_ddd.core.infrastructure.repository import GridFsPersistenceModel, AsyncMotorGridFsGenericRepository


class VideoDataMapper(DataMapper):
    def persistence_model_to_entity(self, instance: GridFsPersistenceModel) -> Video:
        raise NotImplementedError()

    def entity_to_persistence_model(self, video: Video) -> GridFsPersistenceModel:
        return GridFsPersistenceModel(
            file_id=video.id,
            filename=video.name,
            content=entity.content,
            metadata={"content_type": entity.type.value}
        )


class AsyncMotorGridFsVideoRepository(AsyncMotorGridFsGenericRepository, VideoRepository):
    mapper_class = VideoDataMapper
