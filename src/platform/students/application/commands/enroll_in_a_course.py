from lato import Command

from src.platform.courses.application.queries.get_course import GetCourse
from src.platform.students.domain.errors import StudentNotFoundError, CourseNotFoundError
from src.platform.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class EnrollInACourse(Command):
    student_id: str
    course_id: str


async def enroll_in_a_course(command: EnrollInACourse, student_repository: StudentRepository, publish):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    if not student:
        raise StudentNotFoundError(entity_id=command.student_id)

    course_dao = await publish(GetCourse(command.course_id))
    if not course_dao:
        raise CourseNotFoundError(entity_id=command.course_id)

    course_entity = course_dato_to_entity(course_dao)
    student.enroll_in_a_course(course_entity)
    student_repository.add(student)
