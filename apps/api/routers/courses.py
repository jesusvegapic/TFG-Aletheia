from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from lato import Application

from apps.api.dependencies import get_application
from apps.api.models.courses import CreateCourseRequest
from src.courses.application.commands.create_course import CreateCourse
from src.shared.domain.value_objects import GenericUUID

router = APIRouter()


@router.post(
    "/courses/create_course", status_code=201, tags=["courses"], response_model=None
)
@inject
async def create_course(
    request_body: CreateCourseRequest,
    application: Annotated[Application, Depends(get_application)]
):
    command = CreateCourse(
        teacher_id=request_body.teacher_id,
        name=request_body.name,
        description=request_body.description
    )

    await application.execute_async(command)
