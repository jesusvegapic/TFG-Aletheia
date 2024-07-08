from dataclasses import dataclass

from src.framework_ddd.core.domain.errors import EntityNotFoundError


class FacultyApplicationError(Exception):
    pass


class CreateFacultyError(FacultyApplicationError):
    pass


@dataclass(frozen=True)
class FacultyNameError(CreateFacultyError):
    name: str
    max_lenth: int


@dataclass(frozen=True)
class DegreeNameError(CreateFacultyError):
    name: str
    max_length: int


class FacultyNotFoundError(EntityNotFoundError):
    ...
