from unittest import IsolatedAsyncioTestCase

from fastapi import FastAPI
from httpx import AsyncClient
from apps.admin.api import router
from apps.admin.container import ApplicationContainer, Config
from src.shared.domain.ddd.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.custom_loggin import LoggerFactory
from src.framework_ddd.core.infrastructure.sql_alchemy.sql_alchemy_database import Base

TEST_VIDEO_PATH = "../../../src/admin/videos/test_files/test_video.mp4"


class CreateCourseControllerShould(IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        config = Config(
            APP_NAME="api_test",
            DATABASE_URL="sqlite+aiosqlite:///:memory:",
            BUCKET_URL="motor_mongodb://root:example@localhost:27017/",
            DATABASE_ECHO=True,
            DEBUG=True,
            LOGGER_NAME="aletheia acceptance_test"
        )
        LoggerFactory.configure(logger_name="api_test")
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

            self.assertTrue(response.status_code == 201)

    async def test_put_valid_lectio_on_an_existing_course(self):
        async with self.api_client as client:
            course_id = GenericUUID.next_id().hex
            response = await client.put(
                f"/courses/{course_id}",
                json={
                    "teacher_id": GenericUUID.next_id().__str__(),
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia"
                }
            )

            self.assertEqual(response.status_code, 201)

            lectio_metadata = {
                "name": "El ego trascendental",
                "description": "Una mirada desde las coordenadas del materialismo filosofico"
            }

            files = {"video": ("test_video.mp4", open(TEST_VIDEO_PATH, 'rb'), "/video/mp4")}
            lectio_id = GenericUUID.next_id().hex
            response = await client.put(
                f"/courses/{course_id}/lectio/{lectio_id}",
                files=files,
                data=lectio_metadata
            )

            self.assertEqual(response.status_code, 201)
