from lato import Command
from src.akademos.courses.application import akademos_courses_module
from src.akademos.courses.domain.entities import Lectio
from src.akademos.courses.domain.repository import CourseRepository
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.errors import EntityNotFoundError
from src.framework_ddd.core.domain.value_objects import GenericUUID


class AddLectio(Command):  # type: ignore
    lectio_id: str
    course_id: str
    name: str
    description: str
    video: VideoDto

    class Config:
        arbitrary_types_allowed = True


@akademos_courses_module.handler(AddLectio)
async def add_lectio(command: AddLectio, course_repository: CourseRepository, publish):
    course = await course_repository.get(GenericUUID(command.course_id))
    if course:
        lectio = Lectio.create(
            command.lectio_id,
            command.name,
            command.description
        )
        course.add_lectio(lectio, command.video)

        await course_repository.add(course)
        for event in course.pull_domain_events():
            await publish(event)
    else:
        raise EntityNotFoundError(entity_id=command.course_id)
