from fastapi import Query
from src.schemas.pydantic_base import PydanticBaseModel
from typing import Annotated
from datetime import date
from src.core.constants import SigunguName


class TradeHistoryFilter(PydanticBaseModel):
    sigungu_code: str | None = None
    contract_year: int | None = None
    contract_month: int | None = None
    contract_day: int | None = None

    @classmethod
    async def from_params(
        cls,
        sigungu_name: Annotated[
            SigunguName | None, Query(..., description="시군구명")
        ] = None,
        contract_year: Annotated[
            int | None, Query(..., ge=2010, le=2024, description="계약년도")
        ] = None,
        contract_month: Annotated[
            int | None, Query(..., ge=1, le=12, description="계약월")
        ] = None,
        contract_day: Annotated[
            int | None, Query(..., ge=1, le=31, description="계약일")
        ] = None,
    ) -> "TradeHistoryFilter":
        sigungu_code = SigunguName.to_code(sigungu_name) if sigungu_name else None
        return cls(
            sigungu_code=sigungu_code,
            contract_year=contract_year,
            contract_month=contract_month,
            contract_day=contract_day,
        )

    def to_date(self) -> date | None:
        """계약 날짜를 date 객체로 변환"""
        if all(
            v is not None
            for v in [self.contract_year, self.contract_month, self.contract_day]
        ):
            return date(self.contract_year, self.contract_month, self.contract_day)
        return None

    def get_query_filters(self) -> dict:
        """쿼리 필터 조건을 딕셔너리로 반환"""
        filters = {}
        if self.sigungu_code:
            filters["sigungu_code"] = self.sigungu_code
        if self.contract_year:
            filters["contract_year"] = self.contract_year
        if self.contract_month:
            filters["contract_month"] = self.contract_month
        if self.contract_day:
            filters["contract_day"] = self.contract_day
        return filters
