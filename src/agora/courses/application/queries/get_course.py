from sqlalchemy.ext.asyncio import AsyncSession

from src.agora.shared.application.queries import GetCourse, GetCourseResponse, LectioDto
from src.shared.infrastructure.sql_alchemy.models import CourseModel


async def get_course(query: GetCourse, session: AsyncSession) -> GetCourseResponse:
    course_model = await session.get(CourseModel, query.course_id)
    response = course_model_to_get_course_response(course_model)  # type: ignore
    return response


def course_model_to_get_course_response(instance: CourseModel) -> GetCourseResponse:
    return GetCourseResponse(
        instance.id.hex,  # type: ignore
        instance.name,  # type: ignore
        instance.owner.hex,  # type: ignore
        instance.description,  # type: ignore
        [
            LectioDto(
                lectio.id.hex,
                lectio.name
            )
            for lectio in instance.lectios
        ]
    )
