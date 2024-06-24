from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.akademos.courses.application.commands import CreateCourse
from src.akademos.courses.application.commands.create_course import create_course
from src.akademos.courses.domain.entities import Course
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.akademos.courses.unit_test.repository import TestCourseRepository


class TestHandlersShould(IsolatedAsyncioTestCase):
    def setUp(self):
        self.repository = TestCourseRepository()

    async def test_create_valid_course(self):
        command = CreateCourse(
            course_id=GenericUUID.next_id().hex,
            teacher_id=GenericUUID.next_id().hex,
            name="Kant vs Hegel",
            description="La panacea de la filosofia moderna",
            topics=["Historia", "Filosofía"]
        )

        publish = AsyncMock()

        self.repository.add = AsyncMock()

        await create_course(command, self.repository, publish)

        args, kwargs = self.repository.add.call_args

        self.assertTrue(len(args) == 1)

        actual_course = args[0]

        expected_course = Course(
            id=actual_course.id,
            owner=command.teacher_id,
            name=command.name,
            description=command.description,
            topics=command.topics
        )

        self.assertEqual(actual_course, expected_course)
