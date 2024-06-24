from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, File, Form
from lato import Application
from starlette.responses import JSONResponse

from apps.admin.api.dependencies import get_application
from apps.admin.api.models.courses import PostCourseRequest
from src.akademos.courses.application.commands import CreateCourse, AddLectio
from src.akademos.shared.application.dtos import VideoDto

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
        description=request_body.description,
        topics=request_body.topics
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
        name: str = Form(...),  # type: ignore
        description: str = Form(...),  # type: ignore
        video: UploadFile = File(...)  # type: ignore
):
    filename = video.filename
    content_type = video.content_type

    if filename and content_type:

        command = AddLectio(
            lectio_id=lectio_id,
            course_id=course_id,
            name=name,
            description=description,
            video=VideoDto(
                video.file,  # type: ignore
                filename,
                content_type
            )
        )

        await application.execute_async(command)
    else:
        return JSONResponse(
            status_code=400,
            content={
                "message": "filename and content_type are mandatory fields for a video upload"
            }
        )
