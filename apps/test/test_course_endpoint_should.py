from unittest import IsolatedAsyncioTestCase
from fastapi import FastAPI
from httpx import AsyncClient
from apps.api.routers.courses import router
from apps.config.container import ApplicationContainer, Config
from src.shared.domain.value_objects import GenericUUID
from src.shared.infrastructure.database import Base

TEST_VIDEO_PATH = "./test_files/test_video.mp4"


class CreateCourseControllerShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = Config(
            APP_NAME="api_test",
            DATABASE_URL="sqlite+aiosqlite:///:memory:",
            DATABASE_ECHO=True,
            DEBUG=True,
            LOGGER_NAME="api_test"
        )
        container = ApplicationContainer(config=config)
        api = FastAPI(debug=config.DEBUG)
        api.include_router(router)
        api.container = container
        async with container.db_engine().connect() as bd:
            await bd.run_sync(Base.metadata.create_all)

        self.api_client = AsyncClient(app=api, base_url="http://test")

    async def test_post_valid_course(self):
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

    async def test_put_valid_lectio_on_an_existing_course(self):
        async with self.api_client as client:
            course_id = await client.post(
                "/courses/create_course",
                json={
                    "teacher_id": GenericUUID.next_id().__str__(),
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia"
                }
            )

            with open(TEST_VIDEO_PATH, "rb") as video:
                lectio_metadata = {
                    "name": "El ego trascendental",
                    "description": "Una mirada desde las coordenadas del materialismo filosofico"
                }

                multipart = {
                    "metadata": (None, lectio_metadata),
                    "video": ("El_ego_trascendental.mp4", video, "/video/mp4")
                }

                response = await client.put(f"/courses/{course_id}/lectio", files=multipart)
