from typing import List

from src.agora.notifications.domain.events import CoursePublishedNotificationSent
from src.framework_ddd.mailing.domain.entities import EmailMessage


class CoursePublishedNotification(EmailMessage):
    __teacher_name: str
    __teacher_firstname: str
    __name: str
    __description: str
    __topics: List[str]
    __lectios_names: List[str]

    def __init__(
            self,
            id: str,
            to: List[str],
            from_: str,
            teacher_name: str,
            teacher_firstname: str,
            name: str,
            description: str,
            topics: List[str],
            lectios_names: List[str]
    ):
        super().__init__(
            id,
            to,
            from_,
            f"Nuevo curso publicado por el profesor {teacher_name} {teacher_firstname}",
            CoursePublishedNotification.format_body(
                teacher_name,
                teacher_firstname,
                name,
                description,
                topics,
                lectios_names
            )
        )

        self.__teacher_name = teacher_name
        self.__teacher_firstname = teacher_firstname
        self.__name = name
        self.__description = description
        self.__topics = topics
        self.__lectios_names = lectios_names

    @classmethod
    def send(
            cls,
            id: str,
            to: List[str],
            from_: str,
            teacher_name: str,
            teacher_firstname: str,
            name: str,
            description: str,
            topics: List[str],
            lectios_names: List[str]
    ):
        notification = cls(id, to, from_, teacher_name, teacher_firstname, name, description, topics, lectios_names)
        notification._register_event(
            CoursePublishedNotificationSent(
                entity_id=id,
                to=to,
                from_=from_,
                teacher_name=teacher_name,
                teacher_firstname=teacher_firstname,
                name=name,
                description=description,
                topics=topics,
                lectios_names=lectios_names
            )
        )
        return notification

    @property
    def teacher_name(self):
        return self.__teacher_name

    @property
    def teacher_firstname(self):
        return self.__teacher_firstname

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def topics(self):
        return self.__topics

    @property
    def lectios_names(self):
        return self.__lectios_names

    @classmethod
    def format_body(
            cls,
            teacher_name: str,
            teacher_firstname: str,
            name: str,
            description: str,
            topics: List[str],
            lectios_names: List[str]
    ) -> str:
        enumerated_lectios_lines = [f"{i}: {lectio}" for i, lectio in enumerate(lectios_names, 1)]
        topics_aux = topics.copy()
        last_topic = topics_aux.pop()

        text_body = (
            f"Tienes disponible el nuevo curso \"{name}\" sobre {", ".join(topics_aux)} y {last_topic} "
            f"del profesor {teacher_name} {teacher_firstname}\n\n"

            f"{description}\n\n"

            "Lecciones:\n"

            + ("\n".join(enumerated_lectios_lines))
        )

        return text_body
