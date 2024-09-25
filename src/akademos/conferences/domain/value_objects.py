from src.akademos.conferences.domain.errors import ConferenceDescriptionError, ConferenceNameError


class ConferenceName(str):
    def __new__(cls, name: str):
        if name.__len__() > ConferenceName.max_length():
            raise ConferenceNameError(name, ConferenceName.max_length())
        return super().__new__(cls, name)

    @classmethod
    def max_length(cls):
        return 100


class ConferenceDescription(str):
    def __new__(cls, description: str):
        if description.__len__() > ConferenceDescription.max_length():
            raise ConferenceDescriptionError(description, ConferenceDescription.max_length())
        return super().__new__(cls, description)

    @classmethod
    def max_length(cls):
        return 1000
