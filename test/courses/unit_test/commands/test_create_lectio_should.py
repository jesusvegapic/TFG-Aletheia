import tempfile
from unittest.mock import AsyncMock
from src.Academia.courses.domain.entities import Course
from src.Academia.courses.domain.value_objects import CourseName, CourseDescription
from src.shared.domain.ddd.value_objects import GenericUUID
from test.courses.unit_test.courses_module import TestCoursesModule


class CreateLectioShould(TestCoursesModule):

    def setUp(self):
        super().setUp()

    def test_create_valid_lectio_in_an_existing_course(self):

        publish_mock = AsyncMock()

        with tempfile.NamedTemporaryFile("wb") as tmp_file:
            tmp_file.write(b"prueba")
            filename = tmp_file.name

            with open(filename, "rb") as video:
                course_id = Course.next_id().hex
                lectio_id = Lectio.next_id().hex
                command = CreateLectio(
                    course_id=course_id,
                    lectio_id=lectio_id,
                    name="El ego trascendental",
                    description="Una mirada desde las coordenadas del materialismo filosofico",
                    video=video,
                    video_name="garfield.mp4",
                    video_type="/video/mp4"
                )

            get_mock = AsyncMock()

            get_mock.return_value = Course(
                id=Course.next_id(),
                owner=GenericUUID.next_id(),
                name=CourseName("Kant vs Hegel"),
                description=CourseDescription("La panacea de la filosofia moderna")
            )

            self.repository.get = get_mock
            self.repository.add = AsyncMock()

            result = await create_lectio(command, self.repository)

            expected_lectio = Lectio(
                lectio_id,
                LectioName("El ego trascendental"),
                LectioDescription("Una mirada desde las coordenadas del materialismo filosofico")
            )

            expected_command = CreateVideo(
                id=lectio_id,
                video=video,
                video_name="garfield.mp4",
                video_type="/video/mp4"
            )

            args, kwargs = publish_mock.call_args

            actual_command = args[0]

            self.assertEqual(expected_command, actual_command)

            args, kwargs = self.repository.add

            actual_lectio = args[0]

            self.assertEqual(expected_lectio, actual_lectio)
