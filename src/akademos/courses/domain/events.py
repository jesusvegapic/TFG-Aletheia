from typing import ClassVar

from src.framework_ddd.core.domain.events import DomainEvent  # type: ignore


class CourseCreated(DomainEvent):
    owner: str
    name: str
    description: str
    topics: list[str]
