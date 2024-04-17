from dataclasses import dataclass, field
from src.courses.domain.value_objects import CourseState, CourseName, CourseDescription, LectioName, LectioDescription
from src.shared.domain.entities import AggregateRoot, GenericUUID, Entity


@dataclass(kw_only=True)
class Course(AggregateRoot[GenericUUID]):
    owner: GenericUUID
    name: CourseName
    description: CourseDescription
    state: CourseState = field(default=CourseState.CREATED)
    lectios: list['Lectio'] = field(default_factory=list)

    def add_lectio(self, lectio: 'Lectio'):
        self.lectios.append(lectio)


@dataclass(kw_only=True)
class Lectio(Entity[GenericUUID]):
    name: LectioName
    description: LectioDescription
