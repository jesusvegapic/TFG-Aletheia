from typing import Optional, List, Sequence
from src.agora.students.domain.errors import NotEnrolledLectioError, DegreeNotExistsInStudentFacultyError, \
    LectioNotExistsInCourse, StartFinishedLectioError, FinishNotStartedLectioError
from src.agora.students.domain.events import StudentCreated, StudentHasBeenEnrolledInACourse, \
    LectioHasBeenVisitedOnStudentCourse
from src.agora.students.domain.value_objects import LectioStatus
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.application.services import IamService
from src.framework_ddd.iam.domain.entities import PersonalUser
from src.shared.utils.list import find


class Student(PersonalUser):
    __faculty: 'StudentFaculty'
    __degree: GenericUUID
    __courses_in_progress: List['StudentCourse']

    def __init__(
            self,
            id: str,
            name: str,
            firstname: str,
            second_name: str,
            email: str,
            password_hash: bytes,
            faculty: 'StudentFaculty',
            degree: str,
            courses_in_progress: Optional[List['StudentCourse']] = None
    ):
        if faculty.has_degree(degree):
            super().__init__(id, name, firstname, second_name, email, password_hash, False)
            self.__faculty = faculty
            self.__degree = GenericUUID(degree)
            self.__courses_in_progress = courses_in_progress if courses_in_progress else []
        else:
            raise DegreeNotExistsInStudentFacultyError(degree_id=degree, faculty_id=faculty.id)

    @classmethod
    def create(cls,
               id: str,
               name: str,
               firstname: str,
               second_name: str,
               email: str,
               password: str,
               faculty: 'StudentFaculty',
               degree: str
               ):
        student = cls(
            id=id,
            name=name,
            firstname=firstname,
            second_name=second_name,
            email=email,
            password_hash=IamService.hash_password(password),
            faculty=faculty,
            degree=degree
        )
        student._register_event(
            StudentCreated(  # type: ignore
                entity_id=id,
                name=name,
                firstname=firstname,
                second_name=second_name,
                email=email,
                password_hash=IamService.hash_password(password),
                faculty_id=faculty.id,
                degree_id=degree
            )
        )

        return student

    def enroll_in_a_course(self, course: 'StudentCourse'):
        self.__courses_in_progress.append(course)
        self._register_event(StudentHasBeenEnrolledInACourse(entity_id=self.id, course_id=course.course_id))

    def start_lectio_on_a_course(self, course_id: str, lectio: 'StudentLectio'):
        self.__find_lectio(course_id, lectio.id).start()

    def finish_lectio_on_a_course(self, course_id: str, lectio_id: str):
        self.__find_lectio(course_id, lectio_id).finish()

    def set_last_visited_lectio(self, lectio_id: str, course_id: str):
        course = find(lambda course: course.course_id == course_id, self.__courses_in_progress)
        course.set_last_visited_lectio(lectio_id)
        self._register_event(
            LectioHasBeenVisitedOnStudentCourse(
                entity_id=self.id,
                course_id=course_id,
                lectio_id=lectio_id
            )
        )

    def get_last_visited_lectio(self, course_id: str):
        course = find(lambda course: course.course_id == course_id, self.__courses_in_progress)
        return course.last_visited_lectio

    def __find_lectio(self, course_id: str, lectio_id: str) -> 'StudentLectio':
        course = find(lambda course: course.course_id == course_id, self.__courses_in_progress)
        lectio = find(lambda lectio: lectio.id == lectio_id, course.lectios)
        if lectio:
            return lectio
        else:
            raise NotEnrolledLectioError(course_id=course_id, lectio_id=lectio_id)  # type: ignore

    @property
    def faculty(self):
        return self.__faculty

    @property
    def degree(self):
        return self.__degree.hex

    @property
    def courses_in_progress(self):
        return self.__courses_in_progress


class StudentCourse(Entity):
    __course_id: GenericUUID
    __lectios: List['StudentLectio']
    __last_visited_lectio: Optional[GenericUUID]

    def __init__(
            self,
            id: str,
            course_id: str,
            lectios: Optional[List['StudentLectio']] = None,
            last_visited_lectio: Optional['GenericUUID'] = None
    ):
        super().__init__(id)
        self.__course_id = GenericUUID(course_id)
        self.__lectios = lectios if lectios else []
        self.__last_visited_lectio = last_visited_lectio

    def start_lectio(self, lectio: 'StudentLectio'):
        self.__lectios.append(lectio)

    def set_last_visited_lectio(self, lectio_id: str):
        if lectio_id not in [lectio.id for lectio in self.__lectios]:
            raise LectioNotExistsInCourse(lectio_id=lectio_id, course_id=self.id)
        self.__last_visited_lectio = GenericUUID(lectio_id)

    @property
    def course_id(self):
        return self.__course_id.hex

    @property
    def lectios(self):
        return self.__lectios

    @property
    def last_visited_lectio(self):
        return self.__last_visited_lectio


class StudentLectio(Entity):
    __status: LectioStatus

    def __init__(self, id: str, status: Optional[LectioStatus] = None):
        super().__init__(id)
        self.__status = status if status else LectioStatus.NOT_STARTED

    def start(self):
        if self.__status in [LectioStatus.NOT_STARTED, LectioStatus.STARTED]:
            self.__status = LectioStatus.STARTED
        else:
            raise StartFinishedLectioError()

    def finish(self):
        if self.__status in [LectioStatus.STARTED, LectioStatus.FINISHED]:
            self.__status = LectioStatus.FINISHED
        else:
            raise FinishNotStartedLectioError()

    @property
    def status(self):
        return self.__status


class StudentFaculty(Entity):
    __degrees: List['GenericUUID']

    def __init__(self, id: str, degrees: List[GenericUUID]):
        super().__init__(id)
        self.__degrees = degrees

    def has_degree(self, degree: str) -> bool:
        return GenericUUID(degree) in self.__degrees

    @property
    def degrees(self):
        return [degree.hex for degree in self.__degrees]
