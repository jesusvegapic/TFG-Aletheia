from re import split
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.courses.application import agora_courses_module
from src.agora.courses.domain.errors import PrivateCourseError
from src.agora.shared.application.queries import GetCourse, GetCourseResponse, LectioDto
from src.shared.domain.value_objects import CourseState
from src.shared.infrastructure.sql_alchemy.models import CourseModel


@agora_courses_module.handler(GetCourse)
async def get_course(query: GetCourse, session: AsyncSession) -> GetCourseResponse:
    course_model = await session.get(CourseModel, query.course_id)
    if query.user_info.user_id != course_model.owner.hex and course_model.state == CourseState.PUBLISHED:
        raise PrivateCourseError()

    response = course_model_to_get_course_response(course_model)  # type: ignore
    return response


def course_model_to_get_course_response(instance: CourseModel) -> GetCourseResponse:
    return GetCourseResponse(
        id=instance.id.hex,
        name=instance.name,  # type: ignore
        owner=instance.owner.hex,
        description=instance.description,  # type: ignore
        topics=split(";", instance.topics),  # type: ignore
        lectios=[
            LectioDto(
                id=lectio.id.hex,
                name=lectio.name
            )
            for lectio in instance.lectios
        ]
    )
