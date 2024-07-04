from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.shared.application.queries import GetLectio, GetLectioResponse
from src.agora.students.infrastructure.repository import StudentModel, StudentCourseModel
from src.shared.utils.list import find


class GetLastVisitedLectio(Query):
    course_id: str
    student_id: str


async def get_last_visited_lectio(query: GetLastVisitedLectio, session: AsyncSession, publish) -> GetLectioResponse:
    instance = await session.get(StudentModel, query.student_id)
    course: StudentCourseModel = next(find(lambda course: course.id.hex == query.course_id, instance.student_courses))
    response = await publish(GetLectio(lectio_id=course.last_visited_lectio_id.hex))
    return response
