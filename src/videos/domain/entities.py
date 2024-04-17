from dataclasses import dataclass
from tempfile import SpooledTemporaryFile

from src.shared.domain.entities import AggregateRoot
from src.shared.domain.value_objects import GenericUUID
from src.videos.domain.value_objects import VideoName, VideoType


@dataclass(kw_only=True)
class Video(AggregateRoot[GenericUUID]):
    content: SpooledTemporaryFile
    name: VideoName
    type: VideoType
