from typing import Optional
from unittest import IsolatedAsyncioTestCase

from src.agora.students.domain.entities import Student
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.repository import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.repository import User
from src.framework_ddd.iam.domain.value_objects import Email


class TestStudentRepository(StudentRepository):

    def get_by_email(self, email: Email) -> User | None:
        pass

    def get_by_access_token(self, access_token: str) -> User | None:
        pass

    async def add(self, entity: Student):
        pass

    async def get(self, id: GenericUUID) -> Optional[Entity]:
        pass

    async def remove(self, entity: Student):
        pass

    async def remove_by_id(self, id: GenericUUID):
        pass


class TestStudentsModule(IsolatedAsyncioTestCase):
    repository: StudentRepository

    def setUp(self):
        self.repository = TestStudentRepository()
