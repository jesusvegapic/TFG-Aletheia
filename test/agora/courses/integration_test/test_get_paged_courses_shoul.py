from src.agora.courses.application.queries import list_courses
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.shared.domain.value_objects import CourseState
from src.shared.infrastructure.sql_alchemy.models import CourseModel
from test.shared.database import TestInMemorySqlDatabase


class GetPagedCoursesShould(TestInMemorySqlDatabase):

    async def test_get_a_valid_page(self):
        course_ids = map(lambda _: GenericUUID.next_id().hex, range(50))
        course_instances = map(
            lambda course_id:
            CourseModel(
                id=course_id,
                owner=GenericUUID.next_id().hex,
                name="kant vs hegel",
                description="La panacea de la filosofia",
                topics="Filosofía;Linguistica",
                state=CourseState.PUBLISHED
            ),
            course_ids
        )

        for instance in course_instances:
            self.session.add(instance)

        await self.session.commit()

        instances_page = await list_courses.get_paged_courses(self.session, 0, 15)

        self.assertTrue(len(instances_page) == 15)

        second_instances_page = await list_courses.get_paged_courses(self.session, 15, 15)

        print(instances_page)
        print(second_instances_page)

        for instance in instances_page:
            self.assertTrue(instance.id not in [second_instance.id for second_instance in second_instances_page])
