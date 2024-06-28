from src.akademos.videos.domain.entities import Video
from src.akademos.videos.domain.repository import VideoRepository
from src.akademos.videos.infrastructure.errors import NullContentType
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import GridFsPersistenceModel, AsyncMotorGridFsGenericRepository


class VideoDataMapper(DataMapper):
    def model_to_entity(self, instance: GridFsPersistenceModel) -> Video:
        raise NotImplementedError()

    def entity_to_model(self, video: Video) -> GridFsPersistenceModel:
        return GridFsPersistenceModel(
            file_id=GenericUUID(video.id),
            filename=video.name,
            content=video.content,
            metadata={"content_type": video.type}
        )


class AsyncMotorGridFsVideoRepository(AsyncMotorGridFsGenericRepository, VideoRepository):
    mapper_class = VideoDataMapper
