from dataclasses import dataclass
from typing import Dict

from lato import Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.sql_alchemy.models import CourseModel


class GetCourse(Query):
    course_id: str


@dataclass(frozen=True)
class GetCourseResponse:
    course: Dict


async def get_course(query: GetCourse, session: AsyncSession) -> GetCourseResponse:
    course_model = await session.get(CourseModel, query.course_id)
    response = course_model_to_get_course_response(course_model)  # type: ignore
    return response


def course_model_to_get_course_response(instance: CourseModel) -> GetCourseResponse:
    return GetCourseResponse(
        {
            "name": instance.name,
            "owner": instance.owner,
            "description": instance.description,
            "lectios": [
                {
                    "id": lectio.id,
                    "name": lectio.name
                }
                for lectio in instance.lectios
            ]
        }
    )
