from typing import List
from src.akademos.faculties.domain.events import FacultyCreated  # type: ignore
from src.akademos.faculties.domain.value_objects import FacultyName, DegreeName  # type: ignore
from src.framework_ddd.core.domain.entities import Entity, AggregateRoot


class Faculty(AggregateRoot):
    __name: FacultyName
    __degrees: List['Degree']

    def __init__(self, id: str, name: str, degrees: List['Degree']):
        super().__init__(id)
        self.__name = FacultyName(name)
        self.__degrees = degrees

    @classmethod
    def create(cls, id: str, name: str, degrees: List['Degree']):
        faculty = cls(id=id, name=name, degrees=degrees)
        faculty._register_event(
            FacultyCreated(
                entity_id=id,
                name=name,
                degrees=[degree.id for degree in degrees]
            )
        )
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

    @property
    def name(self):
        return self.__name
