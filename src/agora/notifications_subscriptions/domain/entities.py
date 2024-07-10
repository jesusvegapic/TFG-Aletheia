from typing import List

from src.agora.notifications_subscriptions.domain.events import TeacherCoursesSubscriptionCreated
from src.framework_ddd.core.domain.entities import AggregateRoot
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.domain.value_objects import Topic


class NotificationsSubscription(AggregateRoot):
    __subscriber_id: GenericUUID

    def __init__(self, id: str, subscriber_id: str):
        super().__init__(id)
        self.__subscriber_id = GenericUUID(subscriber_id)


    @property
    def subscriber_id(self):
        return self.__subscriber_id.hex


class TeacherCoursesSubscription(NotificationsSubscription):
    __teacher_id: GenericUUID
    __topics: List[Topic]

    def __init__(self, id: str, subscriber_id: str, teacher_id: str, topics: List[str]):
        super().__init__(id, subscriber_id)
        self.__teacher_id = GenericUUID(teacher_id)
        self.__topics = [Topic(topic) for topic in topics]


    @classmethod
    def create(cls, id: str, subscriber_id: str, teacher_id: str, topics: List[str]):
        subscription = cls(id, subscriber_id, teacher_id, topics)
        subscription._register_event(
            TeacherCoursesSubscriptionCreated(
                entity_id=id,
                subscriber_id=subscriber_id,
                teacher_id=teacher_id,
                topics=topics
            )
        )
        return subscription


    @property
    def teacher_id(self):
        return self.__teacher_id.hex

    @property
    def topics(self):
        return self.__topics
