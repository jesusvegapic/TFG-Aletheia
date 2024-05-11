from lato import Command

from src.platform.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StartLectio(Command):
    student_id: str
    lectio_id: str


async def start_lectio(command: StartLectio, student_repository: StudentRepository):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    student.start_lectio(command.lectio_id)
    student_repository.add(student)
