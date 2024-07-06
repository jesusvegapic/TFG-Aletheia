from httpx import AsyncClient
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
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": GenericUUID.next_id().__str__(),
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

        response = await self.api_client.put(students_uri+f"/courses/{course_id}")

        self.assertEqual(response.status_code, 201)
