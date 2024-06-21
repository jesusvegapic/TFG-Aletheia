from src.akademos.courses.domain.value_objects import (  # type: ignore
    CourseName,
    CourseDescription,
    CourseState,
    LectioName,
    LectioDescription,
    Topic
)
from src.akademos.shared.application.events import LectioAdded
from src.framework_ddd.core.domain.entities import AggregateRoot, Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID


class Course(AggregateRoot):
    __owner: GenericUUID
    __name: CourseName
    __description: CourseDescription
    __state: CourseState
    __lectios: list['Lectio'] = []
    __topics: list[Topic] = []

    def __init__(self, id: str, owner: str, name: str, description: str, topics: list[str]):
        super().__init__(id)
        self.__owner = GenericUUID(owner)
        self.__name = CourseName(name)
        self.__description = CourseDescription(description)
        self.__state = CourseState.CREATED
        for topic in topics:
            self.__topics.append(Topic(topic))
        self._register_event(CourseCreatedDomainEvent(id, owner, name, description, topics))  # type: ignore

    def add_lectio(self, lectio: 'Lectio'):
        self.__lectios.append(lectio)
        self._register_event(LectioAdded(self.id, lectio.id, lectio.name, lectio.description, lectio.video_id))


class Lectio(Entity):
    __name: LectioName
    __description: LectioDescription
    __video_id: GenericUUID

    def __init__(self, id: str, name: str, description: str, video_id: str):
        super().__init__(id)
        self.__name = LectioName(name)
        self.__description = LectioDescription(description)
        self.__video_id = GenericUUID(video_id)
        
    @property
    def name(self):
        return self.__name

    @property
    def video_id(self):
        return self.__video_id.hex

    @property
    def description(self):
        return self.__description
