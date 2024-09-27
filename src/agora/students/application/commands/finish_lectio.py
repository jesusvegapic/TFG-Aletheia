from lato import Command
from src.agora.students.application import students_module
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class FinishLectio(Command):
    student_id: str
    course_id: str
    lectio_id: str


@students_module.handler(FinishLectio)
async def finish_lectio(command: FinishLectio, student_repository: StudentRepository, publish):
    student = await student_repository.get(GenericUUID(command.student_id))
    if student:
        student.finish_lectio_on_a_course(command.course_id, command.lectio_id)
        await student_repository.add(student)
        for event in student.pull_domain_events():
            await publish(event)
    else:
        raise StudentNotFoundError(entity_id=command.student_id)
