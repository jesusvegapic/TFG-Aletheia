from lato import Query
from motor.motor_asyncio import AsyncIOMotorClientSession, AsyncIOMotorGridFSBucket
from sqlalchemy.ext.asyncio import AsyncSession


class GetLectio(Query):
    lectio_id: str


async def get_lectio(
        query: GetLectio,
        lectio_session: AsyncSession,
        video_session: AsyncIOMotorClientSession,
        bucket: AsyncIOMotorGridFSBucket
) -> LectioDao:
    lectio_model = await lectio_session.get(LectioModel, GenericUUID(query.lectio_id))
    video_file = await bucket.open_download_stream(query.lectio_id, video_session)
    lectio_dao = lectio_model_and_lectio_file_to_lectio_dao(lectio_model, video_file)
