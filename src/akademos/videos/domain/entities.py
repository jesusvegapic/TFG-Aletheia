from src.akademos.videos.domain.value_objects import VideoName, VideoType
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.core.domain.files import BinaryIOProtocol


class Video(AggregateRoot):
    __content: BinaryIOProtocol
    __name: VideoName
    __type: VideoType

    def __init__(self, id: str, content: BinaryIOProtocol, name: str, type: str):
        super().__init__(id)
        self.__content = content
        self.__name = VideoName(name)
        self.__type = VideoType(type)

    @property
    def content(self):
        return self.__content

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self.__type
