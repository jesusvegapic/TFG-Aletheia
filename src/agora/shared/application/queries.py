from dataclasses import dataclass
from lato import Query
from src.framework_ddd.core.domain.errors import DomainError


class GetCourse(Query):  # type: ignore
    course_id: str


@dataclass(frozen=True)
class GetCourseResponse:
    id: str
    name: str
    owner: str
    description: str
    lectios: list['LectioDto']


@dataclass(frozen=True)
class LectioDto:
    id: str
    name: str


class FailedGetCourseResponse:
    cause: DomainError



class GetLectio(Query):
    lectio_id: str
