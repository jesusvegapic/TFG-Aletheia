class FinishLectio(Command):
    student_id: str
    lectio_id: str


async def finish_lectio(command: FinishLectio, student_repository: StudentRepository, publish):
    student = await student_repository.get_by_id(GenericUUID(command.student_id))
    student.finish_lectio(command.lectio_id)
    student_repository.add(student)
    await publish(student.pull_domain_events())
