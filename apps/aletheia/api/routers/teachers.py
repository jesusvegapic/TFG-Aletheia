from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from lato import Application
from apps.aletheia.api.dependencies import get_application, get_authenticated_super_user_info
from apps.aletheia.api.models.teachers import PutTeacherRequest
from src.agora.teachers.application.queries.get_course_students_progress import GetCourseStudentsProgress
from src.akademos.teachers.application.commands.sign_up_teacher import SignUpTeacher
from src.framework_ddd.iam.application.services import IamUserInfo

router = APIRouter()


@router.put(
    "/teachers/{teacher_id}", status_code=201
)
@inject
async def put_teacher(
        teacher_id: str,
        request_body: PutTeacherRequest,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)]
):
    command = SignUpTeacher(
        teacher_id=teacher_id,
        name=request_body.name,
        firstname=request_body.firstname,
        second_name=request_body.second_name,
        email=request_body.email,
        password=request_body.password,
        faculty_id=request_body.faculty,
        degrees=request_body.degrees,
        position=request_body.position
    )

    await application.execute_async(command)


@router.get(
    "/teachers/courseStudentsProgress/{course_id}"
)
@inject
async def get_course_students_progress(
        course_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)]
):
    query = GetCourseStudentsProgress(
        teacher_id=user_info.user_id,
        course_id=course_id
    )

    response = await application.execute_async(query)

    return response
