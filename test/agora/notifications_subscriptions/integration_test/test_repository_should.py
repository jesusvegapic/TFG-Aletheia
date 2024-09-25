from src.agora.notifications_subscriptions.domain.entities import TeacherCoursesSubscription
from src.agora.notifications_subscriptions.infrastructure.repository import \
    SqlAlchemyNotificationsSubscriptionRepository
from src.agora.shared.infrastructure.models import FacultyModel, DegreeModel
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.infrastructure.user_model import PersonalUserModel, UserModel
from src.shared.infrastructure.sql_alchemy.models import TeacherModel, TeacherDegreesModel
from test.shared.database import TestInMemorySqlDatabase


class SqlAlchemyNotificationsSubscriptionRepositoryShould(TestInMemorySqlDatabase):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.repository = SqlAlchemyNotificationsSubscriptionRepository(self.session)

    async def test_add_valid_teacher_course_subscription(self):
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

        subscription = TeacherCoursesSubscription(
            id=TeacherCoursesSubscription.next_id().hex,
            subscriber_id=GenericUUID.next_id().hex,
            teacher_id=GenericUUID.next_id().hex,
            topics=["Filosofía", "Biología"]
        )

        await self.repository.add(subscription)

        await self.session.commit()

        actual_subscription = await self.repository.get(GenericUUID(subscription.id))

        self.assertEqual(actual_subscription, subscription)
