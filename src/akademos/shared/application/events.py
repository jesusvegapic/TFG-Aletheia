from dataclasses import dataclass
from tempfile import SpooledTemporaryFile

from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.events import DomainEvent


@dataclass(frozen=True)
class LectioAdded(DomainEvent):  # type: ignore
    lectio_id: str
    name: str
    description: str
    video: VideoDto
