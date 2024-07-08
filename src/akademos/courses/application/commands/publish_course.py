from lato import Command
from src.akademos.courses.application import akademos_courses_module
from src.akademos.courses.domain.errors import NotAuthorizedTeacherError
from src.akademos.courses.domain.repository import CourseRepository
from src.framework_ddd.core.domain.errors import EntityNotFoundError
from src.framework_ddd.core.domain.value_objects import GenericUUID


class PublishCourse(Command):
    teacher_id: str
    course_id: str


@akademos_courses_module.handler(PublishCourse)
async def publish_course(command: PublishCourse, course_repository: CourseRepository, publish):
    course = await course_repository.get(GenericUUID(command.course_id))
    if course:
        if course.owner != command.teacher_id:
            raise NotAuthorizedTeacherError()

        course.publish()
        await course_repository.add(course)

        for event in course.pull_domain_events():
            await publish(event)
    else:
        raise EntityNotFoundError(entity_id=command.course_id)
