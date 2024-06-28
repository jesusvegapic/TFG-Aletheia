from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
import bson
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from src.akademos.videos.domain.entities import Video
from src.akademos.videos.infrastructure.repository import AsyncMotorGridFsVideoRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class AsyncMotorGridFsVideoRepositoryShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/")
        self.bucket = AsyncIOMotorGridFSBucket(client.admin)
        self.session = await client.start_session()
        self.repository = AsyncMotorGridFsVideoRepository(self.bucket, self.session)

    async def asyncTearDown(self):
        await self.session.end_session()

    async def test_add_valid_video(self):
        content = MagicMock()
        content.read = MagicMock()
        content.read.return_value = b"papapapap"
        video = Video(
            id=Video.next_id().hex,
            content=content,
            name="doraemon",
            type="video/mp4"
        )

        await self.repository.add(video)

        grid_out = await self.bucket.open_download_stream(bson.Binary.from_uuid(GenericUUID(video.id)))
        self.assertEqual(grid_out.filename, video.name)
        self.assertTrue("content_type" in grid_out.metadata.keys())
        self.assertTrue(grid_out.metadata["content_type"], video.type)
