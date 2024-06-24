from dataclasses import dataclass
from typing import List
from lato import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.infrastructure.sql_alchemy.models import CourseModel


class ListCourses(Query):
    actual_page: int


@dataclass(frozen=True)
class ListCoursesResponse:
    courses: List['ListedCourseDto']


@dataclass(frozen=True)
class ListedCourseDto:
    id: str
    owner: str
    name: str


async def list_courses(query: ListCourses, session: AsyncSession) -> ListCoursesResponse:
    courses_by_page = 15
    start_index = (query.actual_page - 1) * courses_by_page
    course_model_instances = await get_paged_courses(session, start_index, courses_by_page)
    dao = course_model_instances_to_list_courses_response(course_model_instances)
    return dao


async def get_paged_courses(session: AsyncSession, start_index: int, page_size: int) -> List[CourseModel]:
    query_result = await session.execute(select(CourseModel).offset(start_index).limit(page_size))
    return list(query_result.scalars().all())


def course_model_instances_to_list_courses_response(instances: List[CourseModel]) -> ListCoursesResponse:
    return ListCoursesResponse(
        [
            ListedCourseDto(
                id=instance.id.hex,  # type: ignore
                name=instance.name,  # type: ignore
                owner=instance.owner.hex  # type: ignore
            )
            for instance in instances
        ]
    )
