from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers import students, courses
from apps.aletheia.api.routers.students import router


class StudentsControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(students.router)
        self.api.include_router(courses.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")


    async def test_enrolled_a_valid_course(self):
        ...
