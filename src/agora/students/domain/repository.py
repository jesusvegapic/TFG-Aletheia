from abc import ABC

from src.agora.students.domain.entities import Student
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class StudentRepository(GenericRepository[GenericUUID, Student], ABC):
    ...
