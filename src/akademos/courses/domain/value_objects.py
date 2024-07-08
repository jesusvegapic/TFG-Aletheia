
from enum import StrEnum

from src.akademos.courses.domain.errors import CourseNameError, CourseDescriptionError




class CourseName(str):
    def __new__(cls, name: str):
        if name.__len__() > CourseName.max_length():
            raise CourseNameError(name, CourseName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100


class CourseDescription(str):
    def __new__(cls, description: str):
        if description.__len__() > CourseDescription.max_length():
            raise CourseDescriptionError(description, CourseDescription.max_length())
        return super().__new__(cls, description)

    @classmethod
    def max_length(cls):
        return 1000


class LectioName(str):
    def __new__(cls, name: str):
        if name.__len__() > CourseName.max_length():
            raise CourseNameError(name, CourseName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100


class LectioDescription(str):
    def __new__(cls, description: str):
        if description.__len__() > CourseDescription.max_length():
            raise CourseDescriptionError(description, CourseDescription.max_length())
        return super().__new__(cls, description)

    @classmethod
    def max_length(cls):
        return 1000


class Topic(StrEnum):
    Ciencias_sociales_y_humanidades = "Ciencias sociales y humanidades"
    Antropologia = "Antropologia"
    Historia = "Historia"
    Psicologia = "Psicología"
    Sociologia = "Sociología"
    Filosofia = "Filosofía"
    Ciencias_politicas = "Ciencias políticas"
    Relaciones_internacionales = "Relaciones internacionales"
    Estudios_culturales = "Estudios culturales"
    Literatura = "Literatura"
    Linguistica = "Lingüistica"
    Educacion = "Educación"
    Ciencias_naturales_y_matematicas = "Ciencias naturales y matemáticas"
    Biologia = "Biología"
