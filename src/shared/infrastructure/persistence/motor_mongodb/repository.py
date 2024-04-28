# a sentinel value for keeping track of entities removed from the repository
class Removed:
    def __repr__(self):
        return "<Removed entity>"

    def __str__(self):
        return "<Removed entity>"


REMOVED = Removed()


class AsyncMotorGridFsGenericRepository(GenericRepository[GenericUUID, Entity]):
    mapper_class: type[DataMapper[Entity, Base]]
    persistence_model_class: 'GridFsPersistenceModel'

    def __init__(self, bucket: AsyncIOMotorGridFSBucket, session: AsyncIOMotorClientSession, identity_map=None):
        self._session = session
        self._bucket = bucket
        self._identity_map = identity_map or dict()

    @property
    def data_mapper(self):
        return self.mapper_class()

    async def add(self, entity: Entity):
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_persistence_model(entity)
        await self._bucket.upload_from_stream_with_id(
            file_id=bson.Binary.from_uuid(instance.file_id),
            filename=instance.filename,
            source=instance.content,
            metadata=instance.metadata,
            session=self._session
        )

    def map_entity_to_persistence_model(self, entity: Entity) -> 'GridFsPersistenceModel':
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyDataMapper` in the Repository class."
        )

        return self.data_mapper.entity_to_persistence_model(entity)

    async def get(self, id: EntityId) -> Optional[Entity]:
        raise NotImplementedError()

    async def remove(self, entity: Entity):
        raise NotImplementedError()

    async def remove_by_id(self, id: EntityId):
        raise NotImplementedError()

    def collect_events(self):
        pass


@dataclass(kw_only=True)
class GridFsPersistenceModel:
    file_id: UUID
    filename: str
    content: SpooledTemporaryFile
    metadata: dict[str, Any]
