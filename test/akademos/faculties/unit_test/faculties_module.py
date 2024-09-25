from unittest import IsolatedAsyncioTestCase

from src.akademos.faculties.domain.repository import FacultyRepository
from test.shared.test_repository import TestRepository


class TestFacultyRepository(FacultyRepository, TestRepository):
    ...


class TestFacultiesModule(IsolatedAsyncioTestCase):
    repository: FacultyRepository

    def setUp(self):
        self.repository = TestFacultyRepository()
