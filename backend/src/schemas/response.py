from typing import Generic, TypeVar, Literal
from src.schemas.pydantic_base import PydanticBaseModel

T = TypeVar("T")


class BaseResponseModel(PydanticBaseModel, Generic[T]):
    status: Literal["success", "fail", "error"] = "success"


class SingleResponseModel(BaseResponseModel[T]):
    data: T


class MultipleResponseModel(BaseResponseModel[T]):
    data: dict[str, T | list[T]]
