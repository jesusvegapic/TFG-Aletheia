from dataclasses import dataclass
from typing import BinaryIO
from src.shared.domain.entities import AggregateRoot
from src.shared.domain.value_objects import GenericUUID
from src.videos.domain.value_objects import VideoName, VideoType


@dataclass(kw_only=True)
class Video(AggregateRoot[GenericUUID]):
    content: BinaryIO
    name: VideoName
    type: VideoType
