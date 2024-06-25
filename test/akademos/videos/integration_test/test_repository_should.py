import tempfile
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from fastapi import UploadFile
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
        video = Video(
            id=Video.next_id().hex,
            content=content,
            name="doraemon",
            type="video/mp4"
        )

        await self.repository.add(video)
        await self.session.commit_transaction()

        actual_video = await self.repository.get(GenericUUID(video.id))

        self.assertEqual(actual_video, video)
