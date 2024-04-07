from abc import ABC

from src.courses.domain.entities import Course
from src.shared.domain.repositories import GenericRepository
from src.shared.domain.value_objects import GenericUUID


class CourseRepository(GenericRepository[GenericUUID, Course], ABC):
    pass
