from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers import students, courses
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StudentsControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(students.router)
        self.api.include_router(courses.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def test_put_student(self):
        response = await self.api_client.put(
            f"/students/{GenericUUID.next_id().hex}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "pepe@gmail.com",
                "password": "fd23sdf23",
                "faculty": GenericUUID.next_id().hex,
                "degree": GenericUUID.next_id().hex
            }
        )

        self.assertEqual(response.status_code, 201)
