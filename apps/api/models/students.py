from pydantic import BaseModel


class PutStudentRequest(BaseModel):
    email: str
    password: str
    name: str
    firstname: str
    second_name: str
    faculty: str
    degree: str
