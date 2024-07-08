from httpx import AsyncClient

from apps.aletheia.acceptance_test.api.test_courses_endpoint_should import TEST_VIDEO_PATH
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers import students, courses, faculties
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StudentsControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(students.router)
        self.api.include_router(courses.router)
        self.api.include_router(faculties.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def test_put_student(self):
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
            f"/students/{GenericUUID.next_id().hex}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "pepe@gmail.com",
                "password": "fd23sdf23",
                "faculty": faculty_id,
                "degree": first_degree_id
            }
        )

        self.assertEqual(response.status_code, 201)

    async def test_put_enrolled_course_on_student(self):
        course_id = GenericUUID.next_id().hex
        owner = GenericUUID.next_id().hex
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": owner,
                "name": "Kant vs Hegel",
                "description": "La panacea de la historia de la filosofia",
                "topics": ["Filosofía"]
            }
        )
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

        students_uri = f"/students/{GenericUUID.next_id().hex}"

        await self.api_client.put(
            students_uri,
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "pepe@gmail.com",
                "password": "fd23sdf23",
                "faculty": faculty_id,
                "degree": first_degree_id
            }
        )

        await self.api_client.put(students_uri + f"/courses/{course_id}")

        response = await self.api_client.get(students_uri + "/courses")

        expected_response = {
            "courses": [
                {
                    "id": course_id,
                    "name": "Kant vs Hegel",
                    "owner": owner
                }
            ]
        }

        self.assertEqual(response.json(), expected_response)

    async def test_get_last_visited_lectio(self):
        course_id = GenericUUID.next_id().hex
        lectio_id = GenericUUID.next_id().hex
        owner = GenericUUID.next_id().hex
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": owner,
                "name": "Kant vs Hegel",
                "description": "La panacea de la historia de la filosofia",
                "topics": ["Filosofía"]
            }
        )

        video_id = GenericUUID.next_id().hex

        lectio_metadata = {
            "name": "El ego trascendental",
            "description": "Una mirada desde las coordenadas del materialismo filosofico",
            "video_id": video_id
        }
        files = {"video": ("test_video.mp4", open(TEST_VIDEO_PATH, 'rb'), "video/mp4")}

        await self.api_client.put(
            f"/courses/{course_id}/lectios/{lectio_id}",
            files=files,
            data=lectio_metadata
        )

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

        students_uri = f"/students/{GenericUUID.next_id().hex}"

        await self.api_client.put(
            students_uri,
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "pepe@gmail.com",
                "password": "fd23sdf23",
                "faculty": faculty_id,
                "degree": first_degree_id
            }
        )

        await self.api_client.put(students_uri + f"/courses/{course_id}")

        await self.api_client.put(students_uri + f"/courses/{course_id}/lectios/{lectio_id}")

        response = await self.api_client.get(students_uri + f"/courses/{course_id}/lectios")

        response_expected = {
            "lectio_id": lectio_id,
            "name": "El ego trascendental",
            "description": "Una mirada desde las coordenadas del materialismo filosofico",
            "video_id": video_id
        }

        print(response.content)

        self.assertEqual(response.json(), response_expected)
