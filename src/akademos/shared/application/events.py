from dataclasses import dataclass
from tempfile import SpooledTemporaryFile

from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.events import DomainEvent


class LectioAdded(DomainEvent, frozen=True):  # type: ignore
    lectio_id: str
    name: str
    description: str
    video: VideoDto
