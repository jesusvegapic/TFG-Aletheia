from fractal_specifications.generic.operators import EqualsSpecification

from src.platform.students.domain.repository import StudentRepository


async def course_has_been_created(event: CourseHasBeenCreated, student_repository: StudentRepository):
    students = await student_repository.match(
        EqualsSpecification(
            "teacher_courses_subscriptions__teacher_id",
            event.teacher_id
        ).
    )

