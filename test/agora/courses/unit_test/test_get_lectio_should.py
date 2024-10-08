from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.agora.courses.application.queries.get_lectio import get_lectio
from src.agora.shared.application.queries import GetLectio, GetLectioResponse
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import LectioModel


class GetLectioShould(IsolatedAsyncioTestCase):

    async def test_return_valid_response(self):
        query = GetLectio(
            lectio_id=GenericUUID.next_id().hex
        )

        video_id = GenericUUID.next_id()

        session = AsyncMock()
        session.get = AsyncMock()
        session.get.return_value = LectioModel(
            id=query.lectio_id,
            course_id=GenericUUID.next_id(),
            name="contexto histórico",
            description="Análisis desde una perpectiva materialista",
            video_id=video_id
        )

        expected_response = GetLectioResponse(
            lectio_id=query.lectio_id,
            name="contexto histórico",
            description="Análisis desde una perpectiva materialista",
            video_id=video_id.hex
        )

        response = await get_lectio(query, session)

        self.assertEqual(response, expected_response)
