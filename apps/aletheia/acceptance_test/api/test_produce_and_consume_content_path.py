from httpx import AsyncClient
from apps.aletheia.acceptance_test.api.test_fastapi_server import TestFastapiServer
from apps.aletheia.api.routers import videos, teachers, iam, faculties, conferences
from apps.aletheia.api.routers.courses import router
from src.framework_ddd.core.domain.value_objects import GenericUUID

TEST_VIDEO_PATH = "../../../../test/akademos/videos/test_files/test_video.mp4"


class CoursesControllerShould(TestFastapiServer):

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.api.include_router(router)
        self.api.include_router(videos.router)
        self.api.include_router(teachers.router)
        self.api.include_router(iam.router)
        self.api.include_router(faculties.router)
        self.api.include_router(conferences.router)
        self.api_client = AsyncClient(app=self.api, base_url="http://test")

    async def pre_create_teacher(self, teacher_id: str, email: str, password: str):
        faculty_id = GenericUUID.next_id().hex
        first_degree_id = GenericUUID.next_id().hex
        second_degree_id = GenericUUID.next_id().hex
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
                    },
                    {
                        "id": second_degree_id,
                        "name": "Derecho"
                    }
                ]
            }
        )

        await self.api_client.put(
            f"/teachers/{teacher_id}",
            json={
                "name": "pepe",
                "firstname": "gonzalez",
                "second_name": "sanchez",
                "email": email,
                "password": password,
                "faculty": faculty_id,
                "degrees": [first_degree_id, second_degree_id],
                "position": "FULL_PROFESSOR"
            }
        )

        login_response = await self.api_client.post(
            "/auth/accesstoken",
            json={
                "email": email,
                "password": password
            }
        )

        token = login_response.json()["access_token"]

        self.api_client.headers["Authorization"] = f"Bearer {token}"

    async def test_put_valid_lectio_on_an_existing_course(self):
        teacher_id = GenericUUID.next_id().hex
        email = "teacher@aletheia.com"
        password = "test"
        await self.pre_create_teacher(teacher_id, email, password)

        course_id = GenericUUID.next_id().hex
        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": teacher_id,
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

        await self.api_client.patch(f"/courses/{course_id}/publish")

        await self.api_client.put(
            f"/courses/{course_id}/lectios/{lectio_id}",
            files=files,
            data=lectio_metadata
        )

        response = await self.api_client.get(f"/lectios/{lectio_id}")

        json_response_expected = {
            "lectio_id": lectio_id,
            "name": "El ego trascendental",
            "description": "Una mirada desde las coordenadas del materialismo filosofico",
            "video_url": f"/videos/{video_id}"
        }

        self.assertEqual(response.json(), json_response_expected)

        async with self.api_client.stream('GET', json_response_expected["video_url"]) as stream_resp:
            stream_resp.raise_for_status()
            content_disposition = stream_resp.headers.get("Content-Disposition")
            if content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
                self.assertEqual(filename, "test_video.mp4")
                file = b""
                async for chunk in stream_resp.aiter_bytes():
                    file += chunk
            else:
                self.fail()

    async def test_get_a_valid_course(self):
        teacher_id = GenericUUID.next_id().hex
        email = "teacher@aletheia.com"
        password = "test"
        await self.pre_create_teacher(teacher_id, email, password)

        course_id = GenericUUID.next_id().hex
        lectio_id = GenericUUID.next_id().hex

        await self.api_client.put(
            f"/courses/{course_id}",
            json={
                "teacher_id": teacher_id,
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

        response = await self.api_client.get(f"/courses/{course_id}")

        expected_response_json = {
            "id": course_id,
            "owner": teacher_id,
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
        teacher_id = GenericUUID.next_id().hex
        await self.pre_create_teacher(teacher_id, "teacher@aletheia.com", "test")
        for _ in range(30):
            id = GenericUUID.next_id().hex
            await self.api_client.put(
                f"/courses/{id}",
                json={
                    "teacher_id": teacher_id,
                    "name": "Kant vs Hegel",
                    "description": "La panacea de la historia de la filosofia",
                    "topics": ["Filosofía", "Historia"]
                }
            )

            await self.api_client.patch(f"/courses/{id}/publish")

        first_response = await self.api_client.get("/courses")
        second_response = await self.api_client.get("/courses?start=1&topics=Filosofía&topics=Historia")
        void_response = await self.api_client.get("/courses?start=1&topics=Linguistica")

        print(first_response.json())

        self.assertEqual(len(first_response.json()["courses"]), 15)
        self.assertEqual(len(second_response.json()["courses"]), 15)
        self.assertEqual(len(void_response.json()["courses"]), 0)

        for course in first_response.json()["courses"]:
            for other_couser in second_response.json()["courses"]:
                self.assertTrue(course != other_couser)

    async def test_create_valid_conference(self):
        email = "teacher@aletheia.com"
        password = "test"
        teacher_id = GenericUUID.next_id().hex
        await self.pre_create_teacher(teacher_id, email, password)

        video_id = GenericUUID.next_id().hex

        conference_metadata = {
            "name": "El ego trascendental",
            "description": "Una mirada desde las coordenadas del materialismo filosofico",
            "topics": ["Filosofía", "Biología"],
            "video_id": video_id
        }

        files = {"video": ("test_video.mp4", open(TEST_VIDEO_PATH, 'rb'), "video/mp4")}
        conference_id = GenericUUID.next_id().hex

        await self.api_client.put(
            f"/conferences/{conference_id}",
            files=files,
            data=conference_metadata
        )

        response = await self.api_client.get(f"/conferences/{conference_id}")

        response_expected = {
            "id": conference_id,
            "owner": teacher_id,
            "name": conference_metadata["name"],
            "description": conference_metadata["description"],
            "topics": conference_metadata["topics"],
            "video_url": f"/videos/{conference_metadata["video_id"]}"
        }

        self.assertEqual(response.json(), response_expected)

        async with self.api_client.stream('GET', response.json()["video_url"]) as stream_resp:
            stream_resp.raise_for_status()
            content_disposition = stream_resp.headers.get("Content-Disposition")
            if content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
                self.assertEqual(filename, "test_video.mp4")
                file = b""
                async for chunk in stream_resp.aiter_bytes():
                    file += chunk
            else:
                self.fail()
