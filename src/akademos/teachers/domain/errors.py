from dataclasses import dataclass
from typing import List

from src.framework_ddd.core.domain.errors import DomainError


class TeachersModuleError(DomainError):
    pass


@dataclass(frozen=True)
class DegreeNotExistsInTeacherFacultyError(TeachersModuleError):
    degrees_ids: List[str]
    faculty_id: str
