from abc import ABC

from src.platform.students.domain.entities import Student
from src.shared.domain.iam.repository import UserRepository


class StudentRepository(UserRepository, ABC):
    def get_by_email(self, email: Email) -> Student | None:
        ...

    def get_by_access_token(self, access_token: str) -> Student | None:
        ...
