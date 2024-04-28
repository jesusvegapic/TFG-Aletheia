from lato import Command
from src.admin.courses.application import courses_module
from src.admin.courses.domain.entities import Course
from src.admin.courses.domain.repository import CourseRepository
from src.admin.courses.domain.value_objects import CourseName, CourseDescription


class CreateCourse(Command):
    course_id: str
    teacher_id: str
    name: str
    description: str
    topics: list[str]


@courses_module.handler(CreateCourse)
async def create_course(command: CreateCourse, course_repository: CourseRepository, publish):
    course = Course(
        id=GenericUUID(command.course_id),
        owner=GenericUUID(command.teacher_id),
        name=CourseName(command.name),
        description=CourseDescription(command.description),
        topic=[Topic(topic) for topic in command.topics]
    )

    course_repository.add(course)

    await publish(course.pull_domain_events())
