from src.agora.notifications_subscriptions.application.queries.get_teacher_course_subscribers_mailing_list import \
    get_teacher_course_subscribers_mailing_list
from src.agora.notifications_subscriptions.infrastructure.repository import NotificationsSubscriptionModel, \
    NotificationsSubscriptionType
from src.agora.shared.application.queries import GetTeacherCourseSubscribersMailingList, MailingListDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import UserModel
from test.shared.database import TestInMemorySqlDatabase


class GetTeacherCourseSubscribersMailingListShould(TestInMemorySqlDatabase):
    async def test_get_valid_list(self):
        subscriber_one = GenericUUID.next_id()
        subscriber_two = GenericUUID.next_id()

        query = GetTeacherCourseSubscribersMailingList(
            teacher_id=GenericUUID.next_id().hex,
            topics=["Filosofía", "Biología"]
        )

        self.session.add(
            UserModel(
                id=subscriber_one,
                email="user@alehetia.com",
                password="invent",
                is_superuser=False
            )
        )

        self.session.add(
            UserModel(
                id=subscriber_two,
                email="user2@alehetia.com",
                password="invent2",
                is_superuser=False
            )
        )

        self.session.add(
            NotificationsSubscriptionModel(
                id=GenericUUID.next_id(),
                subscriber_id=subscriber_one,
                teacher_id=GenericUUID(query.teacher_id),
                type=NotificationsSubscriptionType.TEACHER_COURSES,
                topics="Filosofía"
            )
        )

        self.session.add(
            NotificationsSubscriptionModel(
                id=GenericUUID.next_id(),
                subscriber_id=subscriber_two,
                teacher_id=GenericUUID(query.teacher_id),
                type=NotificationsSubscriptionType.TEACHER_COURSES,
                topics="Biología"
            )
        )

        await self.session.commit()

        response = await get_teacher_course_subscribers_mailing_list(query=query, session=self.session)

        expected_response = MailingListDto(emails=["user@alehetia.com", "user2@alehetia.com"])

        self.assertEqual(expected_response, response)
