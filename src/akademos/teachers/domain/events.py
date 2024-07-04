from typing import List

from src.framework_ddd.core.domain.events import DomainEvent


class TeacherCreated(DomainEvent):
    email: str
    name: str
    firstname: str
    second_name: str
    faculty_id: str
    degrees: List[str]
    position: str
