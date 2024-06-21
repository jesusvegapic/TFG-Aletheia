from lato import Command
from src.akademos.courses.application import courses_module
from src.akademos.courses.domain.entities import Course
from src.akademos.courses.domain.repository import CourseRepository


class CreateCourse(Command):
    course_id: str
    teacher_id: str
    name: str
    description: str
    topics: list[str]


@courses_module.handler(CreateCourse)
async def create_course(command: CreateCourse, course_repository: CourseRepository, publish):
    course = Course(
        command.course_id,
        command.teacher_id,
        command.name,
        command.description,
        command.topics
    )

    course_repository.add(course)

    await publish(course.pull_domain_events())
