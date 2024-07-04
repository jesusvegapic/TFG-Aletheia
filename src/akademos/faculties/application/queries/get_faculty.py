from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class GetFaculty(Query):
    faculty_id: str


class GetFacultyResponse(BaseModel):
    id: str
    name: str
    degrees: List[str]


async def get_faculty(query: GetFaculty, session: AsyncSession):
    faculty_model = await session.get(FacultyModel, GenericUUID(query.faculty_id))
    dao = faculty_model_to_dao(faculty_model)
    return dao
