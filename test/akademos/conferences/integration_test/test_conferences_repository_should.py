from src.akademos.conferences.domain.entities import Conference
from src.akademos.conferences.infrastructure.repository import SqlAlchemyConferenceRepository
from src.framework_ddd.core.domain.value_objects import GenericUUID
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyConferencesRepositoryShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyConferenceRepository(self.session)

    async def test_add_conference(self):
        conference = Conference(
            id=Conference.next_id().hex,
            owner=GenericUUID.next_id().hex,
            name="La panacea de las panaceas",
            description="Una conferencia mas sobre materialismo",
            topics=["Filosofía"],
            video_id=GenericUUID.next_id().hex
        )

        await self.repository.add(conference)
        await self.session.commit()

        actual_conference = await self.repository.get(GenericUUID(conference.id))

        self.assertEqual(actual_conference, conference)
