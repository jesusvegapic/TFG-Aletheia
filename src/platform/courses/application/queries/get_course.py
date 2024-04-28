from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession


class GetCourse(Query):
    course_id: str


async def get_course(query: GetCourse, session: AsyncSession) -> CourseDao:
    course_model = await session.get(CourseModel, query.course_id)
    dao = course_model_to_dao(course_model)
    return dao