from lato import Command

from src.agora.students.domain.repository import StudentRepository


class SetLastVisitedLectio(Command):
    student_id: str
    lectio_id: str


async def set_last_visited_lectio(command: SetLastVisitedLectio, student_repository: StudentRepository):
    student = await student_repository.get_by_id(command.student_id)
    if student:
        student.set_last_visited_lectio(command.lectio_id)
        student_repository.add(student)
