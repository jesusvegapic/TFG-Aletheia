from src.akademos.videos.domain.events import VideoCreated
from src.akademos.videos.domain.value_objects import VideoName, VideoType
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.core.domain.files import AsyncBinaryIOProtocol


class Video(AggregateRoot):
    __content: AsyncBinaryIOProtocol
    __name: VideoName
    __type: VideoType

    def __init__(self, id: str, content: AsyncBinaryIOProtocol, name: str, type: str):
        super().__init__(id)
        self.__content = content
        self.__name = VideoName(name)
        self.__type = VideoType(type)

    @classmethod
    def create(cls, id: str, content: AsyncBinaryIOProtocol, name: str, type: str):
        video = cls(id=id, content=content, name=name, type=type)
        video._register_event(VideoCreated(entity_id=id, name=name, type=type))
        return video

    @property
    def content(self):
        return self.__content

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> str:
        return self.__type
