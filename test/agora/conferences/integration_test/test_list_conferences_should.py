from src.agora.conferences.application.queries.list_conferences import list_conferences, ListConferences, \
    ListConferencesResponse, ListedConferenceDto
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.infrastructure.sql_alchemy.models import TeacherModel, ConferenceModel, TeacherDegreesModel
from test.shared.database import TestInMemorySqlDatabase


class ListConferencesShould(TestInMemorySqlDatabase):
    async def test_list_conferences(self):
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

        first_conference_id = GenericUUID.next_id()
        second_conference_id = GenericUUID.next_id()
        video_id = GenericUUID.next_id()
        first_conference_instance = ConferenceModel(
            id=first_conference_id,
            owner=teacher_id,
            name="Kant vs hegel",
            description="La panacea de la historia de la filosofía",
            topics="Filosofía;Biología",
            video_id=video_id
        )

        second_conference_instance = ConferenceModel(
            id=second_conference_id,
            owner=teacher_id,
            name="Materialismo filosófico",
            description="La panacea de la historia de la filosofía",
            topics="Filosofía;Biología",
            video_id=video_id
        )

        self.session.add(first_conference_instance)
        self.session.add(second_conference_instance)
        await self.session.commit()

        query = ListConferences(
            page_number=1,
            courses_by_page=15,
            topics=["Filosofía"]
        )

        response = await list_conferences(query, self.session)

        expected_response = ListConferencesResponse(
            conferences=[
                ListedConferenceDto(
                    id=first_conference_id.hex,
                    owner=teacher_id.hex,
                    name="Kant vs hegel"
                ),
                ListedConferenceDto(
                    id=second_conference_id.hex,
                    owner=teacher_id.hex,
                    name="Materialismo filosófico"
                )
            ]
        )

        self.assertEqual(response, expected_response)
