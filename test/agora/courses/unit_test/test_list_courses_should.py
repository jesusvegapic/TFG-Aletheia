from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.courses.application.queries import list_courses
from src.agora.courses.application.queries.list_courses import ListCourses, ListCoursesResponse, ListedCourseDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import CourseModel


class ListCoursesShould(IsolatedAsyncioTestCase):

    async def test_list_courses_correctly(self):
        query = ListCourses(page_number=0, courses_by_page=15, topics=["Filosofía"])
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
                    topics="Filosofía;Linguistica",
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

        await self.assert_query(query, response_expected)

        query = ListCourses(page_number=0, courses_by_page=15, topics=[])
        await self.assert_query(query, response_expected)

        query = ListCourses(page_number=0, courses_by_page=15, topics=["Derecho"])
        response_expected = ListCoursesResponse(
            courses=[]
        )
        await self.assert_query(query, response_expected)

    async def assert_query(self, query: ListCourses, response_expected: ListCoursesResponse):
        actual_response = await list_courses.list_courses(query, AsyncMock())
        self.assertEqual(actual_response, response_expected)
