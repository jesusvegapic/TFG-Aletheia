from sqlalchemy.ext.asyncio import AsyncSession
from src.agora.shared.application.queries import GetTeacherName, GetTeacherNameResponse
from src.agora.teachers.application import agora_teachers_module
from src.agora.teachers.domain.errors import TeacherNotFoundError
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel

@agora_teachers_module.handler(GetTeacherName)
async def get_teacher(query: GetTeacherName, session: AsyncSession):
    teacher = await session.get(PersonalUserModel, GenericUUID(query.teacher_id))

    if teacher:
        return GetTeacherNameResponse(name=teacher.name, firstname=teacher.firstname)  # type: ignore
    else:
        TeacherNotFoundError(entity_id=query.teacher_id)
