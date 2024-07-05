from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType  # type: ignore
from src.akademos.faculties.domain.value_objects import FacultyName
from src.framework_ddd.core.infrastructure.database import Base


class FacultyModel(Base):
    __tablename__ = "faculties"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    name = Column(String(FacultyName.max_length()), nullable=False)
    degrees = relationship('DegreeModel', back_populates="faculty", lazy="selectin")
    #student = relationship('StudentModel', back_populates="faculty")
    #teacher = relationship('TeacherModel', back_populates="faculty")


class DegreeModel(Base):
    __tablename__ = "degrees"
    id = Column(UUIDType(binary=False), primary_key=True)  # type: ignore
    faculty_id = Column(UUIDType(binary=False), ForeignKey(FacultyModel.id))  # type: ignore
    name = Column(String(FacultyName.max_length()), nullable=False)
    faculty = relationship(FacultyModel, back_populates="degrees")
    #student = relationship('StudentModel', back_populates="degree")

