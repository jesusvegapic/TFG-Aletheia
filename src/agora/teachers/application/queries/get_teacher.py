from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession


class GetTeacher(Query):
    teacher_id: str


async def get_teacher(query: GetTeacher, session: AsyncSession):
    teacher_model = await session.get(TeacherModel, GenericUUID(query.teacher_id))
    dao = teacher_model_to_dao
    return dao
