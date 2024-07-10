from operator import or_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.shared.application.queries import GetTeacherCourseSubscribersMailingList, MailingListDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import UserModel


async def get_teacher_course_subscribers_mailing_list(
        query: GetTeacherCourseSubscribersMailingList,
        session: AsyncSession
):
    mailing_list = (
        await session.execute(
            select(UserModel.email)
            .join(TeacherCourseSubscriptionModel)
            .where(
                TeacherCourseSubscriptionModel.teacher_id == GenericUUID(query.teacher_id) and
                or_(
                    *[TeacherCourseSubscriptionModel.topics.contains(topic) for topic in query.topics]
                )
            )
        )
    ).scalars().all()

    return MailingListDto(emails=list(mailing_list))
