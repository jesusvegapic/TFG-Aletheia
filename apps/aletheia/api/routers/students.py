from typing import Annotated
from dependency_injector.wiring import inject
from fastapi import APIRouter
from fastapi.params import Depends
from lato import Application
from apps.aletheia.api.dependencies import get_application
from apps.aletheia.api.models.students import PutStudentRequest
from src.agora.students.application.commands.enroll_in_a_course import EnrollInACourse
from src.agora.students.application.commands.set_last_visited_lectio import SetLastVisitedLectio
from src.agora.students.application.commands.sing_up_student import SignUpStudent
from src.agora.students.application.queries import GetLastVisitedLectio
from src.agora.students.application.queries.list_courses_enrolled import ListCoursesEnrolled

router = APIRouter()


@router.put(
    "/students/{student_id}", status_code=201
)
@inject
async def put_student(
        student_id: str,
        request_body: PutStudentRequest,
        application: Annotated[Application, Depends(get_application)]
):
    command = SignUpStudent(
        student_id=student_id,
        name=request_body.name,
        firstname=request_body.firstname,
        second_name=request_body.second_name,
        email=request_body.email,
        password=request_body.password,
        faculty=request_body.faculty,
        degree=request_body.degree
    )

    await application.execute_async(command)


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


@router.get(
    "/students/{student_id}/courses", status_code=200
)
@inject
async def get_enrolled_courses(
        student_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = ListCoursesEnrolled(student_id=student_id)
    response = await application.execute_async(query)
    return response


@router.put(
    "/students/{student_id}/courses/{course_id}/lectios/{lectio_id}", status_code=200
)
@inject
async def put_last_visited_lectio_on_student_course(
        student_id: str,
        course_id: str,
        lectio_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    command = SetLastVisitedLectio(
        student_id=student_id,
        course_id=course_id,
        lectio_id=lectio_id
    )

    await application.execute_async(command)


@router.get(
    "/students/{student_id}/courses/{course_id}/lectios", status_code=200
)
@inject
async def get_last_visited_lectio_on_student_curse(
        student_id: str,
        course_id: str,
        application: Annotated[Application, Depends(get_application)]
):
    query = GetLastVisitedLectio(
        student_id=student_id,
        course_id=course_id
    )

    response = await application.execute_async(query)
    return response
