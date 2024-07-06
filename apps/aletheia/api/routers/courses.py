from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends, Query
from lato import Application
from starlette.responses import JSONResponse, StreamingResponse
from apps.aletheia.api.dependencies import get_application, UploadFileWrapper
from apps.aletheia.api.main import auth_by_token
from apps.aletheia.api.models.courses import PostCourseRequest
from src.agora.courses.application.queries.list_courses import ListCourses
from src.agora.shared.application.queries import GetCourse, GetCourseResponse, GetLectio, GetLectioResponse
from src.akademos.courses.application.commands import CreateCourse, AddLectio
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.iam.application.services import IamUserInfo

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
        iam_user_info: Annotated[IamUserInfo, Depends(auth_by_token)]
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
                file=UploadFileWrapper(video),
                filename=filename,
                content_type=content_type
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


@router.get(
    "/courses/{course_id}", status_code=200
)
@inject
async def get_course(
        course_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = GetCourse(course_id=course_id)
    response: GetCourseResponse = await application.execute_async(query)
    return response


@router.get(
    "/courses", status_code=200
)
@inject
async def list_courses(
        application: Annotated[Application, Depends(get_application)],
        start: int = Query(0, alias="start"),  # type: ignore
        limit: int = Query(15, alias="limit")  # type: ignore
):
    query = ListCourses(page_number=start, courses_by_page=limit)
    response = await application.execute_async(query)
    return response


@router.get(
    "/lectios/{lectio_id}", status_code=200
)
@inject
async def get_lectio(
        lectio_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    async def stream_video(binaryio_protocol):
        chunk_size = 1024 * 1024  # Tamaño del chunk (1 MB)
        while True:
            data = await binaryio_protocol.read(chunk_size)
            if not data:
                break
            yield data
    query = GetLectio(lectio_id=lectio_id)
    response: GetLectioResponse = await application.execute_async(query)
    return StreamingResponse(
        stream_video(response.video_content),
        media_type=response.video_type,
        headers={
            "Content-Disposition": f"attachment; filename={response.video_name}"
        }
    )
