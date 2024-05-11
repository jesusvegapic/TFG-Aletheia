from src.framework_ddd.core.domain.errors import EntityNotFoundError


class StudentsModuleError(Exception):
    pass


class StudentNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass


class CourseNotFoundError(EntityNotFoundError, StudentsModuleError):
    pass
