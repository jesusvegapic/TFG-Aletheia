from unittest import IsolatedAsyncioTestCase
import bson
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from src.agora.videos.application.queries.get_video import get_video, GetVideo
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.repository import GridFsPersistenceModel
from test.shared.files import TestAsyncBinaryIOProtocol


class GetVideoShould(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        client = AsyncIOMotorClient("mongodb://root:example@localhost:27017/")
        self.bucket = AsyncIOMotorGridFSBucket(client.admin)
        self.session = await client.start_session()

    async def test_get_valid_course(self):
        model_instance = GridFsPersistenceModel(
            file_id=GenericUUID.next_id(),
            filename="garfield.mp4",
            content=TestAsyncBinaryIOProtocol(),
            metadata={"content_type": "video/mp4"}
        )

        await self.bucket.upload_from_stream_with_id(
            bson.Binary.from_uuid(model_instance.file_id),
            model_instance.filename,
            model_instance.content.sync_mode(),
            metadata=model_instance.metadata,
            session=self.session
        )

        query = GetVideo(video_id=model_instance.file_id.hex)

        response = await get_video(query, self.session, self.bucket)

        expected_response = VideoDto(
            video_id=model_instance.file_id.hex,
            file=model_instance.content,
            filename=model_instance.filename,
            content_type=model_instance.metadata["content_type"]
        )

        response = response.model_dump()
        expected_response = expected_response.model_dump()
        response["file"] = await response["file"].read()
        expected_response["file"] = await expected_response["file"].read()

        self.assertEqual(response, expected_response)
