from dataclasses import dataclass
from tempfile import SpooledTemporaryFile
from typing import Optional

from pydantic import BaseModel


class VideoDto(BaseModel):
    file: SpooledTemporaryFile
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
