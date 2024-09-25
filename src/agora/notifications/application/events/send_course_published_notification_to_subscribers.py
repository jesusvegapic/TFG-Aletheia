from src.agora.notifications.application import notifications_module
from src.agora.notifications.domain.entities import CoursePublishedNotification
from src.agora.shared.application.queries import GetTeacherName, GetTeacherCourseSubscribersMailingList, MailingListDto, \
    GetTeacherNameResponse
from src.framework_ddd.mailing.domain.email_sender import EmailSender
from src.framework_ddd.mailing.domain.value_objects import Email
from src.shared.domain.events import CoursePublished


@notifications_module.handler(CoursePublished)
async def send_course_published_notification_to_subscribers(
        event: CoursePublished,
        email_sender: EmailSender,
        aletheia_platform_email: Email,
        publish_query,
        publish
):
    mailing_list: MailingListDto = await publish_query(
        GetTeacherCourseSubscribersMailingList(
            teacher_id=event.owner,
            topics=event.topics
        )
    )

    if len(mailing_list.emails) > 0:
        teacher_name_response: GetTeacherNameResponse = await publish_query(GetTeacherName(teacher_id=event.owner))

        notification = CoursePublishedNotification.send(
            id=CoursePublishedNotification.next_id().hex,
            from_=aletheia_platform_email,
            to=mailing_list.emails,
            teacher_name=teacher_name_response.name,
            teacher_firstname=teacher_name_response.firstname,
            name=event.name,
            description=event.description,
            topics=event.topics,
            lectios_names=event.lectios_names
        )

        await email_sender.send(notification)

        for event in notification.pull_domain_events():
            await publish(event)
