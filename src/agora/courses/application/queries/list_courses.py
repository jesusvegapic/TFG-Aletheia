from dataclasses import dataclass
from re import split
from typing import List, Iterable
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agora.courses.application import agora_courses_module
from src.shared.infrastructure.sql_alchemy.models import CourseModel


class ListCourses(Query):
    page_number: int
    courses_by_page: int
    topics: List[str]


class ListCoursesResponse(BaseModel):
    courses: List['ListedCourseDto']


class ListedCourseDto(BaseModel):
    id: str
    owner: str
    name: str


@agora_courses_module.handler(ListCourses)
async def list_courses(query: ListCourses, session: AsyncSession) -> ListCoursesResponse:
    start_index = query.page_number * query.courses_by_page
    course_model_instances = await get_paged_courses(session, start_index, query.courses_by_page)
    courses_filter_by_topic = filter(
        lambda course: True if len(query.topics) == 0  # type: ignore
        else any(topic in split(";", course.topics) for topic in query.topics),  # type: ignore
        course_model_instances
    )
    dao = course_model_instances_to_list_courses_response(courses_filter_by_topic)  # type: ignore
    return dao


async def get_paged_courses(
        session: AsyncSession,
        start_index: int,
        page_size: int
) -> Iterable[CourseModel]:
    instances = (await session.execute(select(CourseModel).offset(start_index).limit(page_size))).scalars().all()
    return instances


def course_model_instances_to_list_courses_response(instances: Iterable[CourseModel]) -> ListCoursesResponse:
    return ListCoursesResponse(
        courses=[
            ListedCourseDto(
                id=instance.id.hex,  # type: ignore
                name=instance.name,  # type: ignore
                owner=instance.owner.hex  # type: ignore
            )
            for instance in instances
        ]
    )
