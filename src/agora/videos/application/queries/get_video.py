import bson
from lato import Query
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.database import GridOutWrapper
from src.framework_ddd.core.infrastructure.errors import NullFilename, NullContentType


class GetVideo(Query):
    video_id: str


async def get_video(query: GetVideo, session: AsyncIOMotorClientSession, bucket: AsyncIOMotorGridFSBucket):
    grid_out = await bucket.open_download_stream(bson.Binary.from_uuid(GenericUUID(query.video_id)), session)
    filename, content_type = (grid_out.filename, grid_out.content_type)
    if filename and content_type:
        return VideoDto(
            file=GridOutWrapper(grid_out),
            filename=filename,
            content_type=content_type
        )
    else:
        if not filename:
            raise NullFilename(id=query.video_id)
        else:
            raise NullContentType(id=query.video_id)
