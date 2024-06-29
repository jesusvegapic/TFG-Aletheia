from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.courses.application.queries import list_courses
from src.agora.courses.application.queries.list_courses import ListCourses, ListCoursesResponse, ListedCourseDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import CourseModel, LectioModel


class ListCoursesShould(IsolatedAsyncioTestCase):

    async def test_list_courses_correctly(self):
        query = ListCourses(actual_page=1)
        course_id = GenericUUID.next_id().hex
        owner_id = GenericUUID.next_id().hex

        async def get_paged_courses(session: AsyncSession, start_index: int, page_size: int):
            return [
                CourseModel(
                    id=course_id,
                    owner=owner_id,
                    name="kant vs hegel",
                    description="la panacea de la filosofia",
                    state="CREATED",
                    lectios=[]
                )
            ]

        list_courses.get_paged_courses = get_paged_courses

        response_expected = ListCoursesResponse(
            courses=[
                ListedCourseDto(
                    id=course_id,
                    owner=owner_id,
                    name="kant vs hegel"
                )
            ]
        )

        actual_response = await list_courses.list_courses(query, AsyncMock())

        self.assertEqual(actual_response, response_expected)
