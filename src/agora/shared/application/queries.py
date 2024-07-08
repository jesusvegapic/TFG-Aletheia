from typing import List
from lato import Query
from pydantic import BaseModel
from src.framework_ddd.core.domain.errors import DomainError
from src.framework_ddd.iam.application.services import IamUserInfo


class GetCourse(Query):  # type: ignore
    user_info: IamUserInfo
    course_id: str


class GetCourseResponse(BaseModel):
    id: str
    name: str
    owner: str
    description: str
    topics: List[str]
    lectios: List['LectioDto']


class LectioDto(BaseModel):
    id: str
    name: str


class FailedGetCourseResponse:
    cause: DomainError


class GetLectio(Query):
    lectio_id: str


class GetLectioResponse(BaseModel):
    lectio_id: str
    name: str
    description: str
    video_id: str

    class Config:
        arbitrary_types_allowed = True


class ListCoursesResponse(BaseModel):
    courses: List['ListedCourseDto']


class ListedCourseDto(BaseModel):
    id: str
    owner: str
    name: str
