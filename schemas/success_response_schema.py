from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class APISuccessResponse(BaseModel, Generic[T]): # Changed GenericModel to BaseModel
    success: bool
    message: str
    data: T