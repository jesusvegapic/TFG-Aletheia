from unittest.mock import AsyncMock

from src.agora.notifications_subscriptions.application.commands.subscribe_user_to_teacher_courses import \
    SubscribeUserToTeacherCourses, subscribe_user_to_teacher_courses
from src.agora.notifications_subscriptions.domain.entities import TeacherCoursesSubscription
from src.agora.notifications_subscriptions.domain.events import TeacherCoursesSubscriptionCreated
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.agora.notifications_subscriptions.unit_test.notifications_subscriptions_module import \
    TestNotificationsSubscriptionsModule


class SubscribeUserToTeacherCoursesShould(TestNotificationsSubscriptionsModule):

    async def test_create_valid_teacher_course_subscription(self):
        command = SubscribeUserToTeacherCourses(
            subscription_id=GenericUUID.next_id().hex,
            teacher_id=GenericUUID.next_id().hex,
            user_id=GenericUUID.next_id().hex,
            topics=[
                "Biología",
                "Filosofía"
            ]
        )

        self.repository.add = AsyncMock()

        subscription_expected = TeacherCoursesSubscription(
            id=command.subscription_id,
            teacher_id=command.teacher_id,
            subscriber_id=command.user_id,
            topics=command.topics
        )

        publish = AsyncMock()

        publish_query = AsyncMock()

        await subscribe_user_to_teacher_courses(command, self.repository, publish_query, publish)

        args, kwargs = self.repository.add.call_args

        self.assertEqual(args[0], subscription_expected)

        args, kwargs = publish.call_args

        expected_event = TeacherCoursesSubscriptionCreated(
            entity_id=subscription_expected.id,
            subscriber_id=subscription_expected.subscriber_id,
            teacher_id=subscription_expected.teacher_id,
            topics=subscription_expected.topics
        )

        self.assertEqual(args[0].event_dump(), expected_event.event_dump())
