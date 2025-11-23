from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from http import HTTPStatus
from pydantic import Field

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
    status_code: int = Field(default=HTTPStatus.OK, exclude=True)

    @classmethod
    def with_data(cls, data: T, message: Optional[str] = None) -> "Response[T]":
        return cls(success=True, message=message, data=data)

    @classmethod
    def with_error(cls, message: str, status_code: int = HTTPStatus.BAD_REQUEST) -> "Response":
        return cls(success=False, message=message, status_code=status_code)