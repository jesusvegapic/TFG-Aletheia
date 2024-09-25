from typing import List

from src.akademos.teachers.domain.errors import DegreeNotExistsInTeacherFacultyError
from src.akademos.teachers.domain.events import TeacherCreated
from src.akademos.teachers.domain.value_objects import TeacherPosition
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.domain.entities import PersonalUser


class Teacher(PersonalUser):
    __faculty: 'TeacherFaculty'
    __degrees: List[GenericUUID]
    __position: TeacherPosition

    def __init__(
            self,
            id: str,
            email: str,
            hashed_password: bytes,
            name: str,
            firstname: str,
            second_name: str,
            faculty: 'TeacherFaculty',
            degrees: List[str],
            position: str

    ):
        if faculty.has_degrees(degrees):
            super().__init__(id, name, firstname, second_name, email, hashed_password, True)
            self.__faculty = faculty
            self.__position = TeacherPosition(position)
            self.__degrees = [GenericUUID(degree) for degree in degrees]
        else:
            raise DegreeNotExistsInTeacherFacultyError(degrees_ids=degrees, faculty_id=faculty.id)

    @classmethod
    def create(
            cls,
            id: str,
            email: str,
            password: str,
            name: str,
            firstname: str,
            second_name: str,
            faculty: 'TeacherFaculty',
            degrees: List[str],
            position: str
    ):
        teacher = cls(
            id,
            email,
            IamService.hash_password(password),
            name,
            firstname,
            second_name,
            faculty,
            degrees,
            position
        )

        teacher._register_event(
            TeacherCreated(
                entity_id=id,
                email=email,
                name=name,
                firstname=firstname,
                second_name=second_name,
                faculty_id=faculty.id,
                degrees=degrees,
                position=position
            )
        )

        return teacher

    @property
    def faculty(self):
        return self.__faculty

    @property
    def degrees(self):
        return [degree.hex for degree in self.__degrees]

    @property
    def position(self) -> str:
        return self.__position


class TeacherFaculty(Entity):
    __degrees: List[GenericUUID]

    def __init__(self, id: str, degrees: List[GenericUUID]):
        super().__init__(id)
        self.__degrees = degrees

    def has_degrees(self, degrees: List[str]):
        for degree in degrees:
            if GenericUUID(degree) not in self.__degrees:
                return False
        return True
