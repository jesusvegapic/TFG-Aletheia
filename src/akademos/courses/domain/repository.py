from abc import ABC

from src.akademos.courses.domain.entities import Course
from src.framework_ddd.core.domain.repository import GenericRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID


class CourseRepository(GenericRepository[GenericUUID, Course], ABC):
    pass
