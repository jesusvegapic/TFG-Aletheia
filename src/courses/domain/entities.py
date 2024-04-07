from dataclasses import dataclass, field

from src.courses.domain.value_objects import CourseState, CourseName, CourseDescription
from src.shared.domain.entities import AggregateRoot, GenericUUID


@dataclass(kw_only=True)
class Course(AggregateRoot[GenericUUID]):
    owner: GenericUUID
    name: CourseName
    description: CourseDescription
    state: CourseState = field(default=CourseState.CREATED)
