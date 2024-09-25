from unittest import IsolatedAsyncioTestCase
from src.akademos.conferences.domain.repository import ConferenceRepository
from test.shared.test_repository import TestRepository


class TestConferenceRepository(ConferenceRepository, TestRepository):
    ...


class TestConferencesModule(IsolatedAsyncioTestCase):
    repository: ConferenceRepository

    def setUp(self):
        self.repository = TestConferenceRepository()
