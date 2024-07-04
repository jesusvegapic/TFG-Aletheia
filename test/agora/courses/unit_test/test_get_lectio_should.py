from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.agora.courses.application.queries.get_lectio import get_lectio
from src.agora.shared.application.queries import GetLectio, GetLectioResponse
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import LectioModel
from test.shared.files import TestBinaryIOProtocol


class GetLectioShould(IsolatedAsyncioTestCase):

    async def test_return_valid_response(self):
        query = GetLectio(
            lectio_id=GenericUUID.next_id().hex
        )

        session = AsyncMock()
        session.get = AsyncMock()
        session.get.return_value = LectioModel(
            id=query.lectio_id,
            course_id=GenericUUID.next_id(),
            name="contexto histórico",
            description="Análisis desde una perpectiva materialista"
        )

        publish = AsyncMock()

        video = VideoDto(
            file=TestBinaryIOProtocol(),
            filename="los cuatro astros",
            content_type="video/mp4"
        )

        publish.return_value = video

        expected_response = GetLectioResponse(
            lectio_id=query.lectio_id,
            name="contexto histórico",
            description="Análisis desde una perpectiva materialista",
            video_content=video.file,
            video_name=video.filename,
            video_type=video.content_type
        )

        response = await get_lectio(query, session, publish)

        self.assertEqual(response, expected_response)
