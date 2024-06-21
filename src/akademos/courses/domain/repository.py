from abc import ABC

from src.Academia.courses.domain.entities import Course
from src.shared.domain.ddd.repository import GenericRepository
from src.shared.domain.ddd.value_objects import GenericUUID


class CourseRepository(GenericRepository[GenericUUID, Course], ABC):
    pass
