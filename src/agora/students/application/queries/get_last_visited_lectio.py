from lato import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.shared.application.queries import GetLectio, GetLectioResponse
from src.agora.students.infrastructure.repository import StudentModel, StudentCourseModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import LectioModel
from src.shared.utils.list import find


class GetLastVisitedLectio(Query):
    course_id: str
    student_id: str


async def get_last_visited_lectio(
        query: GetLastVisitedLectio,
        session: AsyncSession
) -> GetLectioResponse:
    lectio_model = await find_lectio(query, session)

    return GetLectioResponse(
        lectio_id=lectio_model.id.hex,  # type: ignore
        name=lectio_model.name,  # type: ignore
        description=lectio_model.description,  # type: ignore
        video_id=lectio_model.video_id.hex
    )


async def find_lectio(
        query: GetLastVisitedLectio,
        session: AsyncSession
):
    result = await session.execute(
        select(LectioModel)
        .join(StudentCourseModel)
        .where(
            StudentCourseModel.id == GenericUUID(query.course_id) and
            StudentCourseModel.student_id == GenericUUID(query.student_id)
        )
    )
    return result.scalar_one()
