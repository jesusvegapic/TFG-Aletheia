from dataclasses import dataclass

from lato import Query

from src.framework_ddd.core.domain.errors import DomainError


@dataclass(frozen=True)
class GetCourse(Query):  # type: ignore
    course_id: str


@dataclass(frozen=True)
class GetCourseResponse:
    id: str
    lectios: list[str]


class FailedGetCourseResponse:
    cause: DomainError
