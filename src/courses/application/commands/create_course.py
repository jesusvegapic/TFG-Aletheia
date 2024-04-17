from lato import Command
from src.courses.application import courses_module
from src.courses.domain.entities import Course
from src.courses.domain.repository import CourseRepository
from src.courses.domain.value_objects import CourseName, CourseDescription
from src.shared.application.command_handlers import CommandResult
from src.shared.domain.entities import GenericUUID


class CreateCourse(Command):
    course_id: str
    teacher_id: str
    name: str
    description: str


@courses_module.handler(CreateCourse)
async def create_course(command: CreateCourse, course_repository: CourseRepository) -> CommandResult:
    course = Course(
        id=GenericUUID(command.course_id),
        owner=GenericUUID(command.teacher_id),
        name=CourseName(command.name),
        description=CourseDescription(command.description)
    )

    await course_repository.add(course)

    return CommandResult.success(course.id)
