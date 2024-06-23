from typing import Optional, List, Set

from src.agora.students.domain.errors import DegreeNotExistsInStudentFacultyError, NotEnrolledLectioError, \
    CantStartFinishedLectioError, CantFinishNotStartedLectioError
from src.agora.students.domain.value_objects import LectioStatus
from src.akademos.courses.domain.value_objects import Topic
from src.framework_ddd.core.domain.entities import Entity
from src.framework_ddd.core.domain.value_objects import GenericUUID, FacultyName
from src.framework_ddd.iam.domain.entities import PersonalUser
from src.shared.utils.list import flatmap, find


class Student(PersonalUser):  # type: ignore
    __faculty: 'Faculty'
    __degree: GenericUUID
    __courses_in_progress: Set['Course']
    __last_visited_lectio: Optional['Lectio']

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
            courses_in_progress: Optional[Set['Course']],
            last_visited_lectio: Optional['Lectio']
    ):
        if not faculty.has_degree(degree):
            raise DegreeNotExistsInStudentFacultyError(id=id, degree=degree, faculty=faculty.name)

        super().__init__(id, name, firstname, second_name, email, password_hash, is_superuser)
        self.__faculty = faculty
        self.__degree = GenericUUID(degree)
        self.__courses_in_progress = courses_in_progress if courses_in_progress else set()
        self.__last_visited_lectio = last_visited_lectio

    def enroll_in_a_course(self, course: 'Course'):
        self.__courses_in_progress.add(course)

    def start_lectio(self, lectio_id: str):
        lectio = self.__find_lectio(lectio_id)
        lectio.start()

    def finish_lectio(self, lectio_id: str):
        lectio = self.__find_lectio(lectio_id)
        lectio.finish()

    def set_last_visited_lectio(self, lectio_id: str):
        self.__last_visited_lectio = self.__find_lectio(lectio_id)

    def __find_lectio(self, lectio_id: str) -> 'Lectio':
        lectios = flatmap(lambda course: course.lectios, self.__courses_in_progress)
        lectio = find(lambda lectio: lectio.id == lectio_id, lectios)
        if lectio:
            return lectio
        else:
            raise NotEnrolledLectioError()


class Course(Entity):
    __lectios: Set['Lectio']

    def __init__(self, id: str, lectios: list[dict]):
        super().__init__(id)
        self.__lectios = set(
            map(lambda lectio: Lectio(lectio["id"], lectio["status"]), lectios)
        )

    @property
    def lectios(self):
        return self.__lectios

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        else:
            return self.id == other.id


class Lectio(Entity):
    __status: LectioStatus

    def __init__(self, id: str, status: Optional[str]):
        super().__init__(id)
        self.__status = LectioStatus(status) if status else LectioStatus.NOT_STARTED  # type: ignore

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

    def __eq__(self, other):
        if not isinstance(other, Lectio):
            return False
        else:
            return self.id == other.id


class Faculty(Entity):
    __name: FacultyName
    __degrees: Set[GenericUUID]

    def __init__(self, id: str, name: str, degrees: Set[str]):
        super().__init__(id)
        self.__name = FacultyName(name)
        self.__degrees = set(map(lambda degree_id: GenericUUID(degree_id), degrees))

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
