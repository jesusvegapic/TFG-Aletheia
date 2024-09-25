from typing import List
from lato import Command
from src.agora.shared.application.queries import GetTeacherName
from src.akademos.conferences.application import akademos_conferences_module
from src.akademos.conferences.domain.entities import Conference
from src.akademos.conferences.domain.repository import ConferenceRepository
from src.akademos.shared.application.dtos import VideoDto


class CreateConference(Command):
    teacher_id: str
    conference_id: str
    name: str
    description: str
    topics: List[str]
    video: VideoDto


@akademos_conferences_module.handler(CreateConference)
async def create_conference(
        command: CreateConference,
        conference_repository: ConferenceRepository,
        publish_query,
        publish
):
    await publish_query(GetTeacherName(teacher_id=command.teacher_id))

    conference = Conference.create(
        id=command.conference_id,
        owner=command.teacher_id,
        name=command.name,
        description=command.description,
        topics=command.topics,
        video=command.video
    )

    await conference_repository.add(conference)

    for event in conference.pull_domain_events():
        await publish(event)
