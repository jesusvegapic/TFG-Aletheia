from lato import Command


class CreateFaculty(Command):
    faculty_id: str
    name: str
    degrees: list[str]

async def create_faculty(command: CreateFaculty, faculty_repository: Faculty):
    faculty = Faculty(
        id=GenericUUID(command.faculty_id),
        name=FacultyName(command.name),
        degrees=[Degree(degree_id) for degree_id in command.degrees]
    )

    faculty_repository.add(faculty)
