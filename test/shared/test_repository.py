from typing import Optional
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.repository import GenericRepository, EntityId


class TestRepository(GenericRepository):
    def add(self, entity: Entity):
        pass

    async def get(self, id: EntityId) -> Optional[Entity]:
        pass

    async def remove(self, entity: Entity):
        pass

    async def remove_by_id(self, id: EntityId):
        pass

    def collect_events(self):
        pass
