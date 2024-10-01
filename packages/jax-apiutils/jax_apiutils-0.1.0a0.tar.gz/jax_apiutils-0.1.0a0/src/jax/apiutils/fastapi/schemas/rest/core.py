"""Schemas for API Responses."""

from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel
from .paging import Paging

T = TypeVar("T")


class Error(BaseModel):
    """Schema for error responses."""

    code: int
    message: str


class BaseResponse(BaseModel):
    """Schema for base response."""

    errors: Optional[List[Error]] = None


class Response(BaseResponse, Generic[T]):
    """Schema for response."""

    object: Optional[T] = None

    def __init__(self, *args, **kwargs):
        if args:
            kwargs["object"] = args[0]
        super().__init__(**kwargs)



class CollectionResponse(BaseResponse, Generic[T]):
    """Schema for API responses with collections."""

    data: List[T]
    paging: Optional[Paging] = None

    def __init__(self, *args, **kwargs):
        if args:
            kwargs["data"] = args[0]
        super().__init__(**kwargs)


class GenericResponse(Response, CollectionResponse, Generic[T]):
    """Schema for generic response."""

    object: Optional[T] = None
    data: Optional[List[T]] = None

    def __init(self, *args, **kwargs):
        if args:
            kwargs["object"] = args[0]
            kwargs["data"] = args[1]
        super().__init__(**kwargs)
