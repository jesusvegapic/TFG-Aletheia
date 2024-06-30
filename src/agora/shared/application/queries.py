from dataclasses import dataclass
from enum import StrEnum
from typing import List

from lato import Query
from pydantic import BaseModel

from src.framework_ddd.core.domain.errors import DomainError


class GetCourse(Query):  # type: ignore
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
