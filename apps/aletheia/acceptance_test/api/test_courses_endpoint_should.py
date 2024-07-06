from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers.courses import router
from src.framework_ddd.core.domain.value_objects import GenericUUID

TEST_VIDEO_PATH = "../../../../test/akademos/videos/test_files/test_video.mp4"


class CoursesControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def test_put_valid_lectio_on_an_existing_course(self):
        async with self.api_client as client:
            course_id = GenericUUID.next_id().hex
            await client.put(
                f"/courses/{course_id}",
                json={
                    "teacher_id": GenericUUID.next_id().__str__(),
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia",
                    "topics": ["Filosofía"]
                }
            )

            lectio_metadata = {
                "name": "El ego trascendental",
                "description": "Una mirada desde las coordenadas del materialismo filosofico"
            }
            files = {"video": ("test_video.mp4", open(TEST_VIDEO_PATH, 'rb'), "video/mp4")}
            lectio_id = GenericUUID.next_id().hex

            await client.put(
                f"/courses/{course_id}/lectio/{lectio_id}",
                files=files,
                data=lectio_metadata
            )

            response = await client.get(f"/lectios/{lectio_id}")

            json_response_expected = {
                "lectio_id": lectio_id,
                "name": "El ego trascendental",
                "description": "Una mirada desde las coordenadas del materialismo filosofico",
                "video_url": f"/video/{lectio_id}"
            }

            self.assertEqual(response.json(), json_response_expected)

    async def test_get_a_valid_course(self):
        async with self.api_client as client:
            course_id = GenericUUID.next_id().hex
            owner_id = GenericUUID.next_id().hex
            lectio_id = GenericUUID.next_id().hex
            await client.put(
                f"/courses/{course_id}",
                json={
                    "teacher_id": owner_id,
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia",
                    "topics": ["Filosofía"]
                }
            )

            lectio_metadata = {
                "name": "El ego trascendental",
                "description": "Una mirada desde las coordenadas del materialismo filosofico"
            }
            files = {"video": ("test_video.mp4", open(TEST_VIDEO_PATH, 'rb'), "/video/mp4")}

            await client.put(
                f"/courses/{course_id}/lectio/{lectio_id}",
                files=files,
                data=lectio_metadata
            )

            response = await client.get(f"/courses/{course_id}")

            expected_response_json = {
                "id": course_id,
                "owner": owner_id,
                "name": "Kant vs Hegel",
                "description": "La panacea de la historia de la filosofia",
                "topics": ["Filosofía"],
                "lectios": [
                    {
                        "id": lectio_id,
                        "name": "El ego trascendental"
                    }
                ]
            }

            if response.status_code != 200:
                print(response.json())

            self.assertEqual(response.status_code, 200)

            self.assertEqual(response.json(), expected_response_json)

    async def test_list_courses_correctly(self):
        async with self.api_client as client:
            for _ in range(30):
                id = GenericUUID.next_id().hex
                await client.put(
                    f"/courses/{id}",
                    json={
                        "teacher_id": GenericUUID.next_id().hex,
                        "name": "Kant vs Hegel",
                        "description": "La panacea de la historia de la filosofia",
                        "topics": ["Filosofía"]
                    }
                )

            first_response = await client.get("/courses")
            second_response = await client.get("/courses?start=1")

            print(first_response.json())

            print(second_response.json())

            self.assertEqual(len(first_response.json()["courses"]), 15)
            self.assertEqual(len(second_response.json()["courses"]), 15)

            for course in first_response.json()["courses"]:
                for other_couser in second_response.json()["courses"]:
                    self.assertTrue(course != other_couser)
