from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.agora.shared.application.queries import LectioProgressDto
from src.agora.students.domain.value_objects import LectioStatus
from src.agora.students.infrastructure.repository import StudentCourseModel, StudentModel, StudentLectioModel
from src.framework_ddd.core.domain.value_objects import GenericUUID


class GetCourseStudentsProgress(Query):
    teacher_id: str
    course_id: str


class GetCourseStudentsProgressResponse(BaseModel):
    students_progress: List['StudentCourseProgressDto']


class StudentCourseProgressDto(BaseModel):
    id: str
    name: str
    firstname: str
    second_name: str
    progress: List['LectioProgressDto']
    course_percent_progress: int


async def get_course_students_progress(query: GetCourseStudentsProgress, session: AsyncSession):
    students_courses = (
        await session.execute(
            select(StudentCourseModel)
            .options(
                joinedload(StudentCourseModel.student).joinedload(StudentModel.personal_user),
                joinedload(StudentCourseModel.course),
                joinedload(StudentCourseModel.lectios_in_progress)
            )
            .where(
                StudentCourseModel.id == GenericUUID(query.course_id) and
                StudentCourseModel.course.owner == GenericUUID(query.teacher_id)
            )
        )
    ).scalars().all()

    return GetCourseStudentsProgressResponse(
        students_progress=[
            StudentCourseProgressDto(
                id=student_course.student.id.hex,
                name=student_course.student.personal_user.name,
                firstname=student_course.student.personal_user.firtname,
                second_name=student_course.student.personal_user.second_name,
                progress=[
                    LectioProgressDto(
                        id=lectio.lectio_id.hex,
                        name=lectio.lectio.name,
                        progress=lectio.progress
                    )
                    for lectio in student_course.lectios_in_progress
                ],
                course_percent_progress=course_percent_progress(student_course.lectios_in_progress)
            )
            for student_course in students_courses
        ]
    )


def course_percent_progress(lectios: List[StudentLectioModel]):
    return (
            len(filter(lambda lectio: lectio.progress == LectioStatus.FINISHED, lectios)) /
            len(lectios)
    ) * 100
