from src.shared.infrastructure.persistence.sql_alchemy.database import Base


class CoursePersistenceModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    lectios = relationship(
        "LectioPersistenceModel",
        back_populates="course",
        lazy="joined"
    )


class LectioPersistenceModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CoursePersistenceModel.id))  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    course = relationship(CoursePersistenceModel, back_populates="lectios")
