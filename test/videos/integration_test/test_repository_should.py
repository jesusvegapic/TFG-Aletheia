import tempfile
from unittest import IsolatedAsyncioTestCase
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from src.videos.domain.entities import Video
from src.admin.videos.domain.value_objects import VideoName, VideoType
from src.videos.infrastructure.repository import AsyncMotorGridFsVideoRepository


class AsyncMotorGridFsVideoRepositoryShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        client = AsyncIOMotorClient("motor_mongodb://root:example@localhost:27017/")
        self.bucket = AsyncIOMotorGridFSBucket(client.admin)
        self.session = await client.start_session()
        self.repository = AsyncMotorGridFsVideoRepository(self.bucket, self.session)

    async def asyncTearDown(self):
        await self.session.end_session()

    async def test_add_valid_video(self):
        with tempfile.SpooledTemporaryFile() as content:
            video = Video(
                id=Video.next_id(),
                content=content,
                name=VideoName("doraemon"),
                type=VideoType("video/mp4")
            )

            await self.repository.add(video)
