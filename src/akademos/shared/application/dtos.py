from pydantic import BaseModel
from src.framework_ddd.core.domain.files import AsyncBinaryIOProtocol


class VideoDto(BaseModel):
    video_id: str
    file: AsyncBinaryIOProtocol
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
