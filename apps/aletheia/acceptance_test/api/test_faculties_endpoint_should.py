from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers.faculties import router
from src.framework_ddd.core.domain.value_objects import GenericUUID


class FacultiesEndpointShould(TestFastapiServer):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def test_put_valid_faculty(self):
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

        response = await self.api_client.get(uri)

        json_response_expected = {
            "id": faculty_id,
            "name": "Derecho",
            "degrees": [
                first_degree_id,
                second_degree_id
            ]
        }

        self.assertEqual(response.json(), json_response_expected)
