from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from src.api.dependencies import TradeHistoryFilter
from src.schemas.response import MultipleResponseModel
from src.db.models.apartment_trade_history import ApartmentTradeHistory
from src.db.database import fetch_all
from src.schemas.apartment_trade_history import ApartmentTradeHistoryOutput

router = APIRouter(prefix="/apartment-trade-histories")


@router.get(
    "/",
    response_model=MultipleResponseModel[ApartmentTradeHistoryOutput],
)
async def get_trades(
    trade_filter: Annotated[
        TradeHistoryFilter, Depends(TradeHistoryFilter.from_params)
    ],
) -> MultipleResponseModel[ApartmentTradeHistoryOutput]:
    query = select(ApartmentTradeHistory)

    if trade_filter.sigungu_code:
        query = query.where(
            ApartmentTradeHistory.법정동시군구코드 == trade_filter.sigungu_code
        )
    if trade_filter.contract_year:
        query = query.where(
            ApartmentTradeHistory.계약년도 == trade_filter.contract_year
        )
    if trade_filter.contract_month:
        query = query.where(ApartmentTradeHistory.계약월 == trade_filter.contract_month)
    if trade_filter.contract_day:
        query = query.where(ApartmentTradeHistory.계약일 == trade_filter.contract_day)

    results = await fetch_all(query)

    return MultipleResponseModel[ApartmentTradeHistoryOutput](
        data={
            "trades": [
                ApartmentTradeHistoryOutput.model_validate(result) for result in results
            ],
        },
    )
