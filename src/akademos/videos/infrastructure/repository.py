from src.akademos.videos.domain.entities import Video
from src.akademos.videos.domain.repository import VideoRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import GridFsPersistenceModel, AsyncMotorGridFsGenericRepository


class VideoDataMapper(DataMapper):
    def model_to_entity(self, instance: GridFsPersistenceModel) -> Video:
        return Video(
            id=instance.file_id.hex,
            content=instance.content,  # type: ignore
            name=instance.filename,
            type=instance.metadata["content_type"]  # type: ignore
        )

    def entity_to_model(self, video: Video) -> GridFsPersistenceModel:
        return GridFsPersistenceModel(
            file_id=GenericUUID(video.id),
            filename=video.name,
            content=video.content,
            metadata={"content_type": video.type}
        )


class AsyncMotorGridFsVideoRepository(AsyncMotorGridFsGenericRepository, VideoRepository):
    mapper_class = VideoDataMapper
