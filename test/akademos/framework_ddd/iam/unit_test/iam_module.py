from unittest import IsolatedAsyncioTestCase

from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.domain.repository import UserRepository, User
from src.framework_ddd.mailing.domain.value_objects import Email
from test.shared.test_repository import TestRepository


class TestUserRepository(UserRepository, TestRepository):
    def get_by_email(self, email: Email) -> User | None:
        pass

    ...


class TestIamModule(IsolatedAsyncioTestCase):
    repository: UserRepository
    iam_service: IamService

    def setUp(self):
        self.repository = TestUserRepository()
        self.iam_service = IamService(
            self.repository,
            secret_key="12312kmsdfka2"
        )
