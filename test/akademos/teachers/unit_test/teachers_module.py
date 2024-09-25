from unittest import IsolatedAsyncioTestCase

from src.akademos.teachers.domain.repository import TeacherRepository
from test.shared.test_repository import TestRepository


class TestTeacherRepository(TeacherRepository, TestRepository):
    ...


class TestTeachersModule(IsolatedAsyncioTestCase):
    repository: TeacherRepository

    def setUp(self):
        self.repository = TestTeacherRepository()
