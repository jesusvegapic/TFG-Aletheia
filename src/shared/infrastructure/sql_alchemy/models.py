import uuid

from sqlalchemy import Column, String, Enum, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore

from src.akademos.courses.domain.value_objects import CourseState
from src.framework_ddd.core.infrastructure.database import Base


class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    topics = relationship(
        "TopicModel",
        back_populates="course"
    )
    lectios = relationship(
        "LectioModel",
        back_populates="course"
    )


class LectioModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    course = relationship(CourseModel, back_populates="lectios")


class TopicModel(Base):
    __tablename__ = "topics"
    name = Column(String(255), primary_key=True, nullable=False)
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    course = relationship(CourseModel, back_populates="topics")
