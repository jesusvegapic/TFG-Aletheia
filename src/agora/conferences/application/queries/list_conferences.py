from operator import or_
from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.infrastructure.sql_alchemy.models import ConferenceModel


class ListConferences(Query):
    page_number: int
    courses_by_page: int
    topics: List[str]


class ListConferencesResponse(BaseModel):
    conferences: List['ListedConferenceDto']


class ListedConferenceDto(BaseModel):
    id: str
    name: str
    owner: str


async def list_conferences(query: ListConferences, session: AsyncSession):
    conferences = (
        await session.execute(
            select(ConferenceModel)
            .where(
                or_(
                    *[ConferenceModel.topics.contains(topic) for topic in query.topics]
                ) if len(query.topics) > 1 else ConferenceModel.topics.contains(query.topics[0])
            )
            .offset(query.page_number-1 * query.courses_by_page)
            .limit(query.courses_by_page)
        )
    ).scalars().all()

    return ListConferencesResponse(
        conferences=[
            ListedConferenceDto(
                id=conference.id.hex,
                name=conference.name,  # type: ignore
                owner=conference.owner.hex  # type: ignore
            )
            for conference in conferences
        ]
    )
