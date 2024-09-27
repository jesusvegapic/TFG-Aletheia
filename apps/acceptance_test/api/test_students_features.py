import os
from pathlib import Path

from httpx import AsyncClient
from apps.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.api.routers import courses, iam, faculties, notifications_subscriptions, students, teachers
from src.framework_ddd.core.domain.value_objects import GenericUUID

current_dir = Path(__file__).parent

TEST_VIDEO_PATH = os.path.join(current_dir, "../../../test/akademos/videos/test_files/test_video.mp4")


class StudentsControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(students.router)
        self.api.include_router(courses.router)
        self.api.include_router(faculties.router)
        self.api.include_router(teachers.router)
        self.api.include_router(iam.router)
        self.api.include_router(notifications_subscriptions.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def pre_create_student(self, student_id: str, email: str, password: str, teacher_id: str):
        faculty_id = GenericUUID.next_id().hex
        first_degree_id = GenericUUID.next_id().hex
        uri = f"/faculties/{faculty_id}"

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": self.admin_email,
                "password": self.admin_password
            }
        )

        token = login_response.json()["access_token"]
        self.api_client.headers["Authorization"] = f"Bearer {token}"

        await self.api_client.put(
            uri,
            json={
                "name": "Derecho",
                "degrees": [
                    {
                        "id": first_degree_id,
                        "name": "Ade"
                    }
                ]
            }
        )

        await self.api_client.put(
            f"/students/{student_id}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": email,
                "password": password,
                "faculty": faculty_id,
                "degree": first_degree_id,
            }
        )

        await self.api_client.put(
            f"/teachers/{teacher_id}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": "teacher@aletheia.com",
                "password": "teacher_passwd",
                "faculty": faculty_id,
                "degrees": [first_degree_id],
                "position": "FULL_PROFESSOR"
            }
        )

    async def test_put_enrolled_course_on_student(self):
        email = "student@aletheia.com"
        password = "tests"
        student_id = GenericUUID.next_id().hex
        teacher_id = GenericUUID.next_id().hex
        await self.pre_create_student(student_id, email, password, teacher_id)
        course_id = GenericUUID.next_id().hex
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": self.admin_id,
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
        lectio_id = GenericUUID.next_id().hex

        await self.api_client.put(
            f"/courses/{course_id}/lectios/{lectio_id}",
            files=files,
            data=lectio_metadata
        )

        await self.api_client.patch(f"/courses/{course_id}/publish")

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": email,
                "password": password
            }
        )

        token = login_response.json()["access_token"]
        self.api_client.headers["Authorization"] = f"Bearer {token}"

        students_uri = "/students"

        await self.api_client.put(students_uri + f"/enrolledCourses/{course_id}")

        await self.api_client.patch(
            students_uri + f"/enrolledCourses/{course_id}/lectios/{lectio_id}/stateProgress/start")

        response = await self.api_client.get(students_uri + "/enrolledCourses")

        expected_response = {
            "courses": [
                {
                    "id": course_id,
                    "name": "Kant vs Hegel",
                    "owner": self.admin_id
                }
            ]
        }

        self.assertEqual(response.json(), expected_response)

        response = await self.api_client.get(students_uri + f"/enrolledCourses/{course_id}/stateProgress")

        expected_response = {
            "lectios_progress": [
                {
                    "id": lectio_id,
                    "name": "El ego trascendental",
                    "progress": "STARTED"
                }
            ],
            "course_percent_progress": 0
        }

        self.assertEqual(response.json(), expected_response)

        await self.api_client.patch(
            students_uri + f"/enrolledCourses/{course_id}/lectios/{lectio_id}/stateProgress/finish"
        )

        response = await self.api_client.get(students_uri + f"/enrolledCourses/{course_id}/stateProgress")

        expected_response = {
            "lectios_progress": [
                {
                    "id": lectio_id,
                    "name": "El ego trascendental",
                    "progress": "FINISHED"
                }
            ],
            "course_percent_progress": 100
        }

        self.assertEqual(response.json(), expected_response)

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": self.admin_email,
                "password": self.admin_password
            }
        )

        token = login_response.json()["access_token"]
        self.api_client.headers["Authorization"] = f"Bearer {token}"

        response = await self.api_client.get(f"/teachers/courseStudentsProgress/{course_id}")

        expected_response = {
            "students_progress": [
                {
                    "id": student_id,
                    "name": "pepe",
                    "firstname": "gonzalez",
                    "second_name": "sanchez",
                    "progress": [
                        {
                            "id": lectio_id,
                            "name": "El ego trascendental",
                            "progress": "FINISHED"
                        }
                    ],
                    "course_percent_progress": 100
                }
            ]
        }

        self.assertEqual(expected_response, response.json())

    async def test_get_last_visited_lectio(self):
        email = "student@aletheia.com"
        password = "tests"
        student_id = GenericUUID.next_id().hex
        teacher_id = GenericUUID.next_id().hex
        await self.pre_create_student(student_id, email, password, teacher_id)
        course_id = GenericUUID.next_id().hex
        lectio_id = GenericUUID.next_id().hex
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": self.admin_id,
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

        await self.api_client.patch(f"/courses/{course_id}/publish")

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": email,
                "password": password
            }
        )

        token = login_response.json()["access_token"]
        self.api_client.headers["Authorization"] = f"Bearer {token}"

        students_uri = "/students"

        await self.api_client.put(students_uri + f"/enrolledCourses/{course_id}")

        await self.api_client.patch(students_uri + f"/enrolledCourses/{course_id}/lastVisitedLectio/{lectio_id}")

        response = await self.api_client.get(students_uri + f"/enrolledCourses/{course_id}/lastVisitedLectio")

        response_expected = {
            "lectio_id": lectio_id,
            "name": "El ego trascendental",
            "description": "Una mirada desde las coordenadas del materialismo filosofico",
            "video_id": video_id
        }

        print(response.content)

        self.assertEqual(response.json(), response_expected)

    async def test_put_teacher_courses_subscription(self):
        email = "student@aletheia.com"
        password = "tests"
        student_id = GenericUUID.next_id().hex
        teacher_id = GenericUUID.next_id().hex
        await self.pre_create_student(student_id, email, password, teacher_id)

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": email,
                "password": password
            }
        )

        token = login_response.json()["access_token"]
        self.api_client.headers["Authorization"] = f"Bearer {token}"

        response = await self.api_client.put(
            f"/notificationsSubscriptions/teacherCourses/{GenericUUID.next_id().hex}",
            json={
                "teacher_id": teacher_id,
                "topics": ["Filosofía", "Biología"]
            }
        )

        print(response.content)

        self.assertEqual(response.status_code, 200)
