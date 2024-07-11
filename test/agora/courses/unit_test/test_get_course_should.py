from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.agora.courses.application.queries.get_course import get_course
from src.agora.shared.application.queries import GetCourse, GetCourseResponse, LectioDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel


class GetCourseShould(IsolatedAsyncioTestCase):

    async def test_get_a_valid_course(self):
        course_id = GenericUUID.next_id().hex
        owner_id = GenericUUID.next_id().hex
        lectio_id = GenericUUID.next_id().hex

        query = GetCourse(
            course_id=course_id,
            user_id=owner_id
        )

        session = AsyncMock()
        session.get = AsyncMock()

        course_model = CourseModel(
            id=course_id,
            owner=owner_id,
            name="kant vs hegel",
            description="la panacea de la filosofia",
            state="CREATED",
            topics="Filosofía;Linguistica",
            lectios=[]
        )

        session.get.return_value = course_model

        course_model.lectios.append(
            LectioModel(
                id=lectio_id,
                course_id=course_id,
                name="contexto histórico",
                description="Análisis desde una perpectiva materialista"
            )
        )

        response_expected = GetCourseResponse(
            id=course_id,
            name="kant vs hegel",
            owner=owner_id,
            description="la panacea de la filosofia",
            topics=["Filosofía", "Linguistica"],
            lectios=[
                LectioDto(
                    id=lectio_id,
                    name="contexto histórico"
                )
            ]
        )

        actual_response = await get_course(query, session)

        self.assertEqual(actual_response, response_expected)
