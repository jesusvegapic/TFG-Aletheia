from typing import List, ClassVar, Optional

from src.akademos.courses.domain.events import CourseCreated
from src.akademos.courses.domain.value_objects import (  # type: ignore
    CourseName,
    CourseDescription,
    CourseState,
    LectioName,
    LectioDescription,
    Topic
)
from src.akademos.shared.application.events import LectioAdded
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.entities import AggregateRoot, Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID


class Course(AggregateRoot):
    __owner: GenericUUID
    __name: CourseName
    __description: CourseDescription
    __state: CourseState
    __lectios: List['Lectio']
    __topics: List[Topic]

    def __init__(
            self,
            id: str,
            owner: str,
            name: str,
            description: str,
            topics: List[str],
            state: Optional[str] = None,
            lectios: Optional[List['Lectio']] = None
    ):
        super().__init__(id)
        self.__owner = GenericUUID(owner)
        self.__name = CourseName(name)
        self.__description = CourseDescription(description)
        self.__lectios = lectios if lectios else []
        self.__state = CourseState(state) if state else CourseState.CREATED
        self.__topics = [(Topic(topic)) for topic in topics]

    @classmethod
    def create(cls, id: str, owner: str, name: str, description: str, topics: List[str]) -> 'Course':
        course = cls(id=id, owner=owner, name=name, description=description, topics=topics)
        course._register_event(
            CourseCreated(entity_id=id, owner=owner, name=name, description=description, topics=topics)
        )
        return course

    def add_lectio(self, lectio: 'Lectio', video: VideoDto):
        self.__lectios.append(lectio)
        self._register_event(
            LectioAdded(  # type: ignore
                entity_id=self.id,
                lectio_id=lectio.id,
                name=lectio.name,
                description=lectio.description,
                video=video  # type: ignore
            )
        )

    @property
    def owner(self) -> str:
        return self.__owner.hex

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def state(self) -> str:
        return self.__state

    @property
    def lectios(self):
        return self.__lectios

    @property
    def topics(self) -> List[str]:
        return self.__topics  # type: ignore


class Lectio(Entity):
    __name: LectioName
    __description: LectioDescription

    def __init__(self, id: str, name: str, description: str):
        super().__init__(id)
        self.__name = LectioName(name)
        self.__description = LectioDescription(description)

    @classmethod
    def create(cls, id: str, name: str, description: str) -> 'Lectio':
        return cls(id, name, description)

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description
