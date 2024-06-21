from dataclasses import dataclass
from lato import Command

from src.akademos.courses.application import courses_module
from src.akademos.courses.domain.entities import Lectio
from src.akademos.courses.domain.repository import CourseRepository
from src.framework_ddd.core.domain.errors import EntityNotFoundError
from src.framework_ddd.core.domain.value_objects import GenericUUID


@dataclass(frozen=True)
class AddLectio(Command):  # type: ignore
    lectio_id: str
    course_id: str
    name: str
    description: str
    video_id: str


@courses_module.handler(AddLectio)
async def create_lectio(command: AddLectio, course_repository: CourseRepository, publish):
    course = await course_repository.get(GenericUUID(command.course_id))
    if course:
        lectio = Lectio(command.lectio_id, command.name, command.description, command.video_id)

        course.add_lectio(lectio)

        await course_repository.add(course)

        await publish(course.pull_domain_events())
    else:
        raise EntityNotFoundError(entity_id=course.id)
