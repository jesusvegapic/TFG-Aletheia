from lato import Command

from src.agora.students.application import students_module
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class SetLastVisitedLectio(Command):
    student_id: str
    course_id: str
    lectio_id: str


@students_module.handler(SetLastVisitedLectio)
async def set_last_visited_lectio(command: SetLastVisitedLectio, repository: StudentRepository, publish):
    student = await repository.get(GenericUUID(command.student_id))
    if student:
        student.set_last_visited_lectio(command.lectio_id, command.course_id)
        await repository.add(student)
        for event in student.pull_domain_events():
            publish(event)
    else:
        raise StudentNotFoundError(entity_id=command.student_id)
