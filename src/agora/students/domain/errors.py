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
    degree_id: str
    faculty_id: str


@dataclass(frozen=True)
class NotEnrolledLectioError(StudentsModuleError):
    course_id: str
    lectio_id: str

