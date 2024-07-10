from typing import List

from src.akademos.conferences.domain.events import ConferenceCreated
from src.akademos.conferences.domain.value_objects import ConferenceName, ConferenceDescription
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.domain.value_objects import Topic


class Conference(AggregateRoot):
    __owner: GenericUUID
    __name: ConferenceName
    __description: ConferenceDescription
    __topics: List[Topic]
    __video_id: GenericUUID

    def __init__(self, id: str, owner: str, name: str, description: str, topics: List[str], video_id: str):
        super().__init__(id)
        self.__owner = GenericUUID(owner)
        self.__name = ConferenceName(name)
        self.__description = ConferenceDescription(description)
        self.__topics = [Topic(topic) for topic in topics]
        self.__video_id = GenericUUID(video_id)

    @classmethod
    def create(cls, id: str, owner: str, name: str, description: str, topics: List[str],  video: VideoDto):
        conference = cls(id, owner, name, description, topics, video.video_id)
        conference._register_event(
            ConferenceCreated(
                entity_id=id,
                owner=owner,
                name=name,
                description=description,
                topics=topics,
                video=video
            )
        )
        return conference
