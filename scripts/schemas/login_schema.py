from pydantic import BaseModel
from typing import List


class LoginModel(BaseModel):
    user_name: str
    password: str


class ListVisitorsSchema(BaseModel):
    header_content: List = []
    body_content: List = []
