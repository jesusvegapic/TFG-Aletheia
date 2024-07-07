from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import Application
from starlette.responses import StreamingResponse
from apps.aletheia.api.dependencies import get_application
from src.agora.videos.application.queries import GetVideo
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.files import AsyncBinaryIOProtocol


async def stream_video(binaryio_protocol: AsyncBinaryIOProtocol):
    chunk_size = 1024 * 1024  # Tamaño del chunk (1 MB)
    while True:
        data = await binaryio_protocol.read(chunk_size)
        if not data:
            break
        yield data


router = APIRouter()


@router.get(
    "/videos/{video_id}", status_code=200
)
@inject
async def get_video(
        video_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = GetVideo(video_id=video_id)
    response: VideoDto = await application.execute_async(query)
    return StreamingResponse(
        stream_video(response.file),
        media_type=response.content_type,
        headers={"Content-Disposition": f'attachment; filename="{response.filename}"'}
    )
