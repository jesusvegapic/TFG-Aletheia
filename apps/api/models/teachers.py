from typing import List

from pydantic import BaseModel


class PutTeacherRequest(BaseModel):
    email: str
    password: str
    name: str
    firstname: str
    second_name: str
    faculty: str
    degrees: List[str]
    position: str
