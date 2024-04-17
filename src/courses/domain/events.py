from tempfile import SpooledTemporaryFile

from aiofiles.threadpool.binary import AsyncBufferedReader
from lato import Event
from pydantic import ConfigDict

from src.shared.domain.entities import GenericUUID


class CourseCreated(Event):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: GenericUUID


class VideoIsWaitingForUpload(Event):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    entity_id: str
    video_id: str
    video: SpooledTemporaryFile
    video_name: str
    video_type: str
