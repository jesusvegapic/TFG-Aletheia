from typing import BinaryIO

from tempfile import SpooledTemporaryFile
from lato import Command
from pydantic import ConfigDict

from src.courses.application import courses_module
from src.courses.domain.entities import Lectio
from src.courses.domain.repository import CourseRepository
from src.courses.domain.value_objects import LectioName, LectioDescription
from src.shared.application.integration_events import VideoIsWaitingForUpload
from src.shared.domain.value_objects import GenericUUID


class CreateLectio(Command):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: str
    course_id: str
    name: str
    description: str
    video: SpooledTemporaryFile
    video_name: str
    video_type: str


@courses_module.handler(CreateLectio)
async def create_lectio(command: CreateLectio, course_repository: CourseRepository, publish_async):
    course = await course_repository.get(GenericUUID(command.course_id))
    lectio_id = Lectio.next_id()
    lectio = Lectio(
        id=lectio_id,
        name=LectioName(command.name),
        description=LectioDescription(command.description)
    )

    course.add_lectio(lectio)

    await course_repository.add(course)

    await publish_async(
        VideoIsWaitingForUpload(
            entity_id=course.id.hex,
            video_id=lectio_id.hex,
            content=command.video,
            name=command.video_name,
            type=command.video_type
        )
    )
