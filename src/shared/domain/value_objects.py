from enum import StrEnum


class CourseState(StrEnum):
    CREATED = "CREATED"
    PUBLISHED = "PUBLISHED"


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
