from typing import ClassVar

from src.framework_ddd.core.domain.events import DomainEvent  # type: ignore


class CourseCreated(DomainEvent):
    owner: str
    name: str
    description: str
    topics: list[str]
    event_name: ClassVar[str] = "akademos.course.created"

class CourseHasBeenPublished(DomainEvent):
    ...