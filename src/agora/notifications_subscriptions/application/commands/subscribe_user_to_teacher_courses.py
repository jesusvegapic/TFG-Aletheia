from typing import List
from lato import Command

from src.agora.notifications_subscriptions.application import notifications_subscriptions_module
from src.agora.notifications_subscriptions.domain.entities import TeacherCoursesSubscription
from src.agora.notifications_subscriptions.domain.repository import NotificationsSubscriptionRepository
from src.agora.shared.application.queries import GetTeacherName


class SubscribeUserToTeacherCourses(Command):
    subscription_id: str
    user_id: str
    teacher_id: str
    topics: List[str]


@notifications_subscriptions_module.handler(SubscribeUserToTeacherCourses)
async def subscribe_user_to_teacher_courses(
        command: SubscribeUserToTeacherCourses,
        notifications_subscriptions_repository: NotificationsSubscriptionRepository,
        publish_query,
        publish
):
    await publish_query(GetTeacherName(teacher_id=command.teacher_id))

    subscription = TeacherCoursesSubscription.create(
        id=command.subscription_id,
        subscriber_id=command.user_id,
        teacher_id=command.teacher_id,
        topics=command.topics
    )

    await notifications_subscriptions_repository.add(subscription)

    for event in subscription.pull_domain_events():
        await publish(event)
