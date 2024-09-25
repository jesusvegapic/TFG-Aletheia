from unittest import IsolatedAsyncioTestCase

from src.akademos.courses.domain.repository import CourseRepository
from test.shared.test_repository import TestRepository


class TestCourseRepository(CourseRepository, TestRepository):
    ...


class TestCoursesModule(IsolatedAsyncioTestCase):
    repository: CourseRepository

    def setUp(self):
        self.repository = TestCourseRepository()
