from typing import Set, Optional

from src.akademos.faculties.domain.value_objects import FacultyName, DegreeName  # type: ignore
from src.framework_ddd.core.domain.entities import Entity


class Faculty(Entity):
    __name: FacultyName
    __degrees: Set['Degree']

    def __init__(self, id: str, name: str, degrees: Optional[Set['Degree']] = None):
        super().__init__(id)
        self.__name = FacultyName(name)
        self.__degrees = degrees if degrees else set()

    @property
    def name(self):
        return self.__name

    @property
    def degrees(self):
        return self.__degrees


class Degree(Entity):
    __name: DegreeName

    def __init__(self, id: str, name: str):
        super().__init__(id)
        self.__name = DegreeName(name)
