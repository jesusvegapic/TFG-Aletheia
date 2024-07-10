from operator import or_
from typing import List
from lato import Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
                )
            )
            .offset(query.page_number * query.courses_by_page)
            .limit(query.courses_by_page)
        )
    ).scalars().all()

    return ListConferencesResponse(
        conferences=[
            ListedConferenceDto(
                id=conference.id.hex,
                name=conference.name,
                owner=conference.owner
            )
            for conference in conferences
        ]
    )
