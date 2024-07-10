from dataclasses import dataclass, Field
from src.framework_ddd.core.domain.errors import EntityNotFoundError, DomainError, ApplicationError


class StudentsModuleError(ApplicationError):
    pass


class CreateStudentError(StudentsModuleError):
    ...


class EnrollInACourseError(StudentsModuleError):
    ...


class SetLastVisitedLectioError(StudentsModuleError):
    ...


class StartLectioError(StudentsModuleError):
    ...


class FinishLectioError(StudentsModuleError):
    ...


class StudentNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass


class CourseNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass


@dataclass(frozen=True)
class DegreeNotExistsInStudentFacultyError(StudentsModuleError, DomainError):
    degree_id: str
    faculty_id: str


@dataclass(frozen=True)
class NotEnrolledLectioError(StudentsModuleError, DomainError):
    course_id: str
    lectio_id: str


@dataclass(frozen=True)
class LectioNotExistsInCourse(StudentsModuleError, DomainError):
    lectio_id: str
    course_id: str


@dataclass(frozen=True)
class StartFinishedLectioError(StartLectioError, DomainError):
    ...


@dataclass(frozen=True)
class FinishNotStartedLectioError(FinishLectioError, DomainError):
    ...
