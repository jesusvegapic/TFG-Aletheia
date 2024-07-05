from lato import Command
from src.akademos.faculties.application.queries.get_faculty import GetFaculty
from src.akademos.teachers.application import teachers_module
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


@teachers_module.handler(SignUpTeacher)
async def sign_up_teacher(command: SignUpTeacher, teacher_repository: TeacherRepository, publish_query, publish):
    faculty = await publish_query(GetFaculty(faculty_id=command.faculty_id))

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

    await teacher_repository.add(teacher)

    for event in teacher.pull_domain_events():
        await publish(event)
