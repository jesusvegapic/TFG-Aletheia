from lato import Command
from src.akademos.faculties.application.queries.get_faculty import GetFaculty
from src.akademos.teachers.domain.entities import Teacher, TeacherFaculty
from src.akademos.teachers.domain.repository import TeacherRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class SignUpTeacher(Command):
    teacher_id: str
    email: str
    password: str
    name: str
    firstname: str
    second_name: str
    faculty_id: str
    degrees: list[str]
    position: str


async def sign_up_teacher(command: SignUpTeacher, repository: TeacherRepository, publish):
    faculty = await publish(GetFaculty(faculty_id=command.faculty_id))

    teacher = Teacher.create(
        command.teacher_id,
        command.email,
        command.password,
        command.name,
        command.firstname,
        command.second_name,
        TeacherFaculty(faculty.id, [GenericUUID(degree) for degree in faculty.degrees]),
        command.degrees,
        command.position
    )

    await repository.add(teacher)

    for event in teacher.pull_domain_events():
        await publish(event)
