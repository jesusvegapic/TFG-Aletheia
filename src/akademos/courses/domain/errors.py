from dataclasses import dataclass

from src.framework_ddd.core.domain.errors import DomainError


class CourseApplicationError(Exception):
    pass


class CreateCourseError(CourseApplicationError):
    pass


@dataclass(frozen=True)
class TeacherIdError(CreateCourseError, DomainError):
    value: str


@dataclass(frozen=True)
class CourseNameError(CreateCourseError, DomainError):
    value: str
    max_length: int


@dataclass(frozen=True)
class CourseDescriptionError(CreateCourseError, DomainError):
    value: str
    max_length: int
