from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.courses.application import agora_courses_module
from src.agora.shared.application.queries import GetLectio, GetLectioResponse
from src.agora.videos.application.queries.get_video import GetVideo
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import LectioModel


@agora_courses_module.handler(GetLectio)
async def get_lectio(
        query: GetLectio,
        session: AsyncSession,
        publish_query
) -> GetLectioResponse:
    lectio_model = await session.get(LectioModel, GenericUUID(query.lectio_id))

    return GetLectioResponse(
        lectio_id=lectio_model.id.hex,  # type: ignore
        name=lectio_model.name,  # type: ignore
        description=lectio_model.description,  # type: ignore
        video_id=lectio_model.video_id.hex
    )
