from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession


class GetLastVisitedLectio(Query):
    student_id: str

async def get_last_visited_lectio(query: GetLastVisitedLectio, session: AsyncSession):
    student_model = await session.get(StudentModel, query.student_id)
    lectio_name_dao = student_model_to_lectio_name_dao(student_model)
    return lectio_name_dao
