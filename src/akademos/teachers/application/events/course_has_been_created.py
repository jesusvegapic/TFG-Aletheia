async def course_has_been_created(event: CourseHasBeenCreated, teacher_repository: TeacherRepository):
    teacher = await teacher_repository.get_by_id(event.course_owner)
    if teacher:
        teacher.create_course(GenericUUID(event.entity_id))
        teacher_repository.add(teacher)
    else:
        EntityNotFoundException(repository=teacher_repository, entity_id=event.course_owner)
