from lato import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class ListCourses(Query):
    actual_page: int
    courses_by_page: int


async def list_courses(query: ListCourses, session: AsyncSession) -> ListedCoursesDao:
    start_index = (query.actual_page - 1) * query.courses_by_page
    course_model_instances = await session.execute(select(CourseModel).offset(start_index).limit(query.courses_by_page))
    dao = course_model_instances_to_listed_courses_dao(course_model_instances)
    return dao
