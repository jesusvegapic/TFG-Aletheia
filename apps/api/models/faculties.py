from typing import List

from pydantic import BaseModel

from src.akademos.faculties.application.commands.create_faculty import DegreeDto


class PutFacultyRequest(BaseModel):
    name: str
    degrees: List[DegreeDto]
