from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, File, Form
from lato import Application

from apps.api.dependencies import get_application
from apps.api.models.courses import PostCourseRequest, PostCourseResponse, PutLectioRequest
from src.courses.application.commands.create_course import CreateCourse

router = APIRouter()


@router.put(
    "/courses/{course_id}", status_code=201
)
@inject
async def post_course(
        request_body: PostCourseRequest,
        course_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    command = CreateCourse(
        id=course_id,
        teacher_id=request_body.teacher_id,
        name=request_body.name,
        description=request_body.description
    )

    await application.execute_async(command)


@router.put(
    "/courses/{course_id}/lectio/{lectio_id}", status_code=201
)
@inject
async def put_lectio(
        course_id: str,
        lectio_id: str,
        application: Annotated[Application, Depends(get_application)],
        request_body: PutLectioRequest = Form(...),
        video: UploadFile = File(...)
):
    command = CreateLectio(
        course_id=course_id,
        lectio_id=lectio_id,
        name=request_body,
        description=request_body.description,
        video=video.file,
        video_name=video.filename,
        video_type=video.content_type
    )

    await application.execute_async(command)
