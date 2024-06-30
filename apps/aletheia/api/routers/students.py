from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import Application
from apps.aletheia.api.dependencies import get_application
from src.agora.students.application.commands.enroll_in_a_course import EnrollInACourse

router = APIRouter()


@router.put(
    "/students/{student_id}/courses/{course_id}", status_code=201
)
@inject
async def put_enrolled_course(
        student_id: str,
        course_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    command = EnrollInACourse(
        student_id=student_id,
        course_id=course_id
    )

    await application.execute_async(command)
    