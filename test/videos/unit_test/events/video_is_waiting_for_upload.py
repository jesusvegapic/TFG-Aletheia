import tempfile
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from src.admin.courses.domain.events import VideoIsWaitingForUpload
from src.shared.domain.ddd.value_objects import GenericUUID
from src.videos.application.events.video_is_waiting_for_upload import video_is_waiting_for_upload
from src.videos.domain.entities import Video
from src.admin.videos.domain.value_objects import VideoName, VideoType


class VideoIsWaitingForDownloadShould(IsolatedAsyncioTestCase):

    def setUp(self):
        self.repository = MagicMock()

    async def test_create_a_valid_video(self):
        video = tempfile.SpooledTemporaryFile()
        video_id = Video.next_id()
        event = VideoIsWaitingForUpload(
            entity_id=GenericUUID.next_id().hex,
            video_id=video_id.hex,
            video=video,
            video_name="garfield",
            video_type="/video/mp4"
        )

        add_mock = AsyncMock()
        self.repository.add = add_mock

        await video_is_waiting_for_upload(event, self.repository)

        args, kwargs = self.repository.add.call_args
        actual_video = args[0]

        expected_video = Video(
            id=video_id,
            content=video,
            name=VideoName("garfield"),
            type=VideoType("/video/mp4")
        )

        self.assertEqual(expected_video, actual_video)
