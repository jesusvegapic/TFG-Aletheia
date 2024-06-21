from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession


class GetFaculty(Query):
    faculty_id: str

async def get_faculty(query: GetFaculty, session: AsyncSession):
    faculty_model = await session.get(FacultyModel, GenericUUID(query.faculty_id))
    dao = faculty_model_to_dao(faculty_model)
    return dao
