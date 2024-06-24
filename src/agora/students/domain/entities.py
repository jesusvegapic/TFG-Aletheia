from typing import Optional, List, Set

from pydantic import BaseModel

from src.agora.students.domain.errors import DegreeNotExistsInStudentFacultyError, NotEnrolledLectioError, \
    CantStartFinishedLectioError, CantFinishNotStartedLectioError
from src.agora.students.domain.value_objects import LectioStatus
from src.akademos.courses.domain.value_objects import Topic
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID, FacultyName
from src.framework_ddd.iam.domain.entities import PersonalUser
from src.shared.utils.list import flatmap, find


class Student(PersonalUser):
    __faculty: 'Faculty'
    __degree: GenericUUID
    __courses_in_progress: List['StudentCourse']
    __last_visited_lectio: Optional['StudentLectio']

    def __init__(
            self,
            id: str,
            name: str,
            firstname: str,
            second_name: str,
            email: str,
            password_hash: bytes,
            is_superuser: bool,
            faculty: 'Faculty',
            degree: str,
            courses_in_progress: Optional[List['StudentCourse']] = None,
            last_visited_lectio: Optional['StudentLectio'] = None
    ):
        if not faculty.has_degree(degree):
            raise DegreeNotExistsInStudentFacultyError(id=id, degree=degree, faculty=faculty.name)

        super().__init__(id, name, firstname, second_name, email, password_hash, is_superuser)
        self.__faculty = faculty
        self.__degree = GenericUUID(degree)
        self.__courses_in_progress = courses_in_progress if courses_in_progress else []
        self.__last_visited_lectio = last_visited_lectio

    @classmethod
    def create(
            cls,
            id: str,
            name: str,
            firstname: str,
            second_name: str,
            email: str,
            password_hash: bytes,
            is_superuser: bool,
            faculty: 'Faculty',
            degree: str
    ):
        return cls(id, name, firstname, second_name, email, password_hash, is_superuser, faculty, degree)

    def enroll_in_a_course(self, course: 'StudentCourse'):
        self.__courses_in_progress.append(course)

    def start_lectio(self, lectio_id: str):
        lectio = self.__find_lectio(lectio_id)
        lectio.start()

    def finish_lectio(self, lectio_id: str):
        lectio = self.__find_lectio(lectio_id)
        lectio.finish()

    def set_last_visited_lectio(self, lectio_id: str):
        self.__last_visited_lectio = self.__find_lectio(lectio_id)

    def __find_lectio(self, lectio_id: str) -> 'StudentLectio':
        lectios = flatmap(lambda course: course.lectios, self.__courses_in_progress)
        lectio = find(lambda lectio: lectio.id == lectio_id, lectios)
        if lectio:
            return lectio
        else:
            raise NotEnrolledLectioError()


class StudentCourse(Entity):
    __lectios: List['StudentLectio']

    def __init__(self, id: str, lectios: List['StudentLectio']):
        super().__init__(id)
        self.__lectios = lectios

    @property
    def lectios(self):
        return self.__lectios


class StudentLectio(Entity):
    __status: LectioStatus

    def __init__(self, id: str, status: Optional[LectioStatus] = None):
        super().__init__(id)
        self.__status = status if status else LectioStatus.NOT_STARTED

    def start(self):
        if self.__status is LectioStatus.NOT_STARTED or self.__status is LectioStatus.STARTED:
            self.__status = LectioStatus.STARTED
        else:
            raise CantStartFinishedLectioError()

    def finish(self):
        if self.__status is LectioStatus.STARTED or self.__status is LectioStatus.FINISHED:
            self.__status = LectioStatus.FINISHED
        else:
            raise CantFinishNotStartedLectioError()


class Faculty(Entity):
    __name: FacultyName
    __degrees: List[GenericUUID]

    def __init__(self, id: str, name: str, degrees: List[str]):
        super().__init__(id)
        self.__name = FacultyName(name)
        self.__degrees = [GenericUUID(degree) for degree in degrees]

    def has_degree(self, degree: str) -> bool:
        return GenericUUID(degree) in self.__degrees

    @property
    def name(self):
        return self.__name


class TeacherCoursesSubscription(Entity):
    __teacher_id: GenericUUID
    __topics: list[Topic]

    def __init__(self, id: str, teacher_id: str, topics: List[str]):
        super().__init__(id)
        self.__teacher_id = GenericUUID(teacher_id)
        self.__topics = [Topic(topic) for topic in topics]
