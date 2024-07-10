from typing import List

from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.events import DomainEvent


class ConferenceCreated(DomainEvent):
    owner: str
    name: str
    description: str
    topics: List[str]
    video: VideoDto
