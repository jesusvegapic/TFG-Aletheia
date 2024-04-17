from aiofiles.threadpool.binary import AsyncBufferedReader
from lato import Event
from pydantic import ConfigDict


class VideoIsWaitingForUpload(Event):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    entity_id: str
    video_id: str
    video: AsyncBufferedReader
    video_name: str
    video_type: str

