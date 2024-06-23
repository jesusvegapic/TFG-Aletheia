from dataclasses import dataclass, Field
from src.framework_ddd.core.domain.errors import EntityNotFoundError, DomainError


class StudentsModuleError(DomainError):
    pass


class StudentNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass


class CourseNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass


@dataclass(frozen=True)
class DegreeNotExistsInStudentFacultyError(StudentsModuleError):
    id: str
    degree: str
    faculty: str
    name: str = Field(default="degree_not_exists_in_student_faculty")  # type: ignore


@dataclass(frozen=True)
class NotEnrolledLectioError(StudentsModuleError):
    ...


@dataclass(frozen=True)
class CantStartFinishedLectioError(StudentsModuleError):
    ...


@dataclass(frozen=True)
class CantFinishNotStartedLectioError(StudentsModuleError):
    ...
