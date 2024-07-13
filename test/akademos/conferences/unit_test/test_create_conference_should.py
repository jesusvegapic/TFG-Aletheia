from unittest.mock import AsyncMock
from src.akademos.conferences.application.commands import CreateConference
from src.akademos.conferences.application.commands.create_conference import create_conference
from src.akademos.conferences.domain.entities import Conference
from src.akademos.conferences.domain.events import ConferenceCreated
from src.akademos.shared.application.dtos import VideoDto
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.akademos.conferences.unit_test.conferences_module import TestConferencesModule
from test.shared.files import TestAsyncBinaryIOProtocol


class CreateConferenceShould(TestConferencesModule):
    async def test_create_valid_conference(self):
        command = CreateConference(
            teacher_id=GenericUUID.next_id().hex,
            conference_id=GenericUUID.next_id().hex,
            name="El medievo",
            description="Vista de pajaro del periodo medieval",
            topics=["Filosofía", "Biología"],
            video=VideoDto(
                video_id=GenericUUID.next_id().hex,
                file=TestAsyncBinaryIOProtocol(),
                filename="garfield.mp4",
                content_type="video/mp4"
            )
        )

        publish_query = AsyncMock()
        publish = AsyncMock()
        self.repository.add = AsyncMock()

        await create_conference(command, self.repository, publish_query, publish)

        args, kwargs = self.repository.add.call_args

        expected_conference = Conference(
            id=command.conference_id,
            owner=command.teacher_id,
            name=command.name,
            description=command.description,
            topics=command.topics,
            video_id=command.video.video_id
        )

        self.assertEqual(args[0], expected_conference)

        expected_event = ConferenceCreated(
            entity_id=expected_conference.id,
            owner=expected_conference.owner,
            name=expected_conference.name,
            description=expected_conference.description,
            topics=expected_conference.topics,
            video=command.video
        )

        args, kwargs = publish.call_args

        self.assertEqual(args[0].event_dump(), expected_event.event_dump())
