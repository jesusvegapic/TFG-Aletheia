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
    lectios_progress: List[LectioProgressDto]
    course_percent_progress: int


async def get_course_state_progress(query: GetCourseStateProgress, session: AsyncSession):
    lectios_progress = (
        await session.execute(
            select(StudentLectioModel)
            .options(joinedload(StudentLectioModel.student_course))
            .where(
                StudentLectioModel.student_course_id == GenericUUID(query.course_id) and
                StudentLectioModel.student_course.student_id == GenericUUID(query.student_id)
            )
        )
    ).scalars().all()

    course_percent_progress = int(
        len(list(filter(lambda lectio: lectio.progress == LectioStatus.FINISHED, lectios_progress))) * 100 /
        len(lectios_progress)
    )

    return GetCourseStateProgressResponse(
        lectios_progress=[
            LectioProgressDto(
                id=lectio.lectio_id.hex,  # type: ignore
                name=lectio.lectio.name,
                progress=lectio.progress  # type: ignore
            )
            for lectio in lectios_progress
        ],
        course_percent_progress=course_percent_progress
    )
