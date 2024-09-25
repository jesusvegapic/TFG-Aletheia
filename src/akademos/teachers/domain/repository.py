from abc import ABC
from src.akademos.teachers.domain.entities import Teacher
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class TeacherRepository(GenericRepository[GenericUUID, Teacher], ABC):
    ...
