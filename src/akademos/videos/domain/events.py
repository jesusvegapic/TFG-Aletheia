from src.framework_ddd.core.domain.events import DomainEvent


class VideoCreated(DomainEvent):
    name: str
    type: str
