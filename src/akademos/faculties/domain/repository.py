from abc import ABC

from src.akademos.faculties.domain.entities import Faculty
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class FacultyRepository(GenericRepository[GenericUUID, Faculty], ABC):
    ...
