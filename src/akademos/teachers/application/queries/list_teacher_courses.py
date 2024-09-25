from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession


class ListTeacherCourses(Query):
    teacher_id: str


async def list_teacher_courses(query: ListTeacherCourses, session: AsyncSession, publish):
    teacher_model = await session.get(TeacherModel, GenericUUID(query.teacher_id))
    courses_dao = teacher_model_to_courses_dao(teacher_model)
    return courses_dao
