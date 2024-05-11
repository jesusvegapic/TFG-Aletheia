from dataclasses import dataclass, Field
from typing import Optional

from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.entities import PersonalUser


@dataclass(kw_only=True)
class Student(PersonalUser):  # type: ignore
    faculty: 'Faculty'
    degree: GenericUUID
    courses_in_progress: list['Course'] = Field(default_factory=list)  # type: ignore
    courses_lectios: dict[GenericUUID, 'Lectio'] = Field(default_factory=dict)  # type: ignore
    last_visited_lectio: Optional['Lectio'] = Field(default=None)  # type: ignore

    def __post_init__(self):
        if self.degree not in self.faculty.degrees:
            raise DomainException()

    def enroll_in_a_course(self, course: 'Course'):
        if course not in self.courses_in_progress:
            self.courses_in_progress.append(course)
            for lectio in course.lectios:
                self.courses_lectios[lectio.id] = lectio
        else:
            raise DomainException()

    def start_lectio(self, lectio_id: GenericUUID):
        if lectio_id in self.courses_lectios:
            self.courses_lectios[lectio_id].status = LectioStatus.STARTED
        else:
            raise DomainException()

    def finish_lectio(self, lectio_id: GenericUUID):
        if lectio_id in self.courses_lectios:
            self.courses_lectios[lectio_id].status = LectioStatus.FINISHED
        else:
            raise DomainException()

    def set_last_visited_lectio(self, lectio_id: GenericUUID):
        if lectio_id in self.courses_lectios:
            self.last_visited_lectio = self.courses_lectios[lectio_id]
        else:
            raise DomainException()


@dataclass
class Lectio(Entity[GenericUUID]):
    status: LectioStatus = Field(default=LectioStatus.NOT_STARTED)  # type: ignore


class Faculty(Entity[GenericUUID]):
    degrees: list[GenericUUID]


class TeacherCoursesSubscription(Entity[GenericUUID]):
    teacher_id: GenericUUID
    topics: list[Topic]
