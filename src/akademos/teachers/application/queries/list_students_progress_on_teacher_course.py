from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession


class ListStudentsProgressOnTeacherCourse(Query):
    teacher_id: str
    course_id: str


async def list_students_progress_on_teacher_course(query: ListStudentsProgressOnTeacherCourse, session: AsyncSession):
    course_model = await session.get(CourseModel, GenericUUID(query.course_id))
    if not course_model or course_model.owner_id != GenericUUID(query.teacher_id):
        raise EntityNotFoundException(entity_id=query.course_id)

    students_progress_dao = course_model_to_students_progress_dao(course_model)
    