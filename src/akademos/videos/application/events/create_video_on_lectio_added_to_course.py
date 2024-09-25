from src.akademos.shared.application.events import LectioAdded
from src.akademos.videos.application import videos_module
from src.akademos.videos.domain.entities import Video
from src.akademos.videos.domain.repository import VideoRepository


@videos_module.handler(LectioAdded)
async def create_video_on_lectio_added_to_course(event: LectioAdded, video_repository: VideoRepository, publish):
    video = Video(
        event.video.video_id,
        event.video.file,
        event.video.filename,
        event.video.content_type
    )

    await video_repository.add(video)

    for event in video.pull_domain_events():
        await publish(event)
