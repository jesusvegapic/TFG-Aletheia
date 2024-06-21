from dataclasses import field, dataclass

from src.framework_ddd.core.domain.events import DomainEvent


@dataclass(frozen=True)
class LectioAdded(DomainEvent):  # type: ignore
    lectio_id: str
    name: str
    description: str
    video_id: str
