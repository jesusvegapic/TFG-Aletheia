from lato import Command
from pydantic import BaseModel

from src.akademos.faculties.domain.entities import Faculty, Degree
from src.akademos.faculties.domain.repository import FacultyRepository


class CreateFaculty(Command):
    faculty_id: str
    name: str
    degrees: list['DegreeDto']


class DegreeDto(BaseModel):
    id: str
    name: str


async def create_faculty(command: CreateFaculty, faculty_repository: FacultyRepository, publish):
    faculty = Faculty.create(
        id=command.faculty_id,
        name=command.name,
        degrees=[
            Degree(
                id=degree.id,
                name=degree.name
            )
            for degree in command.degrees
        ]
    )

    await faculty_repository.add(faculty)

    for event in faculty.pull_domain_events():
        await publish(event)
