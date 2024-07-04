from fastapi import Query


class ListCoursesEnrolled(Query):
    student_id: str


async def list_courses_enrolled(query: ListCoursesEnrolled, session: AsyncSession, publish) -> ListedCoursesDao:
    student_model = await session.get(StudentModel, query.student_id)

    if student:
        return courses_daos_to_listed_course_dao([publish(GetCourse(course.id)) for course in student_model.courses])
    else:
        raise EntityNotFoundException(repository=student_repository, student_id=student.id)
