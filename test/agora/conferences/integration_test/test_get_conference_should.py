from re import split

from src.agora.conferences.application.queries.get_conference import GetConference, GetConferenceResponse, \
    get_conference
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.infrastructure.sql_alchemy.models import ConferenceModel, TeacherModel, TeacherDegreesModel
from test.shared.database import TestInMemorySqlDatabase


class GetConferenceShould(TestInMemorySqlDatabase):
    async def test_get_conference(self):
        faculty_id = GenericUUID.next_id()
        degree_id = GenericUUID.next_id()
        self.session.add(
            FacultyModel(
                id=faculty_id,
                name="Derecho",
                degrees=[
                    DegreeModel(
                        id=degree_id,
                        name="Derecho"
                    ),
                    DegreeModel(
                        id=GenericUUID.next_id(),
                        name="Filosofía"
                    )
                ]
            )
        )

        teacher_id = GenericUUID.next_id()

        self.session.add(
            TeacherModel(
                personal_user_id=teacher_id,
                faculty_id=faculty_id,
                position="FULL_PROFESSOR",
                degrees=[TeacherDegreesModel(
                    id=degree_id,
                    teacher_id=teacher_id
                )],
                personal_user=PersonalUserModel(
                    user_id=teacher_id,
                    name="pepito",
                    firstname="gonzalez",
                    second_name="perez",
                    user=UserModel(
                        id=teacher_id,
                        email="pepito@gmail.com",
                        password="dadada",
                        is_superuser=True
                    )
                )
            )
        )

        conference_id = GenericUUID.next_id()
        video_id = GenericUUID.next_id()
        conference_instance = ConferenceModel(
            id=conference_id,
            owner=teacher_id,
            name="Kant vs hegel",
            description="La panacea de la historia de la filosofía",
            topics="Filosofía;Biología",
            video_id=video_id
        )

        self.session.add(conference_instance)

        await self.session.commit()

        query = GetConference(
            conference_id=conference_id.hex
        )

        expected_response = GetConferenceResponse(
            id=conference_id.hex,
            owner=teacher_id.hex,
            name="Kant vs hegel",
            description="La panacea de la historia de la filosofía",
            topics=["Filosofía", "Biología"],
            video_id=video_id.hex
        )

        response = await get_conference(query, self.session)

        self.assertEqual(response, expected_response)
