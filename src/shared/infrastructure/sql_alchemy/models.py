from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.framework_ddd.core.infrastructure.sql_alchemy.sql_alchemy_database import Base


class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    lectios = relationship(
        "LectioModel",
        back_populates="course",
        lazy="joined"
    )


class LectioModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CoursePersistenceModel.id))  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    course = relationship(CourseModel, back_populates="lectios")
