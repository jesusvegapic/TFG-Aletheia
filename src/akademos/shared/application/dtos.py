from pydantic import BaseModel

from src.framework_ddd.core.domain.files import BinaryIOProtocol


class VideoDto(BaseModel):
    file: BinaryIOProtocol
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
