from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.akademos.faculties.domain.entities import Faculty, Degree
from src.akademos.faculties.domain.repository import FacultyRepository
from src.framework_ddd.core.infrastructure.datamapper import DataMapper, MapperEntity, MapperModel
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository


class FacultyDataMapper(DataMapper):

    def model_to_entity(self, instance: FacultyModel) -> Faculty:
        return Faculty(
            id=instance.id.hex,
            name=instance.name,  # type: ignore
            degrees=[
                Degree(
                    id=degree.id.hex,
                    name=degree.name
                )
                for degree in instance.degrees
            ]
        )

    def entity_to_model(self, faculty: Faculty) -> FacultyModel:
        return FacultyModel(
            id=faculty.id,
            name=faculty.name,
            degrees=[
                DegreeModel(
                    id=degree.id,
                    name=degree.name
                )
                for degree in faculty.degrees
            ]
        )


class SqlAlchemyFacultyRepository(FacultyRepository, SqlAlchemyGenericRepository):
    model_class = FacultyModel
    mapper_class = FacultyDataMapper
