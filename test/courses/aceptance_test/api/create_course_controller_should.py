from unittest import IsolatedAsyncioTestCase
from fastapi import FastAPI
from httpx import AsyncClient
from apps.api.config.api_config import ApiConfig
from apps.api.routers.courses import router
from apps.config.container import ApplicationContainer
from src.shared.domain.value_objects import GenericUUID
from src.shared.infrastructure.database import Base


class CreateCourseControllerShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = ApiConfig(DATABASE_URL="sqlite+aiosqlite:///:memory:", DATABASE_ECHO=True, DEBUG=True)
        container = ApplicationContainer(config=config)
        api = FastAPI(debug=config.DEBUG)
        api.include_router(router)
        api.container = container
        async with container.db_engine().connect() as bd:
            await bd.run_sync(Base.metadata.create_all)

        self.api_client = AsyncClient(app=api, base_url="http://test")

    async def test_execute_create_course_command(self):
        async with self.api_client as client:
            response = await client.post(
                "/courses/create_course",
                json={
                    "teacher_id": GenericUUID.next_id().__str__(),
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia"
                }
            )

            print(response)

            self.assertTrue(response.status_code == 201)
