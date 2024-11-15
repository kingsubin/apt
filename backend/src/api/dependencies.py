from fastapi import Query
from src.schemas.pydantic_base import PydanticBaseModel
from typing import Annotated
from src.core.constants import SigunguName, RangeValue


class TradeHistoryFilter(PydanticBaseModel):
    sigungu_code: str | None = None
    range_value: RangeValue = RangeValue.ONE_YEAR

    @classmethod
    async def from_params(
        cls,
        sigungu_name: Annotated[
            SigunguName | None, Query(..., description="시군구명")
        ] = None,
        range_value: Annotated[RangeValue, Query(..., description="기간")] = (
            RangeValue.ONE_YEAR
        ),
    ) -> "TradeHistoryFilter":
        sigungu_code = SigunguName.to_code(sigungu_name) if sigungu_name else None
        return cls(
            sigungu_code=sigungu_code,
            range_value=range_value,
        )
