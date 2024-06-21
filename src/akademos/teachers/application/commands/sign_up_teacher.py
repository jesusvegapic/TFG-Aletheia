from typing import Optional

from lato import Command


class SignUpTeacher(Command):
    teacher_id: str
    email: str
    password: str
    name: str
    surnames: tuple[str, Optional[str]]
    faculty_id: str
    degrees: list[str]
    position: str


async def sign_up_teacher(command: SignUpTeacher, student_repository: TeacherRepository, publish):
    faculty_dao = await publish(GetFaculty(command.faculty_id))
    if faculty_dao:
        for degree_id in command.degrees:
            if degree_id not in faculty_dao.degress:
                raise DomainException()

        teacher = Teacher(
            id=GenericUUID(command.student_id),
            email=Email(email),
            password=Password(command.password),
            name=Name(command.name),
            surnames=Surnames(command.surnames[0], command.surnames[1]),
            faculty=GenericUUID(command.faculty_id),
            degrees=[GenericUUID(degree_id) for degree_id in command.degrees],
            position=TeacherPosition(command.position)
        )

        teacher_repository.add(teacher)

    else:
        raise EntityNotFoundException()
