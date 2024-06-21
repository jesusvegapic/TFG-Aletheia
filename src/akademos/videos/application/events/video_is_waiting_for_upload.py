from src.Academia.courses.domain.events import VideoIsWaitingForUpload
from src.shared.domain.ddd.value_objects import GenericUUID
from src.videos.application import videos_module
from src.videos.domain.entities import Video
from src.videos.domain.repository import VideoRepository
from src.Academia.videos.domain.value_objects import VideoName, VideoType


@videos_module.handler(VideoIsWaitingForUpload)
async def video_is_waiting_for_upload(event: VideoIsWaitingForUpload, video_repository: VideoRepository):
    video = Video(
        id=GenericUUID(event.video_id),
        content=event.video,
        name=VideoName(event.video_name),
        type=VideoType(event.video_type)
    )

    await video_repository.add(video)
