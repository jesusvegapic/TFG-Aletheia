
from enum import StrEnum

from src.courses.domain.errors import CourseNameError, CourseDescriptionError


class CourseState(StrEnum):
    CREATED = "CREATED"


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
