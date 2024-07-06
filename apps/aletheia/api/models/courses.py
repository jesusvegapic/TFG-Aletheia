from typing import List

from pydantic import BaseModel


class PostCourseRequest(BaseModel):
    teacher_id: str
    name: str
    description: str
    topics: List[str]


class PutLectioRequest(BaseModel):
    name: str
    description: str


class GetLectioHttpResponse(BaseModel):
    lectio_id: str
    name: str
    description: str
    video_url: str
    