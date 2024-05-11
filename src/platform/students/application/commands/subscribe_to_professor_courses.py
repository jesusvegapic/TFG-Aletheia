from lato import Command

from src.platform.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class SubscribeToProfessorCoursesByTopics(Command):
    student_id: str
    teacher_id: str
    topics: list[str]


async def subscribe_to_professor_courses_by_topic(
        command: SubscribeToProfessorCoursesByTopics,
        student_repository: StudentRepository,
        publish
):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    if not student:
        raise EntityNotFoundException(repository=student_repository, entity_id=command.student_id)

    if await publish(GetTeacher(command.teacher_id)):
        avaible_topics = map(lambda topic: topic.name, await publish(ListTopics()))

        def validate_topics(topic: str):
            if topic in avaible_topics:
                return Topic(topic)
            else:
                raise DomainException()

        topics = [validate_topics(topic) for topic in command.topics]

        subscription = ProfessorCoursesSubscription(
            id=ProfessorCoursesSubscription.next_id(),
            teacher=GenericUUID(command.teacher_id),
            topics=topics
        )

        student.add_professor_courses_subscription(subscription)

        student_repository.add(student)
