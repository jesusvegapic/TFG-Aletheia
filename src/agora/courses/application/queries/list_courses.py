from dataclasses import dataclass
from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agora.courses.application import agora_courses_module
from src.shared.infrastructure.sql_alchemy.models import CourseModel


class ListCourses(Query):
    page_number: int
    courses_by_page: int


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
    dao = course_model_instances_to_list_courses_response(course_model_instances)
    return dao


async def get_paged_courses(session: AsyncSession, start_index: int, page_size: int) -> List[CourseModel]:
    query_result = await session.execute(select(CourseModel).offset(start_index).limit(page_size))
    return list(query_result.scalars().all())


def course_model_instances_to_list_courses_response(instances: List[CourseModel]) -> ListCoursesResponse:
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
