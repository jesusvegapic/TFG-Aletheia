from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.shared.infrastructure.models import FacultyModel
from src.akademos.faculties.application import faculties_module
from src.akademos.faculties.domain.errors import FacultyNotFoundError
from src.framework_ddd.core.domain.value_objects import GenericUUID


class GetFaculty(Query):
    faculty_id: str


class GetFacultyResponse(BaseModel):
    id: str
    name: str
    degrees: List[str]


@faculties_module.handler(GetFaculty)
async def get_faculty(query: GetFaculty, session: AsyncSession):
    faculty_model = await session.get(FacultyModel, GenericUUID(query.faculty_id))
    if faculty_model:
        return GetFacultyResponse(
            id=faculty_model.id.hex,  # type: ignore
            name=faculty_model.name,  # type: ignore
            degrees=[degree.id.hex for degree in faculty_model.degrees]  # type: ignore
        )
    else:
        raise FacultyNotFoundError(entity_id=query.faculty_id)