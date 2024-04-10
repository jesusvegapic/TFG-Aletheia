from unittest import IsolatedAsyncioTestCase

from test.courses.unit_test.repository import TestCourseRepository


class TestCoursesModule(IsolatedAsyncioTestCase):

    def setUp(self):
        self.repository = TestCourseRepository()
