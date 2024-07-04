from lato import Command
from src.agora.students.domain.entities import Student, StudentFaculty
from src.agora.students.domain.repository import StudentRepository
from src.akademos.faculties.application.queries.get_faculty import GetFaculty, GetFacultyResponse  # type: ignore
from src.framework_ddd.core.domain.value_objects import GenericUUID


class SignUpStudent(Command):
    student_id: str
    email: str
    password: str
    name: str
    firstname: str
    second_name: str
    faculty: str
    degree: str


async def sign_up_student(command: SignUpStudent, repository: StudentRepository, publish):
    faculty: GetFacultyResponse = await publish(GetFaculty(faculty_id=command.faculty))

    student = Student.create(
        command.student_id,
        command.name,
        command.firstname,
        command.second_name,
        command.email,
        command.password,
        StudentFaculty(faculty.id, [GenericUUID(degree) for degree in faculty.degrees]),
        command.degree
    )

    await repository.add(student)

    for event in student.pull_domain_events():
        await publish(event)
