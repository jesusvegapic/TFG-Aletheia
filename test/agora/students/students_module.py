from random import randint
from typing import Optional
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
    def full_fields_random(cls):
        degree_id = GenericUUID.next_id()
        return Student(
            id=Student.next_id().hex,
            name=random_str(randint(1, 30)),
            firstname=random_str(randint(1, 30)),
            second_name=random_str(randint(1, 30)),
            email=random_str(randint(1, 30))+"@gmail.com",
            password_hash=bytes(random_str(randint(1, 30)), 'utf-8'),
            faculty=StudentFaculty(
                id=StudentFaculty.next_id().hex,
                degrees=[degree_id]
            ),
            degree=degree_id.hex,
            courses_in_progress=[
                StudentCourse(
                    id=StudentCourse.next_id().hex,
                    lectios=[
                        StudentLectio(
                            id=StudentLectio.next_id().hex
                        )
                    ]
                )
            ],
            last_visited_lectio=GenericUUID.next_id().hex

        )
