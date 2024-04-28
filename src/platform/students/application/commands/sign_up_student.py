from typing import Optional

from lato import Command

from src.platform.students.domain.repository import StudentRepository


class SignUpStudent(Command):
    student_id: str
    email: str
    password: str
    name: str
    surnames: tuple[str, Optional[str]]
    faculty_id: str
    degree_id: str


async def sign_up_student(command: SignUpStudent, student_repository: StudentRepository, publish):
    faculty_dao = await publish(GetFaculty(command.faculty_id))
    if faculty_dao:
        if command.degree_id not in faculty_dao.degress:
            raise DomainException()

        student = Student(
            id=GenericUUID(command.student_id),
            email=Email(email),
            password=Password(command.password),
            name=Name(command.name),
            surnames=Surnames(command.surnames[0], command.surnames[1]),
            faculty=GenericUUID(command.faculty_id),
            degree=GenericUUID(command.degree_id)
        )

        student_repository.add(student)

    else:
        raise EntityNotFoundException()
