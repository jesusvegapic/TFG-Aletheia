from random import randint
from typing import Optional, List
from unittest import IsolatedAsyncioTestCase

from src.agora.students.domain.entities import Student, StudentFaculty, StudentCourse, StudentLectio
from src.agora.students.domain.repository import StudentRepository
from src.framework_ddd.core.domain.repository import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.repository import User
from src.framework_ddd.iam.domain.value_objects import Email
from test.shared.custom_random import random_str


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


class StudentMother:
    @classmethod
    def random(
            cls,
            id: Optional[str] = None,
            name: Optional[str] = None,
            firstname: Optional[str] = None,
            second_name: Optional[str] = None,
            email: Optional[str] = None,
            password_hash: Optional[bytes] = None,
            faculty: Optional[StudentFaculty] = None,
            degree: Optional[str] = None,
            courses_in_progress: Optional[List[StudentCourse]] = None,
    ):
        degree_id = GenericUUID.next_id()
        lectio_id = GenericUUID.next_id()
        return Student(
            id=id or Student.next_id().hex,
            name=name or random_str(randint(1, 20)),
            firstname=firstname or random_str(randint(1, 20)),
            second_name=second_name or random_str(randint(1, 20)),
            email=email or random_str(randint(1, 30))+"@gmail.com",
            password_hash=password_hash or bytes(random_str(randint(1, 30)), 'utf-8'),
            faculty= faculty or StudentFaculty(
                id=StudentFaculty.next_id().hex,
                degrees=[degree_id]
            ),
            degree=degree or degree_id.hex,
            courses_in_progress=courses_in_progress or [
                StudentCourse(
                    id=StudentCourse.next_id().hex,
                    lectios=[
                        StudentLectio(
                            id=lectio_id.hex
                        )
                    ],
                    last_visited_lectio=lectio_id
                )
            ]
        )
