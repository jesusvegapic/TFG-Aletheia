import uuid
from sqlalchemy_utils import UUIDType  # type: ignore

from src.admin.courses.domain.entities import Course, Lectio
from src.admin.courses.domain.repository import CourseRepository
from src.admin.courses.domain.value_objects import CourseState, CourseName, CourseDescription, LectioName, LectioDescription
from src.shared.domain.ddd.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.ddd_repositories.data_mapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository


def deserialize_id(value: str) -> GenericUUID:
    if isinstance(value, uuid.UUID):
        return GenericUUID(value.hex)
    return GenericUUID(value)


class CourseDataMapper(DataMapper):

    def persistence_model_to_entity(self, instance: CoursePersistenceModel) -> Course:
        def lectio_persistence_model_to_entity(lectio_instance: LectioPersistenceModel) -> Lectio:
            return Lectio(
                id=deserialize_id(lectio_instance.id),  # type: ignore
                name=LectioName(lectio_instance.name),  # type: ignore
                description=LectioDescription(lectio_instance.description)  # type: ignore
            )

        return Course(
            id=deserialize_id(instance.id),  # type: ignore
            owner=deserialize_id(instance.owner),  # type: ignore
            name=CourseName(instance.name),  # type: ignore
            description=CourseDescription(instance.description),  # type: ignore
            state=CourseState(instance.state),  # type: ignore
            lectios=[lectio_persistence_model_to_entity(lectio_instance) for lectio_instance in instance.lectios]
        )

    def entity_to_persistence_model(self, course: Course) -> CoursePersistenceModel:
        def lectio_entity_to_persistence_model(lectio: Lectio):
            return LectioPersistenceModel(
                id=lectio.id,
                course_id=course.id,
                name=lectio.name,
                description=lectio.description
            )

        return CoursePersistenceModel(
            id=course.id,
            owner=course.owner,
            name=course.name,
            description=course.description,
            state=course.state,
            lectios=[lectio_entity_to_persistence_model(lectio) for lectio in course.lectios]
        )


class SqlCourseRepository(SqlAlchemyGenericRepository, CourseRepository):
    mapper_class = CourseDataMapper
    persistence_model_class = CoursePersistenceModel
