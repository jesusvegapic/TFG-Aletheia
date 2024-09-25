from re import split
from src.akademos.conferences.domain.entities import Conference
from src.akademos.conferences.domain.repository import ConferenceRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.core.infrastructure.datamapper import DataMapper
from src.framework_ddd.core.infrastructure.repository import SqlAlchemyGenericRepository
from src.shared.infrastructure.sql_alchemy.models import ConferenceModel


class ConferenceDataMapper(DataMapper):

    def model_to_entity(self, instance: ConferenceModel) -> Conference:
        return Conference(
            id=instance.id.hex,
            owner=instance.owner.hex,
            name=instance.name,  # type: ignore
            description=instance.description,  # type: ignore
            topics=split(";", instance.topics),  # type: ignore
            video_id=instance.video_id.hex
        )

    def entity_to_model(self, entity: Conference) -> ConferenceModel:
        return ConferenceModel(
            id=GenericUUID(entity.id),
            owner=GenericUUID(entity.owner),
            name=entity.name,
            description=entity.description,
            topics=";".join(entity.topics),
            video_id=entity.video_id
        )


class SqlAlchemyConferenceRepository(SqlAlchemyGenericRepository, ConferenceRepository):
    model_class = ConferenceModel
    mapper_class = ConferenceDataMapper
