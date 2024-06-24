import tempfile
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock

from src.akademos.shared.application.dtos import VideoDto
from src.akademos.shared.application.events import LectioAdded
from src.akademos.videos.application.events.create_video_on_lectio_added_to_course import \
    create_video_on_lectio_added_to_course
from src.akademos.videos.domain.entities import Video
from src.framework_ddd.core.domain.value_objects import GenericUUID


class VideoIsWaitingForDownloadShould(IsolatedAsyncioTestCase):

    def setUp(self):
        self.repository = MagicMock()

    async def test_create_a_valid_video_on_lectio_added_to_course(self):
        video = tempfile.SpooledTemporaryFile()
        lectio_id = Video.next_id().hex
        event = LectioAdded(
            entity_id=GenericUUID.next_id().hex,
            lectio_id=lectio_id,
            name="kant vs hegel",
            description="la panacea de la filosofia",
            video=VideoDto(
                file=video,
                filename="garfield",
                content_type="/video/mp4"
            )
        )

        add_mock = AsyncMock()
        publish = AsyncMock()
        self.repository.add = add_mock

        await create_video_on_lectio_added_to_course(event, self.repository, publish)

        args, kwargs = self.repository.add.call_args
        actual_video = args[0]

        expected_video = Video(
            id=lectio_id,
            content=video,
            name="garfield",
            type="/video/mp4"
        )

        self.assertEqual(expected_video, actual_video)
