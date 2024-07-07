import uuid
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore
from src.akademos.courses.domain.value_objects import CourseState, Topic
from src.framework_ddd.core.infrastructure.database import Base


class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    owner = Column(UUIDType(binary=False), default=uuid.uuid4(), nullable=False)  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    state = Column(Enum(CourseState), nullable=False)  # type: ignore
    topics = Column(String(255), nullable=False)
    lectios = relationship(
        "LectioModel",
        back_populates="course",
        lazy="selectin"
    )


class LectioModel(Base):
    __tablename__ = "lectios"
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4())  # type: ignore
    course_id = Column(UUIDType(binary=False), ForeignKey(CourseModel.id))  # type: ignore
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    video_id = Column(UUIDType(binary=False))  # type: ignore
    course = relationship(CourseModel, back_populates="lectios")
