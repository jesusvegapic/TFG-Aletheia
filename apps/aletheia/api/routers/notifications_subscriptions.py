from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import Application

from apps.aletheia.api.dependencies import get_application, get_authenticated_user_info
from apps.aletheia.api.models.notifications_subscriptions import PutTeacherCoursesSubscription
from src.agora.notifications_subscriptions.application.commands.subscribe_user_to_teacher_courses import \
    SubscribeUserToTeacherCourses
from src.framework_ddd.iam.application.services import IamUserInfo

router = APIRouter()


@router.put(
    "/notificationsSubscription/teacherCourses/{subscription_id}"
)
@inject
async def put_teacher_courses_subscription(
        subscription_id: str,
        request_body: PutTeacherCoursesSubscription,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_user_info)]
):
    command = SubscribeUserToTeacherCourses(
        subscription_id=subscription_id,
        user_id=user_info.user_id,
        teacher_id=request_body.teacher_id,
        topics=request_body.topics
    )

    await application.execute_async(command)
