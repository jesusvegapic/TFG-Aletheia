import bson
from lato import Query
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from src.agora.videos.application import agora_videos_module
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.database import AsyncGridOutWrapper
from src.framework_ddd.core.infrastructure.errors import NullFilename, NullContentType


class GetVideo(Query):
    video_id: str


@agora_videos_module.handler(GetVideo)
async def get_video(query: GetVideo, bucket: AsyncIOMotorGridFSBucket):
    grid_out = await bucket.open_download_stream(bson.Binary.from_uuid(GenericUUID(query.video_id)))
    filename, metadata = (grid_out.filename, grid_out.metadata)
    if filename and metadata:
        return VideoDto(
            video_id=query.video_id,
            file=AsyncGridOutWrapper(grid_out),
            filename=filename,
            content_type=metadata["content_type"]
        )
    else:
        if not filename:
            raise NullFilename(id=query.video_id)
        else:
            raise NullContentType(id=query.video_id)
