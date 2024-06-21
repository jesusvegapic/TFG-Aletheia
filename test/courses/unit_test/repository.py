from typing import Optional

from src.Academia.courses.domain.repository import CourseRepository
from src.shared.domain.ddd.repository import EntityId, Entity


class TestCourseRepository(CourseRepository):
    def add(self, entity: Entity):
        pass

    async def get(self, id: EntityId) -> Optional[Entity]:  # type: ignore
        pass

    async def remove(self, entity: Entity):
        pass

    async def remove_by_id(self, id: EntityId):
        pass

    def collect_events(self):
        pass
