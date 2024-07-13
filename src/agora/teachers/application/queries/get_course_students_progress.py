from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agora.shared.application.queries import LectioProgressDto
from src.agora.students.domain.value_objects import LectioStatus
from src.agora.students.infrastructure.repository import StudentCourseModel, StudentLectioModel
from src.agora.teachers.application import agora_teachers_module
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.utils.list import find


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

@agora_teachers_module.handler(GetCourseStudentsProgress)
async def get_course_students_progress(query: GetCourseStudentsProgress, session: AsyncSession):
    students_courses = (
        await session.execute(
            select(StudentCourseModel)
            .where(
                StudentCourseModel.course_id == GenericUUID(query.course_id))
            )
    ).scalars().all()

    if find(lambda student_course: student_course.course.owner != GenericUUID(query.teacher_id), students_courses):
        raise Exception

    return GetCourseStudentsProgressResponse(
        students_progress=[
            StudentCourseProgressDto(
                id=student_course.student.personal_user_id.hex,
                name=student_course.student.personal_user.name,
                firstname=student_course.student.personal_user.firstname,
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
    return int(
        len(list(filter(lambda lectio: lectio.progress == LectioStatus.FINISHED, lectios))) * 100 /
        len(lectios)
    )
