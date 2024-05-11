from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, File, Form
from lato import Application
from apps.admin.api.dependencies import get_application
from apps.admin.api.models.courses import PostCourseRequest
from src.admin.courses.application.commands import CreateCourse
from src.admin.courses.application.commands import CreateLectio

router = APIRouter()


@router.put(
    "/courses/{course_id}", status_code=201
)
@inject
async def put_course(
        request_body: PostCourseRequest,
        course_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    command = CreateCourse(
        course_id=course_id,
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
        name: str = Form(...),
        description: str = Form(...),
        video: UploadFile = File(...)
):

    command = CreateLectio(
        lectio_id=lectio_id,
        course_id=course_id,
        name=name,
        description=description,
        video=video.file,
        video_name=video.filename,
        video_type=video.content_type
    )

    await application.execute_async(command)
