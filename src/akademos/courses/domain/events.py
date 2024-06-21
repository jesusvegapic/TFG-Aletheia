from dataclasses import field

from src.framework_ddd.core.domain.events import DomainEvent  # type: ignore


class CourseCreated(DomainEvent):
    owner: str
    name: str
    description: str
    topics: list[str]
    event_name = field(default="akademos.course.created", init=False)
