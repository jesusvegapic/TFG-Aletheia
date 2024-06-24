from tempfile import SpooledTemporaryFile
from typing import Optional

from src.akademos.videos.domain.value_objects import VideoName, VideoType
from src.framework_ddd.core.domain.entities import AggregateRoot


class Video(AggregateRoot):
    __content: SpooledTemporaryFile
    __name: VideoName
    __type: VideoType

    def __init__(self, id: str, content: SpooledTemporaryFile, name: str, type: str):
        super().__init__(id)
        self.__content = content
        self.__name = VideoName(name)
        self.__type = VideoType(type)
