from lato import Command


class EnrollInACourse(Command):
    student_id: str
    course_id: str


async def enroll_in_a_course(command: EnrollInACourse, student_repository: StudentRepository, publish):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    if student:
        student.enroll_in_a_course(GenericUUID(command.course_id))
        student_repository.add(student)
        await publish(student.pull_domain_events())
