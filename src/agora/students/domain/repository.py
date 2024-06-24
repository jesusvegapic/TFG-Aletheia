from abc import ABC

from src.agora.students.domain.entities import Student
from src.framework_ddd.iam.domain.repository import UserRepository


class StudentRepository(UserRepository[Student], ABC):
    ...
