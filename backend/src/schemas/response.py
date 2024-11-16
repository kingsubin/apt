from typing import Generic, TypeVar, Literal
from src.schemas.pydantic_base import PydanticBaseModel
from pydantic.alias_generators import to_camel
from pydantic import ConfigDict

T = TypeVar("T")


class CamelCaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        # populate_by_name=True,
        # allow_population_by_field_name=True,
        # from_attributes=True,
    )


class BaseResponseModel(PydanticBaseModel, Generic[T]):
    status: Literal["success", "fail", "error"] = "success"


class SingleResponseModel(BaseResponseModel[T]):
    data: T


class MultipleResponseModel(BaseResponseModel[T]):
    data: dict[str, T | list[T]]
