from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends
from lato import Application
from apps.aletheia.api.dependencies import get_application
from apps.aletheia.api.models.teachers import PutTeacherRequest
from src.akademos.teachers.application.commands.sign_up_teacher import SignUpTeacher

router = APIRouter()


@router.put(
    "/teachers/{teacher_id}", status_code=201
)
@inject
async def put_teacher(
        teacher_id: str,
        request_body: PutTeacherRequest,
        application: Annotated[Application, Depends(get_application)]
):
    command = SignUpTeacher(
        teacher_id=teacher_id,
        name=request_body.name,
        firstname=request_body.firstname,
        second_name=request_body.second_name,
        email=request_body.email,
        password=request_body.password,
        faculty_id=request_body.faculty,
        degrees=request_body.degrees,
        position=request_body.position
    )

    await application.execute_async(command)
