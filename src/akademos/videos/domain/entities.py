from dataclasses import dataclass
from tempfile import SpooledTemporaryFile

from src.shared.domain.ddd.entities import AggregateRoot
from src.shared.domain.ddd.value_objects import GenericUUID
from src.Academia.videos.domain.value_objects import VideoName, VideoType


class Video(AggregateRoot[GenericUUID]):
    content: SpooledTemporaryFile
    name: VideoName
    type: VideoType
