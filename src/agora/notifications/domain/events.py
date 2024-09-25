from typing import List

from src.framework_ddd.core.domain.events import DomainEvent


class CoursePublishedNotificationSent(DomainEvent):
    entity_id: str
    to: List[str]
    from_: str
    teacher_name: str
    teacher_firstname: str
    name: str
    description: str
    topics: List[str]
    lectios_names: List[str]
