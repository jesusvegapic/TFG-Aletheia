from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.agora.shared.application.queries import LectioProgressDto
from src.agora.students.domain.value_objects import LectioStatus
from src.agora.students.infrastructure.repository import StudentLectioModel
from src.framework_ddd.core.domain.value_objects import GenericUUID


class GetCourseStateProgress(Query):
    student_id: str
    course_id: str


class GetCourseStateProgressResponse(BaseModel):
    lectios_progress: List[str]


async def get_course_state_progress(query: GetCourseStateProgress, session: AsyncSession):
    lectios_progress = (
        await session.execute(
            select(StudentLectioModel)
            .options(joinedload(StudentLectioModel.course))
            .where(
                StudentLectioModel.student_course_id == GenericUUID(query.course_id) and
                StudentLectioModel.student_course.student_id == GenericUUID(query.student_id)
            )
        )
    ).scalars().all()

    course_percent_progress = (
        len(list(filter(lambda progress: progress == LectioStatus.FINISHED, lectios_progress))) /
        len(lectios_progress)
    ) * 100

    return GetCourseStateProgressResponse(
        lectios_progress=[
            LectioProgressDto(
                id=lectio.lectio_id,
                name=lectio.lectio.name,
                profress=lectio.progress
            )
            for lectio in lectios_progress
        ],
        course_percent_progress=course_percent_progress
    )
