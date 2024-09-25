from typing import List

from src.framework_ddd.core.domain.events import DomainEvent


class FacultyCreated(DomainEvent):
    name: str
    degrees: List[str]
