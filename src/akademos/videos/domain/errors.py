from dataclasses import dataclass

from src.akademos.courses.domain.errors import CourseApplicationError
from src.framework_ddd.core.domain.errors import DomainError


class VideoApplicationError(Exception):
    pass


class CreateVideoError(CourseApplicationError):
    pass


@dataclass(frozen=True)
class VideoNameError(CreateVideoError, DomainError):
    name: str
    max_length: int


@dataclass(frozen=True)
class VideoTypeError(CreateVideoError, DomainError):
    type: str
