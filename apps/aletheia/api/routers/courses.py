from typing import Annotated, List
from dependency_injector.wiring import inject
from fastapi import APIRouter, UploadFile
from fastapi.params import Depends, Query, Form, File
from lato import Application
from starlette.responses import JSONResponse
from apps.aletheia.api.dependencies import get_application, UploadFileWrapper, get_authenticated_super_user_info, \
    get_authenticated_user_info
from apps.aletheia.api.models.courses import PostCourseRequest, GetLectioHttpResponse
from src.agora.courses.application.queries.list_courses import ListCourses
from src.agora.shared.application.queries import GetCourse, GetCourseResponse, GetLectio, GetLectioResponse
from src.akademos.courses.application.commands import CreateCourse, AddLectio
from src.akademos.courses.application.commands.publish_course import PublishCourse
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.iam.application.services import IamUserInfo

router = APIRouter()


@router.put(
    "/courses/{course_id}"
)
@inject
async def put_course(
        request_body: PostCourseRequest,
        course_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)]
):
    command = CreateCourse(
        course_id=course_id,
        teacher_id=user_info.user_id,
        name=request_body.name,
        description=request_body.description,
        topics=request_body.topics
    )

    await application.execute_async(command)


@router.patch(
    "/courses/{course_id}/publish"
)
@inject
async def patch_course_as_published(
        course_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)]
):
    command = PublishCourse(teacher_id=user_info.user_id, course_id=course_id)
    await application.execute_async(command)


@router.put(
    "/courses/{course_id}/lectios/{lectio_id}"
)
@inject
async def put_lectio(
        course_id: str,
        lectio_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)],
        name: str = Form(...),  # type: ignore
        description: str = Form(...),  # type: ignore
        video_id: str = Form(...),  # type: ignore
        video: UploadFile = File(...)  # type: ignore
):
    filename = video.filename
    content_type = video.content_type

    if filename and content_type:

        command = AddLectio(
            teacher_id=user_info.user_id,
            lectio_id=lectio_id,
            course_id=course_id,
            name=name,
            description=description,
            video=VideoDto(
                video_id=video_id,
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
    "/courses/{course_id}"
)
@inject
async def get_course(
        course_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_user_info)]
):
    query = GetCourse(user_id=user_info.user_id, course_id=course_id)
    response: GetCourseResponse = await application.execute_async(query)
    return response


@router.get(
    "/courses"
)
@inject
async def list_courses(
        application: Annotated[Application, Depends(get_application)],
        start: int = Query(0, alias="start"),  # type: ignore
        limit: int = Query(15, alias="limit"),  # type: ignore
        topics: List[str] = Query([], alias="topics")  # type: ignore
):
    query = ListCourses(page_number=start, courses_by_page=limit, topics=topics)
    response = await application.execute_async(query)
    return response


@router.get(
    "/lectios/{lectio_id}"
)
@inject
async def get_lectio(
        lectio_id: str,
        application: Annotated[Application, Depends(get_application)],

):
    query = GetLectio(lectio_id=lectio_id)
    response: GetLectioResponse = await application.execute_async(query)

    return GetLectioHttpResponse(
        lectio_id=response.lectio_id,
        name=response.name,
        description=response.description,
        video_url=f"/videos/{response.video_id}"
    )
