from src.akademos.faculties.domain.errors import DegreeNameError, FacultyNameError  # type: ignore


class FacultyName(str):
    def __new__(cls, name: str):
        if name.__len__() > FacultyName.max_length():
            raise FacultyNameError(name, FacultyName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100


class DegreeName(str):
    def __new__(cls, name: str):
        if name.__len__() > FacultyName.max_length():
            raise DegreeNameError(name, FacultyName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100
