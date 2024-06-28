from typing import Optional, List, Set
from src.agora.students.domain.errors import NotEnrolledLectioError
from src.agora.students.domain.value_objects import LectioStatus
from src.akademos.courses.domain.value_objects import Topic
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID
from src.framework_ddd.iam.domain.entities import PersonalUser
from src.shared.utils.list import find


class Student(PersonalUser):
    __faculty: GenericUUID
    __degree: GenericUUID
    __courses_in_progress: Set['StudentCourse']
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
            faculty: str,
            degree: str,
            courses_in_progress: Optional[Set['StudentCourse']] = None,
            last_visited_lectio: Optional['StudentLectio'] = None
    ):
        super().__init__(id, name, firstname, second_name, email, password_hash, is_superuser)
        self.__faculty = GenericUUID(faculty)
        self.__degree = GenericUUID(degree)
        self.__courses_in_progress = courses_in_progress if courses_in_progress else set()
        self.__last_visited_lectio = last_visited_lectio

    def enroll_in_a_course(self, course: 'StudentCourse'):
        self.__courses_in_progress.add(course)

    def start_lectio_in_course(self, course_id: str, lectio: 'StudentLectio'):
        course = next(find(lambda course: course.id == course_id, self.__courses_in_progress))
        if course:
            course.start_lectio(lectio)

    def finish_lectio(self, course_id: str, lectio_id: str):
        self.__find_lectio(course_id, lectio_id).finish()

    def set_last_visited_lectio(self, course_id: str, lectio_id: str):
        self.__last_visited_lectio = self.__find_lectio(course_id, lectio_id)

    def __find_lectio(self, course_id: str, lectio_id: str) -> 'StudentLectio':
        lectios = find(lambda course: course.id == course_id, self.__courses_in_progress)
        lectio = next(find(lambda lectio: lectio.id == lectio_id, lectios))
        if lectio:
            return lectio
        else:
            raise NotEnrolledLectioError(course_id=course_id, lectio_id=lectio_id)  # type: ignore


class StudentCourse(Entity):
    __lectios: Set['StudentLectio']

    def __init__(self, id: str, lectios: Optional[Set['StudentLectio']] = None):
        super().__init__(id)
        self.__lectios = lectios if lectios else set()

    def start_lectio(self, lectio: 'StudentLectio'):
        self.__lectios.add(lectio)

    @property
    def lectios(self):
        return self.__lectios


class StudentLectio(Entity):
    __status: LectioStatus

    def __init__(self, id: str, status: Optional[LectioStatus] = None):
        super().__init__(id)
        self.__status = status if status else LectioStatus.STARTED

    def finish(self):
        self.__status = LectioStatus.FINISHED


class TeacherCoursesSubscription(Entity):
    __teacher_id: GenericUUID
    __topics: list[Topic]

    def __init__(self, id: str, teacher_id: str, topics: List[str]):
        super().__init__(id)
        self.__teacher_id = GenericUUID(teacher_id)
        self.__topics = [Topic(topic) for topic in topics]
