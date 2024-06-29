from typing import Set, Optional, List

from src.akademos.faculties.domain.events import FacultyCreated  # type: ignore
from src.akademos.faculties.domain.value_objects import FacultyName, DegreeName  # type: ignore
from src.framework_ddd.core.domain.entities import Entity, AggregateRoot


class Faculty(AggregateRoot):
    __name: FacultyName
    __degrees: List['Degree']

    def __init__(self, id: str, name: str, degrees: Optional[List['Degree']] = None):
        super().__init__(id)
        self.__name = FacultyName(name)
        self.__degrees = degrees if degrees else []

    @classmethod
    def create(cls, id: str, name: str, degrees: Optional[List['Degree']] = None):
        faculty = cls(id=id, name=name, degrees=[degree.id for degree in degrees] if degrees else None)
        faculty._register_event(FacultyCreated(entity_id=id, name=name, degrees=degrees))
        return faculty

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
