from typing import Annotated
from fastapi import APIRouter, Depends
from src.schemas.trade_stats import TradeStats
from src.api.dependencies import TradeHistoryFilter
from src.schemas.response import MultipleResponseModel
from src.services.apartment_trade_history import apartment_trade_history_service

router = APIRouter(prefix="/apartment-trade-histories")


@router.get(
    "",
    response_model=MultipleResponseModel[TradeStats],
)
async def get_trades(
    trade_filter: Annotated[
        TradeHistoryFilter, Depends(TradeHistoryFilter.from_params)
    ],
) -> MultipleResponseModel[TradeStats]:
    trade_stats = await apartment_trade_history_service.get_trade_stats(trade_filter)
    return MultipleResponseModel[TradeStats](data={"stats": trade_stats})
