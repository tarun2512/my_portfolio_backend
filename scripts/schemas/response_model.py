from typing import Any, Optional

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    status: str = "Failed"
    message: Optional[str] = ""
    data: Optional[Any]


class DefaultFailureResponse(DefaultResponse):
    error: Any
    message: Optional[Any]


class DefaultSuccessResponse(BaseModel):
    status: str = "success"
    message: Optional[str] = ""
    data: Any


class JSONResponseItem(BaseModel):
    status_code: int = 422
    content: dict = {}
