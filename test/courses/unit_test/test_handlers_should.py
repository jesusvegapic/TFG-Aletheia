from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from src.courses.application.commands import CreateCourse
from src.courses.application.commands.create_course import create_course
from src.courses.domain.entities import Course
from src.courses.domain.value_objects import CourseName, CourseDescription
from src.shared.domain.value_objects import GenericUUID
from test.courses.unit_test.test_repository import TestCourseRepository


class TestHandlersShould(IsolatedAsyncioTestCase):
    def setUp(self):
        self.repository = TestCourseRepository()

    async def test_create_valid_course(self):
        command = CreateCourse(
            teacher_id=GenericUUID.next_id().__str__(),
            name="Kant vs Hegel",
            description="La panacea de la filosofia moderna"
        )

        self.repository.add = AsyncMock()

        await create_course(command, self.repository)

        args, kwargs = self.repository.add.call_args

        self.assertTrue(len(args) == 1)

        actual_course = args[0]

        expected_course = Course(
            id=actual_course.id,
            owner=GenericUUID(command.teacher_id),
            name=CourseName(command.name),
            description=CourseDescription(command.description)
        )

        self.assertEqual(actual_course, expected_course)
