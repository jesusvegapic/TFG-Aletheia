from unittest import IsolatedAsyncioTestCase
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from src.akademos.videos.domain.entities import Video
from src.akademos.videos.infrastructure.repository import AsyncMotorGridFsVideoRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.files import TestAsyncBinaryIOProtocol


class AsyncMotorGridFsVideoRepositoryShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/")
        self.bucket = AsyncIOMotorGridFSBucket(client.admin)
        self.session = await client.start_session()
        self.repository = AsyncMotorGridFsVideoRepository(self.bucket, self.session)

    async def asyncTearDown(self):
        await self.session.end_session()

    async def test_add_valid_video(self):
        video = Video(
            id=Video.next_id().hex,
            content=TestAsyncBinaryIOProtocol(),
            name="doraemon",
            type="video/mp4"
        )

        await self.repository.add(video)

        actual_video = await self.repository.get(GenericUUID(video.id))

        self.assertEqual(actual_video.model_dump(exclude={"content"}), video.model_dump(exclude={"content"}))
