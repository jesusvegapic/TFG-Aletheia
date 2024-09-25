from dataclasses import dataclass

from src.framework_ddd.core.domain.errors import DomainError


class CoursesApplicationError(Exception):
    ...


class GetCourseError(CoursesApplicationError):
    ...


@dataclass(frozen=True)
class PrivateCourseError(GetCourseError, DomainError):
    ...
