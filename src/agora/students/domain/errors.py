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
    name: str = "degree_not_exists_in_student_faculty"


@dataclass(frozen=True)
class NotEnrolledLectioError(StudentsModuleError):
    course_id: str
    lectio_id: str

