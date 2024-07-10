from src.akademos.conferences.domain.events import ConferenceCreated
from src.akademos.videos.application import videos_module
from src.akademos.videos.domain.entities import Video
from src.akademos.videos.domain.repository import VideoRepository


@videos_module.handler(ConferenceCreated)
async def create_video_on_conference_created(event: ConferenceCreated, video_repository: VideoRepository, publish):
    video = Video.create(
        id=event.video.video_id,
        content=event.video.file,
        name=event.video.filename,
        type=event.video.content_type
    )

    await video_repository.add(video)

    for event in video.pull_domain_events():
        await publish(event)
