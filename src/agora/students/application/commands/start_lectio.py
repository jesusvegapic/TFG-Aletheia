from lato import Command
from src.agora.students.domain.entities import StudentLectio
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StartLectio(Command):
    student_id: str
    course_id: str
    lectio_id: str


async def start_lectio(command: StartLectio, student_repository: StudentRepository, publish):
    student = await student_repository.get(GenericUUID(command.student_id))
    if student:
        await publish(ExistsLectioInCourse(course_id=command.course_id, lectio_id=command.lectio_id))
        student.start_lectio_in_course(command.course_id, StudentLectio(command.lectio_id))
        await student_repository.add(student)
        await publish(student.pull_domain_events())
    else:
        raise StudentNotFoundError(id=command.student_id)
