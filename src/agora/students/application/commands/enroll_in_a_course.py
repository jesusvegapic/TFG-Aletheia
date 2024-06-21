from lato import Command
from src.agora.courses.application.queries.get_course import GetCourse
from src.agora.shared.application.queries import GetCourseResponse
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class EnrollInACourse(Command):
    student_id: str
    course_id: str


async def enroll_in_a_course(command: EnrollInACourse, student_repository: StudentRepository, publish):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    if not student:
        raise StudentNotFoundError(entity_id=command.student_id)

    response: GetCourseResponse = await publish(GetCourse(command.course_id))

    course_entity = get_course_response_to_entity(response)
    student.enroll_in_a_course(course_entity)
    student_repository.add(student)
    await publish(student.pull_domain_events())
