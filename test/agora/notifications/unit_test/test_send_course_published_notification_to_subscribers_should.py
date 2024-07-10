from unittest.mock import AsyncMock

from lato import Query

from src.agora.notifications.application.events.send_course_published_notification_to_subscribers import \
    send_course_published_notification_to_subscribers
from src.agora.notifications.domain.entities import CoursePublishedNotification
from src.agora.notifications.domain.events import CoursePublishedNotificationSent
from src.agora.shared.application.queries import GetTeacherCourseSubscribersMailingList, MailingListDto, GetTeacherName, \
    GetTeacherNameResponse
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.mailing.domain.value_objects import Email
from src.shared.domain.events import CoursePublished
from test.agora.notifications.unit_test.notifications_module import TestNotificationsModule


class SendCoursePublishedNotificationToSubscribersShould(TestNotificationsModule):
    async def test_send_valid_course_published_notification(self):
        event = CoursePublished(
            entity_id=GenericUUID.next_id().hex,
            owner=GenericUUID.next_id().hex,
            name="Kant vs hegel",
            description="La panacea de la historia de la filosofía",
            topics=["Derecho", "Biología"],
            lectios_names=[
                "Materialismo filosófico",
                "Ensayos materialistas"
            ]
        )

        async def publish_query(query: Query):
            if isinstance(query, GetTeacherCourseSubscribersMailingList):
                return MailingListDto(
                    emails=["boromir@aletheia.com", "gandalf@aletheia.com"]
                )
            elif isinstance(query, GetTeacherName):
                return GetTeacherNameResponse(
                    name="aragorn",
                    firstname="elessar"
                )

        publish = AsyncMock()

        self.sender.send = AsyncMock()

        expected_notification = CoursePublishedNotification(
            id=GenericUUID.next_id().hex,
            to=["boromir@aletheia.com", "gandalf@aletheia.com"],
            from_="aletheia@aletheia.com",
            teacher_name="aragorn",
            teacher_firstname="elessar",
            name=event.name,
            description=event.description,
            topics=event.topics,
            lectios_names=event.lectios_names
        )

        event_expected = CoursePublishedNotificationSent(
            entity_id=expected_notification.id,
            to=expected_notification.to,
            from_=expected_notification.from_,
            teacher_name=expected_notification.teacher_name,
            teacher_firstname=expected_notification.teacher_firstname,
            name=expected_notification.name,
            description=expected_notification.description,
            topics=expected_notification.topics,
            lectios_names=expected_notification.lectios_names
        )

        await send_course_published_notification_to_subscribers(
            event,
            self.sender,
            Email("aletheia@aletheia.com"),
            publish_query,
            publish
        )

        args, kwargs = self.sender.send.call_args

        self.assertEqual(args[0].model_dump(exclude={"id"}), expected_notification.model_dump(exclude={"id"}))
        self.assertEqual(
            args[0].body,
            "Tienes disponible el nuevo curso Kant vs hegel sobre Derecho y Biología del profesor aragorn elassar\n"

            "La panacea de la historia de la filosofía\n"

            "Lecciones:\n"

            "1: Materialismo filosófico\n"

            "2: Ensayos materialistas\n"
        )

        args, kwargs = publish.call_args

        actual_event = args[0].event_dump()
        actual_event.pop("entity_id")

        event_expected = event_expected.event_dump()
        event_expected.pop("entity_id")

        self.assertEqual(actual_event, event_expected)
