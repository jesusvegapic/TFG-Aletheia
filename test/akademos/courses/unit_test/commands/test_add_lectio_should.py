from unittest.mock import AsyncMock
from src.akademos.courses.application.commands import AddLectio
from src.akademos.courses.application.commands.add_lectio import add_lectio
from src.akademos.courses.domain.entities import Course, Lectio
from src.akademos.shared.application.dtos import VideoDto
from src.akademos.shared.application.events import LectioAdded
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.akademos.courses.unit_test.courses_module import TestCoursesModule
from test.shared.files import TestBinaryIOProtocol


class CreateLectioShould(TestCoursesModule):

    def setUp(self):
        super().setUp()

    async def test_create_valid_lectio_in_an_existing_course(self):
        publish_mock = AsyncMock()
        course_id = Course.next_id().hex
        lectio_id = Lectio.next_id().hex
        file = TestBinaryIOProtocol()
        command = AddLectio(
            course_id=course_id,
            lectio_id=lectio_id,
            name="El ego trascendental",
            description="Una mirada desde las coordenadas del materialismo filosofico",
            video=VideoDto(file=file, filename="garfield.mp4", content_type="/video/mp4")
        )

        get_mock = AsyncMock()

        expected_lectio = Lectio(
            id=lectio_id,
            name="El ego trascendental",
            description="Una mirada desde las coordenadas del materialismo filosofico"
        )

        course_id = Course.next_id().hex
        owner_id = GenericUUID.next_id().hex

        get_mock.return_value = Course(
            id=course_id,
            owner=owner_id,
            name="Kant vs Hegel",
            description="La panacea de la filosofia moderna",
            topics=["Filosofía"]
        )

        expected_course = Course(
            id=course_id,
            owner=owner_id,
            name="Kant vs Hegel",
            description="La panacea de la filosofia moderna",
            lectios=[expected_lectio],
            topics=["Filosofía"]
        )

        self.repository.get = get_mock
        self.repository.add = AsyncMock()

        await add_lectio(command, self.repository, publish_mock)

        expected_event = LectioAdded(
            entity_id=course_id,
            lectio_id=lectio_id,
            name="El ego trascendental",
            description="Una mirada desde las coordenadas del materialismo filosofico",
            video=VideoDto(file=file, filename="garfield.mp4", content_type="/video/mp4")
        )

        args, kwargs = publish_mock.call_args

        actual_event = args[0][0]

        expected_event = expected_event.model_dump(exclude={"id"})
        expected_event["video"].pop("file")
        actual_event = actual_event.model_dump(exclude={"id"})
        actual_event["video"].pop("file")

        self.assertEqual(expected_event, actual_event)

        args, kwargs = self.repository.add.call_args

        actual_course = args[0]

        self.assertEqual(expected_course, actual_course)
