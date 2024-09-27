from typing import Annotated, List
from dependency_injector.wiring import inject
from fastapi import APIRouter, Form, UploadFile
from fastapi.params import Depends, File, Query
from lato import Application
from starlette.responses import JSONResponse
from apps.api.dependencies import get_application, get_authenticated_super_user_info, UploadFileWrapper
from apps.api.models.conferences import GetConferenceHttpResponse
from src.agora.conferences.application.queries.get_conference import GetConference
from src.agora.conferences.application.queries.list_conferences import ListConferences
from src.akademos.conferences.application.commands.create_conference import CreateConference
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.iam.application.services import IamUserInfo

router = APIRouter()


@router.put("/conferences/{conference_id}")
@inject
async def put_conference(
        conference_id: str,
        application: Annotated[Application, Depends(get_application)],
        user_info: Annotated[IamUserInfo, Depends(get_authenticated_super_user_info)],
        name: str = Form(...),  # type: ignore
        description: str = Form(...),  # type: ignore
        topics: List[str] = Form(...),
        video_id: str = Form(...),  # type: ignore
        video: UploadFile = File(...)  # type: ignore
):
    filename = video.filename
    content_type = video.content_type

    if filename and content_type:
        command = CreateConference(
            teacher_id=user_info.user_id,
            conference_id=conference_id,
            name=name,
            description=description,
            topics=topics,
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
    "/conferences/{conference_id}"
)
@inject
async def get_conference(
        conference_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = GetConference(conference_id=conference_id)
    response = await application.execute_async(query)
    return GetConferenceHttpResponse(
        id=response.id,
        owner=response.owner,
        name=response.name,
        description=response.description,
        topics=response.topics,
        video_url=f"/videos/{response.video_id}"
    )


@router.get(
    "/conferences"
)
@inject
async def list_conferences(
        application: Annotated[Application, Depends(get_application)],
        start: int = Query(0, alias="start"),  # type: ignore
        limit: int = Query(15, alias="limit"),  # type: ignore
        topics: List[str] = Query([], alias="topics")  # type: ignore
):
    query = ListConferences(page_number=start, conferences_by_page=limit, topics=topics)
    response = await application.execute_async(query)
    return response
