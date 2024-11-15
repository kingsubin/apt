from typing import Any
from fastapi import APIRouter
from sqlalchemy import select
from src.models import ApartmentTradeHistory
from src.database import fetch_all

router = APIRouter(prefix="/api/v1/trades")

@router.get("/")
async def get_trades(
    법정동시군구코드: str | None = None,
    법정동읍면동코드: str | None = None,
    계약년도: str | None = None,
    계약월: str | None = None,
    계약일: str | None = None,
    count: int = 10,
    page: int = 1,
):
    query = select(ApartmentTradeHistory)

    if 법정동시군구코드:
        query = query.where(ApartmentTradeHistory.법정동시군구코드 == 법정동시군구코드)
    if 법정동읍면동코드:
        query = query.where(ApartmentTradeHistory.법정동읍면동코드 == 법정동읍면동코드)
    if 계약년도:
        query = query.where(ApartmentTradeHistory.계약년도 == 계약년도)
    if 계약월:
        query = query.where(ApartmentTradeHistory.계약월 == 계약월)
    if 계약일:
        query = query.where(ApartmentTradeHistory.계약일 == 계약일)
    
    query = query.limit(count).offset((page - 1) * count)
    
    results = await fetch_all(query)
    next_page = page + 1 if len(results) == count else None
    
    return results, next_page