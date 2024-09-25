from typing import List

from src.framework_ddd.core.domain.events import DomainEvent


class TeacherCoursesSubscriptionCreated(DomainEvent):
    subscriber_id: str
    teacher_id: str
    topics: List[str]
