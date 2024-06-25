from pydantic import BaseModel
from src.shared.utils.files import BinaryIOProtocol


class VideoDto(BaseModel):
    file: BinaryIOProtocol
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
