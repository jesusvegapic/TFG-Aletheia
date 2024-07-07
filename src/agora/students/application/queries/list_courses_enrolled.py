from lato import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.courses.application.queries.list_courses import ListCoursesResponse
from src.agora.shared.application.queries import ListedCourseDto
from src.agora.students.infrastructure.repository import StudentCourseModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import CourseModel


class ListCoursesEnrolled(Query):
    student_id: str


async def list_courses_enrolled(
        query: ListCoursesEnrolled,
        session: AsyncSession
) -> ListCoursesResponse:
    return ListCoursesResponse(
        courses=[
            ListedCourseDto(
                id=course.id.hex,
                owner=course.owner.hex,
                name=course.name
            )
            for course in await get_courses(query, session)
        ]
    )


async def get_courses(
        query: ListCoursesEnrolled,
        session: AsyncSession
):
    result = await session.execute(
        select(CourseModel)
        .join(StudentCourseModel)
        .where(StudentCourseModel.student_id == GenericUUID(query.student_id))
    )

    return result.scalars().all()
