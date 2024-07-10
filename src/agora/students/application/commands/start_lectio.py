from lato import Command
from src.agora.students.domain.entities import StudentLectio
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StartLectio(Command):
    student_id: str
    course_id: str
    lectio_id: str


async def start_lectio(command: StartLectio, student_repository: StudentRepository, publish):
    student = await student_repository.get(GenericUUID(command.student_id))
    if student:
        student.start_lectio_on_a_course(command.course_id, command.lectio_id)
        await student_repository.add(student)
        for event in student.pull_domain_events():
            await publish(event)
    else:
        raise StudentNotFoundError(entity_id=command.student_id)
