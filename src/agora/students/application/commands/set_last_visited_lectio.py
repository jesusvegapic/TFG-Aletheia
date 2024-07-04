from lato import Command
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class SetLastVisitedLectio(Command):
    student_id: str
    lectio_id: str


async def set_last_visited_lectio(command: SetLastVisitedLectio, repository: StudentRepository):
    student = await repository.get(GenericUUID(command.student_id))
    if student:
        student.set_last_visited_lectio(command.lectio_id)
        await repository.add(student)
