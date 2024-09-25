from src.framework_ddd.core.domain.events import DomainEvent


class CoursePublished(DomainEvent):
    owner: str
    name: str
    description: str
    topics: list[str]
    lectios_names: list[str]
