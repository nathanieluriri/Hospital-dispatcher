from typing import Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class APISuccessResponse(GenericModel, Generic[T]):
    success: bool
    message: str
    data: T
