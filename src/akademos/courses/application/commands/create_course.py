from typing import List

from lato import Command
from src.akademos.courses.application import courses_module
from src.akademos.courses.domain.entities import Course
from src.akademos.courses.domain.repository import CourseRepository


class CreateCourse(Command):
    course_id: str
    teacher_id: str
    name: str
    description: str
    topics: List[str]


@courses_module.handler(CreateCourse)
async def create_course(command: CreateCourse, course_repository: CourseRepository, publish):
    course = Course.create(
        id=command.course_id,
        owner=command.teacher_id,
        name=command.name,
        description=command.description,
        topics=command.topics
    )

    await course_repository.add(course)

    await publish(course.pull_domain_events())
