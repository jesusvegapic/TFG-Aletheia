from lato import Command
from src.agora.shared.application.queries import GetCourseResponse, GetCourse
from src.agora.students.application import students_module
from src.agora.students.domain.entities import StudentCourse, StudentLectio
from src.agora.students.domain.errors import StudentNotFoundError
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class EnrollInACourse(Command):
    student_id: str
    course_id: str


@students_module.handler(EnrollInACourse)
async def enroll_in_a_course(command: EnrollInACourse, student_repository: StudentRepository, publish_query, publish):
    student = await student_repository.get(GenericUUID(command.student_id))
    if not student:
        raise StudentNotFoundError(entity_id=command.student_id)

    response: GetCourseResponse = await publish_query(GetCourse(course_id=command.course_id, user_id=student.id))

    student_course = get_course_response_to_entity(response)
    student.enroll_in_a_course(student_course)
    await student_repository.add(student)
    for event in student.pull_domain_events():
        await publish(event)


def get_course_response_to_entity(response: GetCourseResponse) -> StudentCourse:
    return StudentCourse(
        response.id,
        response.course_id,
        [StudentLectio(lectio.id, None) for lectio in response.lectios]
    )
