from typing import Annotated

from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import Application

from apps.aletheia.api.dependencies import get_application
from apps.aletheia.api.models.faculties import PutFacultyRequest
from src.akademos.faculties.application.commands import CreateFaculty
from src.akademos.faculties.application.queries import GetFaculty

router = APIRouter()


@router.put(
    "/faculties/{faculty_id}", status_code=201
)
@inject
async def put_faculty(
        faculty_id: str,
        request_body: PutFacultyRequest,
        application: Annotated[Application, Depends(get_application)]
):
    command = CreateFaculty(
        faculty_id=faculty_id,
        name=request_body.name,
        degrees=request_body.degrees
    )

    await application.execute_async(command)


@router.get("/faculties/{faculty_id}", status_code=200)
@inject
async def get_faculty(
        faculty_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = GetFaculty(faculty_id=faculty_id)
    response = await application.execute_async(query)
    return response
