from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers import teachers, faculties
from src.framework_ddd.core.domain.value_objects import GenericUUID


class TeachersControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(teachers.router)
        self.api.include_router(faculties.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def test_put_teacher(self):
        faculty_id = GenericUUID.next_id().hex
        first_degree_id = GenericUUID.next_id().hex
        second_degree_id = GenericUUID.next_id().hex
        uri = f"/faculties/{faculty_id}"
        await self.api_client.put(
            uri,
            json={
                "name": "Derecho",
                "degrees": [
                    {
                        "id": first_degree_id,
                        "name": "Ade"
                    },
                    {
                        "id": second_degree_id,
                        "name": "Derecho"
                    }
                ]
            }
        )

        response = await self.api_client.put(
            f"/teachers/{GenericUUID.next_id().hex}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "pepe@gmail.com",
                "password": "fd23sdf23",
                "faculty": faculty_id,
                "degrees": [first_degree_id, second_degree_id],
                "position": "FULL_PROFESSOR"
            }
        )

        print(response.json())

        self.assertEqual(response.status_code, 201)
