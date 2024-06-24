from lato import Command
from src.agora.shared.application.queries import GetCourseResponse, GetCourse
from src.agora.students.domain.entities import StudentCourse, StudentLectio
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class EnrollInACourse(Command):
    student_id: str
    course_id: str


async def enroll_in_a_course(command: EnrollInACourse, student_repository: StudentRepository, publish):
    student = await student_repository.get(GenericUUID(command.student_id))
    if not student:
        raise StudentNotFoundError(entity_id=command.student_id)

    response: GetCourseResponse = await publish(GetCourse(course_id=command.course_id))

    student_course = get_course_response_to_entity(response)
    student.enroll_in_a_course(student_course)
    await student_repository.add(student)
    await publish(student.pull_domain_events())


def get_course_response_to_entity(response: GetCourseResponse) -> StudentCourse:
    return StudentCourse(
        response.id,
        [StudentLectio(lectio.id, None) for lectio in response.lectios]
    )
