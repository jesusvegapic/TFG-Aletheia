from re import split
from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.agora.conferences.application import agora_conferences_module
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.infrastructure.sql_alchemy.models import ConferenceModel


class GetConference(Query):
    conference_id: str


class GetConferenceResponse(BaseModel):
    id: str
    owner: str
    name: str
    description: str
    topics: List[str]
    video_id: str


@agora_conferences_module.handler(GetConference)
async def get_conference(query: GetConference, session: AsyncSession):
    conference_instance = await session.get(ConferenceModel, GenericUUID(query.conference_id))
    if conference_instance:
        return GetConferenceResponse(
            id=conference_instance.id.hex,
            owner=conference_instance.owner.hex,
            name=conference_instance.name,  # type: ignore
            description=conference_instance.description,  # type: ignore
            topics=split(";", conference_instance.topics),  # type: ignore
            video_id=conference_instance.video_id.hex
        )
